from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from user.models import User
from user.serializers import UserSerializer
from eatery.models import Eatery
from item.models import Item
from django.shortcuts import get_object_or_404


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
        return Response({"status": "eatery added"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="eatery/remove")
    def remove_favorite_eatery(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        eatery_id = request.data.get("eatery_id")
        eatery = get_object_or_404(Eatery, id=eatery_id)
        user.favorite_eateries.remove(eatery)
        user.save()
        return Response({"status": "eatery removed"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="item/add")
    def add_favorite_item(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        item_id = request.data.get("item_id")
        item = get_object_or_404(Item, id=item_id)
        user.favorite_items.add(item)
        user.save()
        return Response({"status": "item added"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="item/remove")
    def remove_favorite_item(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        item_id = request.data.get("item_id")
        item = get_object_or_404(Item, id=item_id)
        user.favorite_items.remove(item)
        user.save()
        return Response({"status": "item removed"}, status=status.HTTP_200_OK)
