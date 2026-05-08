import flet as ft         

class MenuLogica:
    def __init__(self, page: ft.Page, logica):
        self.page = page             
        self.logica = logica
        self.titulo = ft.Text("Bienvenido al sistema de inventario", color="green", size=30)
            
        self.opcion_entrada = ft.Text("Ingrese la opcion deseada:", color="green", size=20)    
        self.entrada = ft.TextField(label="Opcion", color="green", border_color="blue", cursor_color="white", width=200)
        self.boton_entrada = ft.ElevatedButton("Aceptar", bgcolor="blue", color="white", on_click=self.menu_opcion)
        
        # Campos para la entrada de productos
        self.id_entrada = ft.TextField(label="ID del producto", color="green", border_color="blue", cursor_color="white", width=200)
        self.nombre_entrada = ft.TextField(label="Nombre del producto", color="green", border_color="blue", cursor_color="white", width=200)
        self.cantidad_entrada = ft.TextField(label="Cantidad del producto", color="green", border_color="blue", cursor_color="white", width=200)
        self.precio_entrada = ft.TextField(label="Precio del producto", color="green", border_color="blue", cursor_color="white", width=200)
        
        # Campos para la búsqueda de productos
        self.buscar_id = ft.TextField(label="ID del producto", color="green", border_color="blue", cursor_color="white", width=200)
        self.buscar_nombre = ft.TextField(label="Nombre del producto", color="green", border_color="blue", cursor_color="white", width=200)
    

        self.id_eliminar = ft.TextField(label="ID del producto", color="green", border_color="blue", cursor_color="white", width=200)
        self.nombre_eliminar = ft.TextField(label="Nombre del producto", color="green", border_color="blue", cursor_color="white", width=200)
        
        self.campos = [
            "1. Entrada de productos.",
            "2. Ver productos.",
            "3. Buscar productos.",
            "4. Eliminar productos."
        ]
        
    def fila_opcion(self):
        return ft.Row(
            controls=[
                self.opcion_entrada,
                self.entrada
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        )
        
    def campos_entrada(self):
        lista_opciones = [
            ft.Text(campo, color="green", size=20)
            for campo in self.campos
        ]
        return ft.Column(
            controls=[
                self.titulo,
                *lista_opciones,
                self.fila_opcion(),
                self.boton_entrada
            ],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def formulario_entrada(self):
        formulario = ft.AlertDialog(
            title=ft.Text("Entrada de productos", color="blue"),
            content=ft.Column(
                controls=[
                    self.id_entrada,
                    self.nombre_entrada,
                    self.cantidad_entrada,
                    self.precio_entrada,
                    ft.Button("Guardar", on_click=self.logica.guardar_producto)
                ],
                spacing=10
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
            ]
        )
        self.page.show_dialog(formulario)
        
   
    def ver_productos(self):
        visualizar = ft.AlertDialog(
            title=ft.Text("productos en el inventario"),
            content=ft.Column(
                controls=[
                    ft.Text("Desea ver los productos en el inventario?", color="green", width=200),
                    ft.Button("Visualizar", on_click=self.logica.ver_tabla)
                ]
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
            ]
        )
        self.page.show_dialog(visualizar)
        
    # funcion para buscar productos en el inventario
    def buscar_productos(self):
        buscar = ft.AlertDialog(
            title=ft.Text("Buscar producto"),
            content=ft.Column(
                controls=[
                    ft.Text("Ingrese el ID o nombre del producto", color="green", width=200),
                    self.buscar_id,
                    self.buscar_nombre,
                    ft.Button("Buscar", on_click=self.logica.buscar_los_productos)
                ]
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
            ]
        )
        self.page.show_dialog(buscar)
        
    
    def eliminar_producto(self):
        eliminar = ft.AlertDialog(
            title=ft.Text("Eliminar producto"),
            content=ft.Column(
                controls=[
                    ft.Text("Ingrese el nombre del producto que desea eliminar", color="green", width=200),
                    self.id_eliminar,
                    self.nombre_eliminar,
                    ft.Button("Eliminar", on_click=self.logica.eliminar_los_productos)
                ]
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
            ]
        )
        self.page.show_dialog(eliminar)
        
    
    def menu_opcion(self, e):
        opcion = self.entrada.value
        if opcion == "1":
            self.formulario_entrada()
        elif opcion == "2":
            self.ver_productos()
        elif opcion == "3":
            self.buscar_productos()
        elif opcion == "4":
            self.eliminar_producto()
        else:
            alerta = ft.AlertDialog(
                title=ft.Text("ERROR", color="red"),
                content=ft.Text("Opcion no valida. por favor, ingrese valores validos", color="red"),
                actions=[
                    ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                ]
            )
            self.page.show_dialog(alerta)
        self.entrada.value = ""
        self.page.update()
        