from typing import Dict
from api.dfg.nodes.CornellDiningNow import CornellDiningNow
from api.dfg.nodes.EateriesFromDB import EateriesFromDB
from api.dfg.nodes.EateryStubs import EateryStubs
from api.dfg.nodes.macros.EateryEvents import EateryEvents
from api.dfg.nodes.macros.LeftMergeEateries import LeftMergeEateries
from api.dfg.nodes.system.ConvertToJson import ConvertToJson
from api.dfg.nodes.system.DictResponseWrapper import DictResponseWrapper
from api.dfg.nodes.system.EateryGenerator import EateryGenerator
from api.dfg.nodes.system.InMemoryCache import InMemoryCache
from api.dfg.nodes.system.Mapping import Mapping
from api.dfg.nodes.wait_times.WaitTimeFilter import WaitTimeFilter
from api.dfg.nodes.wait_times.WaitTimes import WaitTimes

main_dfg = DictResponseWrapper(
    ConvertToJson(
        InMemoryCache(
            WaitTimeFilter(
                LeftMergeEateries(
                    Mapping(
                        child=EateryStubs(),
                        fn=lambda eatery, cache: EateryGenerator(
                            eatery_id=eatery.id,
                            wait_times_dfg=WaitTimes(eatery.id, cache),
                        ),
                    ),
                    LeftMergeEateries(
                        Mapping(
                            child=EateryStubs(),
                            fn=lambda eatery, cache: EateryGenerator(
                                eatery_id=eatery.id,
                                events_dfg=EateryEvents(eatery.id, cache),
                            ),
                        ),
                        LeftMergeEateries(
                            EateriesFromDB(),
                            LeftMergeEateries(CornellDiningNow(), EateryStubs()),
                        ),
                    ),
                )
            )
        )
    ),
    re_raise_exceptions=True,
)
