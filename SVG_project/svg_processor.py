# 1. Importamos las librerías necesarias
import os  # Para interactuar con el sistema de archivos (crear carpetas)
from lxml import etree  # Para construir y manipular el XML del SVG
from svgelements import *  # Para entender la geometría del SVG


# 2. Definimos la función principal que hará todo el trabajo
def process_svg(input_path, output_path, target_size=(24, 24)):
    """
    Modifica un SVG para que se ajuste a un tamaño y estructura XML específicos.
    """
    print(f"Procesando: {input_path}")
    # ... (dentro de la función process_svg)
    try:
        # --- ANÁLISIS GEOMÉTRICO ---
        # svgelements analiza el archivo y entiende sus formas
        svg_geom = SVG.parse(input_path)

        # Calculamos el rectángulo imaginario que encierra todo el dibujo
        bbox = svg_geom.bbox()
        if bbox is None:
            print(f"  -> Advertencia: SVG vacío o sin elementos visibles.")
            return

        x, y, x_max, y_max = bbox
        original_width = x_max - x
        original_height = y_max - y

        if original_width == 0 or original_height == 0:
            print(f"  -> Advertencia: El contenido no tiene dimensión.")
            return

        # --- CÁLCULO DE TRANSFORMACIONES ---
        target_w, target_h = target_size

        # Damos un margen del 10% para que el icono no toque los bordes
        padding = 0.9

        # Calculamos cuánto hay que escalar el dibujo para que quepa
        scale = min(
            (target_w * padding) / original_width,
            (target_h * padding) / original_height,
        )

        # Calculamos las nuevas dimensiones y posición del dibujo escalado
        new_width = original_width * scale
        new_height = original_height * scale

        # Calculamos cuánto hay que mover (trasladar) el dibujo para centrarlo
        translate_x = (target_w - new_width) / 2 - (x * scale)
        translate_y = (target_h - new_height) / 2 - (y * scale)

        # Creamos el string de transformación que usará el SVG
        transform_str = (
            f"translate({translate_x:.4f} {translate_y:.4f}) scale({scale:.4f})"
        )
        print(f"  -> Transformación calculada: {transform_str}")

        # Aquí irá la lógica de reconstrucción del XML...
        # ... (a continuación del cálculo de transformaciones)

        # --- RECONSTRUCCIÓN ESTRUCTURAL CON LXML ---
        # lxml analiza el archivo para que podamos manipular su estructura XML
        parser = etree.XMLParser(remove_blank_text=True)
        xml_tree = etree.parse(input_path, parser)
        xml_root = xml_tree.getroot()

        # Creamos la etiqueta raíz <svg> para nuestro nuevo archivo
        new_root = etree.Element(
            "svg",
            width=str(target_w),
            height=str(target_h),
            viewBox=f"0 0 {target_w} {target_h}",
            xmlns="http://www.w3.org/2000/svg",
        )

        # Añadimos la capa de metadatos que necesitas
        metadata = etree.SubElement(new_root, "metadata")
        metadata.text = "Icono procesado con svg_processor.py"

        # Creamos el grupo <g> que contendrá todo el dibujo y aplicará la transformación
        main_group = etree.SubElement(
            new_root, "g", id="main_layer", transform=transform_str
        )

        # Buscamos todos los elementos visuales del SVG original...
        for element in xml_root:
            # La etiqueta de un elemento puede incluir el namespace, ej: {http://www.w3.org/2000/svg}path
            # Usamos `endswith` para ignorar el namespace y solo quedarnos con el nombre de la etiqueta
            if element.tag.endswith(
                (
                    "path",
                    "circle",
                    "rect",
                    "g",
                    "polygon",
                    "polyline",
                    "line",
                    "ellipse",
                )
            ):
                # ...y los movemos dentro de nuestro nuevo grupo
                main_group.append(element)

        # --- GUARDAR EL RESULTADO ---
        output_bytes = etree.tostring(
            new_root, pretty_print=True, xml_declaration=True, encoding="UTF-8"
        )

        with open(output_path, "wb") as f:
            f.write(output_bytes)

        print(f"  -> Archivo guardado en: {output_path}")

    except Exception as e:
        print(f"  -> ERROR: {e}")
    # Por ahora, solo un mensaje de que está en construcción
    print("Lógica de procesamiento pendiente...")


# 3. Este bloque permite que el script se pueda ejecutar directamente
if __name__ == "__main__":
    # Nombre del archivo de entrada que vamos a procesar
    input_file = "input_icon.svg"

    # Crear la carpeta de salida si no existe
    output_folder = "output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Definir la ruta completa del archivo de salida
    output_file = os.path.join(output_folder, "processed_icon.svg")

    # Llamar a nuestra función para que haga la magia
    process_svg(input_file, output_file)

    print("\n¡Proceso completado!")
