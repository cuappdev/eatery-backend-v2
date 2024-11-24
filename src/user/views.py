from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from user.models import User
from user.serializers import UserSerializer
from eatery.models import Eatery
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from google.oauth2 import id_token
from google.auth.transport import requests
from user.models import User
from device_token.models import DeviceToken
import os


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
        device_token = request.data.get("device_token")
        id_token_str = request.data.get("id_token")

        if not device_token:
            return Response(
                {"error": "device_token is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # create device token if doesnt exist
            device_token_obj = DeviceToken.objects.get_or_create(
                device_token=device_token,
                defaults={'user': User.objects.create(netid=None)}
            )
            user = device_token_obj.user
        except Exception as e:
            return Response(
                {"error": f"Error processing device token: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if id_token_str:
            try:
                # verifies token
                idinfo = id_token.verify_oauth2_token(
                    id_token_str, requests.Request(), os.getenv("GOOGLE_CLIENT_ID")
                )

                # ensures token is from Google
                if idinfo["iss"] not in [
                    "accounts.google.com",
                    "https://accounts.google.com",
                ]:
                    return Response(
                        {"error": "Invalid token issuer"},
                        status=status.HTTP_401_UNAUTHORIZED,
                    )

                userid = idinfo["sub"]
                email = idinfo["email"]

                # ensures email is Cornell email
                if not email.endswith("@cornell.edu"):
                    return Response(
                        {"error": "Non-Cornell email used"},
                        status=status.HTTP_401_UNAUTHORIZED,
                    )

                # creates user if not exists
                authenticated_user = User.objects.get_or_create(
                    google_id=userid,
                    defaults={
                        "email": email,
                        "given_name": idinfo.get("given_name", ""),
                        "family_name": idinfo.get("family_name", ""),
                        "netid": email.split("@")[0],
                    },
                )

                if user == authenticated_user:
                    pass
                elif user.netid is None:
                    # was unauthorized user, update to authenticated user

                    # copy favorites
                    authenticated_user.favorite_items = list(
                        set(authenticated_user.favorite_items + user.favorite_items)
                    )
                    authenticated_user.favorite_eateries.add(*user.favorite_eateries.all())
                    authenticated_user.save()

                    # copy device token
                    device_token_obj.user = authenticated_user
                    device_token_obj.save()

                    # delete unauthorized user after merging
                    user.delete()
                else:
                    # device token is associated with a different user, should not happen
                    return Response(
                        {"error": "Device token is associated with another user"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                return Response({"device_token": device_token}, status=status.HTTP_200_OK)

            except ValueError:
                return Response(
                    {"error": "Invalid id_token"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            # no id_token provided, user is anonymous
            if user.netid is None:
                pass
            else:
                # device token associated with an authenticated user but no id_token provided
                return Response(
                    {"error": "Device token associated with an authenticated user"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            return Response({"device_token": device_token}, status=status.HTTP_200_OK)



    @action(detail=False, methods=["post"], url_path="logout")
    def logout(self, request):
        device_token = request.data.get("device_token")
        if not device_token:
            return Response(
                {"error": "Device token required"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            # delete the device token
            device_token_obj = DeviceToken.objects.get(device_token=device_token)
            user = device_token_obj.user
            device_token_obj.delete()

            # if user was anonymous and has no device tokens, delete the user
            if user.netid is None and not DeviceToken.objects.filter(user=user).exists():
                user.delete()

            return Response(
                {"message": "Logged out successfully"}, status=status.HTTP_200_OK
            )
        except DeviceToken.DoesNotExist:
            return Response(
                {"error": "Invalid device token"}, status=status.HTTP_400_BAD_REQUEST
            )
