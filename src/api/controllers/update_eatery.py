from django.http import QueryDict
from api.models import EateryStore
from mimetypes import guess_extension, guess_type
import base64
import requests
import os


class UpdateEateryController:
    def __init__(self, id: int, update_map: QueryDict, image):
        """
        Update_map is a dictionary that maps the fields we want to update to
        the values we want to map them to

        Requires: id is a valid id and all keys in update_map are valid fields
            in the EateryStore class
        Raises: Exception when invalid keys are provided
        """
        self.id = id
        self.update_data = {}

        if image is not None:
            img_url = self.upload_image(image)
            self.update_data["image_url"] = img_url

        for key, val in update_map.items():
            try:
                self.update_data[key] = val
            except:
                raise Exception("Invalid update field(s) provided")

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
        except:
            raise Exception("Image uploading unsuccessful")

    def process(self):
        """
        Selects DB entry we want to update and updates it using provided data
        """

        # Uses double-splat to map stored update dict to kwargs
        EateryStore.objects.filter(id=self.id).update(**self.update_data)
