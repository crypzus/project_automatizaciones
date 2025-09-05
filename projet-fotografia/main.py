import time
from datetime import datetime, timedelta
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel # 1. Importamos la herramienta para crear plantillas
from typing import Optional   # 2. Importamos una ayuda para campos opcionales
from dropbox_manager import get_link_compartidos, dbx

# 3. Creamos nuestra plantilla para los datos del webhook
class WebhookData(BaseModel):
    event_type: str
    job_id: str
    style: Optional[str] = None # Este campo puede que no siempre venga
    client_name: Optional[str] = None
    property_address: Optional[str] = None



# 1. Creamos la aplicación
app = FastAPI()

# El diccionario para guardar temporalmente la información de los trabajos
trabajos_pendientes = {}

def monitor_folder_uploads(job_id:str, folder_path:str):
    """
    Esta función se ejecuta en segundo plano para monitorear una carpeta de Dropbox.
    """
    print(f"[{job_id}] - Iniciando monitoreo de la carpeta: {folder_path}")
    # Pausa inicial de 10 minutos para dar tiempo a que comience la subida
    time.sleep(20)
    last_activity_time = datetime.now()
    previous_file_count = -1
    
    while True:
        try:
            ## Obtenemos la lista de archivos en la carpeta
            files = dbx.files_list_folder(folder_path, recursive=True).entries # type: ignore
            current_file_count = len(files)
            
            print(f"[{job_id}] - Revisando... Archivos encontrados: {current_file_count}")
            
            if current_file_count > previous_file_count:
                print(f"[{job_id}] - ¡Atividad detectada! Se subieron nuevos archivos.")
                last_activity_time = datetime.now()
                previous_file_count = current_file_count
            
            # Comprobamos si han pasado 30 minutos desde la última actividad
            inactivity_period = datetime.now() - last_activity_time
            if inactivity_period > timedelta(seconds=30):
                print(f"[{job_id}] - No se ha detectado actividad por 30 minutos.")
               
                # Ahora que sabemos que la subida terminó, obtenemos el enlace
                enlace = get_link_compartidos(folder_path)
                if enlace:
                     print(f"[{job_id}] - Enlace de Dropbox:{enlace}")
                     # El próximo paso será llamar a la función de envío de correo aquí
                else:
                    print(f"[{job_id}] - No se puedo generar el enlace de Dropbox.")
                break #salimos del bucle de monitoreo
        
        except Exception as e:
            print(f"[{job_id}] - Error durante el monitoreo: {e}")
            break
        #esperemos 5 minutos antes de la siguiente revision
        time.sleep(10)
        
            


@app.post("/webhook")
async def recibir_webhook(data: WebhookData, background_tasks: BackgroundTasks): # <--- ¡El gran cambio está aquí!
    print(f"Webhook recibido. Tipo de evento: {data.event_type}")

    # Lógica para manejar diferentes tipos de eventos
    if data.event_type == "Pedido creado":
        print(f"Nuevo pedido creado para el trabajo {data.job_id} con estilo {data.style}")
        # Guardamos la información clave para usarla más tarde
        trabajos_pendientes[data.job_id] = {
            "style": data.style,
            "client_name": data.client_name,
            "property_address": data.property_address
        }

    elif data.event_type == "Fotógrafo completado":
        print(f"Fotógrafo ha completado el trabajo {data.job_id}")
        if data.job_id in trabajos_pendientes:
            print("Este trabajo está en nuestra lista de pendientes.")
            info_trabajo = trabajos_pendientes[data.job_id]
            
             # Construimos la ruta de la carpeta (usando el método robusto con job_id)
            folder_path =  f"/Apps/AutomatizacionFotografia/{data.job_id}"
            # ¡Activamos el vigilante en segundo plano!
            background_tasks.add_task(monitor_folder_uploads, data.job_id, folder_path)
            
            print(f"Tarea de monitoreo para {data.job_id} iniciando en segundo plano, La app sigue libre.")
            # Ya no eliminamos el trabajo pendiente aquí, lo haremos después de enviar el correo
        else:
            print(f"Alerta: Trabajo {data.job_id} completado pero no teniamos registro del pedido.")
           
            
    print("Estado actual de trabajos pendientes:", trabajos_pendientes)
    return {"status": "procesado", "job_id": data.job_id}