#!/usr/bin/env python3
# encoding: utf-8
#
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2021-2024 Henrik tom Wörden <h.tomwoerden@indiscale.com>
# Copyright (C) 2021-2023 Research Group Biomedical Physics, MPI-DS Göttingen
# Copyright (C) 2021-2023 Alexander Schlemmer <alexander.schlemmer@ds.mpg.de>
# Copyright (C) 2021-2024 Indiscale GmbH <info@indiscale.com>
# Copyright (C) 2024 Daniel Hornung <d.hornung@indiscale.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# ** end header
#

"""
Crawl a file structure using a yaml cfood definition and synchronize
the acuired data with LinkAhead.
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
import traceback
import uuid
import warnings
from argparse import RawTextHelpFormatter
from copy import deepcopy
from datetime import datetime
from enum import Enum
from typing import Any, List, Optional, Union

import linkahead as db
import yaml
from caosadvancedtools.cache import UpdateCache
from caosadvancedtools.crawler import Crawler as OldCrawler
from caosadvancedtools.serverside.helper import send_mail
from caosadvancedtools.utils import create_entity_link
from linkahead.apiutils import (EntityMergeConflictError, compare_entities,
                                merge_entities)
from linkahead.cached import cache_clear, cached_get_entity_by
from linkahead.common.datatype import get_list_datatype, is_reference
from linkahead.exceptions import EmptyUniqueQueryError
from linkahead.utils.escape import escape_squoted_text

from .config import get_config_setting
from .converters import Converter, ConverterValidationError
from .debug_tree import DebugTree
from .identifiable import Identifiable
from .identifiable_adapters import (CaosDBIdentifiableAdapter,
                                    IdentifiableAdapter,
                                    LocalStorageIdentifiableAdapter)
from .logging import configure_server_side_logging
from .macros import defmacro_constructor, macro_constructor
from .scanner import (create_converter_registry, initialize_converters,
                      load_definition, scan_directory, scan_structure_elements)
from .stores import GeneralStore
from .structure_elements import StructureElement

logger = logging.getLogger(__name__)

SPECIAL_PROPERTIES_STRICT = ("description", "name", "id", "path")
SPECIAL_PROPERTIES_NOT_STRICT = ("file", "checksum", "size")

# Register the macro functions from the submodule:
yaml.SafeLoader.add_constructor("!defmacro", defmacro_constructor)
yaml.SafeLoader.add_constructor("!macro", macro_constructor)


class ForbiddenTransaction(Exception):
    pass


def check_identical(record1: db.Entity, record2: db.Entity, ignore_id=False):
    """Check whether two entities are identical.

This function uses compare_entities to check whether two entities are identical
in a quite complex fashion:

- If one of the entities has additional parents or additional properties -> not identical
- If the value of one of the properties differs -> not identical
- If datatype, importance or unit are reported different for a property by compare_entities
   return "not_identical" only if these attributes are set explicitely by record1.
   Ignore the difference otherwise.
- If description, name, id or path appear in list of differences -> not identical.
- If file, checksum, size appear -> Only different, if explicitely set by record1.

record1 serves as the reference, so datatype, importance and unit checks are carried
out using the attributes from record1. In that respect, the function is not symmetrical
in its arguments.
    """
    comp = compare_entities(record1, record2)

    if ignore_id:
        if "id" in comp[0]:
            del comp[0]["id"]
        if "id" in comp[1]:
            del comp[1]["id"]

    for j in range(2):
        for label in ("parents", ):
            if len(comp[j][label]) > 0:
                return False
    for special_property in SPECIAL_PROPERTIES_STRICT:
        if special_property in comp[0] or special_property in comp[1]:
            return False

    for special_property in SPECIAL_PROPERTIES_NOT_STRICT:
        if special_property in comp[0]:
            attr_val = comp[0][special_property]
            other_attr_val = (comp[1][special_property]
                              if special_property in comp[1] else None)
            if attr_val is not None and attr_val != other_attr_val:
                return False

    for key in comp[0]["properties"]:
        if len(comp[0]["properties"][key]) == 0:
            # This is a new property
            return False
        for attribute in ("datatype", "importance", "unit"):
            # only make an update for those attributes if there is a value difference and
            # the value in the crawled_data is not None
            if attribute in comp[0]["properties"][key]:
                attr_val = comp[0]["properties"][key][attribute]
                other_attr_val = (comp[1]["properties"][key][attribute]
                                  if attribute in comp[1]["properties"][key] else None)
                if attr_val is not None and attr_val != other_attr_val:
                    return False

        if "value" in comp[0]["properties"][key]:
            return False

    # Check for removed properties:
    for key in comp[1]["properties"]:
        if len(comp[1]["properties"][key]) == 0:
            # This is a removed property
            return False

    return True


def _resolve_datatype(prop: db.Property, remote_entity: db.Entity):
    """ sets the datatype on the given property (side effect) """

    if remote_entity.role == "Property":
        datatype = remote_entity.datatype
    elif remote_entity.role == "RecordType":
        datatype = remote_entity.name
    else:
        raise RuntimeError("Cannot set datatype.")

    # Treat lists separately
    if isinstance(prop.value, list) and not datatype.startswith("LIST"):
        datatype = db.LIST(datatype)

    prop.datatype = datatype
    return prop


def _treat_merge_error_of(newrecord, record):
    """
    The parameters are two entities that cannot be merged with the merge_entities function.

    # This function checks for two obvious cases where no merge will ever be possible:
    # 1. Two Entities with differing IDs
    # 2. Two non-Entity values which differ

    It creates a more informative logger message and raises an Exception in those cases.
    """
    for this_p in newrecord.properties:
        that_p = record.get_property(this_p.name)

        if that_p is None:
            logger.debug(f"Property {this_p.name} does not exist in the second entity. Note that "
                         "this should not be the reason for the merge conflict.")
            continue

        if (isinstance(this_p.value, db.Entity)
                and isinstance(that_p.value, db.Entity)):
            if this_p.value.id is not None and that_p.value.id is not None:
                if this_p.value.id != that_p.value.id:
                    logger.error("The Crawler is trying to merge two entities "
                                 "because they should be the same object (same"
                                 " identifiables), but they reference "
                                 "different Entities with the same Property."
                                 f"Problematic Property: {this_p.name}\n"
                                 f"Referenced Entities: {this_p.value.id} and "
                                 f"{that_p.value.id}\n"
                                 f"{record}\n{newrecord}")
                    raise RuntimeError("Cannot merge Entities")
        elif (not isinstance(this_p.value, db.Entity)
              and not isinstance(that_p.value, db.Entity)):
            if ((this_p.value != that_p.value)
                # TODO can we also compare lists?
                and not isinstance(this_p.value, list)
                    and not isinstance(that_p.value, list)):
                logger.error(
                    "The Crawler is trying to merge two entities because they should be the same "
                    "object (same identifiables), but they have different values for the same "
                    "Property.\n"
                    f"Problematic Property: {this_p.name}\n"
                    f"Values: {this_p.value} and {that_p.value}\n"
                    f"{record}\n{newrecord}")
                raise RuntimeError("Cannot merge Entities")


class SecurityMode(Enum):
    RETRIEVE = 0
    INSERT = 1
    UPDATE = 2


class TreatedRecordLookUp():
    """tracks Records and Identifiables for which it was checked whether they exist in the remote
    server

    For a given Record it can be checked, whether it exists in the remote sever if
    - it has a (valid) ID
    - it has a (valid) path (FILEs only)
    - an identifiable can be created for the Record.

    Records are added by calling the `add` function and they are then added to the internal
    existing or missing list depending on whether the Record has a valid ID.
    Additionally, the Record is added to three look up dicts. The keys of those are paths, IDs and
    the representation of the identifiables.

    The extreme case, that one could imagine, would be that the same Record occurs three times as
    different Python objects: one that only has an ID, one with only a path and one without ID and
    path but with identifying properties. During `split_into_inserts_and_updates` all three
    must be identified with each other (and must be merged). Since we require, that treated
    entities have a valid ID if they exist in the remote server, all three objects would be
    identified with each other simply using the IDs.

    In the case that the Record is not yet in the remote server, there cannot be a Python object
    with an ID. Thus we might have one with a path and one with an identifiable. If that Record
    does not yet exist, it is necessary that both Python objects have at least either the path or
    the identifiable in common.
    """

    def __init__(self):
        self._id_look_up: dict[int, db.Entity] = {}
        self._path_look_up: dict[str, db.Entity] = {}
        self._identifiable_look_up: dict[str, db.Entity] = {}
        self.remote_missing_counter = -1
        self._missing: dict[int, db.Entity] = {}
        self._existing: dict[int, db.Entity] = {}

    def add(self, record: db.Entity, identifiable: Optional[Identifiable] = None):
        """
        Add a Record that was treated, such that it is contained in the internal look up dicts

        This Record MUST have an ID if it was found in the remote server.
        """
        if record.id is None:
            if record.path is None and identifiable is None:
                raise RuntimeError("Record must have ID or path or an identifiable must be given."
                                   f"Record is\n{record}")
            record.id = self.remote_missing_counter
            self.remote_missing_counter -= 1
            self._add_any(record, self._missing, identifiable)
        else:
            self._add_any(record, self._existing, identifiable)

    def get_any(self, record: db.Entity, identifiable: Optional[Identifiable] = None):
        """
        Check whether this Record was already added. Identity is based on ID, path or Identifiable
        represenation
        """
        if record.id is not None and record.id in self._id_look_up:
            return self._id_look_up[record.id]
        if record.path is not None and record.path in self._path_look_up:
            return self._path_look_up[record.path]
        if (identifiable is not None and identifiable.get_representation() in
                self._identifiable_look_up):
            return self._identifiable_look_up[identifiable.get_representation()]

    def get_existing(self, record: db.Entity, identifiable: Optional[Identifiable] = None):
        """ Check whether this Record exists on the remote server

        Returns: The stored Record
        """
        rec = self.get_any(record, identifiable)
        if id(rec) in self._existing:
            return rec
        else:
            return None

    def get_missing(self, record: db.Entity, identifiable: Optional[Identifiable] = None):
        """ Check whether this Record is missing on the remote server

        Returns: The stored Record
        """
        rec = self.get_any(record, identifiable)
        if id(rec) in self._missing:
            return rec
        else:
            return None

    def get_missing_list(self):
        """ Return all Records that are missing in the remote server """
        return list(self._missing.values())

    def get_existing_list(self):
        """ Return all Records that exist in the remote server """
        return list(self._existing.values())

    def _add_any(self, record: db.Entity, lookup, identifiable: Optional[Identifiable] = None):
        if record.id is not None:
            self._id_look_up[record.id] = record
        if record.path is not None:
            self._path_look_up[record.path] = record
        if identifiable is not None:
            self._identifiable_look_up[identifiable.get_representation()] = record
        lookup[id(record)] = record


class Crawler(object):
    """
    Crawler class that encapsulates crawling functions.
    Furthermore it keeps track of the storage for records (record store) and the
    storage for values (general store).
    """

    def __init__(self,
                 generalStore: Optional[GeneralStore] = None,
                 debug: Optional[bool] = None,
                 identifiableAdapter: Optional[IdentifiableAdapter] = None,
                 securityMode: SecurityMode = SecurityMode.UPDATE):
        """
        Create a new crawler and initialize an empty RecordStore and GeneralStore.

        Deprecated arguments:
        - The debug argument does not have an effect anymore.
        - generalStore: This argument does not have an effect anymore. It might be added to the scanning
                        functions in the scanner module in the future, if needed.

        Parameters
        ----------
        identifiableAdapter : IdentifiableAdapter
             TODO describe
        securityMode : int
             Whether only retrieves are allowed or also inserts or even updates.
             Please use SecurityMode Enum
        """

        # Remove this once the property `crawled_data` is no longer needed for compatibility
        # reasons
        self._crawled_data = None

        # The following caches store records, where we checked whether they exist on the remote
        # server. Since, it is important to know whether they exist or not, we store them into two
        # different caches.
        self.treated_records_lookup = TreatedRecordLookUp()

        # TODO does it make sense to have this as member variable?
        self.securityMode = securityMode
        # TODO does it make sense to have this as member variable(run_id)?
        self.generate_run_id()

        self.identifiableAdapter: IdentifiableAdapter = LocalStorageIdentifiableAdapter()
        if identifiableAdapter is not None:
            self.identifiableAdapter = identifiableAdapter

        if debug is not None:
            warnings.warn(DeprecationWarning(
                "The debug argument of the Crawler class is deprecated and has no effect."))

        if generalStore is not None:
            warnings.warn(DeprecationWarning(
                "The generalStore argument of the Crawler class is deprecated and has no effect."))

    def load_converters(self, definition: dict):
        warnings.warn(DeprecationWarning(
            "The function load_converters in the crawl module is deprecated. "
            "Please use create_converter_registry from the scanner module."))
        return create_converter_registry(definition)

    def load_definition(self, crawler_definition_path: str):
        warnings.warn(DeprecationWarning(
            "The function load_definition in the crawl module is deprecated. "
            "Please use load_definition from the scanner module."))
        return load_definition(crawler_definition_path)

    def initialize_converters(self, crawler_definition: dict, converter_registry: dict):
        warnings.warn(DeprecationWarning(
            "The function initialize_converters in the crawl module is deprecated. "
            "Please use initialize_converters from the scanner module."))
        return initialize_converters(crawler_definition, converter_registry)

    def generate_run_id(self):
        self.run_id = uuid.uuid1()

    def start_crawling(self, items: Union[list[StructureElement], StructureElement],
                       crawler_definition: dict,
                       converter_registry: dict,
                       restricted_path: Optional[list[str]] = None):

        warnings.warn(DeprecationWarning(
            "The function start_crawling in the crawl module is deprecated. "
            "Please use scan_structure_elements from the scanner module."))

        data = scan_structure_elements(
            items, crawler_definition, converter_registry, restricted_path)
        self.crawled_data = data
        return data

    @property
    def crawled_data(self):
        warnings.warn(DeprecationWarning(
            "The use of self.crawled_data is depricated. You should not access this variable. "
            "Instead, create the data with the scanner and then pass it as argument to Crawler "
            "functions"))
        return self._crawled_data

    @crawled_data.setter
    def crawled_data(self, arg):
        self._crawled_data = arg

    def crawl_directory(self,
                        crawled_directory: str,
                        crawler_definition_path: str,
                        restricted_path: Optional[list[str]] = None):
        """
        The new main function to run the crawler on a directory.
        """

        warnings.warn(DeprecationWarning(
            "The function crawl_directory in the crawl module is deprecated. "
            "Please use scan_directory from the scanner module."))

        data = scan_directory(crawled_directory,
                              crawler_definition_path,
                              restricted_path)
        self.crawled_data = data
        return data

    def _has_reference_value_without_id(self, ident: Identifiable) -> bool:
        """
        Returns True if there is at least one value in the properties and backrefs attributes of
        ``ident`` which:

        a) is a reference property AND
        b) where the value is set to a
           :external+caosdb-pylib:py:class:`db.Entity <caosdb.common.models.Entity>`
           (instead of an ID) AND
        c) where the ID of the value (the
           :external+caosdb-pylib:py:class:`db.Entity <caosdb.common.models.Entity>` object in b))
           is not set (to an integer)

        Returns
        -------
        bool
            True if there is a value without id (see above)

        Raises
        ------
        ValueError
            If no Identifiable is given.
        """
        if ident is None:
            raise ValueError("Identifiable has to be given as argument")
        for pvalue in list(ident.properties.values()) + ident.backrefs:
            if isinstance(pvalue, list):
                for el in pvalue:
                    if isinstance(el, db.Entity) and el.id is None:
                        return True
            elif isinstance(pvalue, db.Entity) and pvalue.id is None:
                return True
        return False

    @staticmethod
    def create_flat_list(ent_list: list[db.Entity], flat: Optional[list[db.Entity]] = None):
        """
        Recursively adds entities and all their properties contained in ent_list to
        the output list flat.

        TODO: This function will be moved to pylib as it is also needed by the
              high level API.
        """
        # Note: A set would be useful here, but we do not want a random order.
        if flat is None:
            flat = list()
        for el in ent_list:
            if el not in flat:
                flat.append(el)
        for ent in ent_list:
            for p in ent.properties:
                # For lists append each element that is of type Entity to flat:
                if isinstance(p.value, list):
                    for el in p.value:
                        if isinstance(el, db.Entity):
                            if el not in flat:
                                flat.append(el)
                                Crawler.create_flat_list([el], flat)
                elif isinstance(p.value, db.Entity):
                    if p.value not in flat:
                        flat.append(p.value)
                        Crawler.create_flat_list([p.value], flat)
        return flat

    def _has_missing_object_in_references(self, ident: Identifiable, referencing_entities: dict):
        """
        returns False if any value in the properties attribute is a db.Entity object that
        is contained in the `remote_missing_cache`. If ident has such an object in
        properties, it means that it references another Entity, where we checked
        whether it exists remotely and it was not found.
        """
        if ident is None:
            raise ValueError("Identifiable has to be given as argument")
        for pvalue in list(ident.properties.values()) + ident.backrefs:
            # Entity instead of ID and not cached locally
            if (isinstance(pvalue, list)):
                for el in pvalue:
                    elident = self.identifiableAdapter.get_identifiable(
                        el, referencing_entities[id(el)])
                    if (isinstance(el, db.Entity)
                            and self.treated_records_lookup.get_missing(el, elident) is not None):
                        return True
            if (isinstance(pvalue, db.Entity) and self.treated_records_lookup.get_missing(
                pvalue,
                    self.identifiableAdapter.get_identifiable(pvalue,
                                                              referencing_entities[id(pvalue)])
            ) is not None):
                # might be checked when reference is resolved
                return True
        return False

    def replace_references_with_cached(self, record: db.Record, referencing_entities: dict):
        """
        Replace all references with the versions stored in the cache.

        If the cache version is not identical, raise an error.
        """
        for p in record.properties:
            if (isinstance(p.value, list)):
                lst = []
                for el in p.value:
                    if (isinstance(el, db.Entity) and el.id is None):
                        cached = self.treated_records_lookup.get_any(
                            el,
                            self.identifiableAdapter.get_identifiable(
                                el, referencing_entities[id(el)]))
                        if cached is None:
                            lst.append(el)
                            continue
                        if not check_identical(cached, el, True):
                            if isinstance(p.value, db.File):
                                if p.value.path != cached.path:
                                    raise RuntimeError(
                                        "The cached and the referenced entity are not identical.\n"
                                        f"Cached:\n{cached}\nReferenced:\n{el}"
                                    )
                            else:
                                raise RuntimeError(
                                    "The cached and the referenced entity are not identical.\n"
                                    f"Cached:\n{cached}\nReferenced:\n{el}"
                                )
                        lst.append(cached)
                    else:
                        lst.append(el)
                p.value = lst
            if (isinstance(p.value, db.Entity) and p.value.id is None):
                cached = self.treated_records_lookup.get_any(
                    p.value, self.identifiableAdapter.get_identifiable(
                        p.value, referencing_entities[id(p.value)]))
                if cached is None:
                    continue
                if not check_identical(cached, p.value, True):
                    if isinstance(p.value, db.File):
                        if p.value.path != cached.path:
                            raise RuntimeError(
                                "The cached and the referenced entity are not identical.\n"
                                f"Cached:\n{cached}\nReferenced:\n{p.value}"
                            )
                    else:
                        raise RuntimeError(
                            "The cached and the referenced entity are not identical.\n"
                            f"Cached:\n{cached}\nReferenced:\n{p.value}"
                        )
                p.value = cached

    @staticmethod
    def bend_references_to_new_object(old, new, entities):
        """ Bend references to the other object
        Iterate over all entities in `entities` and check the values of all properties of
        occurances of old Entity and replace them with new Entity
        """
        for el in entities:
            for p in el.properties:
                if isinstance(p.value, list):
                    for index, val in enumerate(p.value):
                        if val is old:
                            p.value[index] = new
                else:
                    if p.value is old:
                        p.value = new

    def _merge_identified(self, newrecord, record, try_to_merge_later, all_records):
        """ tries to merge record into newrecord

        If it fails, record is added to the try_to_merge_later list.
        In any case, references are bent to the newrecord object.

        """
        try:
            merge_entities(
                newrecord, record, merge_references_with_empty_diffs=False,
                merge_id_with_resolved_entity=True)
        except EntityMergeConflictError:
            _treat_merge_error_of(newrecord, record)
            # We cannot merge but it is none of the clear case where merge is
            # impossible. Thus we try later
            try_to_merge_later.append(record)
            if newrecord.id is not None:
                record.id = newrecord.id
        except NotImplementedError:
            print(newrecord)
            print(record)
            raise
        Crawler.bend_references_to_new_object(
            old=record, new=newrecord,
            entities=all_records
        )

    def _identity_relies_on_unchecked_entities(self, record: db.Record, referencing_entities):
        """
        If a record for which it could not yet be verified whether it exists in LA or not is part
        of the identifying properties, this returns True, otherwise False
        """

        registered_identifiable = self.identifiableAdapter.get_registered_identifiable(record)
        if registered_identifiable is None:
            return False
        refs = self.identifiableAdapter.get_identifying_referencing_entities(referencing_entities,
                                                                             registered_identifiable)
        if any(el is None for el in refs):
            return True

        refs = self.identifiableAdapter.get_identifying_referenced_entities(
            record, registered_identifiable)
        if any([self.treated_records_lookup.get_any(el) is None for el in refs]):
            return True

        return False

    @staticmethod
    def create_reference_mapping(flat: list[db.Entity]):
        """
        Create a dictionary of dictionaries of the form:
        dict[int, dict[str, list[Union[int,None]]]]

        - The integer index is the Python id of the value object.
        - The string is the name of the first parent of the referencing object.

        Each value objects is taken from the values of all properties from the list flat.

        So the returned mapping maps ids of entities to the ids of objects which are referring
        to them.
        """
        # TODO we need to treat children of RecordTypes somehow.
        references: dict[int, dict[str, list[Union[int, None]]]] = {}
        for ent in flat:
            if id(ent) not in references:
                references[id(ent)] = {}
            for p in ent.properties:
                val = p.value
                if not isinstance(val, list):
                    val = [val]
                for v in val:
                    if isinstance(v, db.Entity):
                        if id(v) not in references:
                            references[id(v)] = {}
                        if ent.parents[0].name not in references[id(v)]:
                            references[id(v)][ent.parents[0].name] = []
                        references[id(v)][ent.parents[0].name].append(ent.id)

        return references

    def split_into_inserts_and_updates(self, ent_list: list[db.Entity]):
        flat = Crawler.create_flat_list(ent_list)
        all_records = list(flat)

        # TODO: can the following be removed at some point
        for ent in flat:
            if ent.role == "Record" and len(ent.parents) == 0:
                raise RuntimeError(f"Records must have a parent.\n{ent}")

        try_to_merge_later = []

        # Check whether Records can be identified without identifiable
        for i in reversed(range(len(flat))):
            record = flat[i]
            # 1. Can it be identified via an ID?
            if record.id is not None:
                treated_record = self.treated_records_lookup.get_existing(record)
                if treated_record is not None:
                    self._merge_identified(treated_record, record, try_to_merge_later, all_records)
                    all_records.remove(record)
                    referencing_entities = self.create_reference_mapping(all_records)
                else:
                    self.treated_records_lookup.add(record, None)
                assert record.id
                del flat[i]
            # 2. Can it be identified via a path?
            elif record.path is not None:
                try:
                    existing = cached_get_entity_by(path=record.path)
                except EmptyUniqueQueryError:
                    existing = None
                if existing is not None:
                    record.id = existing.id
                    # TODO check the following copying of _size and _checksum
                    # Copy over checksum and size too if it is a file
                    record._size = existing._size
                    record._checksum = existing._checksum
                treated_record = self.treated_records_lookup.get_any(record)
                if treated_record is not None:
                    self._merge_identified(treated_record, record, try_to_merge_later, all_records)
                    all_records.remove(record)
                    referencing_entities = self.create_reference_mapping(all_records)
                else:
                    # TODO add identifiable if possible
                    self.treated_records_lookup.add(record, None)
                assert record.id
                del flat[i]

        entity_was_treated = True
        # flat contains Entities which could not yet be checked against the remote server
        while entity_was_treated and len(flat) > 0:
            entity_was_treated = False
            referencing_entities = self.create_reference_mapping(all_records)

            # For each element we try to find out whether we can find it in the server or whether
            # it does not yet exist. Since a Record may reference other unkown Records it might not
            # be possible to answer this right away.
            # The following checks are done on each Record:
            # 1. Is it in the cache of already checked Records?
            # 2. Can it be checked on the remote server?
            # 3. Does it have to be new since a needed reference is missing?
            for i in reversed(range(len(flat))):
                record = flat[i]

                if self._identity_relies_on_unchecked_entities(record,
                                                               referencing_entities[id(record)]):
                    continue

                identifiable = self.identifiableAdapter.get_identifiable(
                    record,
                    referencing_entities=referencing_entities[id(record)])

                # 1. Is it in the cache of already checked Records?
                if self.treated_records_lookup.get_any(record, identifiable) is not None:
                    treated_record = self.treated_records_lookup.get_any(record, identifiable)
                    # Since the identifiables are the same, treated_record and record actually
                    # describe the same object.
                    # We merge record into treated_record in order to prevent loss of information
                    self._merge_identified(treated_record, record, try_to_merge_later, all_records)
                    all_records.remove(record)
                    referencing_entities = self.create_reference_mapping(all_records)

                    del flat[i]
                    entity_was_treated = True

                # 2. Can it be checked on the remote server?
                elif not self._has_reference_value_without_id(identifiable):
                    identified_record = (
                        self.identifiableAdapter.retrieve_identified_record_for_identifiable(
                            identifiable))
                    if identified_record is None:
                        # identifiable does not exist remotely -> record needs to be inserted
                        self.treated_records_lookup.add(record, identifiable)
                    else:
                        # side effect
                        record.id = identified_record.id
                        record.path = identified_record.path
                        self.treated_records_lookup.add(record, identifiable)
                    assert record.id
                    del flat[i]
                    entity_was_treated = True

                # 3. Does it have to be new since a needed reference is missing?
                # (Is it impossible to check this record because an identifiable references a
                # missing record?)
                elif self._has_missing_object_in_references(identifiable, referencing_entities):
                    self.treated_records_lookup.add(record, identifiable)
                    assert record.id
                    del flat[i]
                    entity_was_treated = True

            for record in flat:
                self.replace_references_with_cached(record, referencing_entities)

        # We postponed the merge for records where it failed previously and try it again now.
        # This only might add properties of the postponed records to the already used ones.
        for record in try_to_merge_later:
            identifiable = self.identifiableAdapter.get_identifiable(
                record,
                referencing_entities=referencing_entities[id(record)])
            newrecord = self.treated_records_lookup.get_any(record, identifiable)
            merge_entities(newrecord, record, merge_id_with_resolved_entity=True)
        if len(flat) > 0:
            circle = self.detect_circular_dependency(flat)
            if circle is None:
                logger.error("Failed, but found NO circular dependency. The data is as follows:"
                             + str(self.compact_entity_list_representation(flat,
                                                                           referencing_entities)))
            else:
                logger.error("Found circular dependency (Note that this might include references "
                             "that are not identifying properties): "
                             + self.compact_entity_list_representation(circle,
                                                                       referencing_entities))

            raise RuntimeError(
                f"Could not finish split_into_inserts_and_updates. Circular dependency: "
                f"{circle is not None}")

        # remove negative IDs
        missing = self.treated_records_lookup.get_missing_list()
        for el in missing:
            if el.id is None:
                raise RuntimeError("This should not happen")  # TODO remove
            if el.id >= 0:
                raise RuntimeError("This should not happen")  # TODO remove
            el.id = None

        return (missing, self.treated_records_lookup.get_existing_list())

    def replace_entities_with_ids(self, rec: db.Record):
        for el in rec.properties:
            if isinstance(el.value, db.Entity):
                if el.value.id is not None:
                    el.value = el.value.id
            elif isinstance(el.value, list):
                for index, val in enumerate(el.value):
                    if isinstance(val, db.Entity):
                        if val.id is not None:
                            el.value[index] = val.id

    @ staticmethod
    def compact_entity_list_representation(entities, referencing_entities: List) -> str:
        """ a more readable representation than the standard xml representation

        TODO this can be removed once the yaml format representation is in pylib
        """
        text = "\n--------\n"

        grouped = {"": []}
        for ent in entities:
            if not ent.parents:
                grouped[""].append(ent)
            for parent in ent.parents:
                if parent.name not in grouped:
                    grouped[parent.name] = []
                grouped[parent.name].append(ent)
        if not grouped[""]:
            del grouped[""]
        for parent, group in grouped.items():
            text += f"\n> Parent: {parent}\n"
            for ent in group:
                if ent.name is not None:
                    text += f"\n>> Name: {ent.name}\n"
                else:
                    text += "\n>> name: # No name"
                text += f"{[ent.name for ent in ent.parents]}\n"
                props = {p.name: p.value for p in ent.properties}
                text += f"{props}\n"
                text += f"is_referenced_by:\n{referencing_entities[id(ent)]}\n"

        return text + "--------\n"

    @ staticmethod
    def detect_circular_dependency(flat: list[db.Entity]):
        """
        Detects whether there are circular references in the given entity list and returns a list
        where the entities are ordered according to the chain of references (and only the entities
        contained in the circle are included. Returns None if no circular dependency is found.

        TODO: for the sake of detecting problems for split_into_inserts_and_updates we should only
        consider references that are identifying properties.
        """
        circle = [flat[0]]
        closed = False
        while not closed:
            current = circle[-1]
            added_to_circle = False
            for p in current.properties:
                if isinstance(p.value, list):
                    for pval in p.value:
                        if pval in flat:
                            if pval in circle:
                                closed = True
                            circle.append(pval)
                            added_to_circle = True
                else:
                    if p.value in flat:
                        if p.value in circle:
                            closed = True
                        circle.append(p.value)
                        added_to_circle = True
            if not added_to_circle:
                return None
        return circle

    @ staticmethod
    def _merge_properties_from_remote(
            crawled_data: list[db.Record],
            identified_records: list[db.Record]
    ):
        """Merge entity representation that was created by crawling the data with remotely found
        identified records s.th. new properties and property values are updated correctly but
        additional properties are not overwritten.

        Parameters
        ----------
        crawled_data : list[db.Record]
            List of the Entities  created by the crawler
        identified_records : list[db.Record]
            List of identified remote Records

        Returns
        -------
        to_be_updated : list[db.Record]
            List of merged records
        """
        to_be_updated = []
        for target, identified in zip(crawled_data, identified_records):
            # Special treatment for name and description in case they have been
            # set in the server independently from the crawler
            for attr in ["name", "description"]:
                if getattr(target, attr) is None:
                    # The crawler didn't find any name or description, i.e., not
                    # an empty one. In this case (and only in this), keep any
                    # existing name or description.
                    setattr(target, attr, getattr(identified, attr))

            # Create a temporary copy since the merge will be conducted in place
            tmp = deepcopy(identified)
            # A force merge will overwrite any properties that both the
            # identified and the crawled record have with the values of the
            # crawled record while keeping existing properties intact.
            merge_entities(tmp, target, force=True)
            to_be_updated.append(tmp)

        return to_be_updated

    @ staticmethod
    def remove_unnecessary_updates(
            crawled_data: list[db.Record],
            identified_records: list[db.Record]
    ):
        """Compare the Records to be updated with their remote
        correspondant. Only update if there are actual differences.

        Returns
        -------
        update list without unecessary updates

        """
        if len(crawled_data) != len(identified_records):
            raise RuntimeError("The lists of updates and of identified records need to be of the "
                               "same length!")
        actual_updates = []
        for i in reversed(range(len(crawled_data))):

            if not check_identical(crawled_data[i], identified_records[i]):
                logger.debug("Sheduled update because of the folllowing diff:\n"
                             + str(compare_entities(crawled_data[i], identified_records[i])))
                actual_updates.append(crawled_data[i])

        return actual_updates

    @ staticmethod
    def execute_parent_updates_in_list(to_be_updated, securityMode, run_id, unique_names):
        """
        Execute the updates of changed parents.

        This method is used before the standard inserts and needed
        because some changes in parents (e.g. of Files) might fail
        if they are not updated first.
        """
        logger.debug("=== Going to execute parent updates ===")
        Crawler.set_ids_and_datatype_of_parents_and_properties(to_be_updated)
        parent_updates = db.Container()

        for entity in to_be_updated:
            old_entity = cached_get_entity_by(eid=entity.id)

            # Check whether the parents have been changed and add them if missing
            # in the old entity:
            changes_made = False
            for parent in entity.parents:
                found = False
                for old_parent in old_entity.parents:
                    if old_parent.id == parent.id:
                        found = True
                        break
                if not found:
                    old_entity.add_parent(id=parent.id)
                    changes_made = True
            if changes_made:
                parent_updates.append(old_entity)
        logger.debug("RecordTypes need to be added to the following entities:")
        logger.debug(parent_updates)
        if len(parent_updates) > 0:
            if securityMode.value > SecurityMode.INSERT.value:
                parent_updates.update(unique=False)
            elif run_id is not None:
                update_cache = UpdateCache()
                update_cache.insert(parent_updates, run_id)
                logger.info("Some entities need to be updated because they are missing a parent "
                            "RecordType. The update was NOT executed due to the chosen security "
                            "mode. This might lead to a failure of inserts that follow.")
                logger.info(parent_updates)

    @ staticmethod
    def _get_property_id_for_datatype(rtname: str, name: str):
        return cached_get_entity_by(
            query=f"FIND Entity '{escape_squoted_text(rtname)}' "
                  f"with name='{escape_squoted_text(name)}'").id

    @ staticmethod
    def replace_name_with_referenced_entity_id(prop: db.Property):
        """changes the given property in place if it is a reference property that has a name as
        value

        If the Property has a List datatype, each element is treated separately.
        If the datatype is generic, i.e. FILE or REFERENCE, values stay unchanged.
        If the value is not a string, the value stays unchanged.
        If the query using the datatype and the string value does not uniquely identify an Entity,
        the value stays unchanged.
        If an Entity is identified, then the string value is replaced by the ID.
        """
        if get_list_datatype(prop.datatype) is None:  # not a list
            if (isinstance(prop.value, str) and is_reference(prop.datatype) and
                    prop.datatype != db.FILE and prop.datatype != db.REFERENCE):  # datatype is a non-generic reference and value is a string
                try:
                    # the get_entity function will raise an error if not unique
                    prop.value = Crawler._get_property_id_for_datatype(
                        rtname=prop.datatype, name=prop.value)
                except (db.EmptyUniqueQueryError, db.QueryNotUniqueError):
                    logger.error("The Property {prop.name} with datatype={prop.datatype} has the "
                                 "value {prop.value} and there is no appropriate Entity with such "
                                 "a name.")
                    raise
        else:
            dt = get_list_datatype(prop.datatype)
            if not (is_reference(dt) and dt != db.FILE and dt != db.REFERENCE):
                return
            propval = []
            for el in prop.value:
                if isinstance(el, str):
                    try:
                        # the get_entity function will raise an error if not unique
                        propval.append(Crawler._get_property_id_for_datatype(rtname=dt,
                                                                             name=el))
                    except (db.EmptyUniqueQueryError, db.QueryNotUniqueError):
                        logger.error(
                            "The Property {prop.name} with datatype={prop.datatype} has the "
                            "value {prop.value} and there is no appropriate Entity with such "
                            "a name.")
                        raise
                else:
                    propval.append(el)
            prop.value = propval

    @ staticmethod
    def execute_inserts_in_list(to_be_inserted, securityMode,
                                run_id: Optional[uuid.UUID] = None,
                                unique_names=True):
        for record in to_be_inserted:
            for prop in record.properties:
                if prop.name == "name":
                    raise Exception('Cannot search for the property with name "name"')
                entity = cached_get_entity_by(name=prop.name)
                _resolve_datatype(prop, entity)
                Crawler.replace_name_with_referenced_entity_id(prop)
        logger.debug("INSERT")
        logger.debug(to_be_inserted)
        if len(to_be_inserted) > 0:
            if securityMode.value > SecurityMode.RETRIEVE.value:
                db.Container().extend(to_be_inserted).insert(unique=unique_names)
            elif run_id is not None:
                update_cache = UpdateCache()
                update_cache.insert(to_be_inserted, run_id, insert=True)

    @ staticmethod
    def set_ids_and_datatype_of_parents_and_properties(rec_list):
        for record in rec_list:
            for parent in record.parents:
                if parent.id is None:
                    parent.id = cached_get_entity_by(name=parent.name).id
            for prop in record.properties:
                if prop.id is None:
                    entity = cached_get_entity_by(name=prop.name)
                    prop.id = entity.id
                    _resolve_datatype(prop, entity)

    @ staticmethod
    def execute_updates_in_list(to_be_updated, securityMode,
                                run_id: Optional[uuid.UUID] = None,
                                unique_names=True):
        Crawler.set_ids_and_datatype_of_parents_and_properties(to_be_updated)
        logger.debug("UPDATE")
        logger.debug(to_be_updated)
        if len(to_be_updated) > 0:
            if securityMode.value > SecurityMode.INSERT.value:
                db.Container().extend(to_be_updated).update(unique=unique_names)
            elif run_id is not None:
                update_cache = UpdateCache()
                update_cache.insert(to_be_updated, run_id)

    @ staticmethod
    def check_whether_parent_exists(records: list[db.Entity], parents: list[str]):
        """ returns a list of all records in `records` that have a parent that is in `parents`"""
        problems = []
        for rec in records:
            for parent in rec.parents:
                if parent.name in parents:
                    problems.append(rec)
        return problems

    def synchronize(self,
                    commit_changes: bool = True,
                    unique_names: bool = True,
                    crawled_data: Optional[list[db.Record]] = None,
                    no_insert_RTs: Optional[list[str]] = None,
                    no_update_RTs: Optional[list[str]] = None,
                    path_for_authorized_run: Optional[str] = "",
                    ):
        """
        This function applies several stages:
        1) Retrieve identifiables for all records in crawled_data.
        2) Compare crawled_data with existing records.
        3) Insert and update records based on the set of identified differences.

        This function makes use of an IdentifiableAdapter which is used to retrieve
        register and retrieve identifiables.

        if commit_changes is True, the changes are synchronized to the CaosDB server.
        For debugging in can be useful to set this to False.

        Parameters
        ----------
        no_insert_RTs : list[str], optional
            list of RecordType names. Records that have one of those RecordTypes
            as parent will not be inserted
        no_update_RTs : list[str], optional
            list of RecordType names. Records that have one of those RecordTypes
            as parent will not be updated
        path_for_authorized_run : str, optional
            only used if there are changes that need authorization before being
            applied. The form for rerunning the crawler with the authorization
            of these changes will be generated with this path. See
            ``caosadvancedtools.crawler.Crawler.save_form`` for more info about
            the authorization form.

        Returns
        -------
        inserts and updates
            the final to_be_inserted and to_be_updated as tuple.
        """
        if crawled_data is None:
            warnings.warn(DeprecationWarning(
                "Calling synchronize without the data to be synchronized is deprecated. Please "
                "use for example the Scanner to create this data."))
            crawled_data = self.crawled_data

        to_be_inserted, to_be_updated = self.split_into_inserts_and_updates(crawled_data)

        for el in to_be_updated:
            # all entity objects are replaced by their IDs except for the not yet inserted ones
            self.replace_entities_with_ids(el)

        identified_records = []
        for record in to_be_updated:
            if record.id is not None:
                # TODO: use cache here?
                identified_records.append(cached_get_entity_by(eid=record.id))
            else:
                raise Exception("Please report a bug: At this stage all records to be updated"
                                " should have an ID")
        # Merge with existing data to prevent unwanted overwrites
        to_be_updated = self._merge_properties_from_remote(to_be_updated, identified_records)
        # remove unnecessary updates from list by comparing the target records
        # to the existing ones
        to_be_updated = self.remove_unnecessary_updates(to_be_updated, identified_records)

        if no_insert_RTs:
            ins_problems = self.check_whether_parent_exists(to_be_inserted, no_insert_RTs)
        else:
            ins_problems = []
        if no_update_RTs:
            upd_problems = self.check_whether_parent_exists(to_be_updated, no_update_RTs)
        else:
            upd_problems = []
        if len(ins_problems) > 0 or len(upd_problems) > 0:
            raise ForbiddenTransaction(
                "One or more Records that have a parent which is excluded from inserts or updates."
                f"\nRecords excluded from inserts have the following RecordTypes:\n{[el.parents[0].name for el in ins_problems]}"
                f"\nRecords excluded from updates have the following RecordTypes:\n{[el.parents[0].name for el in upd_problems]}"
            )

        logger.info(f"Going to insert {len(to_be_inserted)} Entities and update "
                    f"{len(to_be_updated)} Entities.")
        if commit_changes:
            cache_clear()
            self.execute_parent_updates_in_list(to_be_updated, securityMode=self.securityMode,
                                                run_id=self.run_id, unique_names=unique_names)
            logger.info(f"Added parent RecordTypes where necessary.")
            self.execute_inserts_in_list(
                to_be_inserted, self.securityMode, self.run_id, unique_names=unique_names)
            logger.info(f"Executed inserts:\n"
                        + self.create_entity_summary(to_be_inserted))
            self.execute_updates_in_list(
                to_be_updated, self.securityMode, self.run_id, unique_names=unique_names)
            logger.info(f"Executed updates:\n"
                        + self.create_entity_summary(to_be_updated))

        update_cache = UpdateCache()
        pending_inserts = update_cache.get_inserts(self.run_id)
        if pending_inserts:
            Crawler.inform_about_pending_changes(
                pending_inserts, self.run_id, path_for_authorized_run)

        pending_updates = update_cache.get_updates(self.run_id)
        if pending_updates:
            Crawler.inform_about_pending_changes(
                pending_updates, self.run_id, path_for_authorized_run)

        return (to_be_inserted, to_be_updated)

    @ staticmethod
    def create_entity_summary(entities: list[db.Entity]):
        """ Creates a summary string reprensentation of a list of entities."""
        parents = {}
        for el in entities:
            for pp in el.parents:
                if pp.name not in parents:
                    parents[pp.name] = [el]
                else:
                    parents[pp.name].append(el)
        output = ""
        for key, value in parents.items():
            output += f"{key}:\n"
            for el in value:
                output += create_entity_link(el) + ", "

            output = output[:-2] + "\n"
        return output

    @ staticmethod
    def inform_about_pending_changes(pending_changes, run_id, path, inserts=False):
        # Sending an Email with a link to a form to authorize updates is
        if get_config_setting("send_crawler_notifications"):
            filename = OldCrawler.save_form(
                [el[3] for el in pending_changes], path, run_id)
            OldCrawler.send_mail([el[3] for el in pending_changes], filename)

        for i, el in enumerate(pending_changes):

            logger.debug(
                """
UNAUTHORIZED UPDATE ({} of {}):
____________________\n""".format(i + 1, len(pending_changes)) + str(el[3]))
        logger.info("There were unauthorized changes (see above). An "
                    "email was sent to the curator.\n"
                    "You can authorize the " +
                    ("inserts" if inserts else "updates")
                    + " by invoking the crawler"
                    " with the run id: {rid}\n".format(rid=run_id))

    @ staticmethod
    def debug_build_usage_tree(converter: Converter):
        res: dict[str, dict[str, Any]] = {
            converter.name: {
                "usage": ", ".join(converter.metadata["usage"]),
                "subtree": {}
            }
        }

        for subconv in converter.converters:
            d = Crawler.debug_build_usage_tree(subconv)
            k = list(d.keys())
            if len(k) != 1:
                raise RuntimeError(
                    "Unkonwn error during building of usage tree.")
            res[converter.name]["subtree"][k[0]] = d[k[0]]
        return res

    def save_debug_data(self, filename: str, debug_tree: DebugTree = None):
        """
        Save the information contained in a debug_tree to a file named filename.
        """

        paths: dict[str, Union[dict, list]] = dict()

        def flatten_debug_info(key):
            mod_info = debug_tree.debug_metadata[key]
            paths[key] = dict()
            for record_name in mod_info:
                if key == "provenance":
                    paths[key][record_name] = dict()
                    for prop_name in mod_info[record_name]:
                        paths[key][record_name][prop_name] = {
                            "structure_elements_path": "/".join(
                                mod_info[record_name][prop_name][0]),
                            "converters_path": "/".join(
                                mod_info[record_name][prop_name][1])}
                elif key == "usage":
                    paths[key][record_name] = ", ".join(mod_info[record_name])
        for key in ("provenance", "usage"):
            flatten_debug_info(key)

        # TODO: clarify what this was used for
        # paths["converters_usage"] = [self.debug_build_usage_tree(
        #     cv) for cv in self.debug_converters]

        with open(filename, "w") as f:
            f.write(yaml.dump(paths, sort_keys=False))


def _create_status_record(logfile_url, run_id):
    """Insert a CrawlerRun Record

    CrawlerRun Records are used to have a (somewhat) persistent feedback from crawler runs that
    are easyly accessible by users.
    """
    if get_config_setting("create_crawler_status_records"):
        (db.Record()
            .add_parent('CrawlerRun')
            .add_property('logfile', logfile_url)
            .add_property('status', "RUNNING")
            .add_property('run_id', run_id)
            .add_property('started', datetime.now().isoformat())
         .insert())


def _update_status_record(run_id, n_inserts, n_updates, status):
    """Update the CrawlerRun Record

    The Record is identified using the run_id. The status is changed and some information about the
    run is added.
    """
    if get_config_setting("create_crawler_status_records"):
        cr_rec = db.execute_query(f"FIND RECORD CrawlerRun WITH run_id={run_id}", unique=True)
        cr_rec.get_property('status').value = status
        (cr_rec
            .add_property(db.execute_query(
                f"FIND Property with name='number_of_inserted_entities'", unique=True).id,
                n_inserts)
            .add_property(
                db.execute_query(f"FIND Property with name='number_of_updated_entities'",
                                 unique=True).id, n_updates)
            .add_property(
                db.execute_query(f"FIND Property with name='finished'",
                                 unique=True).id, datetime.now().isoformat()))
        cr_rec.update()


def _notify_about_inserts_and_updates(n_inserts, n_updates, logfile, run_id):
    """send an email notification

    Only if there were inserts or updates.

    The email contains some basic information and a link to the log and the CrawlerRun Record.
    """
    if not get_config_setting("send_crawler_notifications"):
        return
    if n_inserts == 0 and n_updates == 0:
        return
    text = f"""Dear Curator,
the CaosDB Crawler successfully crawled the data and
- inserted {n_inserts} new Entities and
- updated {n_updates} existing Entities.

"""

    if get_config_setting("create_crawler_status_records"):
        domain = get_config_setting("public_host_url")
        text += ("You can checkout the CrawlerRun Record for more information:\n"
                 f"{domain}/Entity/?P=0L10&query=find%20crawlerrun%20with%20run_id=%27{run_id}%27\n\n")
    text += (f"You can download the logfile here:\n{domain}/Shared/" + logfile)
    send_mail(
        from_addr=get_config_setting("sendmail_from_address"),
        to=get_config_setting("sendmail_to_address"),
        subject="Crawler Update",
        body=text)


def _treat_deprecated_prefix(prefix, remove_prefix):
    """notify about deprecation and use given value"""
    if prefix != "":
        warnings.warn(DeprecationWarning("The prefix argument is deprecated and will be removed "
                                         "in the future. Please use `remove_prefix` instead."))
        if remove_prefix is not None:
            raise ValueError("Please do not supply the (deprecated) `prefix` and the "
                             "`remove_prefix` argument at the same time. Only use "
                             "`remove_prefix` instead.")
        return prefix
    return remove_prefix


def _fix_file_paths(crawled_data: list[db.Entity],
                    add_prefix: Optional[str],
                    remove_prefix: Optional[str]):
    """
    Adjust the path according to add_/remove_prefix

    Also remove the `file` attribute from File entities (because inserts need currently be done
    by loadfiles.

    Arguments:
    ------------

    crawled_data: list[db.Entity]
            A list of entities. This list will be searched for instances of db.File.

    add_prefix: Optional[str]
            If add_prefix is not None, the given prefix will be added in front of elem.path.

    remove_prefix: Optional[str]
            If remove_prefix is not None the given prefix will be removed from the front of
            elem.path. In this case a RuntimeError will be raised if any path of a file does
            not begin with "remove_prefix".

    """
    for elem in crawled_data:
        if isinstance(elem, db.File):
            # correct the file path:
            # elem.file = os.path.join(args.path, elem.file)
            if remove_prefix:
                if elem.path.startswith(remove_prefix):
                    elem.path = elem.path[len(remove_prefix):]
                else:
                    raise RuntimeError("Prefix shall be removed from file path but the path "
                                       "does not start with the prefix:"
                                       f"\n{remove_prefix}\n{elem.path}")
            if add_prefix:
                elem.path = add_prefix + elem.path
            elem.file = None
            # TODO: as long as the new file backend is not finished
            #       we are using the loadFiles function to insert symlinks.
            #       Therefore, I am setting the files to None here.
            #       Otherwise, the symlinks in the database would be replaced
            #       by uploads of the files which we currently do not want to happen.


def _check_record_types(crawled_data):
    """Check for all parents in crawled_data whether they exists

    raise Error if it does not
    """
    rtsfinder = dict()

    for elem in crawled_data:
        # Check whether all needed RecordTypes exist:
        if len(elem.parents) > 0:
            for parent in elem.parents:
                if parent.name in rtsfinder:
                    continue

                rt = db.RecordType(name=parent.name)
                try:
                    rt.retrieve()
                    rtsfinder[parent.name] = True
                except db.TransactionError:
                    rtsfinder[parent.name] = False

    notfound = [k for k, v in rtsfinder.items() if not v]
    if len(notfound) > 0:
        raise RuntimeError("Missing RecordTypes: {}". format(", ".join(notfound)))


def _store_dry_run_data(ins, upd):
    """write insets and updates to a file """
    inserts = [str(i) for i in ins]
    updates = [str(i) for i in upd]
    with open("dry.yml", "w") as f:
        f.write(yaml.dump({
            "insert": inserts,
            "update": updates}))


def crawler_main(crawled_directory_path: str,
                 cfood_file_name: str,
                 identifiables_definition_file: Optional[str] = None,
                 debug: bool = False,
                 provenance_file: Optional[str] = None,
                 dry_run: bool = False,
                 prefix: str = "",
                 securityMode: SecurityMode = SecurityMode.UPDATE,
                 unique_names=True,
                 restricted_path: Optional[list[str]] = None,
                 remove_prefix: Optional[str] = None,
                 add_prefix: Optional[str] = None,
                 ):
    """

    Parameters
    ----------
    crawled_directory_path : str
        path to be crawled
    cfood_file_name : str
        filename of the cfood to be used
    identifiables_definition_file : str
        filename of an identifiable definition yaml file
    debug : bool
        DEPRECATED, whether or not to run in debug mode
    provenance_file : str
        provenance information will be stored in a file with given filename
    dry_run : bool
        do not commit any chnages to the server
    prefix : str
        DEPRECATED, remove the given prefix from file paths
    securityMode : int
        securityMode of Crawler
    unique_names : bool
        whether or not to update or insert entities inspite of name conflicts
    restricted_path: optional, list of strings
            Traverse the data tree only along the given path. When the end of the given path
            is reached, traverse the full tree as normal. See docstring of 'scanner' in
            module 'scanner' for more details.
    remove_prefix : Optional[str]
        Remove the given prefix from file paths.
        See docstring of '_fix_file_paths' for more details.
    add_prefix : Optional[str]
        Add the given prefix to file paths.
        See docstring of '_fix_file_paths' for more details.

    Returns
    -------
    return_value : int
        0 if successful
    """
    try:
        crawler = Crawler(securityMode=securityMode)

        # setup logging and reporting if serverside execution
        if "SHARED_DIR" in os.environ:
            userlog_public, htmluserlog_public, debuglog_public = configure_server_side_logging()
            _create_status_record(
                get_config_setting("public_host_url") + "/Shared/" + htmluserlog_public, crawler.run_id)

        debug_tree = DebugTree()
        crawled_data = scan_directory(
            crawled_directory_path, cfood_file_name, restricted_path, debug_tree=debug_tree)
        _fix_file_paths(crawled_data, add_prefix, remove_prefix)
        _check_record_types(crawled_data)

        if provenance_file is not None and debug:
            crawler.save_debug_data(debug_tree=debug_tree, filename=provenance_file)

        if identifiables_definition_file is not None:
            ident = CaosDBIdentifiableAdapter()
            ident.load_from_yaml_definition(identifiables_definition_file)
            crawler.identifiableAdapter = ident

        remove_prefix = _treat_deprecated_prefix(prefix, remove_prefix)

        if dry_run:
            inserts, updates = crawler.synchronize(commit_changes=False, crawled_data=crawled_data)
            _store_dry_run_data(inserts, updates)
        else:
            inserts, updates = crawler.synchronize(commit_changes=True, unique_names=unique_names,
                                                   crawled_data=crawled_data,
                                                   path_for_authorized_run=crawled_directory_path)
            if "SHARED_DIR" in os.environ:
                _notify_about_inserts_and_updates(len(inserts), len(updates), userlog_public,
                                                  crawler.run_id)
                _update_status_record(crawler.run_id, len(inserts), len(updates), status="OK")
        return 0
    except ForbiddenTransaction as err:
        logger.debug(traceback.format_exc())
        logger.error(err)
        _update_status_record(crawler.run_id, 0, 0, status="FAILED")
        return 1
    except ConverterValidationError as err:
        logger.debug(traceback.format_exc())
        logger.error(err)
        _update_status_record(crawler.run_id, 0, 0, status="FAILED")
        return 1
    except Exception as err:
        logger.debug(traceback.format_exc())
        logger.debug(err)

        if "SHARED_DIR" in os.environ:
            domain = get_config_setting("public_host_url")
            logger.error("Unexpected Error: Please tell your administrator about this and provide the"
                         f" following path.\n{domain}/Shared/" + debuglog_public)
        _update_status_record(crawler.run_id, 0, 0, status="FAILED")
        return 1


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=RawTextHelpFormatter)
    parser.add_argument("cfood_file_name",
                        help="Path name of the cfood yaml file to be used.")
    mg = parser.add_mutually_exclusive_group()
    mg.add_argument("-r", "--restrict", nargs="*",
                    help="Restrict the crawling to the subtree at the end of the given path."
                    "I.e. for each level that is given the crawler only treats the element "
                    "with the given name.")
    mg.add_argument("--restrict-path", help="same as restrict; instead of a list, this takes a "
                    "single string that is interpreded as file system path. Note that a trailing"
                    "separator (e.g. '/') will be ignored. Use --restrict if you need to have "
                    "empty strings.")
    parser.add_argument("--provenance", required=False,
                        help="Path name of the provenance yaml file. "
                        "This file will only be generated if this option is set.")
    parser.add_argument("--debug", required=False, action="store_true",
                        help="Path name of the cfood yaml file to be used.")
    parser.add_argument("crawled_directory_path",
                        help="The subtree of files below the given path will "
                        "be considered. Use '/' for everything.")
    parser.add_argument("-c", "--add-cwd-to-path", action="store_true",
                        help="If given, the current working directory(cwd) is added to the Python "
                        "path.")
    parser.add_argument("-s", "--security-mode", choices=["retrieve", "insert", "update"],
                        default="retrieve",
                        help="Determines whether entities may only be read from the server, or "
                        "whether inserts or even updates may be done.")
    parser.add_argument("-n", "--dry-run", action="store_true",
                        help="Create two files dry.yml to show"
                        "what would actually be committed without doing the synchronization.")

    # TODO: load identifiables is a dirty implementation currently
    parser.add_argument("-i", "--load-identifiables",
                        help="Load identifiables from the given yaml file.")
    parser.add_argument("-u", "--unique-names",
                        help="Insert or updates entities even if name conflicts exist.")
    parser.add_argument("-p", "--prefix",
                        help="DEPRECATED, use --remove-prefix instead. Remove the given prefix "
                        "from the paths of all file objects.")
    parser.add_argument("--remove-prefix",
                        help="Remove the given prefix from the paths of all file objects.")
    parser.add_argument("--add-prefix",
                        help="Add the given prefix to the paths of all file objects.")

    return parser.parse_args()


def split_restricted_path(path):
    """
    Split a path string into components separated by slashes or other os.path.sep.
    Empty elements will be removed.
    """
    # This implementation leads to infinite loops
    # for "ill-posed" paths (see test_utilities.py"):
    # elements = []
    # while path != "/":
    #     path, el = os.path.split(path)
    #     if el != "":
    #         elements.insert(0, el)
    return [i for i in path.split(os.path.sep) if i != ""]


def main():
    args = parse_args()

    conlogger = logging.getLogger("connection")
    conlogger.setLevel(level=logging.ERROR)

    if args.prefix:
        print("Please use '--remove-prefix' option instead of '--prefix' or '-p'.")
        return -1

    # logging config for local execution
    logger.addHandler(logging.StreamHandler(sys.stdout))
    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    if args.add_cwd_to_path:
        sys.path.append(os.path.abspath("."))
    restricted_path = None
    if args.restrict_path:
        restricted_path = split_restricted_path(args.restrict_path)
    if args.restrict:
        restricted_path = args.restrict

    sys.exit(crawler_main(
        crawled_directory_path=args.crawled_directory_path,
        cfood_file_name=args.cfood_file_name,
        identifiables_definition_file=args.load_identifiables,
        debug=args.debug,
        provenance_file=args.provenance,
        dry_run=args.dry_run,
        securityMode={"retrieve": SecurityMode.RETRIEVE,
                      "insert": SecurityMode.INSERT,
                      "update": SecurityMode.UPDATE}[args.security_mode],
        unique_names=args.unique_names,
        restricted_path=restricted_path,
        remove_prefix=args.remove_prefix,
        add_prefix=args.add_prefix,
    ))


if __name__ == "__main__":
    main()
