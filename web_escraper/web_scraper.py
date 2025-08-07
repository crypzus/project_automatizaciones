# guadar archivos csv
import csv

# se usa para obtener datos de la web
import requests

# se usa para parsear el html información mas específica
from bs4 import BeautifulSoup


def obtener_html(url):
    """
    Obtiene el HTML de una URL dada.
    args:
    url:la URL de la página web a descargar.
    :return:
    str: Contenido HTML de la página, None si hay error.
    """
    try:
        # Configurar el User-agent para evitar bloqueos
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        # realizar la peticion GEt

        respuesta = requests.get(url, headers=headers, timeout=10)

        # verificar si la peticion fue exitosa
        if respuesta.status_code == 200:
            return respuesta.text
        else:
            print(f"Error al obtener la pagina:Codigo de estado{respuesta.status_code}")
            return None
    except Exception as e:
        print(f"Error al obtener la pagina :{e}")
        return None


def extraer_titulos_noticias(html):
    """
    extrae los titulos de noticas de la pagina html
        args:
            html:el contenido html de la pagina
        returns:
            list:lista de titulos encntrados
    """
    # crear el objeto BeautifulSoup para analizar el html
    soup = BeautifulSoup(html, "html.parser")

    # buscar todos los elementos que podrian contener titulos de noticias
    # Nota: estos selectores son genericos y puede necesitar ajustes segun el sitio web
    titulos = []

    # buscar em elementos h1.h2, h3 que podrian contener titulos

    for heading in soup.find_all(["h1", "h2", "h3"]):
        # filtrar solo los que aparecen ser titulos de noticias (pot ejemplos, con cierta longintud)
        if heading.text.strip() and len(heading.text.strip()) > 15:
            titulos.append(heading.text.strip())
    # buscar tambien elementos con claes comunes para titulos de noticias
    for elemento in soup.select(".title, .headline, .article-title, .news-title"):
        if elemento.text.strip() and elemento.text.strip() not in titulos:
            titulos.append(elemento.text.strip())
    return titulos


def extraer_articulos(html):
    """
    extrae los titulos de noticas de la pagina html
        args:
            html:el contenido html de la pagina
        returns:
            list:lista de diccionario con informacionde los articulos
    """
    # crear el objeto BeautifulSoup para analizar el html
    soup = BeautifulSoup(html, "html.parser")

    # lista para alamnacenar los articulo
    articulos = []
