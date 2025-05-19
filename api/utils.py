import ast
import configparser
import json
import openai
from pydantic import BaseModel, Field
from typing import Literal

# ----------------- CONFIG -----------------
config = configparser.ConfigParser()
config.read('config.ini')

MODELS = config['API']['MODELS']
MODELS = eval(MODELS)
OPENAI_MODEL = config['API']['OPENAI_MODEL']
openai.api_key = config['API']['OPENAI_API_KEY']

genero_nombre_propio_titular = ast.literal_eval(config['VARIABLES']['genero_nombre_propio_titular'])
genero_personas_mencionadas = ast.literal_eval(config['VARIABLES']['genero_personas_mencionadas'])
genero_periodista = ast.literal_eval(config['VARIABLES']['genero_periodista'])
tema = ast.literal_eval(config['VARIABLES']['tema'])

# Extraemos las claves y las convertimos a int
genero_nombre_propio_titular_values = tuple(int(k) for k in genero_nombre_propio_titular.keys())
genero_personas_mencionadas_values = tuple(int(k) for k in genero_personas_mencionadas.keys())
genero_periodista_values = tuple(int(k) for k in genero_periodista.keys())
tema_values = tuple(int(k) for k in tema.keys())

class AnalysisResponse(BaseModel):
    nombre_propio_titular: list[str]
    genero_nombre_propio_titular: list[Literal[ *genero_nombre_propio_titular_values ]]
    cita_textual_titular: list[str]
    personas_mencionadas: list[str]
    genero_personas_mencionadas: list[Literal[ *genero_personas_mencionadas_values ]]
    tema: Literal[ *tema_values ]
    genero_periodista: Literal[ *genero_periodista_values ]


# CONTENIDO GENERAL
def analyze_contenido_general(model:str, text:str):

    if MODELS[model] == OPENAI_MODEL:
        try:
            # Llamada al modelo
            completion = openai.beta.chat.completions.parse(
                model=MODELS[model],
                messages=[
                    {
                        "role": "system", 
                        "content": f"""
                                        Eres un analizador de noticias deportivas. Tu tarea es extraer de cada noticia los siguientes campos y devolver **únicamente** un JSON que cumpla con este esquema de Pydantic (ResponseFormat):

                                        Requerimientos por campo:
                                        1. nombre_propio_titular: lista de nombres propios en el titular (personas).
                                        2. genero_nombre_propio_titular: lista del género de los nombres de las personas que aparecen en el titular. Tiene que tener corresponencia con la lista anterior de "nombre_propio_titular". Usa {genero_nombre_propio_titular} para las etiquetas.
                                        3. cita_textual_titular: lista de citas literales que aparezcan en el titular (entre comillas).
                                        4. personas_mencionadas: lista de nombres de personas que aparecen en el cuerpo del texto.
                                        5. genero_personas_mencionadas: lista del género de los nombres de las personas que aparecen en el cuerpo del texto. Tiene que tener corresponencia con la lista anterior de "personas_mencionadas". Usa {genero_personas_mencionadas} para las etiquetas.
                                        6. tema: identifica el deporte principal de la noticia con el número correspondiente: {tema}.
                                        7. genero_periodista: a partir del nombre del periodista, asigna: {genero_periodista}.

                                        **IMPORTANTE**:
                                        - Devuelve **solo** el JSON (sin explicaciones, sin ningún texto adicional).
                                        - Asegúrate de respetar tipos: listas, enteros, cadenas.
                                    """ 
                    },
                    {
                        "role": "user", 
                        "content": f"""
                                    Articulo: {text}
                                    """
                                                    }
                ],
                response_format=AnalysisResponse
            )
            
            # Extraer la respuesta
            response_message = completion.choices[0].message.content
            print(f"{response_message=}")

            # Usamos json.loads para convertir el string JSON a un objeto Python
            response_data = json.loads(response_message)

            return response_data

        except Exception as e:
            print(f"Error: {e}")
        
    else:
        # Si el modelo no es OpenAI, se puede implementar otro tipo de análisis
        # Aquí puedes agregar tu lógica para otros modelos
        raise NotImplementedError(f"Modelo {model} no soportado.")
    


def analyze_text(model: str, text: str) -> dict:
    response_contenido_general = analyze_contenido_general(model, text)
    return {
        'response_contenido_general': response_contenido_general
    }