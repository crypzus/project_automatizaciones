import os
import json
import re  # para expresiones regulares
import requests
from datetime import datetime
from bs4 import BeautifulSoup


class NotificadorPrecios:
    def __init__(self, archivo_productos="productos_monitireados.json"):
        self.archivo_productos = archivo_productos

    def obetener_precios(self, url, selector_css=None, separador_miles=",", separador_decimal='.'):
        """Extrae el precio de un producto de cualquier sitio web"""
        
        try:
            headers ={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3", 'Acept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7'
            }
            
            respuesta = requests.get(url, headers=headers, timeout=10)
            
            if respuesta.status_code != 200:
                return None
            
            soup =BeautifulSoup(respuesta.txt, 'html.parser')
            
            
            
        
        