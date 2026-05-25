import flet as ft         
import json


class LogicaFuncional:
    def __init__(self, page: ft.Page, db):
        self.page = page
        self.db = db
     
     # funcion para guardar los productos en el inventario   
    def guardar_producto(self, e):
        try:
            ID_val = self.menu.id_entrada.value.strip()
            nombre_val = self.menu.nombre_entrada.value.strip()
            cantidad_val = int(self.menu.cantidad_entrada.value.strip())
            precio_val = float(self.menu.precio_entrada.value.strip())

            if not ID_val or not nombre_val:
                alerta = ft.AlertDialog(
                    title=ft.Text("ERROR", color="red"),
                    content=ft.Text("Todos los campos son obligatorios. Por favor, complete todos los campos.", color="red"),
                    alignment=ft.Alignment.CENTER,
                    actions=[
                        ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                    ]
                )
                self.page.show_dialog(alerta)
                return

            elif not nombre_val.isalpha():
                alerta = ft.AlertDialog(
                    title=ft.Text("ERROR", color="red"),
                    content=ft.Text("El nombre del producto no puede contener números o caracteres especiales.", color="red"),
                    alignment=ft.Alignment.CENTER,
                    actions=[
                        ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                    ]
                )
                self.page.show_dialog(alerta)
                return
            if nombre_val in self.db.inventario:
                alerta = ft.AlertDialog(
                    title=ft.Text("ERROR", color="red"),
                    content=ft.Text("El nombre ya existe.", color="red"),
                    alignment=ft.Alignment.CENTER,
                    actions=[
                        ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                    ]
                )
                self.page.show_dialog(alerta)
                return
            
            for nombre, datos in self.db.inventario.items():
                if datos["ID"] == ID_val:
                    alerta = ft.AlertDialog(
                        title=ft.Text("ERROR", color="red"),
                        content=ft.Text("El ID ya existe.", color="red"),
                        alignment=ft.Alignment.CENTER,
                        actions=[
                            ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                        ]
                    )
                    self.page.show_dialog(alerta)
                    return 
            
            self.db.inventario[nombre_val] = {
                "ID": ID_val,
                "Cantidad": cantidad_val,
                "Precio": precio_val
            }
            with open("inventario.json", "w") as archivo:
                json.dump(self.db.inventario, archivo, indent=4)
            self.db.actualizar_tabla()    
                
            self.menu.id_entrada.value = ""
            self.menu.nombre_entrada.value = ""
            self.menu.cantidad_entrada.value = ""
            self.menu.precio_entrada.value = ""
            self.menu.id_entrada.focus()
            self.page.update()
                
            self.page.show_dialog(ft.AlertDialog(
                title=ft.Text("Éxito", color="green"),
                content=ft.Text("Producto guardado correctamente.", color="green"),
                alignment=ft.Alignment.CENTER,
                actions=[
                    ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                ]
            ))
        except ValueError:
            alerta = ft.AlertDialog(
                title=ft.Text("ERROR", color="red"),
                content=ft.Text("los campos deben ser válidos.", color="red"),
                alignment=ft.Alignment.CENTER,
                actions=[
                    ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                ]
            )
            self.page.show_dialog(alerta)
            
    # funcion para visualizar los productos en el inventario  
    def ver_tabla(self, e):
        self.db.actualizar_tabla()
        self.tabla = ft.AlertDialog(
            title=ft.Text("Productos en el inventario"),
            content=self.db.contenedor_tabla,
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
            ]
        )
        self.page.show_dialog(self.tabla)
        
        
    # funcion para buscar los productos en el inventario
    def buscar_los_productos(self, e):
        self.db.actualizar_tabla()
        producto_id = self.menu.buscar_id.value.strip()
        producto_nombre = self.menu.buscar_nombre.value.strip()
        
        if producto_id == "" and producto_nombre == "":
            alerta = ft.AlertDialog(
                title=ft.Text("ERROR", color="red"),
                content=ft.Text("Por favor, ingrese un ID o un nombre para buscar.", color="red"),
                alignment=ft.Alignment.CENTER,
                actions=[
                    ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                ]
            )
            self.page.show_dialog(alerta)
            return
        if producto_nombre:
            if producto_nombre not in self.db.inventario:
                alerta = ft.AlertDialog(
                    title=ft.Text("ERROR", color="red"),
                    content=ft.Text("No se encontró ningún producto con el NOMBRE proporcionado.", color="red"),
                    alignment=ft.Alignment.CENTER,
                    actions=[
                        ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                    ]
                )
                self.menu.buscar_id.value = ""
                self.menu.buscar_nombre.value = ""
                self.page.show_dialog(alerta)
                self.page.update()
                return
            else:
                datos = self.db.inventario[producto_nombre]
                self.page.show_dialog(ft.AlertDialog(
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
                        ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                    ]
                ))
                self.menu.buscar_id.value = ""
                self.menu.buscar_nombre.value = ""
                self.page.update()
                return
                
        elif producto_id:
            encontrado = False
            for nombre, datos in self.db.inventario.items():
                if datos["ID"] == producto_id:
                    encontrado = True
                    self.page.show_dialog(ft.AlertDialog(
                        title=ft.Text("Resultado de la búsqueda"),
                        content=ft.Column(
                            controls=[
                                ft.Text(f"ID: {datos['ID']}", color="green"),
                                ft.Text(f"Nombre: {nombre}", color="green"),
                                ft.Text(f"Cantidad: {datos['Cantidad']}", color="green"),
                                ft.Text(f"Precio: {datos['Precio']}", color="green")
                            ]
                        ),
                        actions=[ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())]
                    ))
                    self.menu.buscar_id.value = ""
                    self.menu.buscar_nombre.value = ""
                    self.page.update()
                    return
            if not encontrado:
                self.page.show_dialog(ft.AlertDialog(
                    title=ft.Text("Resultado de la búsqueda"),
                    content=ft.Text("No se encontró ningún producto con el ID proporcionado.", color="red"),
                    actions=[ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())]
                ))
                self.menu.buscar_id.value = ""
                self.menu.buscar_nombre.value = ""
                self.page.update()
                return
                
    
    # funcion para eliminar productos del inventario
    def eliminar_los_productos(self, e):
        self.db.actualizar_tabla()
        eliminar_id = self.menu.id_eliminar.value.strip()
        eliminar_nombre = self.menu.nombre_eliminar.value.strip()
        
        if eliminar_id == "" and eliminar_nombre == "":
            alerta = ft.AlertDialog(
                title=ft.Text("ERROR", color="red"),
                content=ft.Text("Por favor, ingrese un ID o un nombre para eliminar.", color="red"),
                alignment=ft.Alignment.CENTER,
                actions=[
                    ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                ]
            )
            self.page.show_dialog(alerta)
            return
        elif eliminar_nombre:
            if eliminar_nombre not in self.db.inventario:
                alerta = ft.AlertDialog(
                    title=ft.Text("ERROR", color="red"),
                    content=ft.Text("No se encontró ningún producto con el NOMBRE proporcionado.", color="red"),
                    alignment=ft.Alignment.CENTER,
                    actions=[
                        ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                    ]
                )
                self.menu.id_eliminar.value = ""
                self.menu.nombre_eliminar.value = ""
                self.page.show_dialog(alerta)
                self.page.update()
                return
            else:
                del self.db.inventario[eliminar_nombre]
                with open("inventario.json", "w") as archivo:
                    json.dump(self.db.inventario, archivo, indent=4)
                self.db.actualizar_tabla()
                alerta = ft.AlertDialog(
                    title=ft.Text("Exito", color="green"),
                    content=ft.Text("Producto eliminado con exito.", color="green"),
                    alignment=ft.Alignment.CENTER,
                    actions=[
                        ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                    ]
                )  
                self.menu.id_eliminar.value = ""
                self.menu.nombre_eliminar.value = ""
                self.page.update()
                self.page.show_dialog(alerta)
                return
        if eliminar_id:
            encontrar = False
            for nombre, datos in self.db.inventario.items():
                if datos["ID"] == eliminar_id:
                    encontrar = True
                    del self.db.inventario[nombre]
                    with open("inventario.json", "w") as archivo:
                        json.dump(self.db.inventario, archivo, indent=4)
                    self.db.actualizar_tabla()
                    alerta = ft.AlertDialog(
                        title=ft.Text("Exito", color="green"),
                        content=ft.Text("Producto eliminado con exito.", color="green"),
                        alignment=ft.Alignment.CENTER,
                        actions=[
                            ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                        ]
                    )
                    self.menu.id_eliminar.value = ""
                    self.menu.nombre_eliminar.value = ""
                    self.page.show_dialog(alerta)
                    self.page.update()
                    return
            if not encontrar:
                alerta = ft.AlertDialog(
                    title=ft.Text("ERROR", color="red"),
                    content=ft.Text("No se encontro ningun producto con el ID proporcionado.", color="red"),
                    alignment=ft.Alignment.CENTER,
                    actions=[
                        ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                    ]
                )
                self.menu.id_eliminar.value = ""
                self.menu.nombre_eliminar.value = ""
                self.page.show_dialog(alerta)
                self.page.update()
                return
    