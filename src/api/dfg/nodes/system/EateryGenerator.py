from api.dfg.nodes.DfgNode import DfgNode
from api.datatype.Eatery import Eatery, EateryID
from typing import Optional

class EateryGenerator(DfgNode):

    def __init__(
        self, 
        eatery_id: EateryID,
        events_dfg: Optional[DfgNode] = None, 
        wait_times_dfg: Optional[DfgNode] = None
    ):
        self.eatery_id = eatery_id
        self.events_dfg = events_dfg
        self.wait_times_dfg = wait_times_dfg

    def __call__(self, *args, **kwargs) -> list:
        return Eatery(
            id = self.eatery_id,
            events=None if self.events_dfg is None else self.events_dfg(*args, **kwargs),
            wait_times=None if self.wait_times_dfg is None else self.wait_times_dfg(*args, **kwargs)
        )

    def description(self):
        return "EateryGenerator"
