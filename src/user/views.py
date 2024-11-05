from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from user.models import User
from user.serializers import UserSerializer
from eatery.models import Eatery
from item.models import Item
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from google.oauth2 import id_token
from google.auth.transport import requests
from user.models import User
from user_session.models import UserSession
import secrets
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
    
    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        id_token_str = request.data.get('idToken')
        user = request.data.get('user')

        if not id_token_str or not user:
            return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # verifies token
            idinfo = id_token.verify_oauth2_token(id_token_str, requests.Request(), os.getenv('GOOGLE_CLIENT_ID'))

            # ensures token is from Google
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                return Response({'error': 'Invalid token issuer'}, status=status.HTTP_401_UNAUTHORIZED)

            userid = idinfo['sub']
            email = idinfo['email']

            # ensures email is Cornell email
            if not email.endswith('@cornell.edu'):
                return Response({'error': 'Non-Cornell email used'}, status=status.HTTP_401_UNAUTHORIZED)

            # creates user if not exists
            user = User.objects.get_or_create(
                google_id=userid,
                defaults={
                    'email': email,
                    'given_name': idinfo.get('given_name', ''),
                    'family_name': idinfo.get('family_name', ''),
                    'netid': email.split('@')[0],
                }
            )

            # creates session token and makes new user session
            session_token = secrets.token_hex(20)
            UserSession.objects.create(user=user)

            return Response({'session_token': session_token}, status=status.HTTP_200_OK)

        except ValueError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['post'], url_path='logout')
    def logout(self, request):
        session_token = request.data.get('session_token')
        if not session_token:
            return Response({'error': 'Session token required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # gets and deletes user session
            user_session = UserSession.objects.get(session_token=session_token)
            user_session.delete()
            return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        except UserSession.DoesNotExist:
            return Response({'error': 'Invalid session token'}, status=status.HTTP_400_BAD_REQUEST)
