from openai import OpenAI
from datetime import datetime
import os
import sys
from dotenv import load_dotenv
load_dotenv()

if getattr(sys, 'frozen', False):
    # Estamos en un .exe empaquetado con PyInstaller
    basedir = sys._MEIPASS
else:
    # Ejecutando en modo normal
    basedir = os.path.dirname(__file__)

env_path = os.path.join(basedir, '.env')
load_dotenv(dotenv_path=env_path)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def obtener_fecha_hora_actual():
    return datetime.now().strftime("%d/%m/%Y %H/%M/%S")

# Configurar API key de OpenAI con la nueva URL base
client = OpenAI(api_key=OPENAI_API_KEY,
                base_url="https://api.openai.com/v1/")


def solicitud_unitaria_gpt(instrucciones, user_text, model="gpt-4.1-nano"):

    messages = [
        {"role": "user", "content": instrucciones},
        {"role": "user", "content": user_text}
    ]
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=False
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error al comunicarse con OpenAI: {str(e)}"


def elegir_modulo(user_text):
    instrucciones_clasificacion = ("""
        Identifica la intención del usuario en el siguiente texto, 
        debes ser flexible al identificar diferentes formas de decir lo mismo: 
        Si el usuario desea redactar CV (o algo que fonéticamente se parezca ej: 
        'CB', 'CD' o 'SE VE') o redactar hoja de vida, responde con R001. 
        Si el usuario desea postular a trabajos también dicho por ejemplo como 
        'buscar chamba' o 'buscar trabajo', responde con R002. 
        Si el usuario desea revisar postulaciones pasadas también dicho 
        por ejemplo como 'ver a dónde ha postulado' o 'ver  postulaciones', responde con R003.
        Si el usuario desea cerrar sesión, responde con R004.
        Si no se puede identificar la intención del usuario, responde con R000. "
        Debes responder únicamente con el codigo de la intención, sin ningún otro texto adicional.
        """
    )
    return solicitud_unitaria_gpt(instrucciones_clasificacion, user_text)



def tiene_cuenta(user_text):
    instrucciones_clasificacion = (
        """
        Identifica si el usuario dice tener o no tener, debes 
        ser flexible al identificar diferentes formas de decir lo mismo: 
        Si el usuario indica que sí tiene, responde con R001. 
        Si el usuario indica que no tiene, responde con R002. 
        En cualquier otro caso, responde con R000. 
        Debes responder únicamente con el codigo de la intención, 
        sin ningún otro texto adicional.
        """
    )
    return solicitud_unitaria_gpt(instrucciones_clasificacion, user_text)

def ir_menu_principal(user_text):
    instrucciones_clasificacion = (
        "Identifica si el usuario desea volver al menu principal o salir: "
        "Si el usuario indica que desea volver al menu principal, responde con R001. "
        "Si el usuario indica que desea salir, responde con R002. "
        "En cualquier otro caso, responde con R000. "
        "Debes responder únicamente con el codigo de la intención, sin ningún otro texto adicional."
    )
    return solicitud_unitaria_gpt(instrucciones_clasificacion, user_text)

def intencion_nuevo_cv(user_text):
    instrucciones_clasificacion = (
        "Identifica si el usuario desea crear una nueva hoja de vida (CV, CD, CB, etc) o si quiere modificar la ya existente: "
        "Si el usuario indica que desea crear uno nuevo, responde con R001. "
        "Si el usuario indica que desea modificar el ya existente o partir de uno ya creado, responde con R002. "
        "Debes responder únicamente con el codigo de la intención, sin ningún otro texto adicional."
    )
    return solicitud_unitaria_gpt(instrucciones_clasificacion, user_text)

def mejorar_cv_formacion(contenido):
    instrucciones_mejora = (f"""
        Considera que la fecha y hora actual es: {obtener_fecha_hora_actual()}.
        Mejora la redacción de la siguiente transcripción de una entrevista, debes usarla para rellenar
        la sección de mi curriculum correspondiente a mi formación.
        En la entrevista las ideas estan desordenadas, debes organizarlas.
        solo dame la versión mejorada. Necesito que corrijas nombres en caso de estar mal 
        escritos o no presentar mayúsculas, mejorar redacción para hacerla más formal y específica
        y eliminar cualquier error gramatical. Debes ser específico y no dar explicaciones adicionales.
        Solo debes devolver la lista de elementos, sin ningún otro texto adicional como una presentación o subtítulo.
        Debes incluir el nombre de la institución y el año de inicio y fin.
        Utiliza listas con bullets y no párrafos. Utiliza únicamente la información 
        que te doy a continuación y no añadas nada más, no inventes información como el lugar donde se formó.
        En caso de que el usuario mencione siglas, déjalo como siglas, 
        no asumas el nombre completo.
        Considera que está pensado para usarse en Perú
        No debería tener ningún otro texto adicional, ni siquiera un título o subtítulo.
        Este es un ejemplo de cómo debería quedar la redacción de cada línea: 
        "•  Ingeniería de Sistemas, Universidad Peruana de Ciencias Aplicadas (UPC), 2019 - 2021" 
        tipo de estudios, lugar, siglas (de haber), periodo.
        Los bullets deben ser aptos para microsoft word, por lo que deben ser bullets no guiones.
        """
    )
    return solicitud_unitaria_gpt(instrucciones_mejora, contenido)

def mejorar_cv_habilidades(contenido):
    instrucciones_mejora = (f"""
        Considera que la fecha y hora actual es: {obtener_fecha_hora_actual()}.
        Mejora la redacción de la siguiente transcripción de una entrevista, debes usarla para rellenar
        la sección de mi curriculum correspondiente a mis habilidades técnicas, 
        solo dame la versión mejorada. 
        En la entrevista las ideas estan desordenadas, debes organizarlas.
        Necesito que corrijas nombres en caso de estar mal 
        escritos o no presentar mayúsculas, mejorar redacción para hacerla más formal y específica
        y eliminar cualquier error gramatical. Debes ser específico y no dar explicaciones adicionales.
        Solo debes devolver la lista de elementos, sin ningún otro texto adicional como una presentación o subtítulo.
        Debes incluir el nombre de la habilidad y el nivel de 
        dominio (básico, intermedio o avanzado).
        El nivel de dominio debe estar entre paréntesis.
        Si no se indica el nivel, por defecto asume que es nivel intermedio.
        Utiliza listas con bullets y no párrafos. Utiliza únicamente la información 
        que te doy a continuación y no añadas nada más.
        Considera que está pensado para usarse en Perú
        Este es un ejemplo de cómo debería quedar la redacción de cada línea: "•  Manejo de Python (Intermedio)", habilidad y nivel.
        Los bullets deben ser aptos para microsoft word, por lo que deben ser bullets no guiones.
        """
    )
    return solicitud_unitaria_gpt(instrucciones_mejora, contenido)

def mejorar_cv_experiencia(contenido):
    instrucciones_mejora = (f"""
        Considera que la fecha y hora actual es: {obtener_fecha_hora_actual()}.
        Mejora la redacción de la siguiente transcripción de una entrevista, debes usarla para rellenar
        la sección de mi curriculum correspondiente a mis experiencia laboral.
        En la entrevista las ideas estan desordenadas, debes organizarlas.
        Necesito que corrijas nombres en caso de estar mal 
        escritos o no presentar mayúsculas, mejorar redacción para hacerla más formal y específica
        y eliminar cualquier error gramatical. Debes ser específico y no dar explicaciones adicionales.
        Solo debes devolver la lista de elementos, sin ningún otro texto adicional como una presentación o subtítulo.
        
        Debes incluir únicamente el nombre de la empresa (de haber 
        mencionado siglas, estas deben ir entre paréntesis, dar prioridad al nombre completo), el cargo 
        (en caso de mencionarse, si no, omitir este dato), y el año de inicio y fin, utiliza la fecha 
        actual como referencia.
        
        Utiliza listas con bullets y no párrafos. Utiliza únicamente la información 
        que te doy a continuación y no añadas nada más. En caso de que el usuario mencione siglas, déjalo como siglas, 
        no asumas el nombre completo.
        Considera que está pensado para usarse en Perú
        Este es un ejemplo de cómo debería quedar la redacción de cada línea: 
        "•  Diario El Comercio, Periodista, 2024 - 2025" empresa, cargo, periodo.
        Los bullets deben ser aptos para microsoft word, por lo que deben ser bullets no guiones.
        """
    )
    return solicitud_unitaria_gpt(instrucciones_mejora, contenido)

def conformidad_seccion(user_text):
    instrucciones_clasificacion = (
       "El usuario deberá dar su conformidad o inconformidad con una sección, si confirma o está conforme o le parece bien o correcto o conforme, responde R001."
       "si niega o pide repetir o hacerlo otra vez o corregir, responde R002. Solo debes responder con el código de la intención, sin ningún otro texto adicional."
    )
    return solicitud_unitaria_gpt(instrucciones_clasificacion, user_text)


def confirmacion(user_text):
    instrucciones_clasificacion = (
        """
       El usuario deberá dar su conformidad o inconformidad, si confirma o está conforme o le parece bien o correcto o conforme o dice "así" o "si", responde R001.
       si niega o pide repetir o hacerlo otra vez, responde R002. Solo debes responder con el código de la intención, sin ningún otro texto adicional.
       """
    )
    return solicitud_unitaria_gpt(instrucciones_clasificacion, user_text)

def corregir_departamento(user_text):
    instrucciones_mejora = (
       "El usuario te dará el nombre de un departamento de Perú, corrige el nombre del departamento, "
       "debes responder únicamente con el nombre corregido, sin ningún otro texto adicional. "
    )
    return solicitud_unitaria_gpt(instrucciones_mejora, user_text)

def precisar_puesto(user_text):
    instrucciones_mejora = (
       "Recibirás una transcripción de un puesto de trabajo, corrige el nombre del puesto, "
       "debes responder únicamente con el nombre corregido, sin ningún otro texto adicional. "
    )
    return solicitud_unitaria_gpt(instrucciones_mejora, user_text)


def resumir_ofertas(user_text):
    instrucciones_resumen = (
       """
       La siguiente información es una lista de ofertas laborales que le interesan al usuario, tu misión es resumir cada oferta laboral,
       debes devolver únicamente el resumen de cada oferta, sin ningún otro texto adicional. Longitud máxima de 150 palabras por oferta.
       Prioriza mencionar el título, la empresa, la descripción y los requisitos de la oferta; en cuanto a las aptitudes puedes omitirlas 
       si no mencionan una habilidad técnica o manejo de algún software. Después de nombrar cada oferta debes finalizar con tres puntos suspensivos (...)
       tras lo cual debes iniciar la siguiente oferta.
       La estructura del resumen de cada oferta debe ser la siguiente:
       - "La oferta número _ es:" e iniciar con el titulo de la oferta, 
       - luego "Esta oferta fue publicada por la empresa: _empresa_"), 
       - después dar un resumen de la descripción (dicho como "en la descripción se menciona"), 
       - después menciona los requisitos y aptitudes (dicho como "lo que se requiere a los postulantes es que"), 
       - finalmente menciona los beneficios en caso de que se especifiquen. 
       Deberás iniciar tu redacción con "Se encontraron _cantidad_ ofertas, esta es la lista de ofertas encontradas para ti: ". 
       Considera que si el titulo del puesto es similar a "diseñador/a" o "diseñador(a)" 
       o cualquier otra profesion que pueda tener una barra inclinada o paréntesis para indicar género,
       deberás decirlo como su versión neutra o masculina. Después de haber mencionado todas las ofertas, pregunta al usuario 
       si desea postular a alguna de las ofertas, o si prefiere que las repitas.
       En caso de reconocer una palabra en inglés, deberás escribirla de forma fonética en español, de forma que el usuario pueda entenderla,
       por ejemplo, si la palabra es "software", deberás escribirla como "sofwar".
       """
    )
    return solicitud_unitaria_gpt(instrucciones_resumen, user_text)



def resumir_oferta(user_text):
    instrucciones_resumen = (
       """
       La siguiente información pertenece a una oferta laboral que le interesa al usuario, tu misión es resumirla,
       debes devolver únicamente el resumen, sin ningún otro texto adicional. Longitud máxima de 70 palabras.
       Prioriza mencionar el título, la empresa, la descripción y los requisitos de la oferta; en cuanto a las aptitudes puedes omitirlas 
       si no mencionan una habilidad técnica o manejo de algún software.
       La estructura del resumen de cada oferta debe ser la siguiente:
       - "La siguiente oferta es:" e iniciar con el titulo de la oferta, 
       - luego "Esta oferta fue publicada por la empresa: _empresa_"), 
       - después dar un resumen de la descripción (dicho como "en la descripción se menciona"), 
       - después menciona los requisitos y aptitudes (dicho como "lo que se requiere a los postulantes es que"), 
       - finalmente menciona los beneficios en caso de que se especifiquen. 
       Considera que si el titulo del puesto es similar a "diseñador/a" o "diseñador(a)" 
       o cualquier otra profesion que pueda tener una barra inclinada o paréntesis para indicar género,
       deberás decirlo como su versión neutra o masculina, con el ejemplo anterior, quedaría solo colo "diseñador". 
       En caso de reconocer una palabra en inglés, deberás escribirla de forma fonética en español, de forma que el usuario pueda entenderla,
       por ejemplo, si la palabra es "software", deberás escribirla como "sofwar".
       Al final deberás preguntar al usuario: "¿Te agrada esta oferta? Di 'sí' para seleccionarla o 'no' para pasar a la siguiente."
       """
    )
    return solicitud_unitaria_gpt(instrucciones_resumen, user_text)


def resumir_oferta_review(user_text):
    instrucciones_resumen = (
       """
       La siguiente información pertenece a una oferta laboral que le interesa al usuario, tu misión es resumirla,
       debes devolver únicamente el resumen, sin ningún otro texto adicional. Longitud máxima de 20 palabras.
       Prioriza mencionar el título, la empresa (di su nombre completo) y la descripción
       """
    )
    return solicitud_unitaria_gpt(instrucciones_resumen, user_text)



def intencion_retroceder(user_text):
    instrucciones_analisis = (
        """
       Recibirás un texto del usuario, identifica si el usuario desea retroceder en el flujo de conversación o no. 
       Si el usuario afirma o dice "sí" o indica que desea retroceder o volver al paso anterior o cualquier otra forma, responde con R001.
       La otra posible intención es que el usuario quiera volver al menú principal o inicio, en cuyo caso debes responder con R002.
       En cualquier otro caso, devuelve el texto original del usuario sin modificaciones. 
       """
    )
    return solicitud_unitaria_gpt(instrucciones_analisis, user_text)

def identificar_profesion(user_text):
    instrucciones_analisis = (
        """
       Recibirás la transcripción de usuario mencionando una profesión o puesto de trabajo, 
       deberás identificar la profesión o puesto de trabajo mencionado. en caso de que lo haya mencionado no como un sustantivo, deberás corregirlo, 
       por ejemplo, si el usuario dice "diseño" deberás corregirlo a "diseñador", si dice "ingenieria" deberás corregirlo a "ingeniero". 
       El caso es que siempre deberá mencionarse como el rol y no como la carrera.
       Solo debes devolver el nombre de la profesión o puesto de trabajo corregido,
       sin ningún otro texto adicional.
       """
    )
    return solicitud_unitaria_gpt(instrucciones_analisis, user_text)


def elegir_oferta(user_text):
    instrucciones_clasificacion = ("""
       El usuario deberá dar su conformidad o inconformidad sobre su interés 
       en la oferta laboral que se le ha presentado, por ejemplo podría decir "sí, esa", "claro", "esa me agrada", "está bien", "quiero esa", "esa",
       "postulemos a esa", vamos a esa", "me gusta esa oferta", "esa me parece bien", "esa me interesa", "esa es la que quiero postular",
       "esa es la que quiero postular", "esa es la oferta que quiero postular", "esa es la oferta que me interesa",
       entre otros similares; en cualquiera de esos casos, responde R001.
       si niega responde R002. Solo debes responder con el código de la intención, sin ningún otro texto adicional.
       """
    )
    return solicitud_unitaria_gpt(instrucciones_clasificacion, user_text)


def identificar_modalidad(user_text):
    instrucciones_clasificacion = ("""
       El usuario deberá indicar la modalidad de trabajo que prefiere, las tres modalidades son:
         "Virtual" y "Presencial/Hibrido", solo esas dos. Si el usuario menciona 
         "Virtual", "Remoto", "Teletrabajo" o cualquier otra forma de referirse a trabajar desde casa, 
         responde con R001.
         Si el usuario menciona "Presencial", "Híbrido", "Presencial con teletrabajo", "una que me permita ambas"
         o cualquier otra forma de referirse a trabajar en una oficina o lugar físico, responde con R002.
         Si no lo identificas, responde con R001.
         Solo debes responder con el código de la intención, sin ningún otro texto adicional.
         """
    )
    return solicitud_unitaria_gpt(instrucciones_clasificacion, user_text)