
from api.dfg.DfgNode import DfgNode
from api.dfg.preparation.datatype.EateryStub import EateryStub

import json

class EateryStubs(DfgNode):
    ALL_EATERIES_PATH = "static_sources/cornell_eateries.json"

    def __call__(self, *args, **kwargs) -> list[EateryStub]:
        eateries = []

        with open(EateryStubs.ALL_EATERIES_PATH) as f:
            json_eateries = json.load(f)["eateries"]

            for json_eatery in json_eateries:
                eateries.append(EateryStubs.eatery_from_json(json_eatery))

        return eateries

    @staticmethod
    def eatery_from_json(json_eatery: dict) -> EateryStub:
        return EateryStub(
            name = json_eatery["name"],
            id = json_eatery["id"]
        )
