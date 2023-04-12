from rest_framework import status
from rest_framework.response import Response


def success_response(data="", status=status.HTTP_200_OK):
    """Returns a Response with `status` (200 default) and `data` if provided."""
    return Response({"data": data}, status=status)


def failure_response(message="", status=status.HTTP_404_NOT_FOUND):
    """Returns a Response with `status` (404 default) and `message` if provided."""
    return Response({"error": message}, status=status)