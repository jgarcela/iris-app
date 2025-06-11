# api/routes/data.py

# ==================================
#  LIBRARIES 
# ==================================
from flask import Blueprint, abort, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
from bson import ObjectId

from database.db import db
from api.utils.logger import logger

import api

# ==================================
#  BLUEPRINT 
# ==================================
bp = Blueprint('data', __name__, url_prefix='/data')


# ==================================
#  ENDPOINTS 
# ==================================
@bp.route('/get_document/<doc_id>', methods=['GET'])
def get_document(doc_id):
    # 1) validar ObjectId
    try:
        oid = ObjectId(doc_id)
    except Exception:
        return jsonify({'error': 'ID inválido'}), 400

    # 2) recuperar de Mongo
    doc = db.iris_analysis.find_one({'_id': oid})
    if not doc:
        return jsonify({'error': 'Documento no encontrado'}), 404

    # 3) serializar _id para JSON
    doc['_id'] = str(doc['_id'])
    return jsonify(doc), 200


@bp.route("/get_contexto", methods=["GET"])
def get_contexto():
    try:
        # 1. Seleccionamos la colección específica
        collection = db[api.COLLECTION_DATA]

        # 2. Devuelve una lista de strings con los valores únicos.
        contextos_unicos = collection.distinct(api.CONTEXTO_DATA)

    except Exception as e:
        # En caso de error, devolvemos un 500 con el mensaje
        return jsonify({"error": str(e)}), 500

    # 3. Devolvemos la lista de contextos únicos en formato JSON
    return jsonify({"contextos": contextos_unicos})


# Dado que Flask jsonify no sabe serializar ObjectId, definimos
# un pequeño helper que itera un documento y reemplaza el campo "_id".
def serialize_doc(doc: dict) -> dict:
    """
    Recibe un documento recibido de MongoDB (con ObjectId en '_id')
    y devuelve un dict con '_id' convertido a str, y el resto de campos tal cual.
    """
    salida = {}
    for clave, valor in doc.items():
        if isinstance(valor, ObjectId):
            salida[clave] = str(valor)
        else:
            salida[clave] = valor
    return salida

@bp.route("/<collection_name>", methods=["GET"]) # Aquí añadimos el parámetro <collection_name>
def get_data_from_collection(collection_name): # El nombre de la colección se pasa como argumento
    """
    Este endpoint devuelve una lista con todos los documentos de la colección especificada por 'collection_name'.
    Cada documento se serializa convirtiendo el ObjectId a string.
    """
    try:
        # 3.1. Obtenemos la colección dinámicamente
        # Usamos db[collection_name] para seleccionar la colección
        cursor = db[collection_name].find({})
    except Exception as e:
        # Si ocurre un error en la consulta a Mongo, devolvemos un 500
        abort(500, description=f"Error al consultar la base de datos o colección '{collection_name}': {e}")

    # 3.2. Convertimos el cursor a lista, serializando cada doc
    lista_documentos = []
    for doc in cursor:
        lista_documentos.append(serialize_doc(doc))

    # 3.3. Devolvemos el JSON con la lista completa
    return jsonify(lista_documentos), 200