#!/usr/bin/env python3
# encoding: utf-8
#
# ** header v3.0
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2021 Henrik tom Wörden
#               2021 Alexander Schlemmer
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

from typing import Dict as tDict
import warnings


class StructureElement(object):
    """ base class for elements in the hierarchical data structure """

    def __init__(self, name):
        # Used to store usage information for debugging:
        self.metadata: tDict[str, set[str]] = {
            "usage": set()
        }

        self.name = name

    def __str__(self):
        return self.get_name()

    def get_name(self):
        return self.name


class FileSystemStructureElement(StructureElement):
    def __init__(self, name: str, path: str):
        super().__init__(name)
        self.path = path

    def __str__(self):
        class_name_short = str(self.__class__).replace(
            "<class \'", "")[:-2]
        return "{}: {}, {}".format(class_name_short, self.name, self.path)


class NoneElement(StructureElement):
    pass


class Directory(FileSystemStructureElement):
    pass


class File(FileSystemStructureElement):
    pass


class JSONFile(File):
    pass


class DictElement(StructureElement):
    def __init__(self, name: str, value: dict):
        super().__init__(name)
        self.value = value


class TextElement(StructureElement):
    def __init__(self, name: str, value: str):
        super().__init__(name)
        self.value = value


class DictTextElement(TextElement):
    def __init__(self, *args, **kwargs):
        warnings.warn(DeprecationWarning("This class is depricated. Please use TextElement."))
        super().__init__(*args, **kwargs)


class IntegerElement(StructureElement):
    def __init__(self, name: str, value: int):
        super().__init__(name)
        self.value = value


class DictIntegerElement(IntegerElement):
    def __init__(self, *args, **kwargs):
        warnings.warn(DeprecationWarning("This class is depricated. Please use IntegerElement."))
        super().__init__(*args, **kwargs)


class BooleanElement(StructureElement):
    def __init__(self, name: str, value: bool):
        super().__init__(name)
        self.value = value


class DictBooleanElement(BooleanElement):
    def __init__(self, *args, **kwargs):
        warnings.warn(DeprecationWarning("This class is depricated. Please use BooleanElement."))
        super().__init__(*args, **kwargs)


class ListElement(StructureElement):
    def __init__(self, name: str, value: list):
        super().__init__(name)
        self.value = value


class DictListElement(ListElement):
    def __init__(self, *args, **kwargs):
        warnings.warn(DeprecationWarning("This class is depricated. Please use ListElement."))
        super().__init__(*args, **kwargs)


class FloatElement(StructureElement):
    def __init__(self, name: str, value: float):
        super().__init__(name)
        self.value = value


class DictFloatElement(FloatElement):
    def __init__(self, *args, **kwargs):
        warnings.warn(DeprecationWarning("This class is depricated. Please use FloatElement."))
        super().__init__(*args, **kwargs)


class Dict(DictElement):
    def __init__(self, *args, **kwargs):
        warnings.warn(DeprecationWarning("This class is depricated. Please use DictElement."))
        super().__init__(*args, **kwargs)


class DictDictElement(DictElement):
    def __init__(self, *args, **kwargs):
        warnings.warn(DeprecationWarning("This class is depricated. Please use DictElement."))
        super().__init__(*args, **kwargs)
