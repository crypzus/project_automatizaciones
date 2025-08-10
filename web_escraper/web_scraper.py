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
    # buscar elementos que podrian ser articulos
    # nota: estos selectores son genericos y puede necesitar ajustes segun el sitio web
    for articulo_elem in soup.select("article, .article, .post, .new-item"):
        articulo = {}
        # extraer titulo
        titulo_elem = articulo_elem.find(
            ["h1", "h2", "h3"]
        ) or articulo_elem.select_one(".titulo, .headline, .p")
        if titulo_elem:
            articulo["titulo"] = titulo_elem.text.strip()
        else:
            continue  # si no hya titulo, pasar al siguiente
        # extrae fecha si esta disponible
        fecha_elem = articulo_elem.select_one(".date, .time, .published, .timestamp")
        articulo["fecha"] = fecha_elem.text.strip() if fecha_elem else ""

        # extraer el resumen si esta disponible
        resumen_elem = articulo_elem.select_one(
            ".summary, .excerpt, .description, .snippet, .p"
        )
        articulo["resumen"] = resumen_elem.text.strip() if resumen_elem else ""

        # añadir a la lista de articulos
        articulos.append(articulo)

    return articulos


def guardar_en_csv(datos, nombre_archivo):
    """guarda una lista de diccionarios en un archivo csv

    args:
    Datos: lista de diccionario con los datos a guardar
    nomb_archivo: nombre del archivo CSV a crear

    returns:
    bool: True si se guardo corretamente, False en caso contratio

    """

    try:
        # verifica que hay datos par guardar
        if not datos:
            print("No hay datos para guardar .")
            return False
        # obtener los nombre de las colunas del prier diccionario
        columnas = datos[0].keys()

        with open(nombre_archivo, "w", newline="", encoding="utf-8") as archivo_csv:
            writer = csv.DictWriter(archivo_csv, fieldnames=columnas)
            writer.writeheader()  # ecribe encabezados
            writer.writerows(datos)  # escribe fila de datos
        print(f" Datos guardadods exitosamente en '{nombre_archivo}'")
        return True
    except Exception as e:
        print(f" Error al guardar en csv:{e}")
        return False


def main():
    """funcion principal del programa"""
    print("===WEB SCRAPER BASICO===")
    # solicitar url al usario

    url = input("ingresa la URL de la pagina web a analizar: ")

    # obtener el HTML de la pagina
    print(f"Descargando  contenido de {url}...")
    html = obtener_html(url)
    if not html:
        print("NO de puedo obtener el contenido de a pagina.")
        return
    print("Contenido descargado correctamente.")

    print("\n Opciones:")
    print("1. Extraer titulos de noticias")
    print("2. Extraer articulos completos")

    opcion = input("\n Seleciona una opcion (1-2): ")

    if opcion == "1":
        # Extraer titulos de noticias
        print("\n Extrayendo titulos de noticias...")
        titulos = extraer_titulos_noticias(html)

        print(f"\n Se encotraron {len(titulos)} titulos:")
        for i, titulo in enumerate(titulos, 1):
            print(f"{i}. {titulo}")
        # guardar en csv
        if (
            titulos
            and input(
                "\n ¿Desea guardar los titulos en un archivo CSV? (s/n): "
            ).lower()
            == "s"
        ):
            # convertir la lista de titulos a una lista de diccionario
            datos = [
                {"numero": i, "titulo": titulo} for i, titulo in enumerate(titulos, 1)
            ]
            guardar_en_csv(datos, "titulos_noticias.csv")

    elif opcion == "2":
        # Extraer articulos
        print("\n Extrayendo articulos de noticias...")
        articulos = extraer_articulos(html)

        print(f"\n Se encotraron {len(articulos)} articulos.")
        for i, articulo in enumerate(articulos, 1):
            print(f"\n {i}. {articulo.get('titulo', 'sin titulo')}")
            if articulo.get("fecha"):
                print(f"   Fecha: {articulo['fecha']}")
            if articulo.get("resumen"):
                print(f"   Resumen: {articulo['resumen'][:100]}...")
            # if articulo.get("enlace"):
            #     print(f" Enlace: {articulo['enlace']}")
        # guardar en csv
        if (
            articulos
            and input(
                "\n ¿Desea guardar los articuloa en un archivo CSV? (s/n): "
            ).lower()
            == "s"
        ):
            guardar_en_csv(articulos, "articulos_noticias.csv")
        else:
            print("opcion no validad.")


if __name__ == "__main__":
    main()
