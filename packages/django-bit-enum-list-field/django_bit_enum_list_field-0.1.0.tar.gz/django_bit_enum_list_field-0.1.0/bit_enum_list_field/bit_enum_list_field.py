from __future__ import annotations
from enum import Enum
from typing import Type, List, Union

from django.db.models import BigIntegerField

from bit_enum_list_field.lookups.bit_enum_list_all_lookup import BitEnumListAllLookup
from bit_enum_list_field.lookups.bit_enum_list_any_lookup import BitEnumListAnyLookup
from bit_enum_list_field.lookups.bit_enum_list_none_lookup import BitEnumListNoneLookup


class BitEnumListField(BigIntegerField):
    def __init__(self, enum: Type[Enum], *args, **kwargs):
        self.enum = enum
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(BitEnumListField, self).deconstruct()
        args = [self.enum] + args
        return name, path, args, kwargs

    def get_prep_value(self, value: Union[List[Enum], Enum, int]):
        if isinstance(value, int):
            return value
        if isinstance(value, Enum):
            value = [value]
        out = 0
        for elem in value:
            out |= self.to_bit_value(elem)
        return out

    # noinspection PyUnusedLocal
    def from_db_value(self, value, expression, connection):
        output = []
        for x in self.enum:
            if value & self.to_bit_value(x):
                output.append(x)
        return output

    @staticmethod
    def to_bit_value(i: Enum):
        return pow(2, i.value)


BitEnumListField.register_lookup(BitEnumListAllLookup)
BitEnumListField.register_lookup(BitEnumListAnyLookup)
BitEnumListField.register_lookup(BitEnumListNoneLookup)
