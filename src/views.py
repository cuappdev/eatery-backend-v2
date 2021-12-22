from django.http import JsonResponse
from src.dfg.DictResponseWrapper import DictResponseWrapper
from src.dfg.EateryGroupByType import EateryGroupByType
from src.dfg.EateryToJson import EateryToJson
from src.dfg.ExternalEateries import ExternalEateries
from src.dfg.Concat import Concat
from src.dfg.CornellDiningNow import CornellDiningNow
from src.dfg.InMemoryCache import InMemoryCache

dataflow_graph = DictResponseWrapper(
    EateryToJson(
        EateryGroupByType(
            InMemoryCache(
                Concat([
                    CornellDiningNow(),
                    ExternalEateries()
                ])
            )
        )
    )
)


def index(request):
    result = dataflow_graph()
    return JsonResponse(result)
