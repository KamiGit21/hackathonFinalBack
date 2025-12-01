import os
import firebase_admin
from firebase_admin import credentials, firestore

from app.core.config import settings

if not firebase_admin._apps:
    cred_path = os.getenv("FIREBASE_CREDENTIALS", settings.FIREBASE_CREDENTIALS)
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()
