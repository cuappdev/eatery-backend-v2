# Eatery type returned to the frontend

from datetime import date
from typing import Mapping, Optional
from .Eatery import Eatery
from .WaitTimesByDay import WaitTimesByDay

import pytz

class EateryResult:

    def __init__(
            self,
            eatery: Eatery,
            wait_times_by_day: list[WaitTimesByDay]
    ):
        self.eatery = eatery
        self.wait_times_by_day = wait_times_by_day

    def to_json(
            self,
            tzinfo: Optional[pytz.timezone] = None,
            start: Optional[date] = None,
            end: Optional[date] = None
    ):
        eatery_json = self.eatery.to_json(tzinfo=tzinfo, start=start, end=end)
        eatery_json["wait_times_by_day"] = [day_wait_times.to_json() for day_wait_times in self.wait_times_by_day]
        return eatery_json
