#!/usr/bin/env python3
# encoding: utf-8
#
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2022 Henrik tom Wörden
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

from __future__ import annotations
import linkahead as db
from datetime import datetime
import json
from hashlib import sha256
from typing import Union
import logging

logger = logging.getLogger(__name__)


class Identifiable():
    """
    The fingerprint of a Record in CaosDB.

    This class contains the information that is used by the CaosDB Crawler to identify Records.
    On one hand, this can be the ID or a Record or the path of a File.
    On the other hand, in order to check whether a Record exits in the CaosDB Server, a query can
    be created using the information contained in the Identifiable.

    Parameters
    ----------
    record_type: str, this RecordType has to be a parent of the identified object
    name: str, the name of the identified object
    properties: dict, keys are names of Properties; values are Property values
                Note, that lists are not checked for equality but are interpreted as multiple
                conditions for a single Property.
    path: str, In case of files: The path where the file is stored.
    backrefs: list, TODO future
    """

    def __init__(self, record_id: int = None, path: str = None, record_type: str = None,
                 name: str = None, properties: dict = None,
                 backrefs: list[Union[int, str]] = None):
        if (record_id is None and path is None and name is None
                and (backrefs is None or len(backrefs) == 0)
                and (properties is None or len(properties) == 0)):
            raise ValueError("There is no identifying information. You need to add a path or "
                             "properties or other identifying attributes.")
        if properties is not None and 'name' in [k.lower() for k in properties.keys()]:
            raise ValueError("Please use the separete 'name' keyword instead of the properties "
                             "dict for name")
        self.record_id = record_id
        self.path = path
        self.record_type = record_type
        self.name = name
        if name == "":
            self.name = None
        self.properties: dict = {}
        if properties is not None:
            self.properties = properties
        self.backrefs: list[Union[int, db.Entity]] = []
        if backrefs is not None:
            self.backrefs = backrefs

    def get_representation(self) -> str:
        return sha256(Identifiable._create_hashable_string(self).encode('utf-8')).hexdigest()

    @staticmethod
    def _value_representation(value) -> str:
        """returns the string representation of property values to be used in the hash function

        The string is the path of a File Entity, the CaosDB ID or Python ID of other Entities
        (Python Id only if there is no CaosDB ID) and the string representation of bool, float, int
        and str.
        """

        if value is None:
            return "None"
        elif isinstance(value, db.File):
            return str(value.path)
        elif isinstance(value, db.Entity):
            if value.id is not None:
                return str(value.id)
            else:
                return "PyID=" + str(id(value))
        elif isinstance(value, list):
            return "[" + ", ".join([Identifiable._value_representation(el) for el in value]) + "]"
        elif (isinstance(value, str) or isinstance(value, int) or isinstance(value, float)
              or isinstance(value, datetime)):
            return str(value)
        else:
            raise ValueError(f"Unknown datatype of the value: {value}")

    @staticmethod
    def _create_hashable_string(identifiable: Identifiable) -> str:
        """
        creates a string from the attributes of an identifiable that can be hashed
        String has the form "P<parent>N<name>R<reference-ids>a:5b:10"
        """
        rec_string = "P<{}>N<{}>R<{}>".format(
            identifiable.record_type,
            identifiable.name,
            [Identifiable._value_representation(el) for el in identifiable.backrefs])
        # TODO this structure neglects Properties if multiple exist for the same name
        for pname in sorted(identifiable.properties.keys()):
            rec_string += ("{}:".format(pname) +
                           Identifiable._value_representation(identifiable.properties[pname]))
        return rec_string

    def __eq__(self, other) -> bool:
        """
        Identifiables are equal if they belong to the same Record. Since ID and path are on their
        own enough to identify the Record it is sufficient if those attributes are equal.
        1. both IDs are set (not None)  -> equal if IDs are equal
        2. both paths are set (not None)  -> equal if paths are equal
        3. equal if attribute representations are equal
        """
        if not isinstance(other, Identifiable):
            raise ValueError("Identifiable can only be compared to other Identifiable objects.")
        elif self.record_id is not None and other.record_id is not None:
            return self.record_id == other.record_id
        elif self.path is not None and other.path is not None:
            return self.path == other.path
        elif self.get_representation() == other.get_representation():
            return True
        else:
            return False

    def __repr__(self):
        pstring = json.dumps(self.properties)
        return (f"{self.__class__.__name__} for RT {self.record_type}: id={self.record_id}; "
                f"name={self.name}\n\tpath={self.path}\n"
                f"\tproperties:\n{pstring}\n"
                f"\tbackrefs:\n{self.backrefs}")
