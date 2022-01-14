from datetime import datetime
from api.datatype.Eatery import EateryID
from api.models import ReportStore

class CreateReportController:

    def __init__(self, eatery_id: EateryID, type: str, content: str):
        self.eatery_id = eatery_id
        self.type = type
        self.content = content

    def process(self):
        current_timestamp = datetime.now().timestamp()
        ReportStore.objects.create(
            eatery_id = self.eatery_id.value,
            type = self.type,
            content = self.content,
            created_timestamp = current_timestamp
        )
        