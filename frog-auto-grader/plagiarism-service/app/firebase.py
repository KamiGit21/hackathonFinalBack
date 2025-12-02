import firebase_admin
from firebase_admin import credentials, firestore

# Cargar credenciales del servicio
cred = credentials.Certificate("serviceAccountKey.json")

# Inicializar solo si no está ya inicializado
default_app = firebase_admin.initialize_app(cred)

db = firestore.client()

def save_report(data: dict):
    """Guarda el reporte de plagio en Firestore."""
    collection = db.collection("plagiarism_reports")
    collection.add(data)
