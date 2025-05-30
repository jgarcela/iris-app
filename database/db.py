# database/db.py
import configparser
from pymongo import MongoClient



# ----------------- CONFIG -----------------
config = configparser.ConfigParser()
config.read('config.ini')

# Leer configuración desde config.ini
db_config = config['DATABASE']

host = db_config['HOST']
port = int(db_config['PORT'])
username = db_config['USERNAME']
password = db_config['PASSWORD']
db_name = db_config['DATABASE_NAME']

# Construir URI de conexión (autenticación si se usa)
if username and password:
    uri = f"mongodb://{username}:{password}@{host}:{port}/"
else:
    uri = f"mongodb://{host}:{port}/"

# ----------------- MONGODB -----------------
client = MongoClient(uri)
db = client[db_name]

print(f"Conectado a la base de datos '{db_name}' en {host}:{port}")