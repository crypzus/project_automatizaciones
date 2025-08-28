import os
import dropbox
from dotenv import load_dotenv


#Carga las variables del archivo .env para que estén disponibles 
load_dotenv()
#Lee el token de acceso desde la variable de entorno
DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")

#Inicializa el cliente de Dropbox con nuestro token de acceso
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

def get_link_compartidos(folder_path):
    """Obtiene los enlaces compartidos de una carpeta específica en Dropbox."""
    
    try:
        #Intenta crear un nuevo enlace compartido
        link_metada = dbx.sharing_create_shared_link_with_settings(path=folder_path)
        print(f"Nuevo enelace creado para:{folder_path}")
        return link_metada.url
    except dropbox.exceptions.ApiError as error:
        #Si el enlace ya exixte, la API devuelve un error específico
        if error.error.is_shared_link_already_exists():
            #Si ya existe,simplemente obtenemos el enlace existente
            links =dbx.sharing_list_shared_links(path=folder_path, direct_only=True).links
            print(f"enlace ya existia para: {folder_path}")
            return links[0].url
        else:
            #Si es otro tipo de error, lo mostramos y devolvemos None.
            print(f"Error de API en Dropbox: {error}")
            return None
            
    