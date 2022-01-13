from typing import Mapping
from enum import Enum

from api.datatype.Eatery import EateryID

class FieldType(Enum):
    INT = 'int'
    STRING = 'str'
    EATERYID = "eateryid"
    

def verify_json_fields(json, field_type_map: Mapping[str, FieldType]):
    for field in field_type_map:
        if field not in json:
            return False
        if field_type_map[field] is FieldType.INT:
            if not isinstance(json[field], int):
                return False
        elif field_type_map[field] is FieldType.STRING:
            if not isinstance(json[field], str):
                return False
        elif field_type_map[field] is FieldType.EATERYID:
            if not isinstance(json[field], int) or EateryID(json[field]) == None:
                return False
            
    return True

def success_json(data):
    return {
        "success": True,
        "data": data,
        "error": None
    }

def error_json(error: str):
    return {
        "success": False,
        "data": None,
        "error": error
    }
