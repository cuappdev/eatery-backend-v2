from datetime import date, timedelta

import pytz
from django.http import JsonResponse
from api.dfg.CalculateWaitTimes import CalculateWaitTimes

from api.dfg.Concat import Concat
from api.dfg.CornellDiningNow import CornellDiningNow
from api.dfg.DictResponseWrapper import DictResponseWrapper
from api.dfg.EateryToJson import EateryToJson
from api.dfg.ExternalEateries import ExternalEateries
from api.dfg.GoogleSheetsEateries import GoogleSheetsEateries

dataflow_graph = DictResponseWrapper(
    EateryToJson(
        CalculateWaitTimes(
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

def google_sheets_eateries(request):
    dfg = DictResponseWrapper(
        EateryToJson(
            GoogleSheetsEateries(
                spreadsheet_id="1ImfeTUA6I1Ub-aavgIW53Pf7EVB694f1294NPSCRd5c"
            )
        )
    )

    result = dfg(
        tzinfo=pytz.timezone("US/Eastern"),
        start=date.today(),
        end=date.today() + timedelta(days=7)
    )

    return JsonResponse(result)