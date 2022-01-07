from datetime import date, timedelta

import pytz
from django.http import JsonResponse
from api.datatype.Eatery import Eatery

from api.dfg.CornellDiningNow import CornellDiningNow
from api.dfg.EateryStubs import EateryStubs
from api.dfg.ExternalEateries import ExternalEateries
from api.dfg.macros.EateryEvents import EateryEvents

from api.dfg.util.DictResponseWrapper import DictResponseWrapper
from api.dfg.util.ConvertToJson import ConvertToJson
from api.dfg.util.EateryGenerator import EateryGenerator
from api.dfg.util.InMemoryCache import InMemoryCache
from api.dfg.util.Mapping import Mapping

from api.dfg.macros.LeftMergeEateries import LeftMergeEateries

from api.dfg.wait_times.WaitTimes import WaitTimes
from api.dfg.wait_times.WaitTimeFilter import WaitTimeFilter

main_dfg = DictResponseWrapper(
    ConvertToJson(
        InMemoryCache(
            WaitTimeFilter(
                LeftMergeEateries(
                    Mapping(
                        child=EateryStubs(),
                        fn = lambda eatery, cache: EateryGenerator(
                            eatery_id=eatery.id,
                            wait_times_dfg=WaitTimes(eatery.id, cache)
                        )
                    ),
                    LeftMergeEateries(
                        Mapping(
                            child = EateryStubs(),
                            fn = lambda eatery, cache: EateryGenerator(
                                eatery_id=eatery.id,
                                events_dfg=EateryEvents(eatery.id, cache)
                            )
                        ),
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
        )
    ),
    re_raise_exceptions=True
)


def index(request):
    tzinfo = pytz.timezone("US/Eastern")
    reload = request.GET.get('reload')
    result = main_dfg(
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
