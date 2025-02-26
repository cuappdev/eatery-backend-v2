from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests
import os

from user.models import User
from user.serializers import UserSerializer
from eatery.models import Eatery

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=["post"], url_path="eatery/add")
    def add_favorite_eatery(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        eatery_id = request.data.get("eatery_id")
        eatery = get_object_or_404(Eatery, id=eatery_id)
        user.favorite_eateries.add(eatery)
        user.save()
        user_data = UserSerializer(user).data
        return Response(user_data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="eatery/remove")
    def remove_favorite_eatery(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        eatery_id = request.data.get("eatery_id")
        eatery = get_object_or_404(Eatery, id=eatery_id)
        user.favorite_eateries.remove(eatery)
        user.save()
        user_data = UserSerializer(user).data
        return Response(user_data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="item/add")
    def add_favorite_item(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        item_name = request.data.get("item_name")
        if item_name and item_name not in user.favorite_items:
            user.favorite_items.append(item_name)
            user.save()
        user_data = UserSerializer(user).data
        return Response(user_data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="item/remove")
    def remove_favorite_item(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        item_name = request.data.get("item_name")
        if item_name in user.favorite_items:
            user.favorite_items.remove(item_name)
            user.save()
        user_data = UserSerializer(user).data
        return Response(user_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="login")
    def login(self, request):
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            id_token_str = auth_header[7:]
        else:
            id_token_str = request.data.get("id_token")

        if not id_token_str:
            return Response({"error": "id_token is required"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            idinfo = google_id_token.verify_oauth2_token(
                id_token_str, requests.Request(), os.getenv("GOOGLE_CLIENT_ID")
            )
            if idinfo.get("iss") not in ["accounts.google.com", "https://accounts.google.com"]:
                return Response({"error": "Invalid token issuer"},
                                status=status.HTTP_401_UNAUTHORIZED)

            google_user_id = idinfo["sub"]

            # # ensure the email is a Cornell email.
            # if not email.endswith("@cornell.edu"):
            #     return Response({"error": "Non-Cornell email used"},
            #                     status=status.HTTP_401_UNAUTHORIZED)


            user, _ = User.objects.get_or_create(
                google_id=google_user_id,
                defaults={
                    # "email": email,
                    "given_name": idinfo.get("given_name", ""),
                    "family_name": idinfo.get("family_name", ""),
                    # "netid": email.split("@")[0],
                },
            )

            favorites = request.data.get("favorite_items")
            if favorites and isinstance(favorites, list):
                merged_favorites = list(set(user.favorite_items + favorites))
                user.favorite_items = merged_favorites

            fcm_token = request.data.get("fcm_token")
            if fcm_token:
                user.fcm_token = fcm_token

            user.save()
            user_data = UserSerializer(user).data
            return Response(user_data, status=status.HTTP_200_OK)

        except ValueError:
            return Response({"error": "Invalid id_token"},
                            status=status.HTTP_400_BAD_REQUEST)
