import firebase_admin
from firebase_admin import credentials, firestore
from django.conf import settings

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS)
    firebase_admin.initialize_app(cred)

db = firestore.client()

print("Firebase initialized successfully!")
