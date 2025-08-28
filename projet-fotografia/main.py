from fastapi import FastAPI
from pydantic import BaseModel # 1. Importamos la herramienta para crear plantillas
from typing import Optional   # 2. Importamos una ayuda para campos opcionales
from dropbox_manager import get_link_compartidos

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

@app.post("/webhook")
async def recibir_webhook(data: WebhookData): # <--- ¡El gran cambio está aquí!
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
            direccion = info_trabajo.get("property_address", "direccion-desconocida")
            
            #Construimos  la ruta de la carpeta(!se hara dinamico despues !)
            ruta_carpeta_dropbox = f"/Apps/AutomatizacionFotografia/{direccion}"
            print(f"Buscando enlace para la carpeta: {ruta_carpeta_dropbox}")
            enlace = get_link_compartidos(ruta_carpeta_dropbox)
            if enlace:
                print(f"¡Exito! El enlace compartido es:{enlace}")
            else:
                print("Error: No se ouedo obtener el enlace de Dropbox")         
        else:
            print("Alerta: Trabajo completado pero no teníamos registro del pedido.")

    print("Estado actual de trabajos pendientes:", trabajos_pendientes)
    return {"status": "procesado", "job_id": data.job_id}