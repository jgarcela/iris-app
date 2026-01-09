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
COLLECTION_DATA_ETIQUETAS = config['DATABASE'].get('COLLECTION_DATA_ETIQUETAS', 'iris_data_etiquetas')
COLLECTION_USERS = config['DATABASE']['COLLECTION_USERS']
COLLECTION_ROLES = config['DATABASE']['COLLECTION_ROLES']
COLLECTION_PERMISSIONS = config['DATABASE']['COLLECTION_PERMISSIONS']
COLLECTION_SEMANA_CIENCIA = config['DATABASE'].get('COLLECTION_SEMANA_CIENCIA', 'iris_semana_ciencia_2025')
COLLECTION_ANALYSIS_SEMANA_CIENCIA = config['DATABASE'].get('COLLECTION_ANALYSIS_SEMANA_CIENCIA', 'iris_analysis_semana_ciencia_2025')
COLLECTION_CONTACT = config['DATABASE'].get('COLLECTION_CONTACT', 'iris_contact')


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
DB_DATA_ETIQUETAS = db[COLLECTION_DATA_ETIQUETAS]
DB_USERS       = db[COLLECTION_USERS]
DB_ROLES       = db[COLLECTION_ROLES]
DB_PERMISSIONS = db[COLLECTION_PERMISSIONS]
DB_SEMANA_CIENCIA = db[COLLECTION_SEMANA_CIENCIA]
DB_ANALYSIS_SEMANA_CIENCIA = db[COLLECTION_ANALYSIS_SEMANA_CIENCIA]
DB_CONTACT = db[COLLECTION_CONTACT]

# Índices
DB_USERS.create_index('email', unique=True)
DB_ROLES.create_index('name', unique=True)
DB_PERMISSIONS.create_index('name', unique=True)
# Índices básicos para la colección del desafío si procede
try:
    DB_SEMANA_CIENCIA.create_index('created_at')
except Exception:
    pass

# Índice para mensajes de contacto
try:
    DB_CONTACT.create_index('created_at')
except Exception:
    pass


print(f"Conectado a la base de datos '{db_name}' en {host}:{port}")