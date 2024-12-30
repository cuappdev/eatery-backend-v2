import firebase_admin
from firebase_admin import credentials

from django.conf import settings

# Initialize Firebase Admin SDK
cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS)
firebase_admin.initialize_app(cred)

print("Firebase initialized successfully!")
