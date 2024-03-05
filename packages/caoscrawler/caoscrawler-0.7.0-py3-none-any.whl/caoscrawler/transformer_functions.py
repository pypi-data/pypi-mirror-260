#!/usr/bin/env python3
# encoding: utf-8
#
# This file is a part of the LinkAhead Project.
#
# Copyright (C) 2024 Indiscale GmbH <info@indiscale.com>
# Copyright (C) 2024 Henrik tom Wörden <h.tomwoerden@indiscale.com>
# Copyright (C) 2023 Alexander Schlemmer <alexander.schlemmer@ds.mpg.de>
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

"""
Defnition of default transformer functions.
"""
import re
from typing import Any


def submatch(in_value: Any, in_parameters: dict):
    """
    Substitute the variable if it matches the regexp stored in "match".

    Returns the "in" value if it does NOT match the reg exp of 'match'.
    Otherwise (if it matches) the value of 'then' stored in the second argument is returned.
    """
    if "match" not in in_parameters or "then" not in in_parameters:
        raise RuntimeError("Mandatory parameters missing.")
    if re.match(in_parameters["match"], in_value) is not None:
        return in_parameters["then"]
    return in_value


def split(in_value: Any, in_parameters: dict):
    """calls the string 'split' function on the first argument and uses the value of the key
    'marker' stored in the second argument
    """
    if "marker" not in in_parameters:
        raise RuntimeError("Mandatory parameter missing.")
    if not isinstance(in_value, str):
        raise RuntimeError("must be string")
    return in_value.split(in_parameters['marker'])


def replace(in_value: Any, in_parameters: dict):
    """calls the string 'replace' function on the first argument and uses the value of the keys
    'remove' and 'insert' stored in the second argument
    """
    if "remove" not in in_parameters or "insert" not in in_parameters:
        raise RuntimeError("Mandatory parameter missing.")
    if not isinstance(in_value, str):
        raise RuntimeError("must be string")
    return in_value.replace(in_parameters['remove'], in_parameters['insert'])
