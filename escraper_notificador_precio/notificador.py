import os
import json
import re  # para expresiones regulares
import requests
from datetime import datetime
from bs4 import BeautifulSoup


class NotificadorPrecios:
    def __init__(self, archivo_productos="productos_monitireados.json"):
        self.archivo_productos = archivo_productos

    def obtener_precios(self, url, selector_css=None, separador_miles=","):
        """Extrae el precio de un producto de cualquier sitio web"""

        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
                "Accept-Language": "es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7",
            }

            respuesta = requests.get(url, headers=headers, timeout=10)

            if respuesta.status_code != 200:
                return None

            soup = BeautifulSoup(respuesta.text, "html.parser")

            # buscar el precio usando slectores css comunes
             # Si hay un selector personalizado, úsalo
            if selector_css:
                precio_elem = soup.select_one(selector_css)
                if not precio_elem:
                    return None
                precio_texto = precio_elem.text.strip()
            else:
                # Intentar MercadoLibre (andes-money-amount)
                fraction = soup.select_one(".andes-money-amount__fraction")
                cents = soup.select_one(".andes-money-amount__cents")
                if fraction:
                    precio_texto = fraction.text.strip().replace(".", "").replace(",", "")
                    if cents:
                        precio_texto += "." + cents.text.strip()
                else:
                    # Fallback: buscar otros selectores comunes
                    selectores_comunes = [
                        ".precio",
                        ".offer-price",
                        ".curent-price",
                        "[itemprop='price']",
                        ".price-value",
                        ".price-current",
                        ".a-price",
                        ".a-offscreen",
                        "#priceblock-ourprice",
                        ".price",
                        ".product-price",
                        ".current-price",
                        ".offer-price",
                        ".final-price",
                    ]
                    precio_elem = None
                    for selector in selectores_comunes:
                        precio_elem = soup.select_one(selector)
                        if precio_elem:
                            break
                        
                    if not precio_elem:
                        return None
                    precio_texto = precio_elem.text.strip()
                    
            print("DEBUG precio bruto:", precio_texto)
            
            # --- normalización automática ---
            precio_texto = precio_texto.replace(" ", "")
            precio_limpio = re.sub(r"[^\d.,]", "", precio_texto)
            
            if "," in precio_limpio and "." in precio_limpio:
            # ejemplo: "1.234,56" -> miles con punto, decimales con coma
                precio_limpio = precio_limpio.replace(".", "").replace(",", ".")
            elif "," in precio_limpio:
            # ejemplo: "199,99" -> coma como decimal
                precio_limpio = precio_limpio.replace(",", ".")
            elif "." in precio_limpio:
                partes = precio_limpio.split(".")
                if len(partes[-1]) == 3:
                    # ejemplo: "4.085" -> punto como miles
                    precio_limpio = precio_limpio.replace(".", "")
                # si son 1 o 2 dígitos, lo dejamos como decimal

            match = re.search(r"\d+\.\d+|\d+", precio_limpio)
            return float(match.group()) if match else None
        except Exception as e:
            print("Error en obtener precios: ", e)
            return None

    def cargar_productos(self):
        """Carga la lista de productos monitoreados desde el archivo."""
        if os.path.exists(self.archivo_productos):
            try:
                with open(self.archivo_productos, "r", encoding="utf-8") as file:
                    return json.load(file)
            except Exception:
                pass
        return []

    def guardar_productos(self, productos):
        """Guarda la lista de productos monitoreados en el archivo."""
        try:
            with open(self.archivo_productos, "w", encoding="utf-8") as file:
                json.dump(productos, file, indent=4, ensure_ascii=False)
            return True
        except Exception:
            return False

    def agregar_productos(
        self, nombre, url, precio_deseado, selector_css=None, separador_miles=","
    ):
        """Agrega un nuevo producto a la lista de monitoreo."""
        productos = self.cargar_productos()

        # verificamos si el producto ya existe
        for producto in productos:
            if producto["url"] == url:
                return False
        # obtenemos el precio actual
        precio_actual = self.obtener_precios(url, selector_css, separador_miles)

        # crear el nuevo producto
        nuevo_producto = {
            "nombre": nombre,
            "url": url,
            "precio_deseado": float(precio_deseado),
            "selector_css": selector_css,
            "separador_miles": separador_miles,
            "precio_actual": precio_actual,
            "fecha_agregado": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "historial_precios": [],
        }

        if precio_actual is not None:
            nuevo_producto["historial_precios"].append(
                {
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "precio": precio_actual,
                }
            )

        productos.append(nuevo_producto)
        self.guardar_productos(productos)
        return True

    def actualizar_precios(self):
        """Actualiza los precios de todos los productos monitoreados."""
        productos = self.cargar_productos()
        productos_actualizados = []

        for producto in productos:
            separador_miles = producto.get("separador_miles", ",")
            precio_actual = self.obtener_precios(
                producto["url"], producto.get("selector_css"), separador_miles
            )

            if precio_actual is not None:
                precio_anterior = producto.get("precio_actual")
                producto["precio_actual"] = precio_actual
            # agregar al historial si el precio ha cambiado
            producto["historial_precios"].append(
                {
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "precio": precio_actual,
                }
            )
            # limitar el historial a los ultimos 30 registros
            if len(producto["historial_precios"]) > 30:
                producto["historial_precios"] = producto["historial_precios"][-30:]

            # verificar si el precio ha bajado o alcanzado el precio deseado
            if precio_actual <= producto["precio_deseado"]:
                productos_actualizados.append(producto)

        self.guardar_productos(productos)
        return productos_actualizados

    def eliminar_productos(self, indice):
        """Elimina un producto de la lista de monitoreo por su índice."""
        productos = self.cargar_productos()
        
        if not productos or indice < 1 or indice > len(productos):
            return False
        productos.pop(indice- 1)
        self.guardar_productos(productos)
        return True