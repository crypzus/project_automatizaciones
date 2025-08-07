import os
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# ----------------- Funciones de conversión -----------------


def listar_formatos_soportados():
    """Lista los formatos soportados."""
    formatos = ["JPG", "JPEG", "PNG", "GIF", "TIFF", "WEBP"]
    print("Formatos soportados:")
    for formato in formatos:
        print(f"- {formato}")
    return formatos


def convertir_img(ruta_imagen, formato_salida, carpeta_destino=None):
    """Convierte una imagen a otro formato."""
    try:
        if not os.path.exists(ruta_imagen):
            print(f"ERROR: La imagen '{ruta_imagen}' no existe.")
            return None

        nombre_archivo = os.path.basename(ruta_imagen)
        nombre_base = os.path.splitext(nombre_archivo)[0]

        if carpeta_destino is None:
            carpeta_destino = os.path.join(os.path.dirname(ruta_imagen), "convertidas")
        os.makedirs(carpeta_destino, exist_ok=True)

        formato_salida = formato_salida.lower().strip(".")
        ruta_salida = os.path.join(carpeta_destino, f"{nombre_base}.{formato_salida}")

        imagen = Image.open(ruta_imagen)

        if formato_salida == "gif":
            if imagen.mode in ("RGBA", "LA"):
                # Crea un fondo blanco y pega la imagen encima (elimina la transparencia)
                fondo = Image.new("RGB", imagen.size, (255, 255, 255))
                fondo.paste(
                    imagen, mask=imagen.split()[-1]
                )  # Usa el canal alfa como máscara
                imagen = fondo.convert("P", palette=Image.ADAPTIVE)
            else:
                imagen = imagen.convert("P", palette=Image.ADAPTIVE)

        imagen.save(ruta_salida)
        print(f"Imagen convertida y guardada en: {ruta_salida}")
        return ruta_salida

    except Exception as e:
        print(f"ERROR al convertir la imagen: {e}")
        return None


def convertir_multiple_img(carpeta_origen, formato_salida, carpeta_destino=None):
    """Convierte todas las imágenes en una carpeta."""
    if not os.path.exists(carpeta_origen):
        print(f"ERROR: La carpeta '{carpeta_origen}' no existe.")
        return 0

    extensiones = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"]

    if carpeta_destino is None:
        carpeta_destino = os.path.join(carpeta_origen, "convertidas")
    os.makedirs(carpeta_destino, exist_ok=True)

    contador = 0
    for archivo in os.listdir(carpeta_origen):
        ruta = os.path.join(carpeta_origen, archivo)
        if os.path.isfile(ruta) and any(
            archivo.lower().endswith(ext) for ext in extensiones
        ):
            if convertir_img(ruta, formato_salida, carpeta_destino):
                contador += 1

    return contador


# ----------------- Interfaz gráfica -----------------


def abrir_archivo():
    ruta = filedialog.askopenfilename(
        title="Seleccionar imagen",
        filetypes=[("Imágenes", "*.jpg;*.jpeg;*.png;*.gif;*.tiff;*.webp")],
    )
    entrada_origen.delete(0, tk.END)
    entrada_origen.insert(0, ruta)


def abrir_carpeta():
    carpeta = filedialog.askdirectory(title="Seleccionar carpeta")
    entrada_origen.delete(0, tk.END)
    entrada_origen.insert(0, carpeta)


def seleccionar_destino():
    carpeta = filedialog.askdirectory(title="Seleccionar carpeta destino")
    entrada_destino.delete(0, tk.END)
    entrada_destino.insert(0, carpeta)


def convertir():
    ruta_origen = entrada_origen.get()
    destino = entrada_destino.get()
    formato = combo_formatos.get().lower()

    if not ruta_origen or not formato:
        nota.set("⚠️ Debes seleccionar ruta y formato.")
        return

    try:
        if os.path.isdir(ruta_origen):
            cantidad = convertir_multiple_img(ruta_origen, formato, destino)
            nota.set(f"✅ Se convirtieron {cantidad} imágenes.")
        else:
            salida = convertir_img(ruta_origen, formato, destino)
            if salida:
                nota.set(f"✅ Imagen convertida: {os.path.basename(salida)}")
            else:
                nota.set("❌ Error al convertir la imagen.")
    except Exception as e:
        nota.set(f"❌ Error: {e}")


# ----------------- Ventana -----------------

ventana = tk.Tk()
ventana.title("Convertidor de Imágenes")
ventana.geometry("500x300")

tk.Label(
    ventana,
    text="CONVERTIDOR DE IMAGENES\n JPG, JPEG, PNG, GIF, TIFF, WEBP",
    font=("Helvetica", 16, "bold"),
).pack(pady=10)

tk.Label(ventana, text="Ruta de origen:").pack()
entrada_origen = tk.Entry(ventana, width=60)
entrada_origen.pack()

frame_botones = tk.Frame(ventana)
frame_botones.pack()
tk.Button(frame_botones, text="Seleccionar imagen", command=abrir_archivo).pack(
    side=tk.LEFT, padx=5
)
tk.Button(frame_botones, text="Seleccionar carpeta", command=abrir_carpeta).pack(
    side=tk.LEFT, padx=5
)

tk.Label(ventana, text="Ruta de destino:").pack()
entrada_destino = tk.Entry(ventana, width=60)
entrada_destino.pack()
tk.Button(
    ventana, text="Seleccionar carpeta destino", command=seleccionar_destino
).pack(pady=5)

tk.Label(ventana, text="Formato de salida:").pack()
combo_formatos = ttk.Combobox(
    ventana, values=["JPG", "JPEG", "PNG", "GIF", "TIFF", "WEBP"]
)
combo_formatos.pack()

tk.Button(ventana, text="Convertir", command=convertir, bg="green", fg="white").pack(
    pady=10
)

nota = tk.StringVar()
tk.Label(ventana, textvariable=nota, fg="blue").pack()

ventana.mainloop()
