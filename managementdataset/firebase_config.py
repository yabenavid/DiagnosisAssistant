import firebase_admin
from firebase_admin import credentials, storage

# Ruta al archivo de credenciales descargado desde Firebase
cred = credentials.Certificate("secrets/proyecto-1-5fd7e-24d703a1a39b.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'proyecto-1-5fd7e.appspot.com'  # Reemplaza con tu bucket de Storage
})

# Inicializar Storage
bucket = storage.bucket()
