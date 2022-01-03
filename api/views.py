from datetime import date, timedelta

import pytz
from django.http import JsonResponse
from api.dfg.waittimes.FetchTransactionCounts import FetchTransactionCounts

from api.dfg.preparation.CornellDiningNow import CornellDiningNow
from api.dfg.preparation.EateryStubs import EateryStubs
from api.dfg.preparation.ExternalEateries import ExternalEateries

from api.dfg.assembly.AssembleEateries import AssembleEateries
from api.dfg.waittimes.AddWaitTimesToEateries import AddWaitTimesToEateries

from api.dfg.DictResponseWrapper import DictResponseWrapper
from api.dfg.EateryToJson import EateryToJson
from api.dfg.InMemoryCache import InMemoryCache

dataflow_graph = DictResponseWrapper(
    EateryToJson(
        InMemoryCache(
            AddWaitTimesToEateries(
                eateries=AssembleEateries(
                    stubs=EateryStubs(),
                    cornell_dining=CornellDiningNow(),
                    override=ExternalEateries()
                ),
                transaction_counts = FetchTransactionCounts()
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
        reload=reload is not None and reload is not "false",
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