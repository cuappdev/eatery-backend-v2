from typing import TypeVar, Optional

from api.datatype.Eatery import Eatery
from api.datatype.Event import Event
from api.datatype.WaitTimesByDay import WaitTimesByDay
from api.dfg.DfgNode import DfgNode
from api.dfg.EateryToJson import EateryToJson

T = TypeVar('T')

class LeftMerge(DfgNode):

    def __init__(self, left: DfgNode, right: DfgNode):
        self.left = left
        self.right = right

    def __call__(self, *args, **kwargs):
        merged_eateries = []
        right_eateries = self.right(*args, **kwargs)
        for left_eatery in self.left(*args, **kwargs):
            updated_eatery = next((right_eatery for right_eatery in right_eateries if right_eatery.id == left_eatery.id), None)
            if updated_eatery == None:
                merged_eateries.append(left_eatery)
            else:
                right_eateries = [right_eatery for right_eatery in right_eateries if right_eatery.id != left_eatery.id]

        merged_eateries.add(right_eateries)
        return merged_eateries

    @staticmethod 
    def merge_eateries(left: Eatery, right: Eatery):
        merged_events = LeftMerge.merge_events(left.events, right.events)
        return Eatery(
            id=left.id,
            name=LeftMerge.merge_fields(left.name, right.name),
            campus_area=LeftMerge.merge_fields(left.campus_area, right.campus_area),
            events=merged_events,
            latitude=LeftMerge.merge_fields(left.latitude, right.latitude),
            longitude=LeftMerge.merge_fields(left.longitude, right.longitude),
            location=LeftMerge.merge_fields(left.location, right.location),
            online_order=LeftMerge.merge_fields(left.online_order, right.online_order),
            online_order_url=LeftMerge.merge_fields(left.online_order_url, right.online_order_url),
            wait_times=LeftMerge.merge_and_filter_waittimes(left.wait_times, right.wait_times, merged_events)
        )

    @staticmethod
    def merge_fields(left: Optional[T], right: Optional[T]) -> Optional[T]:
        return right if left is None else left

    @staticmethod
    def merge_events(left: list[Event], right: list[Event]):
        merged_events = []
        for left_event in left:
            right = [
                right_event for right_event in right if 
                right_event.canonical_date != left_event.canonical_date or 
                right_event.description != left_event.description
            ]
            merged_events.add(left_event)
        merged_events.add(right)
        return merged_events

    @staticmethod
    def merge_and_filter_waittimes(left: list[WaitTimesByDay], right: list[WaitTimesByDay], events: list[Event]) -> list[WaitTimesByDay]:
        wait_times_filtered = []
        wait_times = LeftMerge.merge_fields(left, right)
        if wait_times is None:
            return None
        for wait_times_by_day in wait_times:
            wait_times_by_day_filtered = []
            for wait_time in wait_times_by_day.daily_wait_times:
                if any([wait_time.timestamp in event for event in events]):
                    wait_times_by_day_filtered.append(wait_time)
            wait_times_filtered.append(
                WaitTimesByDay(canonical_date=wait_times_by_day.canonical_date, wait_times=wait_times_by_day_filtered)
            )
        return wait_times_filtered
        

    def children(self):
        return self.children

    def description(self):
        return "Merge"