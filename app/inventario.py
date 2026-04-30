import flet as ft     
import os   
import json   

def main(page: ft.Page):
    page.title = "Sistema de Inventario"
    page.bgcolor = "black"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.icon = "portada_sistema.ico"
    
    # titulo de bienvenida
    titulo = ft.Text("Bienvenido al sistema de inventario", color="green", size=30)
    page.add(titulo)
    
    # funcion para cargar el inventario json
    def cargar_inventario():
        if not os.path.exists("inventario.json") or os.path.getsize("inventario.json") == 0:
            return {}
        
        with open("inventario.json", "r") as archivo:
            return json.load(archivo)
    
    # bd de inventario
    inventario = cargar_inventario()
    
    # tabla de productos
    tabla_productos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", color="green")),
            ft.DataColumn(ft.Text("Nombre", color="green")),
            ft.DataColumn(ft.Text("Cantidad", color="green")),
            ft.DataColumn(ft.Text("Precio", color="green"))
        ],
        rows=[]
    )
    
    contenedor_tabla = ft.Container(
        content=ft.Column(
            controls=[tabla_productos],
            scroll="auto"),
        width=600,
        height=400,
        border=ft.border.all(1, "blue"),
        padding=10,
        margin=10,
        bgcolor="black"
    )
    
    # funcion para actualizar la tabla de productos
    def actualizar_tabla():
        tabla_productos.rows.clear()

        for nombre, datos in inventario.items():
            fila = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(datos["ID"], color="green")),
                    ft.DataCell(ft.Text(nombre, color="green")),
                    ft.DataCell(ft.Text(str(datos["Cantidad"]), color="green")),
                    ft.DataCell(ft.Text(str(datos["Precio"]), color="green"))
                ]
            )
            tabla_productos.rows.append(fila)

        page.update()
        
    # campos de entrada
    campos = [
        "1. Entrada de productos.",
        "2. Ver productos.",
        "3. Buscar productos.",
        "4. Eliminar productos."
    ]
    
    for campo in campos:
        texto_campo = ft.Text(campo, color="green", size=20)
        page.add(texto_campo)
    
    # entrada de texto
    texto_entrada = ft.Text("Elija una opcion valida del menu:", color="green", size=20)
    entrada_opcion = ft.TextField(label="Opcion", color="green", border_color="blue", cursor_color="white", width=200)
    
    fila_entrada = ft.Row(
        controls=[texto_entrada, entrada_opcion],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10
    )
    page.add(fila_entrada)
    
    # campos para el formulario de entrada de productos
    ID_producto = ft.TextField(label="ID", color="green", border_color="blue", cursor_color="white", width=200)
    nombre_producto = ft.TextField(label="Nombre", color="green", border_color="blue", cursor_color="white", width=200)
    cantidad_producto = ft.TextField(label="Cantidad", color="green", border_color="blue", cursor_color="white", width=200)
    precio_producto = ft.TextField(label="Precio", color="green", border_color="blue", cursor_color="white", width=200)
    
    # funcion para guardar los productos 
    def guardar_producto():
        try:
            ID_val = ID_producto.value.strip()
            nombre_val = nombre_producto.value.strip()
            cantidad_val = int(cantidad_producto.value.strip())
            precio_val = float(precio_producto.value.strip())

            if not ID_val or not nombre_val:
                alerta = ft.AlertDialog(
                    title=ft.Text("ERROR", color="red"),
                    content=ft.Text("Todos los campos son obligatorios. Por favor, complete todos los campos.", color="red"),
                    alignment=ft.Alignment.CENTER,
                    actions=[
                        ft.TextButton("Cerrar", on_click=lambda e: page.pop_dialog())
                    ]
                )
                page.show_dialog(alerta)
                return
            elif not nombre_val.isalpha():
                alerta = ft.AlertDialog(
                    title=ft.Text("ERROR", color="red"),
                    content=ft.Text("El nombre debe contener solo letras.", color="red"),
                    alignment=ft.Alignment.CENTER,
                    actions=[
                        ft.TextButton("Cerrar", on_click=lambda e: page.pop_dialog())
                    ]
                )
                page.show_dialog(alerta)
                return
            if nombre_val in inventario:
                alerta = ft.AlertDialog(
                    title=ft.Text("ERROR", color="red"),
                    content=ft.Text("El nombre ya existe.", color="red"),
                    alignment=ft.Alignment.CENTER,
                    actions=[
                        ft.TextButton("Cerrar", on_click=lambda e: page.pop_dialog())
                    ]
                )
                page.show_dialog(alerta)
                return
            
            for nombre, datos in inventario.items():
                if datos["ID"] == ID_val:
                    alerta = ft.AlertDialog(
                        title=ft.Text("ERROR", color="red"),
                        content=ft.Text("El ID ya existe.", color="red"),
                        alignment=ft.Alignment.CENTER,
                        actions=[
                            ft.TextButton("Cerrar", on_click=lambda e: page.pop_dialog())
                        ]
                    )
                    page.show_dialog(alerta)
                    return 
            
            inventario[nombre_val] = {
                "ID": ID_val,
                "Cantidad": cantidad_val,
                "Precio": precio_val
            }
            with open("inventario.json", "w") as archivo:
                json.dump(inventario, archivo, indent=4)
            actualizar_tabla()    
                
            ID_producto.value = ""
            nombre_producto.value = ""
            cantidad_producto.value = ""
            precio_producto.value = ""
            page.update()
                
            page.show_dialog(ft.AlertDialog(
                title=ft.Text("Éxito", color="green"),
                content=ft.Text("Producto guardado correctamente.", color="green"),
                alignment=ft.Alignment.CENTER,
                actions=[
                    ft.TextButton("Cerrar", on_click=lambda e: page.pop_dialog())
                ]
            ))
        except ValueError:
            alerta = ft.AlertDialog(
                title=ft.Text("ERROR", color="red"),
                content=ft.Text("La cantidad y el precio deben ser números válidos.", color="red"),
                alignment=ft.Alignment.CENTER,
                actions=[
                    ft.TextButton("Cerrar", on_click=lambda e: page.pop_dialog())
                ]
            )
            page.show_dialog(alerta)
    
    # funcion para mostrar la tabla de productos    
    def ver_tabla():
        actualizar_tabla()
        tabla = ft.AlertDialog(
            title=ft.Text("Productos en el inventario"),
            content=contenedor_tabla,
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: page.pop_dialog())
            ]
        )
        page.show_dialog(tabla)
        
    def buscar_los_productos():
        actualizar_tabla()
        producto_id = buscar_id.value.strip()
        producto_nombre = buscar_nombre.value.strip()
        
        if producto_id == "" and producto_nombre == "":
            alerta = ft.AlertDialog(
                title=ft.Text("ERROR", color="red"),
                content=ft.Text("Por favor, ingrese un ID o un nombre para buscar.", color="red"),
                alignment=ft.Alignment.CENTER,
                actions=[
                    ft.TextButton("Cerrar", on_click=lambda e: page.pop_dialog())
                ]
            )
            page.show_dialog(alerta)
            return
        if producto_nombre:
            if producto_nombre not in inventario:
                alerta = ft.AlertDialog(
                    title=ft.Text("ERROR", color="red"),
                    content=ft.Text("No se encontró ningún producto con el NOMBRE proporcionado.", color="red"),
                    alignment=ft.Alignment.CENTER,
                    actions=[
                        ft.TextButton("Cerrar", on_click=lambda e: page.pop_dialog())
                    ]
                )
                page.show_dialog(alerta)
                return
            else:
                datos = inventario[producto_nombre]
                page.show_dialog(ft.AlertDialog(
                    title=ft.Text("Resultado de la búsqueda"),
                    content=ft.Column(
                        controls=[
                            ft.Text(f"ID: {datos['ID']}", color="green"),
                            ft.Text(f"Nombre: {producto_nombre}", color="green"),
                            ft.Text(f"Cantidad: {datos['Cantidad']}", color="green"),
                            ft.Text(f"Precio: {datos['Precio']}", color="green")
                        ]
                    ),
                    actions=[
                        ft.TextButton("Cerrar", on_click=lambda e: page.pop_dialog())
                    ]
                )
            )
                
        elif producto_id:
            encontrado = False
            for nombre, datos in inventario.items():
                if datos["ID"] == producto_id:
                    encontrado = True
                    page.show_dialog(ft.AlertDialog(
                        title=ft.Text("Resultado de la búsqueda"),
                        content=ft.Column(
                            controls=[
                                ft.Text(f"ID: {datos['ID']}", color="green"),
                                ft.Text(f"Nombre: {nombre}", color="green"),
                                ft.Text(f"Cantidad: {datos['Cantidad']}", color="green"),
                                ft.Text(f"Precio: {datos['Precio']}", color="green")
                            ]
                        ),
                        actions=[ft.TextButton("Cerrar", on_click=lambda e: page.pop_dialog())]
                    ))
                    return
            if not encontrado:
                page.show_dialog(ft.AlertDialog(
                    title=ft.Text("Resultado de la búsqueda"),
                    content=ft.Text("No se encontró ningún producto con el ID proporcionado.", color="red"),
                    actions=[ft.TextButton("Cerrar", on_click=lambda e: page.pop_dialog())]
                ))
    
    # funcion para eliminar los productos
    def eliminar_los_produtos():
        actualizar_tabla()
        eliminar_id = id_eliminar.value.strip()
        eliminar_nombre = nombre_eliminar.value.strip()
        
        if eliminar_id == "" and eliminar_nombre == "":
            alerta = ft.AlertDialog(
                title=ft.Text("ERROR", color="red"),
                content=ft.Text("Por favor, ingrese un ID o un nombre para eliminar.", color="red"),
                alignment=ft.Alignment.CENTER,
                actions=[
                    ft.TextButton("Cerrar", on_click=lambda e: page.pop_dialog())
                ]
            )
            page.show_dialog(alerta)
            return
        elif eliminar_nombre:
            if eliminar_nombre not in inventario:
                alerta = ft.AlertDialog(
                    title=ft.Text("ERROR", color="red"),
                    content=ft.Text("No se encontró ningún producto con el NOMBRE proporcionado.", color="red"),
                    alignment=ft.Alignment.CENTER,
                    actions=[
                        ft.TextButton("Cerrar", on_click=lambda e: page.pop_dialog())
                    ]
                )
                page.show_dialog(alerta)
                return
            else:
                del inventario[eliminar_nombre]
                with open("inventario.json", "w") as archivo:
                    json.dump(inventario, archivo, indent=4)
                actualizar_tabla()
                alerta = ft.AlertDialog(
                    title=ft.Text("Exito", color="green"),
                    content=ft.Text("Producto eliminado con exito.", color="green"),
                    alignment=ft.Alignment.CENTER,
                    actions=[
                        ft.TextButton("Cerrar", on_click=lambda e: page.pop_dialog())
                    ]
                )  
                id_eliminar.value = ""
                nombre_eliminar.value = ""
                page.update()
                page.show_dialog(alerta)
                return
        if eliminar_id:
            encontrar = False
            for nombre, datos in inventario.items():
                if datos["ID"] == eliminar_id:
                    encontrar = True
                    del inventario[nombre]
                    with open("inventario.json", "w") as archivo:
                        json.dump(inventario, archivo, indent=4)
                    actualizar_tabla()
                    alerta = ft.AlertDialog(
                        title=ft.Text("Exito", color="green"),
                        content=ft.Text("Producto eliminado con exito.", color="green"),
                        alignment=ft.Alignment.CENTER,
                        actions=[
                            ft.TextButton("Cerrar", on_click=lambda e: page.pop_dialog())
                        ]
                    )
                    page.show_dialog(alerta)
                    return
            if not encontrar:
                alerta = ft.AlertDialog(
                    title=ft.Text("ERROR", color="red"),
                    content=ft.Text("No se encontro ningun producto con el ID proporcionado.", color="red"),
                    alignment=ft.Alignment.CENTER,
                    actions=[
                        ft.TextButton("Cerrar", on_click=lambda e: page.pop_dialog())
                    ]
                )
                page.show_dialog(alerta)
                return
        
           
    # funcion para mostrar el formulario y guadar los productos
    def formulario_entrada():
        formulario = ft.AlertDialog(
            title=ft.Text("Entrada de productos"),
            content=ft.Column(
                controls=[
                    ID_producto,
                    nombre_producto,
                    cantidad_producto,
                    precio_producto,
                    ft.Button("Guardar", on_click=guardar_producto)
                ]
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: page.pop_dialog())
            ]
        )
        page.show_dialog(formulario)
      
    # funcion para mostrar los productos en el inventario    
    def ver_productos():
        visualizar = ft.AlertDialog(
            title=ft.Text("productos en el inventario"),
            content=ft.Column(
                controls=[
                    ft.Text("Desea ver los productos en el inventario?", color="green", width=200),
                    ft.Button("Visualizar", on_click=ver_tabla)
                ]
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: page.pop_dialog())
            ]
        )
        page.show_dialog(visualizar)
        
        
    buscar_id = ft.TextField(label="ID del producto", color="green", border_color="blue", cursor_color="white", width=200)
    buscar_nombre = ft.TextField(label="Nombre del producto", color="green", border_color="blue", cursor_color="white", width=200)
    # funcion para buscar productos en el inventario
    def buscar_productos():
        buscar = ft.AlertDialog(
            title=ft.Text("Buscar producto"),
            content=ft.Column(
                controls=[
                    ft.Text("Ingrese el nombre del producto que desea buscar", color="green", width=200),
                    buscar_id,
                    buscar_nombre,
                    ft.Button("Buscar", on_click=buscar_los_productos)
                ]
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: page.pop_dialog())
            ]
        )
        page.show_dialog(buscar)
    
    id_eliminar = ft.TextField(label="ID del producto", color="green", border_color="blue", cursor_color="white", width=200)
    nombre_eliminar = ft.TextField(label="Nombre del producto", color="green", border_color="blue", cursor_color="white", width=200)
    def eliminar_producto():
        eliminar = ft.AlertDialog(
            title=ft.Text("Eliminar producto"),
            content=ft.Column(
                controls=[
                    ft.Text("Ingrese el nombre del producto que desea eliminar", color="green", width=200),
                    id_eliminar,
                    nombre_eliminar,
                    ft.Button("Eliminar", on_click=eliminar_los_produtos)
                ]
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: page.pop_dialog())
            ]
        )
        page.show_dialog(eliminar)


    # funcion para manejar las opciones del menu
    def manejar_opciones(e):
        opcion = entrada_opcion.value.strip()
        if opcion == "1":
            formulario_entrada()
        elif opcion == "2":
            ver_productos()
        elif opcion == "3":
            buscar_productos()
        elif opcion == "4":
            eliminar_producto()
        else:
            alerta = ft.AlertDialog(
                title=ft.Text("ERROR", color="red"),
                content=ft.Text("Opcion no valida, por favor elija una opcion del menu", color="red"),
                alignment=ft.Alignment.CENTER,
                actions=[
                    ft.TextButton("Cerrar", on_click=lambda e: page.pop_dialog())
                ]
            )
            page.show_dialog(alerta)
        entrada_opcion.value = ""
        page.update()
            
    # boton para aceptar la opcion del menu
    boton_aceptar = ft.Button("Aceptar", on_click=manejar_opciones)
    page.add(boton_aceptar)


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")