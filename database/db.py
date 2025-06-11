# database/db.py
import configparser
from pymongo import MongoClient



# ==================================
#  CONFIG 
# ==================================
config = configparser.ConfigParser()
config.read('config.ini')

# Leer configuración desde config.ini
db_config = config['DATABASE']

host = db_config['HOST']
port = int(db_config['PORT'])
username = db_config['USERNAME']
password = db_config['PASSWORD']
db_name = db_config['DATABASE_NAME']

COLLECTION_ANALYSIS = config['DATABASE']['COLLECTION_ANALYSIS']
COLLECTION_DATA = config['DATABASE']['COLLECTION_DATA']
COLLECTION_USERS = config['DATABASE']['COLLECTION_USERS']
COLLECTION_ROLES = config['DATABASE']['COLLECTION_ROLES']
COLLECTION_PERMISSIONS = config['DATABASE']['COLLECTION_PERMISSIONS']


# Construir URI de conexión (autenticación si se usa)
if username and password:
    uri = f"mongodb://{username}:{password}@{host}:{port}/"
else:
    uri = f"mongodb://{host}:{port}/"

# ==================================
#  CLIENTE MONGODB 
# ==================================
client = MongoClient(uri)
db = client[db_name]

# ==================================
#  COLECCIONES
# ==================================
# Referencias convenientes
DB_ANALYSIS    = db[COLLECTION_ANALYSIS]
DB_DATA        = db[COLLECTION_DATA]
DB_USERS       = db[COLLECTION_USERS]
DB_ROLES       = db[COLLECTION_ROLES]
DB_PERMISSIONS = db[COLLECTION_PERMISSIONS]


# Índices
DB_USERS.create_index('email', unique=True)
DB_ROLES.create_index('name', unique=True)
DB_PERMISSIONS.create_index('name', unique=True)


print(f"Conectado a la base de datos '{db_name}' en {host}:{port}")