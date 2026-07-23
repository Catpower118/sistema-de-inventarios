import flet as ft         

# creamos la clase Menu para manejar las opciones del menu (frontend)
class MenuLogica:
    def __init__(self, page: ft.Page, logica):
        self.page = page             
        self.logica = logica
        self.titulo = ft.Text("Bienvenido al sistema de inventario", color="white", size=30)
            
        # Campos para la entrada de opciones del menu    
        self.opcion_entrada = ft.Text("Ingrese la opcion deseada:", color="white", size=20)    
        self.entrada = ft.TextField(label="Opcion", color="white", border_color="blue", cursor_color="white", width=200)
        self.entrada.on_submit = self.menu_opcion
        self.boton_entrada = ft.ElevatedButton("Aceptar", bgcolor="blue", color="white", on_click=self.menu_opcion)
        
        # Campos para la entrada de productos
        self.nombre_entrada = ft.TextField(label="Nombre del producto", color="green", border_color="blue", cursor_color="white", width=200)
        self.precio_entrada = ft.TextField(label="Precio del producto", color="green", border_color="blue", cursor_color="white", width=200)
        self.cantidad_entrada = ft.TextField(label="Cantidad del producto", color="green", border_color="blue", cursor_color="white", width=200)
        self.stock_entrada = ft.TextField(label="Stock del producto", color="green", border_color="blue", cursor_color="white", width=200)
        
        # Campos para la búsqueda de productos
        self.buscar_id = ft.TextField(label="ID del producto", color="green", border_color="blue", cursor_color="white", width=200)
    
        # Campos para eliminar productos
        self.id_eliminar = ft.TextField(label="ID del producto", color="green", border_color="blue", cursor_color="white", width=200)
        
        # campos para la edición de productos
        self.modificar_id = ft.TextField(label="ID del producto", color="green", border_color="blue", cursor_color="white", width=200)
        self.tipo  = ft.TextField(label="tipo (entrada/salida).", color="green", border_color="blue", cursor_color="white", width=200)
        self.modificar_cantidad = ft.TextField(label="Cantidad del producto", color="green", border_color="blue", cursor_color="white", width=200)
        
        
        # Lista de opciones del menu
        self.contenedor = ft.Container(
            content=ft.Column(
                controls=[ft.Text("1. Entrada de productos.", color="white", size=20)],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER
            ),
            bgcolor="#123446",
            border_radius=10,
            padding=10,
            height=150,
            width=300,
            animate_scale=ft.Animation(500, ft.AnimationCurve.EASE_IN_OUT),
            opacity=0.8
        )
        self.contenedor_2 = ft.Container(
            content=ft.Column(
                controls=[ft.Text("2. Ver productos.", color="white", size=20)],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER
            ),
            bgcolor="#123446",
            border_radius=10,
            padding=10,
            height=150,
            width=300,
            opacity=0.8
        )
        self.contenedor_3 = ft.Container(
            content=ft.Column(
                controls=[ft.Text("3. Buscar productos.", color="white", size=20)],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER
            ),
            bgcolor="#123446",
            border_radius=10,
            padding=10,
            height=150,
            width=300,
            opacity=0.8
        )
        self.contenedor_4 = ft.Container(
            content=ft.Column(
                controls=[ft.Text("4. Eliminar productos.", color="white", size=20)],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER
            ),
            bgcolor="#123446",
            border_radius=10,
            padding=10,
            height=150,
            width=300,
            opacity=0.8
        )
        # boton para aceptar la opción de edición
        self.boton_entrada_edicion = ft.Button("Aceptar", bgcolor="blue", color="white", on_click=self.menu_edicion)
        self.texto_entrada = ft.Text("Ingrese una opcion valida", color="white", size=20)
        self.entrada_edicion = ft.TextField(label="Opcion", color="white", border_color="blue", cursor_color="white", width=200)
        self.entrada_edicion.on_submit = self.menu_edicion
    
    # funcion para las opciones del menu principal
    def filas_opciones(self):
        return ft.Row(
            controls=[
                self.contenedor,
                self.contenedor_2,
                self.contenedor_3,
                self.contenedor_4
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        )
    
    # funcion para la fila de entrada de opciones del menu
    def fila_opcion(self):
        return ft.Row(
            controls=[
                self.opcion_entrada,
                self.entrada
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        )
    
    # funcion para mostrar el contenido de cada opción del menu
    def campos_entrada(self):
        return ft.Column(
            controls=[
                self.titulo,
                self.filas_opciones(),
                self.fila_opcion(),
                self.boton_entrada
            ],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    
    # funcion para guardar los productos
    def formulario_entrada(self):
        formulario = ft.AlertDialog(
            title=ft.Text("Entrada de productos", color="blue"),
            content=ft.Column(
                controls=[
                    self.nombre_entrada,
                    self.precio_entrada,
                    self.cantidad_entrada,
                    self.stock_entrada,
                    ft.Button("Guardar", on_click=self.logica.guardar_producto)
                ],
                spacing=10
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
            ]
        )
        self.page.show_dialog(formulario)
        self.page.update()
    
    # funcion para mostrar los productos en el inventario
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
                    ft.Text("Ingrese el ID del producto", color="green", width=200),
                    self.buscar_id,
                    ft.Button("Buscar", on_click=self.logica.buscar_los_productos)
                ]
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
            ]
        )
        self.page.show_dialog(buscar)
        
    # funcion para eliminar productos del inventario
    def eliminar_producto(self):
        eliminar = ft.AlertDialog(
            title=ft.Text("Eliminar producto"),
            content=ft.Column(
                controls=[
                    ft.Text("Ingrese el ID del producto que desea eliminar", color="green", width=200),
                    self.id_eliminar,
                    ft.Button("Eliminar", on_click=self.logica.eliminar_los_productos)
                ]
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
            ]
        )
        self.page.show_dialog(eliminar)
    
    # funcion para validar si el campo de entrada esta vacio
    def campo_vacio(self):
        alerta = ft.AlertDialog(
            title=ft.Text("ERROR", color="red"),
            content=ft.Text("El campo no puede estar vacio.", color="red"),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
            ]
        )
        self.page.show_dialog(alerta)
    
    #funcion principal para manejar las opciones del menu
    def menu_opcion(self, e):
        try:
            opcion = self.entrada.value
            if opcion == "":
                self.campo_vacio()
            elif opcion == "1":
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
        except Exception as ex:
            error_1 = ft.AlertDialog(
                title=ft.Text("ERROR", color="red"),
                content=ft.Text(f"Ocurrio un error: {str(ex)}", color="red"),
                actions=[
                    ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                ]
            )
            self.page.show_dialog(error_1)
        finally:
            self.entrada.value = ""
            self.page.update()
     
     # funcion para mostrar las opciones de edición   
    def opcion_edicion(self):
        contenedor_1 = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("1. Registar entrada o salida del producto.", color="white", size=20)
                ],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER
            ),
            bgcolor="#123446",
            border_radius=10,
            padding=10,
            height=150,
            width=500,
            opacity=0.8
        )
        return ft.Row(
            controls=[
                contenedor_1
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        )
    
    # funcion para la fila de entrada de opciones del menu
    def entradas_edicion(self):
        return ft.Row(
            controls=[
                self.texto_entrada,
                self.entrada_edicion
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER
        )
    
    # funcion para mostrar las opciones de edición
    def campos_edicion(self):
        return ft.Column(
            controls=[
                self.opcion_edicion(),
                self.entradas_edicion(),
                self.boton_entrada_edicion
            ],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    
    # funcion para modificar productos del inventario
    def modificar_producto(self):
        alerta = ft.AlertDialog(
            title=ft.Text("Entrada del producto"),
            content=ft.Column(
                controls=[
                    self.modificar_id,
                    self.tipo,
                    self.modificar_cantidad,
                    ft.Button("Actualizar", on_click=self.logica.actualizar_producto)
                ]
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
            ]
        )
        self.page.show_dialog(alerta)
        self.page.update()
    
    # funcion principal para manejar las opciones de edición del menu    
    def menu_edicion(self, e):
        try:
            opcion = self.entrada_edicion.value.strip()
            if opcion == "":
                self.campo_vacio()
            elif opcion == "1":
                self.modificar_producto()
            else:
                alerta = ft.AlertDialog(
                    title=ft.Text("ERROR", color="red"),
                    content=ft.Text("Opcion no valida. por favor, ingrese valores validos", color="red"),
                    actions=[
                        ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                    ]
                )
                self.page.show_dialog(alerta)
        except Exception as ex:
            error = ft.AlertDialog(
                title=ft.Text("ERROR", color="red"),
                content=ft.Text(f"Ocurrio un error: {str(ex)}", color="red"),
                actions=[
                    ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                ]
            )
            self.page.show_dialog(error)
        finally:
            self.entrada_edicion.value = ""
            self.page.update()
        
    # funcion para mostrar las opciones de edición del menu
    def pestanas_division(self):
        return  ft.SafeArea(
            expand=True,
            content=ft.Tabs(
                selected_index=0,
                length=3,
                expand=True,
                content=ft.Column(
                    expand=True,
                    controls=[
                        ft.TabBar(
                            tabs=[
                                ft.Tab(label="Menu", icon=ft.Icons.SETTINGS_SYSTEM_DAYDREAM),
                                ft.Tab(label="Edicion", icon=ft.Icons.SETTINGS),
                                ft.Tab(label="Stock", icon=ft.Icons.SETTINGS_SUGGEST),
                            ]
                        ),
                        ft.TabBarView(
                            expand=True,
                            controls=[
                                ft.Container(
                                    expand=True,
                                    alignment=ft.Alignment.CENTER,
                                    content=self.campos_entrada()
                                ),
                                ft.Container(
                                    expand=True,
                                    alignment=ft.Alignment.CENTER,
                                    content=self.campos_edicion()
                                ),
                                ft.Container(
                                    expand=True,
                                    alignment=ft.Alignment.CENTER,
                                    content=self.logica.stock_tabla()
                                ),
                            ]
                        )
                    ]
                )
            )
        )
        