import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

REMITENTE = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("EMAIL_PASSWORD")

#define la lsita de correos de tus equipos
DESTINATARIOS_PREMIUM = ["crypzus91@gmail.com"]
DESTINATARIOS_BASIC = ["bastardomejiasines1998@gmail.com"]

def send_notification_email(job_info: dict, dropbox_link:str):
    """
    Envía un correo de notificación al equipo de edición correcto.
    """
    style = job_info.get("style", "Basico")
    if "premium" in style.lower():
        destinatarios = DESTINATARIOS_PREMIUM
    else:
        destinatarios = DESTINATARIOS_BASIC
    
    #---Creacion del mensaje ---
    
    message = MIMEMultipart("alternative")
    message["Subject"] = f"Nuevo Trabajo listo para Edición: {job_info.get('property_address')}"
    message["From"] = REMITENTE
    message["To"] = ",".join(destinatarios)
    
     # Cuerpo del correo en formato HTML para que se vea bien
    html = f"""
    <html>
    <body>
        <p>Hola equipo,</p>
        <p>Un nuevo trabajo de fotografía está listo para ser editado. Aquí están los detalles:</p>
        <ul>
        <li><strong>Cliente:</strong> {job_info.get('client_name')}</li>
        <li><strong>Dirección:</strong> {job_info.get('property_address')}</li>
        <li><strong>Estilo de Edición:</strong> {style}</li>
        </ul>
        <p><strong><a href="{dropbox_link}">Haz clic aquí para acceder a los archivos en Dropbox</a></strong></p>
        <p>¡Gracias!</p>
    </body>
    </html>
    """
    # Adjuntamos el HTML al mensaje
    message.attach(MIMEText(html, "html"))
    
    try:
        #---envio del correo---
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls() #inicia conexion segura
        server.login(REMITENTE, PASSWORD)
        server.sendmail(REMITENTE, destinatarios, message.as_string())
        server.quit()
        print(f"Correo de notificacion para {job_info.get('job_id')} enviado a: {destinatarios}")
        return True
    except Exception as e:
        print (f"Error al enviar el correo: {e}")
        return False