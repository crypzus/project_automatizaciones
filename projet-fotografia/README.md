# Automatización para Flujo de Fotografía Inmobiliaria

Este proyecto es un servicio de automatización en Python que conecta los webhooks de Spiro con Dropbox para notificar a un equipo de editores cuando los archivos de una sesión de fotos están listos.

---

## Requisitos Previos

- Python 3.8 o superior.

---

## Instalación

1.  **Clonar el repositorio o descargar los archivos.**

2.  **Crear y activar un entorno virtual:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # En Mac/Linux
    # o
    venv\Scripts\activate    # En Windows
    ```

3.  **Instalar las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

---

## Configuración

1.  Crea una copia del archivo `.env.example` y renómbrala a `.env`.
    ```bash
    cp .env.example .env
    ```
2.  Abre el archivo `.env` y rellena las siguientes variables con tus credenciales:
    - `DROPBOX_ACCESS_TOKEN`: Tu token de acceso de la API de Dropbox.
    - `EMAIL_ADDRESS`: La dirección de correo (Gmail) que enviará las notificaciones.
    - `EMAIL_PASSWORD`: La contraseña de aplicación de 16 dígitos generada en tu cuenta de Google.

---

## Cómo Ejecutarlo

Para iniciar el servidor en un entorno de desarrollo local, ejecuta el siguiente comando:

```bash
uvicorn main:app --reload
```
