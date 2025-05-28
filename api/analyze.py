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
MODELS = ast.literal_eval(MODELS)
OPENAI_MODEL = config['API']['OPENAI_MODEL']
openai.api_key = config['API']['OPENAI_API_KEY']

# ----------------- CONTENIDO GENERAL -----------------
genero_nombre_propio_titular = ast.literal_eval(config['VARIABLES']['GENERO_NOMBRE_PROPIO_TITULAR'])
genero_personas_mencionadas = ast.literal_eval(config['VARIABLES']['GENERO_PERSONAS_MENCIONADAS'])
genero_periodista = ast.literal_eval(config['VARIABLES']['GENERO_PERIODISTA'])
tema = ast.literal_eval(config['VARIABLES']['TEMA'])

# Extraemos las claves y las convertimos a int
genero_nombre_propio_titular_values = tuple(int(k) for k in genero_nombre_propio_titular.keys())
genero_personas_mencionadas_values = tuple(int(k) for k in genero_personas_mencionadas.keys())
genero_periodista_values = tuple(int(k) for k in genero_periodista.keys())
tema_values = tuple(int(k) for k in tema.keys())

class ContenidoGeneralResponse(BaseModel):
    nombre_propio_titular: list[str]
    genero_nombre_propio_titular: list[Literal[ *genero_nombre_propio_titular_values ]]
    cita_textual_titular: list[str]
    personas_mencionadas: list[str]
    genero_personas_mencionadas: list[Literal[ *genero_personas_mencionadas_values ]]
    tema: Literal[ *tema_values ]
    genero_periodista: Literal[ *genero_periodista_values ]

class ContenidoGeneralResponse_NoTitular(BaseModel):
    personas_mencionadas: list[str]
    genero_personas_mencionadas: list[Literal[ *genero_personas_mencionadas_values ]]
    tema: Literal[ *tema_values ]
    genero_periodista: Literal[ *genero_periodista_values ]


# ----------------- LENGUAJE -----------------
lenguaje_sexista = ast.literal_eval(config['VARIABLES']['LENGUAJE_SEXISTA'])
lenguaje_vars = ast.literal_eval(config['VARIABLES']['LENGUAJE_VARS'])

# Extraemos las claves y las convertimos a int
lenguaje_sexista_values = tuple(int(k) for k in lenguaje_sexista.keys())
lenguaje_vars_values = tuple(int(k) for k in lenguaje_vars.keys())


class LenguajeSexista(BaseModel):
    etiqueta: list[Literal[ *lenguaje_sexista_values ]]
    ejemplos_articulo: list[str]

class LenguajeVars(BaseModel):
    etiqueta: list[Literal[ *lenguaje_vars_values ]]
    ejemplos_articulo: list[str]


class LenguajeResponse(BaseModel):
    lenguaje_sexista: LenguajeSexista
    masculino_generico: LenguajeVars
    hombre_humanidad: LenguajeVars
    dual_aparente: LenguajeVars
    cargos_mujeres: LenguajeVars
    sexismo_social: LenguajeVars
    androcentrismo: LenguajeVars
    asimetria: LenguajeVars
    infantilizacion: LenguajeVars
    denominacion_sexualizada: LenguajeVars
    denominacion_redundante: LenguajeVars
    denominacion_dependiente: LenguajeVars
    excepcion_noticiabilidad: LenguajeVars
    comparacion_mujeres_hombres: LenguajeVars


# ----------------- FUENTES -----------------
tipo_fuente = ast.literal_eval(config['VARIABLES']['TIPO_FUENTE'])
# Extraemos las claves y las convertimos a int
tipo_fuente_values = tuple(int(k) for k in tipo_fuente.keys())

class Declaracion(BaseModel):
    nombre_fuente: str
    genero_fuente: Literal[ *genero_periodista_values ]
    tipo_fuente: Literal[ *tipo_fuente_values ]
    declaracion_fuente: str

class FuentesResponse(BaseModel):
    fuentes: list[Declaracion]

# ----------------- FUNCIONES -----------------
def analyze_text(model:str, text:str, title:str, task:str):

    print(f"[/ANALYSIS/ANALYZE] {task} Analysis...")

    # Response format
    if task == "contenido_general":
        if title == "":
            response_format = ContenidoGeneralResponse_NoTitular
            task = "contenido_general_notitular"
        else:
            response_format = ContenidoGeneralResponse
    if task == "lenguaje":
        response_format = LenguajeResponse
    if task == "fuentes":
        response_format = FuentesResponse
    
    # Prompt
    with open(f'api/prompts/{task}.txt', 'r', encoding='utf-8') as f:
        prompt = f.read()

    user_prompt = f"""
                    Titulo: {title}
                    Articulo: {text}
                    """

    # Predicción
    if MODELS[model] == OPENAI_MODEL:
        try:
            # Llamada al modelo
            completion = openai.beta.chat.completions.parse(
                model=MODELS[model],
                messages=[
                    {
                        "role": "system", 
                        "content": prompt
                    },
                    {
                        "role": "user", 
                        "content": user_prompt
                    }
                ],
                response_format=response_format
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