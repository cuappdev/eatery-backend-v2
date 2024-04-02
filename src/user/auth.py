# Import the Firebase service
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
import os

cred = credentials.Certificate(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))
default_app = firebase_admin.initialize_app(cred)


# Initialize the default app
# default_app = firebase_admin.initialize_app()
print(default_app.name)  # "[DEFAULT]"

uid = "DTkATsJbRJd5VO3E82V7M8HbTS83"
user = auth.get_user(uid)
print(user.email)
