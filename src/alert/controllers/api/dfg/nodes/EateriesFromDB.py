from datetime import datetime

from api.dfg.nodes.DfgNode import DfgNode
from eatery.datatype.Eatery import Eatery, EateryID
from eatery.models import EateryStore
from eatery.serializers import EateryStoreSerializer

# eventually need to deprecate this for a custom DB backend storing all of the overrides


class EateriesFromDB(DfgNode):
    def __call__(self, *args, **kwargs) -> list[Eatery]:
        eateries = EateryStore.objects.all()
        serialized_eateries = EateryStoreSerializer(data=eateries, many=True)
        serialized_eateries.is_valid()
        return list(serialized_eateries.data)
            

    @staticmethod
    def none_repr(str):
        return None if str == None or len(str) == 0 else str

    @staticmethod
    def eatery_from_serialized(
        serialized_eatery: dict, serialized_alerts: list[dict]
    ) -> Eatery:
        return Eatery(
            id=EateryID(serialized_eatery["id"]),
            name=EateriesFromDB.none_repr(serialized_eatery["name"]),
            image_url=EateriesFromDB.none_repr(serialized_eatery["image_url"]),
            menu_summary=EateriesFromDB.none_repr(serialized_eatery["menu_summary"]),
            campus_area=EateriesFromDB.none_repr(serialized_eatery["campus_area"]),
            events=None,
            latitude=serialized_eatery["latitude"],
            longitude=serialized_eatery["longitude"],
            payment_accepts_cash=serialized_eatery["payment_accepts_cash"],
            payment_accepts_brbs=serialized_eatery["payment_accepts_brbs"],
            payment_accepts_meal_swipes=serialized_eatery[
                "payment_accepts_meal_swipes"
            ],
            location=EateriesFromDB.none_repr(serialized_eatery["location"]),
            online_order_url=EateriesFromDB.none_repr(
                serialized_eatery["online_order_url"]
            ),
            
        )

    def description(self):
        return "EateriesFromDB"
