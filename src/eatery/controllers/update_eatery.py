import base64
import os
import requests
from django.http import QueryDict

from eatery.datatype.Eatery import EateryID
from eatery.models import Eatery


class UpdateEateryController:
    def __init__(self, id: EateryID, update_map: QueryDict, image):
        """
        Update_map is a dictionary that maps the fields we want to update to
        the values we want to map them to

        Requires: id is a valid id and all keys in update_map are valid fields
            in the EateryStore class (except username/password cannot be provided),
            as well as an optional image field containing an image file to be uploaded
        """
        self.id = id
        self.update_data = {}

        if image is not None:
            img_url = self.upload_image(image)
            self.update_data["image_url"] = img_url

        # Query dict is immutable, so need to do this to remove id
        to_remove = ["id"]
        self.update_data = {}
        for key, val in update_map.items():
            if key not in to_remove:
                self.update_data[key] = val

    def upload_image(self, image):
        """
        Helper method that asynchronously uploads image bytes to assets repo
        Returns: stored image URL
        Raises: Exception invalid file extension when a non jpg, jpeg, gif, or png is provided
        """

        valid_extensions = ["jpg", "jpeg", "gif", "png"]
        extension = (str(image)).split(".")
        extension = extension[len(extension) - 1]
        if extension == "jpg":
            extension = "jpeg"

        if extension not in valid_extensions:
            raise Exception("Invalid File Extension")

        b64_encoded_image = b""
        # Encodes bytes in chunks to handle large image files efficiently
        for chunk in image.chunks():
            b64_encoded_image += base64.b64encode(chunk)

        b64_encoded_image = b64_encoded_image.decode("utf-8")

        response = requests.post(
            "https://upload.cornellappdev.com/upload/",
            json={
                "bucket": os.environ["IMAGE_BUCKET"],
                "image": f"data:image/{extension};base64,{b64_encoded_image}",
            },
        )

        try:
            return response.json()["data"]
        except Exception:
            raise Exception("Image uploading unsuccessful")

    """
    Pull new data from CornellDiningNow
    >> left merge Eatery and CornellDiningNow
    >> left merge Events and CornellDiningNow
    """

    def compare(self):
        pass

    def process(self):
        """
        Selects DB entry we want to update and updates it using provided data
        """
        # use double-splat to convert dict to kwargs
        Eatery.objects.filter(id=self.id.value).update(**self.update_data)
