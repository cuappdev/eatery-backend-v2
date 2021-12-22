from datetime import date, timedelta

import pytz
from django.http import JsonResponse

from src.dfg.Concat import Concat
from src.dfg.CornellDiningNow import CornellDiningNow
from src.dfg.DictResponseWrapper import DictResponseWrapper
from src.dfg.EateryGroupByType import EateryGroupByType
from src.dfg.EateryToJson import EateryToJson
from src.dfg.ExternalEateries import ExternalEateries

dataflow_graph = DictResponseWrapper(
    EateryToJson(
        EateryGroupByType(
            Concat([
                CornellDiningNow(),
                ExternalEateries()
            ])
        )
    ),
    re_raise_exceptions=True
)


def index(request):
    tzinfo = pytz.timezone("US/Eastern")
    result = dataflow_graph(
        tzinfo=tzinfo,
        start=date.today(),
        end=date.today() + timedelta(days=7)
    )
    return JsonResponse(result)
