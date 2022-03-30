from datetime import datetime, timedelta
from api.models import EateryStore
from api.datatype.Eatery import EateryID
import os
import hashlib
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.hashers import PBKDF2PasswordHasher as handler
from rest_framework import status

hasher = handler()

def get_user_by_id(id):
    return EateryStore.objects.filter(id=id.value).first()

def get_user_by_email(email):
    return EateryStore.objects.filter(email=email).first()

def get_user_by_session_token(session_token):
    return EateryStore.objects.filter(session_token=session_token).first()

def extract_token(request):
    auth_header = request.headers.get("Authorization")
    if auth_header is None:
        raise Exception("Malformed Request: missing auth header")

    bearer_token = auth_header.replace("Bearer ", "").strip()
    if bearer_token is None or not bearer_token:
        raise Exception("Malformed Request: missing bearer header")

    return bearer_token

def _urlsafe_base_64():
    return hashlib.sha1(os.urandom(64)).hexdigest()

def renew_session(user):
    session_token = _urlsafe_base_64()
    session_expiration = datetime.now() + timedelta(days=1)

    user.session_token = session_token
    user.session_expiration = session_expiration
    user.save()
    
    return session_token

class RegisterController:
    """
    If this eatery hasn't registered an email or password yet, then give 
    the eatery associated with EateryID an email and password.

    This:
        1) avoids registering email and password manually in admin, and 
        2) stores password hashed (not raw) in EateryStore
    """

    def __init__(self, id: EateryID, email: str, password: str):
        self.id = id
        self.email = email
        self.password = hasher.encode(password, "seasalt2")

        self.register_user = {}
        self.register_user["email"] = email
        self.register_user["password"] = password


    def process(self):
        user = get_user_by_id(self.id)
        if user is not None:
            raise Exception("User already registered")

        user = EateryStore.objects.filter(id = self.id.value).first()
        user.email = self.email
        user.password = self.password
        user.save()        
 

class PasswordRequestController:
    """send an email with link to update password"""
    def __init__(self, email: str):
        self.email = email

        self.user = get_user_by_email(email)
        self.subject = "Password Reset Requested"
        
        email_template_name = "password_reset_email.txt"
        email_info = {
            "email": email,
            'domain':'0.0.0.0:8000',
            'site_name': 'eatery',
            "uid": _urlsafe_base_64(),
            "user": self.user,
            'token': renew_session(self.user),
            'protocol': 'http',
        }

        self.reset_email = render_to_string(email_template_name, email_info)


    def process(self):
        send_mail(self.subject, self.reset_email, "admin@example.com", [self.user.email], fail_silently=False)

class UpdatePasswordController:
    """
    Given an email, the current (old) password, 
    change user's password to something new.
    """
    def __init__(self, password: str, token: str):
        self.password = password 
        self.token = token

    def verify_password(self, password):
        pass

    def process(self):
        user = get_user_by_session_token(self.token)

        if user is None:
            raise Exception("invalid token for password request")

        user.password = hasher.encode(self.password, "seasalt2")
        user.save()

    
class LoginController:
    """
    Given an email and password, verify the user's credentials.
    If email and password are correct, return new session token.
    """
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password 

    def verify_password(self, password):
        return hasher.verify(self.password, password)
        
    def process(self):
        user = get_user_by_email(self.email)
        if user is None:
            raise Exception("user not found.")

        user_password = getattr(user, "password")
        if not self.verify_password(user_password):
            raise Exception("Invalid email or password")

        token = renew_session(user)

        return token


class VerificationController:
    """
    Check if given session token is still valid.
    If not, prompt user to login again.
    """
    def __init__(self, session_token):
        self.session_token = session_token

    def verify_session_token(self, session_token, session_expiration):
        dt = timezone.make_aware(datetime.now(), timezone.get_default_timezone())
        return self.session_token == session_token and dt < session_expiration
        
    def process(self):
        user = get_user_by_session_token(self.session_token)
        if user is None:
            raise Exception("user not found")

        user_session_token = getattr(user, "session_token")
        user_session_expiration = getattr(user, "session_expiration")

        if user_session_token is None or not self.verify_session_token(user_session_token, user_session_expiration):
            raise Exception("Invalid session token. Please log in again.")
        

        

        

        