from typing import Union

from api.datatype.EateryResult import EateryResult
from api.dfg.DfgNode import DfgNode


class EateryToJson(DfgNode):

    def __init__(self, child: DfgNode):
        self.child = child

    def __call__(self, *args, **kwargs):
        result = self.child(*args, **kwargs)
        return EateryToJson.to_json(result, *args, **kwargs)

    @staticmethod
    def to_json(obj: Union[list, dict, EateryResult], *args, **kwargs):
        if isinstance(obj, list):
            return [
                EateryToJson.to_json(elem, *args, **kwargs)
                for elem in obj
            ]

        elif isinstance(obj, dict):
            return {
                key: EateryToJson.to_json(value, *args, **kwargs)
                for key, value in obj.items()
            }

        else:
            return obj.to_json(
                tzinfo=kwargs.get("tzinfo"),
                start=kwargs.get("start"),
                end=kwargs.get("end")
            )

    def children(self):
        return [self.child]
