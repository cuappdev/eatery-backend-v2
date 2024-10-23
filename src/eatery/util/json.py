from enum import Enum
from typing import List, Mapping, Optional

from eatery.datatype.Eatery import EateryID


class FieldType(Enum):
    INT = "int"
    STRING = "str"
    EATERYID = "eateryid"


def verify_json_fields(
    json, field_type_map: Mapping[str, FieldType], nullable: Optional[List] = []
):
    for field in field_type_map:
        if field not in json:
            return field in nullable
        if field_type_map[field] is FieldType.INT:
            if not isinstance(json[field], int):
                return False
        elif field_type_map[field] is FieldType.STRING:
            if not isinstance(json[field], str):
                return False
        elif field_type_map[field] is FieldType.EATERYID:
            if not isinstance(json[field], int) or EateryID(json[field]) is None:
                return False

    for field in json:
        if field not in field_type_map and field not in nullable:
            return False

    return True


def success_json(data):
    return {"success": True, "data": data, "error": None}


def error_json(error: str):
    return {"success": False, "data": None, "error": error}
