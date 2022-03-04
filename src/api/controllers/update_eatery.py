from django.http import QueryDict
from api.models import EateryStore
import base64
import asyncio


class UpdateEateryController:
    def __init__(self, id: int, update_map: QueryDict, image):
        '''
        Update_map is a dictionary that maps the fields we want to update to 
        the values we want to map them to

        Requires: id is a valid id and all keys in update_map are valid columns
        '''
        self.id = id
        self.update_data = {}
        allowed_fields = ["name", "menu_summary", "location", "campus_area", "online_order_url", "latitude",
                          "longitude", "payment_accepts_meal_swipes", "payment_accepts_brbs", "payment_accepts_cash"]

        if image is not None:
            asyncio.run(self.upload_image(image))

        for key, val in update_map.items():
            if key in allowed_fields:
                self.update_data[key] = val

    async def upload_image(self, image):
        '''
        Helper method that asynchronously uploads image bytes to assets repo
        Returns: stored image URL
        '''

        b64_encoded_image = b""
        # Encodes bytes in chunks to handle large image files efficiently
        for chunk in image.chunks():
            b64_encoded_image += base64.b64encode(chunk)

        print(b64_encoded_image)

    def process(self):
        '''
        Selects the DB entry we want to update and updates it using provided data
        '''

        # Uses double-splat to map stored update dict to kwargs
        EateryStore.objects.filter(id=self.id).update(**self.update_data)
