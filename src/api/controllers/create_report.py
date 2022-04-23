from datetime import datetime
from typing import Optional

from api.models import ReportStore
from eatery.datatype.Eatery import EateryID


class CreateReportController:
    def __init__(self, type: str, content: str, eatery_id: Optional[EateryID] = None):
        self.eatery_id = eatery_id
        self.type = type
        self.content = content

    def process(self):
        current_timestamp = datetime.now().timestamp()
        ReportStore.objects.create(
            eatery_id=self.eatery_id.value if self.eatery_id else None,
            type=self.type,
            content=self.content,
            created_timestamp=current_timestamp,
        )
