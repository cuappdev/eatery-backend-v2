from datetime import date, timedelta

import pytz
from django.http import JsonResponse
from rest_framework.views import APIView

from dfg.nodes.CornellDiningNow import CornellDiningNow
from dfg.nodes.EateryStubs import EateryStubs
from dfg.nodes.EateriesFromDB import EateriesFromDB
from dfg.nodes.macros.EateryEvents import EateryEvents

from dfg.nodes.system.DictResponseWrapper import DictResponseWrapper
from dfg.nodes.system.ConvertToJson import ConvertToJson
from dfg.nodes.system.EateryGenerator import EateryGenerator
from dfg.nodes.system.InMemoryCache import InMemoryCache
from dfg.nodes.system.Mapping import Mapping

from dfg.nodes.macros.LeftMergeEateries import LeftMergeEateries

from dfg.nodes.wait_times.WaitTimes import WaitTimes
from dfg.nodes.wait_times.WaitTimeFilter import WaitTimeFilter

class MainDfgView(APIView):
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
                                EateriesFromDB(),
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

    def get(self, request):
        tzinfo = pytz.timezone("US/Eastern")
        reload = request.GET.get('reload')
        result = self.main_dfg(
            tzinfo=tzinfo,
            reload=reload is not None and reload != "false",
            start=date.today(),
            end=date.today() + timedelta(days=7)
        )
        return JsonResponse(result)