from datetime import date, timedelta

import pytz
from django.http import JsonResponse

from api.dfg.CornellDiningNow import CornellDiningNow
from api.dfg.EateryStubs import EateryStubs
from api.dfg.ExternalEateries import ExternalEateries

from api.dfg.DictResponseWrapper import DictResponseWrapper
from api.dfg.EateryToJson import EateryToJson
from api.dfg.InMemoryCache import InMemoryCache
from api.dfg.macros.LeftMergeEateries import LeftMergeEateries
from api.dfg.WaitTimes import WaitTimes
from api.dfg.WaitTimeFilter import WaitTimeFilter

dataflow_graph = DictResponseWrapper(
    EateryToJson(
        InMemoryCache(
            WaitTimeFilter(
                LeftMergeEateries(
                    WaitTimes(),
                    LeftMergeEateries(
                        ExternalEateries(),
                        LeftMergeEateries(
                            CornellDiningNow(),
                            EateryStubs()
                        )
                    )
                )
            )
        )
    ),
    re_raise_exceptions=True
)

def index(request):
    tzinfo = pytz.timezone("US/Eastern")
    reload = request.GET.get('reload')
    result = dataflow_graph(
        tzinfo=tzinfo,
        reload=reload is not None and reload != "false",
        start=date.today(),
        end=date.today() + timedelta(days=7)
    )
    return JsonResponse(result)

def google_sheets_eateries(request):
    # dfg = DictResponseWrapper(
    #     EateryToJson(
    #         GoogleSheetsEateries(
    #             spreadsheet_id="1ImfeTUA6I1Ub-aavgIW53Pf7EVB694f1294NPSCRd5c"
    #         )
    #     )
    # )

    # result = dfg(
    #     tzinfo=pytz.timezone("US/Eastern"),
    #     start=date.today(),
    #     end=date.today() + timedelta(days=7)
    # )

    return JsonResponse([])