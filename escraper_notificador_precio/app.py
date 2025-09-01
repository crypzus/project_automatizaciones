from notificador import NotificadorPrecios


def mostrar_productos(notifica):
    productos = notifica.cargar_productos()

    if not productos:
        print("\n No hay productos monitoreados.")
        return

    print(f"\n === PRODUCTOS MONITOREADOS {len(productos)}===")

    # mostrar historial de precios
    for i, producto in enumerate(productos, 1):
        print(f"\n {i}. {producto['nombre']}")
        print(f"   URL: {producto['url']}")
        print(f"  Precio Deseado:{producto['precio_deseado']}")
        print(f" Precio Actual: {producto.get('precio_actual','No Disponible')}")

        # Mostrar historial de precio  si existe
        if producto.get("historial_precios"):
            print("  Historial de precios recientes: ")
            for registro in producto["historial_precios"][-3:]:
                print(f"     {registro['fecha']}:{registro['precio']}")


def main():
    """Función principal del programa con menu interativo."""
    print("=== NOTIFICADOR DE PRECIOS ===")

    # crear una instacia del notificador
    notifica = NotificadorPrecios()

    while True:
        print("\n Opciones: ")
        print(" 1. Agregar un producto  monitorear")
        print(" 2. Mostrar productos monitoreados")
        print(" 3. Actualizar precios")
        print(" 4. Eliminar un producto")
        print(" 5. Salir")

        opcion = input("\n Seleccione una opcion (1-5): ")

        if opcion == "1":
            nombre = input("\n Ingrese el nombre del producto: ")
            url = input("Ingrese la URL del producto: ")
            precio_deseado = float(input("ingrese el precio deseado: "))
            usar_selector = (
                input(
                    " Deseas  especificar un selector CSS personalizado?(s/n): "
                ).lower()
                == "s"
            )
            selector_css = None

            if usar_selector:
                selector_css = input("Ingresa el selector CSS para el precio:")
            # Preguntar por el precio de miles
            separador_miles = input(
                "¿Cual es el separador de miles en el precio? (. O , )[por defecto ',']: "
            ).strip()
            if separador_miles not in [",", "."]:
                separador_miles = ","
                print("Usando separador de miles por defecto:','")

            resultado = notifica.agregar_productos(
                nombre, url, precio_deseado, selector_css, separador_miles
            )

            if resultado:
                print(f"\n Producto '{nombre}' agregado corectamente.")
            else:
                print(
                    f"\n No se puedo agregar el producto '{nombre}' (posiblemente ya existe)."
                )

        elif opcion == "2":
            # mostrar productos
            mostrar_productos(notifica)

        elif opcion == "3":
            # actulizar precios
            print("\n Actualizando precios de todos los productos...")
            productos_actualizados = notifica.actualizar_precios()
            if productos_actualizados:
                print(
                    f"\n ¡Se encontraron {len(productos_actualizados)} productos bajo el precio deseado!"
                )
                for producto in productos_actualizados:
                    print(
                        f"- {producto['nombre']}: Precio actual {producto['precio_actual']}"
                    )
            else:
                print("\n No se encontraron cambios importantes en los precios.")

        elif opcion == "4":
            # Eliminar un producto

            mostrar_productos(notifica)
            productos = notifica.cargar_productos()
            if productos:
                try:
                    indice = int(
                        input("\n Ingrese el numero del producto a eliminar: ")
                    )

                    if notifica.eliminar_productos(indice):
                        print(f"\n Producto #{indice} elimino correctamente.")
                    else:
                        print(f"\n No se pudo elimar  el producto #{indice}")
                except ValueError:
                    print("\n  Por favor ingrese un numero valido.")
            else:
                print("\n No hay productos para eliminar.")

        elif opcion == "5":
            print("\n Saliendo del programa. ¡Hasta luego!")
            break
        else:
            print("\n Opcion invalida. Por favor seleccione una opcion del 1 al 5.")


if __name__ == "__main__":
    main()
