import os
import csv
import statistics
import matplotlib.pyplot as plt


def cargar_datos_csv(ruta_archivo):
    """
    Carga datos desde un archivo csv

    args:
    ruta_archivo: ruta del archivo CSV a cargar

    returns:
    tuple: (encabezados, datos) donde encabezados es una lista de nommbres de columnas
    y datos es una lista de dicionarios con los datos
    """
    try:
        if not os.path.exists(ruta_archivo):
            print(f"Error: el archivo '{ruta_archivo}' no existe. ")
            return None, None
        # leer arivo csv
        encabezados = []
        datos = []

        with open(ruta_archivo, "r", newline="", encoding="utf-8") as archivo_csv:
            # crear una lector CSV
            lector = csv.reader(archivo_csv)

            # leer la primera fila como emcabezado
            encabezados = next(lector)

            # leer los demas datos del archivo Csv
            for fila in lector:
                # crear un diccionario de cada fila
                if len(fila) == len(encabezados):
                    fila_dict = {}
                    for i, valor in enumerate(fila):
                        try:
                            # primero intentamos convertir el valor str en un valor int
                            fila_dict[encabezados[i]] = int(valor)
                        except ValueError:
                            try:
                                # si no es entero, intentar convertir en float
                                fila_dict[encabezados[i]] = float(valor)
                            except ValueError:
                                # si no es numero , dejar como str
                                fila_dict[encabezados[i]] = valor
                    datos.append(fila_dict)
        print(
            f"se cargaron {len(datos)} filas de datos con {len(encabezados)} columnas."
        )
        return encabezados, datos
    except Exception as e:
        print(f"error de archivo Csv: {e}. ")
        return None, None


cargar_datos_csv("Gym_Exercise_Dataset_export.csv")


def mostrar_resumen_datos(encabezados, datos):
    """
    muestra un resuemen de los datos cargados
    Args:
    encabezados: lista de nombre de columna
    datos: lista de diccionario con los datos

    """
    if not datos:
        print("No hay datos para mostrar.")
        return
    print("\n===RESUMEN DE DATOS===")
    print(f"total de registros: {len(datos)}")
    print(f"columnas: {', '.join(encabezados)}")

    # Mostrar las primeras 5 filas
    # esto se puediera hacer con la library de panda a modo de ejemplo lo aremos sin el
    print("\n Primeras 5 filas:")
    for i, fila in enumerate(datos[:5]):
        print(f"fila {i+1}: {fila}")


def analizar_columna_numerica(datos, columna):
    """Analiza una columna numerica y muestra estadisticas basicas
    args:
    datos: lista de diccionarios con los datos
    columna: nombre de la columna a analizar
    returns:
    dict: un diccionario con las estadisticas basicas de la columna
    """
    # extraer los valores de la columna, filtrando solo los que son numericos

    valores = []
    for fila in datos:
        if columna in fila and isinstance(fila[columna], (int, float)):
            valores.append(fila[columna])

        # verificar si hay valores numericos
    if not valores:
        print(f"no hay valores numericos en la columna '{columna}'.")
        return None

    # calcular estadisticas basicas
    estadisticas = {
        "columna": columna,
        "total_valores": len(valores),
        "minimo": min(valores),
        "maximo": max(valores),
        "suma": sum(valores),
        "promedio": sum(valores) / len(valores),
        "mediana": statistics.median(valores),
        "desviacion_estandar": statistics.stdev(valores) if len(valores) > 1 else 0,
    }
    return estadisticas


def mostrar_estatisticas(estadisticas):
    """Muestra las estadisticas de una columna numerica
    args:
    estadisticas: dict con las estadisticas de la columna
    """

    if not estadisticas:
        return

    print(f"\n===ESTADISTICAS DE LA COLUMNA '{estadisticas['columna']}'===")
    print(f"total de valores: {estadisticas['total_valores']}")
    print(f" valor minimo: {estadisticas['minimo']}")
    print(f"Valor maximo:{estadisticas['maximo']}")
    print(f"Suma: {estadisticas['suma']}")
    print(f"Promedio:{estadisticas['promedio']:.2f}")
    print(f"Mediana:{estadisticas['mediana']:.2f}")
    print(f"Desviacion estandar:{estadisticas['desviacion_estandar']:.2f}")


def agrupar_y_promediar(datos, columna_x, columna_y):
    """
    Agrupa los datos por columna_x y calcula el promedio de columna_y para cada grupo.
    Args:
        datos: lista de diccionarios con los datos
        columna_x: nombre de la columna para agrupar
        columna_y: nombre de la columna para calcular el promedio
    Returns:
        tuple: (valores_x, promedios_y)
    """
    grupos_x = {}
    for fila in datos:
        if (
            columna_x in fila
            and columna_y in fila
            and isinstance(fila[columna_y], (int, float))
        ):
            valor_x = str(fila[columna_x])
            valor_y = fila[columna_y]
            if valor_x not in grupos_x:
                grupos_x[valor_x] = []
            grupos_x[valor_x].append(valor_y)

    valores_x = []
    promedios_y = []
    for valor_x, valores_y in grupos_x.items():
        if valores_y:
            valores_x.append(valor_x)
            promedios_y.append(sum(valores_y) / len(valores_y))
    return valores_x, promedios_y


def generar_graficos_barras(datos, columna_x, columna_y, titulo=None):
    """Genera un grafico de barras mostrando el promedio de los valores Y para cada valor de X
    args:
    datos: lista de diccionarios con los datos
    columna_x: nombre de la columna para el eje X
    columna_y: nombre de la columna para el eje Y
    titulo: titulo del grafico (opcional)
    returns:
    bool: True si se genero el grafico, False si hubo un error"""

    try:
        valores_x, promedios_y = agrupar_y_promediar(datos, columna_x, columna_y)
        # verificar que hay datos para graficar
        if len(valores_x) < 2:
            print("No hay suficientes datos para generar el grafico.")
            return False

        # ordenar valores_x y promedios_y juntos
        pares = list(zip(valores_x, promedios_y))
        try:
            # Intenta ordenar como números
            pares.sort(key=lambda x: float(x[0]))
        except ValueError:
            # Si falla, ordena como strings
            pares.sort(key=lambda x: str(x[0]).lower())
            valores_x, promedios_y = zip(*pares)

        # crear el grafico de barras
        # usando import matplotlib.pyplot as plt
        plt.figure(figsize=(10, 6))
        plt.bar(valores_x, promedios_y, color="green")

        # añadir etiquetas y titulo
        plt.xlabel(columna_x)
        plt.ylabel(f"promedio de {columna_y}")
        plt.title(titulo or f"Promedio de {columna_x} por {columna_y}")

        # rotar etiquetas del eje X si son muchas
        if len(valores_x) > 10:
            plt.xticks(rotation=45, ha="right")

        # ajustar layout
        plt.tight_layout()

        # mostrar el grafico
        plt.show()
        return True
    except Exception as e:
        print(f"Error al genrar el grafico: {e}")
        return False


def generar_graficos_lineas(datos, columna_x, columna_y, titulo=None):
    """Genera un grafico de barras mostrando el promedio de los valores Y para cada valor de X
    args:
    datos: lista de diccionarios con los datos
    columna_x: nombre de la columna para el eje X
    columna_y: nombre de la columna para el eje Y
    titulo: titulo del grafico (opcional)
    returns:
    bool: True si se genero el grafico, False si hubo un error"""

    try:
        valores_x, promedios_y = agrupar_y_promediar(datos, columna_x, columna_y)
        # verificar que hay datos para graficar
        if len(valores_x) < 2:
            print("No hay suficientes datos para generar el grafico.")
            return False

        # ordenar valores_x y promedios_y juntos
        pares = list(zip(valores_x, promedios_y))
        try:
            # Intenta ordenar como números
            pares.sort(key=lambda x: float(x[0]))
        except ValueError:
            # Si falla, ordena como strings
            pares.sort(key=lambda x: str(x[0]).lower())
            valores_x, promedios_y = zip(*pares)

        # crear el grafico de lienea
        # usando import matplotlib.pyplot as plt
        plt.figure(figsize=(10, 6))
        plt.plot(valores_x, promedios_y, marker="o", linestyle="-", color="skyblue")

        # añadir etiquetas y titulo
        plt.xlabel(columna_x)
        plt.ylabel(f"promedio de {columna_y}")
        plt.title(titulo or f"Promedio de {columna_x} por {columna_y}")

        # rotar etiquetas del eje X si son muchas
        if len(valores_x) > 10:
            plt.xticks(rotation=45, ha="right")

        # ajustar layout
        plt.tight_layout()

        # mostrar el grafico
        plt.show()
        return True
    except Exception as e:
        print(f"Error al genrar el grafico: {e}")
        return False


def main():
    """Función principal para ejecutar el análisis de datos"""
    print("===ANALISIS DE DATOS CSV===")

    # solicitar la ruta del archivo CSV
    ruta_archivo = input("Ingrese la ruta del archivo CSV: ").strip()
    # cargar datos
    encabezados, datos = cargar_datos_csv(ruta_archivo)

    if not datos:
        print("No se pudieron cargar los datos.")
        return
    # mostrar resumen de datos
    mostrar_resumen_datos(encabezados, datos)

    while True:
        # menu de opciones
        print("\n===MENU DE OPCIONES===")
        print("1. Analizar columna numérica")
        print("2. Generar gráfico de barras")
        print("3. Generar gráfico de líneas")
        print("4. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            # analizar columna numerica
            print("\ncolumnas disponibles:")
            for i, encabezado in enumerate(encabezados):
                print(f"{i + 1}. {encabezado}")
