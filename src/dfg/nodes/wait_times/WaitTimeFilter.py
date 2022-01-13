from dfg.datatype.WaitTimesDay import WaitTimesDay
from dfg.nodes.DfgNode import DfgNode


# Removes all wait times that are not part of the eatery's events

class WaitTimeFilter(DfgNode):
    def __init__(self, child: DfgNode):
        self.child = child

    def children(self):
        return [self.child]

    def __call__(self, *args, **kwargs):
        eateries = self.child(*args, **kwargs)
        result = []
        for eatery in eateries:
            if eatery.wait_times is None:
                result.append(eatery.clone())
            else:
                wait_times_filtered = []
                for day_wait_times in eatery.wait_times:
                    filtered_data = []
                    for wait_time_data in day_wait_times.data:
                        eatery_events = eatery.events()
                        if any([wait_time_data.timestamp in event for event in eatery_events]):
                            filtered_data.append(wait_time_data)
                    if len(filtered_data) > 0:
                        wait_times_filtered.append(WaitTimesDay(
                            canonical_date=day_wait_times.canonical_date,
                            data=filtered_data
                        ))
                eatery_clone = eatery.clone()
                eatery_clone.wait_times = wait_times_filtered
                result.append(eatery_clone)
        return result

    def description(self):
        return "WaitTimeFilter"
