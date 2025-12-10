# Sistema de Postulación Laboral por Voz

Este proyecto es una aplicación de escritorio diseñada para facilitar la búsqueda y postulación a empleos a través de una interfaz controlada completamente por voz. Su objetivo es ofrecer una experiencia de usuario accesible, especialmente para personas con discapacidad visual o motriz, permitiendo navegar por todo el proceso de postulación sin necesidad de interacciones manuales complejas.

## 📜 Descripción General

El sistema guía al usuario a través de un flujo conversacional que abarca desde la creación de una cuenta y la elaboración de un currículum (CV), hasta la búsqueda de ofertas de empleo, la selección de una vacante y el inicio del proceso de postulación. La aplicación integra múltiples tecnologías de vanguardia para ofrecer una experiencia fluida y natural:

  * **Reconocimiento de Voz**: Para recibir y transcribir las órdenes del usuario.
  * **Procesamiento de Lenguaje Natural (PLN)**: Para comprender la intención detrás de los comandos de voz.
  * **Síntesis de Voz (Texto a Voz)**: Para proporcionar retroalimentación y guía auditiva constante.
  * **Web Scraping**: Para obtener ofertas de empleo actualizadas de portales de trabajo.

Además, la aplicación cuenta con una funcionalidad de "talkback" que verbaliza las teclas presionadas, mejorando la accesibilidad durante la introducción de datos.

## ✨ Funcionalidades Principales

  * **Navegación por Voz**: Toda la interfaz se controla mediante comandos de voz. El sistema está diseñado para ser flexible y reconocer distintas formas de expresar una misma intención.
  * **Gestión de Cuentas de Usuario**:
      * Registro de nuevos usuarios solicitando datos como nombre, correo electrónico y contraseña a través de la voz.
      * Inicio de sesión para usuarios existentes.
      * Comunicación con un backend para la persistencia de los datos.
  * **Creación y Gestión de Currículum (CV)**:
      * El usuario puede dictar la información de su CV por secciones: formación académica, habilidades técnicas y experiencia laboral.
      * El sistema utiliza IA para mejorar la redacción, corregir errores gramaticales y dar un formato profesional al contenido dictado.
      * Permite modificar un CV ya existente, revisando cada sección de forma interactiva.
      * Genera un archivo `.docx` descargable con el CV en un formato limpio y profesional.
  * **Búsqueda de Empleo Personalizada**:
      * El usuario puede especificar el puesto de trabajo, la modalidad (virtual, presencial o híbrida) y la región de su interés.
      * La aplicación realiza web scraping en tiempo real sobre el portal *Computrabajo* para encontrar ofertas que coincidan con los criterios.
  * **Proceso de Postulación Asistido**:
      * Las ofertas encontradas son resumidas y leídas en voz alta al usuario.
      * El usuario puede elegir la oferta de su interés para iniciar la postulación.
      * El sistema genera un enlace directo a la página de postulación de la oferta seleccionada.
  * **Seguimiento de Postulaciones**:
      * Permite al usuario consultar un historial de las ofertas a las que ha postulado.
  * **Accesibilidad Mejorada**:
      * La función de `talkback` ofrece retroalimentación auditiva inmediata al presionar cualquier tecla, facilitando la interacción para usuarios con discapacidad visual.

## 🛠️ Arquitectura y Tecnologías

El sistema está compuesto por varios módulos que trabajan en conjunto para ofrecer una experiencia integral:

1.  **`main.py` (Orquestador)**:

      * Es el punto de entrada de la aplicación.
      * Lanza el proceso de la interfaz de usuario (`prototipo.py`) y el script de `talkback.py` de forma concurrente.
      * Abre automáticamente la aplicación en el navegador web del usuario.

2.  **`prototipo.py` (Interfaz de Usuario y Lógica Principal)**:

      * Construido con **Streamlit**, este módulo gestiona toda la interfaz gráfica y el flujo de la aplicación.
      * Utiliza la biblioteca **`sounddevice`** para grabar el audio del micrófono del usuario.
      * Se integra con **Google Cloud Speech-to-Text** para transcribir los comandos de voz.
      * Usa **`gTTS` (Google Text-to-Speech)** para generar las respuestas de audio.
      * Realiza web scraping con **`requests`** y **`BeautifulSoup`**.
      * Se comunica con una **API REST** (desplegada en AWS) para la gestión de datos de usuarios, CVs y postulaciones.

3.  **`agentes_intencion.py` (Cerebro de IA)**:

      * Utiliza la API de **OpenAI (GPT)** para procesar el texto transcrito.
      * Identifica la **intención** del usuario (ej. "crear CV", "buscar trabajo") y la traduce a códigos que la aplicación puede entender.
      * **Mejora y formatea** el contenido dictado por el usuario para el CV, asegurando una redacción profesional.
      * **Resume** las descripciones de las ofertas de empleo para una presentación auditiva clara y concisa.

4.  **`talkback.py` (Soporte de Accesibilidad)**:

      * Se ejecuta en segundo plano para no interferir con la aplicación principal.
      * Usa **`pynput`** para escuchar los eventos del teclado y **`pyttsx3`** para verbalizar las teclas presionadas en tiempo real.

## 🚀 Instalación y Uso

Para ejecutar este proyecto de forma local, sigue estos pasos:

1.  **Clonar el repositorio**:

    ```bash
    git clone https://github.com/daniel7apata/sistema-postulacion-laboral.git
    cd sistema-postulacion-laboral
    ```

2.  **Crear un entorno virtual (recomendado)**:

    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3.  **Instalar las dependencias**:
    Asegúrate de tener un archivo `requirements.txt` con todas las bibliotecas necesarias y ejecútalo.

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar las variables de entorno**:

      * Crea un archivo `.env` en la raíz del proyecto.
      * Añade las claves de API necesarias, como se muestra en el archivo `.env.example` (si existe). Deberás incluir:
        ```
        OPENAI_API_KEY="tu_clave_de_openai"
        GOOGLE_APPLICATION_CREDENTIALS="ruta/a/tu/archivo_de_credenciales.json"
        ```

5.  **Ejecutar la aplicación**:

    ```bash
    python main.py
    ```

    La aplicación se iniciará y se abrirá una pestaña en tu navegador web. Para comenzar, solo tienes que hacer clic en el botón de la pantalla principal y empezar a hablar.

-----
