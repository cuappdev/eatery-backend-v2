from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
import requests as http_requests
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

    @action(detail=False, methods=["post"], url_path="authorize")
    def authorize(self, request):
        auth_header = request.headers.get("Authorization")

        # header should be in the form "Bearer <session_id>"
        if not auth_header:
            return Response({"error": "Missing authorization header"},
                            status=status.HTTP_400_BAD_REQUEST)
        if not auth_header.startswith("Bearer "):
            return Response({"error": "Invalid authorization header - must start with 'Bearer '"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        session_id = auth_header[7:]

        device_id = request.data.get("deviceId")
        pin = request.data.get("pin")
        fcm_token = request.data.get("fcmToken")

        if not device_id or not pin:
            return Response({"error": "deviceId, pin required"},
                            status=status.HTTP_400_BAD_REQUEST)

        # prepare payload for GET API
        payload = {
            "method": "createPIN",
            "params": {
                "PIN": pin,
                "deviceId": device_id,
                "sessionId": session_id
            }
        }

        # call createPIN from GET API
        try:
            get_response = http_requests.post(
                "https://services.get.cbord.com/GETServices/services/json/user",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            result = get_response.json()
        except Exception as e:
            return Response({"error": "Error communicating with GET API", "details": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        """
        note: right now if session_id is invalid, response is "error": "4001|Session not found" 
        and this retuns 400 
        """
        # return 401 if “Error: not validated” in result otherwise return 400
        if result.get("exception"):
            if "not validated" in result.get("exception"):
                return Response({"error": result.get("exception")},
                                status=status.HTTP_401_UNAUTHORIZED)
            return Response({"error": result.get("exception")},
                            status=status.HTTP_400_BAD_REQUEST)

        favorites = request.data.get("favorite_items")

        user, _ = User.objects.get_or_create(
            device_id=device_id,
            defaults={}
        )

        # merge favorites if they exist
        if favorites and isinstance(favorites, list):
            merged_favorites = list(set(user.favorite_items + favorites))
            user.favorite_items = merged_favorites

        if fcm_token:
            user.fcm_token = fcm_token

        user.save()
        user_data = UserSerializer(user).data
        return Response(user_data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["post"], url_path="refresh")
    def refresh(self, request):
        device_id = request.data.get("deviceId")
        pin = request.data.get("pin")
        if not device_id or not pin:
            return Response({"error": "deviceId and pin are required"},
                            status=status.HTTP_400_BAD_REQUEST)

        payload = {
            "method": "authenticatePIN",
            "params": {
                "systemCredentials": {
                    "domain": "",
                    "userName": "get_mobile",
                    "password": "NOTUSED"
                },
                "deviceId": device_id,
                "pin": pin
            }
        }

        # refresh sessionId with GET API's authenticatePIN method
        try:
            get_response = http_requests.post(
                "https://services.get.cbord.com/GETServices/services/json/authentication",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            result = get_response.json()
        except Exception as e:
            return Response({"error": "Error communicating with GET API", "details": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # if exception, return 401 and user should be fully logged out
        if result.get("exception"):
            return Response({"error": result.get("exception")},
                            status=status.HTTP_401_UNAUTHORIZED)

        new_session_id = result.get("response")
        if not new_session_id:
            return Response({"error": "Failed to retrieve new sessionId"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"sessionId": new_session_id}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="transactions")
    def transactions(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return Response({"error": "Missing authorization header"},
                            status=status.HTTP_400_BAD_REQUEST)
        if not auth_header.startswith("Bearer "):
            return Response({"error": "Invalid authorization header - must start with 'Bearer '"},
                            status=status.HTTP_400_BAD_REQUEST)
        session_id = auth_header[7:]
        
        # note: gets 100 most recent transcations including meal swipes, so we dont
        # have an exact number of BRB transactions. can change to date range if it 
        # becomes a problem
        payload = {
            "method": "retrieveTransactionHistoryWithinDateRange",
            "params": {
                "paymentSystemType": 0,
                "queryCriteria": {
                    "maxReturnMostRecent": 100,
                    "newestDate": None,
                    "oldestDate": None,
                    "accountId": None
                },
                "sessionId": session_id
            }
        }
        
        try:
            get_response = http_requests.post(
                "https://services.get.cbord.com/GETServices/services/json/commerce",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            result = get_response.json()
        except Exception as e:
            return Response({"error": "Error communicating with GET API", "details": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # brb transactions (tenderId == "000000449")
        transactions = result.get("response", {}).get("transactions", [])
        brb_transactions = []
        for txn in transactions:
            account_name = txn.get("accountName", "")
            if "City Bucks" in account_name or "Big Red Bucks" in account_name:
                brb_transactions.append({
                    "amount": txn.get("amount"),
                    "tenderId": txn.get("tenderId"),
                    "accountName": account_name,
                    "date": txn.get("postedDate"),
                    "location": txn.get("locationName")
                })
        
        return Response({"transactions": brb_transactions}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["post"], url_path="accounts")
    def accounts(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return Response({"error": "Missing or invalid authorization header"},
                            status=status.HTTP_400_BAD_REQUEST)
        session_id = auth_header[7:]
        
        device_id = request.data.get("deviceId")
        if not device_id:
            return Response({"error": "deviceId is required"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        payload = {
            "method": "retrieveAccounts",
            "params": {
                "sessionId": session_id
            }
        }
        
        try:
            get_response = http_requests.post(
                "https://services.get.cbord.com/GETServices/services/json/commerce",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            result = get_response.json()
        except Exception as e:
            return Response({"error": "Error communicating with GET API", "details": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        accounts = result.get("response", {}).get("accounts", [])
        brb_account = None
        city_bucks_account = None
        laundry_account = None
        
        for account in accounts:
            display_name = account.get("accountDisplayName", "")
            if "Big Red Bucks" in display_name and brb_account is None:
                brb_account = account
            # two city bucks accounts, one for GET which is not the main one
            if "City Bucks" in display_name and "GET" not in display_name and city_bucks_account is None:
                city_bucks_account = account
            if "Laundry" in display_name and laundry_account is None:
                laundry_account = account
            if brb_account and city_bucks_account and laundry_account:
                break
        
        try:
            user = User.objects.get(device_id=device_id)
        except User.DoesNotExist:
            return Response({"error": "User not found for the given deviceId"}, status=status.HTTP_404_NOT_FOUND)
        
        # update brb balance and account name
        if brb_account:
            user.brb_balance = brb_account.get("balance", 0)
            user.brb_account_name = brb_account.get("accountDisplayName", "")
        else:
            user.brb_account_name = None

        if city_bucks_account:
            user.city_bucks_balance = city_bucks_account.get("balance", 0)
            user.city_bucks_account_name = city_bucks_account.get("accountDisplayName", "")
        else:
            user.city_bucks_account_name = None

        if laundry_account:
            user.laundry_balance = laundry_account.get("balance", 0)
            user.laundry_account_name = laundry_account.get("accountDisplayName", "")
        else:
            user.laundry_account_name = None

        user.save()

        return Response({
            "brb": {"name": user.brb_account_name, "balance": user.brb_balance},
            "city_bucks": {"name": user.city_bucks_account_name, "balance": user.city_bucks_balance},
            "laundry": {"name": user.laundry_account_name, "balance": user.laundry_balance}
        }, status=status.HTTP_200_OK)