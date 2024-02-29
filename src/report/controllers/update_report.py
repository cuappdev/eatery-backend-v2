from django.http import QueryDict

from eatery.datatype.Eatery import EateryID
from report.models import Report


class UpdateReportController:
    def __init__(self, id: int, update_map: QueryDict):
        """
        Update_map is a dictionary that maps the fields we want to update to
        the values we want to map them to

        Requires: id is a valid id and all keys in update_map are valid fields
            in the EateryStore class (except username/password cannot be provided),
            as well as an optional image field containing an image file to be uploaded
        """
        self.id = id
        self.update_data = {}

        # Query dict is immutable, so need to do this to remove id
        to_remove = ["id"]
        self.update_data = {}
        for key, val in update_map.items():
            if key not in to_remove:
                self.update_data[key] = val

    def process(self):
        """
        Selects DB entry we want to update and updates it using provided data
        """
        Report.objects.filter(id=self.id.value).update(**self.update_data)
        