from typing import TypeVar, Optional

from api.datatype.Eatery import Eatery
from api.datatype.Event import Event
from api.datatype.WaitTimesDay import WaitTimesDay
from api.dfg.DfgNode import DfgNode
from api.dfg.EateryToJson import EateryToJson

T = TypeVar('T')

class LeftMerge(DfgNode):

    def __init__(self, left: DfgNode, right: DfgNode):
        self.left = left
        self.right = right

    def children(self):
        return [self.left, self.right]

    def __call__(self, *args, **kwargs):
        merged_eateries = []
        right_eateries = self.right(*args, **kwargs)
        for left_eatery in self.left(*args, **kwargs):
            updated_eatery = next((right_eatery for right_eatery in right_eateries if right_eatery.id == left_eatery.id), None)
            if updated_eatery == None:
                merged_eateries.append(left_eatery)
            else:
                right_eateries = [right_eatery for right_eatery in right_eateries if right_eatery.id != left_eatery.id]
                merged_eateries.append(LeftMerge.merge_eateries(left_eatery, updated_eatery))

        return merged_eateries

    @staticmethod 
    def merge_eateries(left: Eatery, right: Eatery):
        merged_events = LeftMerge.merge_events(left.events(), right.events())
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
            merged_events.append(left_event)
        merged_events.extend(right)
        return merged_events

    @staticmethod
    def merge_and_filter_waittimes(left: list[WaitTimesDay], right: list[WaitTimesDay], events: list[Event]) -> list[WaitTimesDay]:
        wait_times_filtered = []
        wait_times = LeftMerge.merge_fields(left, right)
        if wait_times is None:
            return None
        for wait_times_by_day in wait_times:
            filtered_data = []
            for wait_time_data in wait_times_by_day.data:
                if any([wait_time_data.timestamp in event for event in events]):
                    filtered_data.append(wait_time_data)
            wait_times_filtered.append(
                WaitTimesDay(canonical_date=wait_times_by_day.canonical_date, data=filtered_data)
            )
        return wait_times_filtered
        

    def children(self):
        return self.children

    def description(self):
        return "LeftMerge"