from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from user.models import User, UserFCMDevice
from user.serializers import UserSerializer
from eatery.models import Eatery
from item.models import Item
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny

# from rest_framework.permissions import IsAuthenticated


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
        item_id = request.data.get("item_id")
        item = get_object_or_404(Item, id=item_id)
        user.favorite_items.add(item)
        user.save()
        user_data = UserSerializer(user).data
        return Response(user_data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="item/remove")
    def remove_favorite_item(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        item_id = request.data.get("item_id")
        item = get_object_or_404(Item, id=item_id)
        user.favorite_items.remove(item)
        user.save()
        user_data = UserSerializer(user).data
        return Response(user_data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["post"],
        url_path="register_fcm_token",
        permission_classes=[AllowAny],
    )
    def register_fcm_token(self, request):
        registration_id = request.data.get("registration_id")
        device_id = request.data.get("device_id")
        device_type = request.data.get("device_type")

        if not (registration_id and device_id and device_type):
            return Response(
                {"success": False, "message": "All fields are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Update or create the FCM device without associating it to a user
        device, created = UserFCMDevice.objects.update_or_create(
            device_id=device_id,
            defaults={
                "registration_id": registration_id,
                "type": device_type,
                "user": None,  # No user associated for now
            },
        )

        response_data = {
            "success": True,
            "message": "FCM token registered successfully.",
            "device": {
                "device_id": device.device_id,
                "registration_id": device.registration_id,
                "device_type": device.type,
                "created": created,
            },
        }

        return Response(response_data, status=status.HTTP_200_OK)
