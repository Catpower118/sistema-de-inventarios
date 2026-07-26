import flet as ft         
import database.queries as qu


class LogicaFuncional:
    def __init__(self, page: ft.Page, db):
        self.page = page
        self.db = db
        self.query = qu.Queries(page)
     
     # funcion para guardar los productos en el inventario   
    def guardar_producto(self, e):
        try:
            nombre_val = self.menu.nombre_entrada.value.strip()
            precio_val_str = self.menu.precio_entrada.value.strip()
            cantidad_val_str = self.menu.cantidad_entrada.value.strip()
            stock_val_str = self.menu.stock_entrada.value.strip()

            if not nombre_val or not cantidad_val_str or not precio_val_str or not stock_val_str:
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

            if not nombre_val.replace(" ", "").isalpha():
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
            if not cantidad_val_str.isdigit() or not stock_val_str.isdigit():
                alerta = ft.AlertDialog(
                    title=ft.Text("ERROR", color="red"),
                    content=ft.Text("La cantidad y el stock deben ser números enteros.", color="red"),
                    alignment=ft.Alignment.CENTER,
                    actions=[
                        ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                    ]
                )
                self.page.show_dialog(alerta)
                return
            
            if precio_val_str.count('.') > 1:
                alerta = ft.AlertDialog(
                    title=ft.Text("ERROR", color="red"),
                    content=ft.Text("El precio no puede contener más de un punto decimal.", color="red"),
                    alignment=ft.Alignment.CENTER,
                    actions=[
                        ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                    ]
                )
                self.page.show_dialog(alerta)
                return
            try:
                precio_val = float(precio_val_str)
                cantidad_val = int(cantidad_val_str)
                stock_val = int(stock_val_str)
            except ValueError:
                alerta = ft.AlertDialog(
                    title=ft.Text("ERROR", color="red"),
                    content=ft.Text("La cantidad, el stock y el precio deben ser números válidos.", color="red"),
                    alignment=ft.Alignment.CENTER,
                    actions=[
                        ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                    ]
                )
                self.page.show_dialog(alerta)
                return
            
            if cantidad_val <= 0:
                alerta = ft.AlertDialog(
                    title=ft.Text("ERROR", color="red"),
                    content=ft.Text("La cantidad debe ser un número positivo.", color="red"),
                    alignment=ft.Alignment.CENTER,
                    actions=[
                        ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                    ]
                )
                self.page.show_dialog(alerta)
                return
            
            if stock_val <= 0:
                alerta = ft.AlertDialog(
                    title=ft.Text("ERROR", color="red"),
                    content=ft.Text("El stock debe ser un número positivo.", color="red"),
                    alignment=ft.Alignment.CENTER,
                    actions=[
                        ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                    ]
                )
                self.page.show_dialog(alerta)
                return
            
            if precio_val <= 0:
                alerta = ft.AlertDialog(
                    title=ft.Text("ERROR", color="red"),
                    content=ft.Text("El precio debe ser un número positivo.", color="red"),
                    alignment=ft.Alignment.CENTER,
                    actions=[
                        ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                    ]
                )
                self.page.show_dialog(alerta)
                return
            
            self.query.guardar_producto(nombre_val, precio_val, cantidad_val, stock_val)
            self.db.actualizar_tabla()
            
        except Exception as e:
            mensaje_error = ft.AlertDialog(
                title=ft.Text("ERROR"),
                content=ft.Text(f"Error: {e}"),
                actions=[
                    ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                ]
            )
            self.page.show_dialog(mensaje_error)
        finally:
            self.menu.nombre_entrada.value = ""
            self.menu.precio_entrada.value = ""
            self.menu.cantidad_entrada.value = ""
            self.menu.stock_entrada.value = ""
            
            
            
            
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
        try:
            self.db.actualizar_tabla()
            producto_id = self.menu.buscar_id.value.strip()
        
            if not producto_id:
                alerta = ft.AlertDialog(
                    title=ft.Text("ERROR", color="red"),
                    content=ft.Text("Por favor, ingrese un ID para buscar.", color="red"),
                    alignment=ft.Alignment.CENTER,
                    actions=[
                        ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                    ]
                )
                self.page.show_dialog(alerta)
                self.page.update()
                return
            if not producto_id.isdigit():
                alerta = ft.AlertDialog(
                    title=ft.Text("ERROR", color="red"),
                    content=ft.Text("El ID debe ser un número entero.", color="red"),
                    alignment=ft.Alignment.CENTER,
                    actions=[
                        ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                    ]
                )
                self.page.show_dialog(alerta)
                self.page.update()
                return
        
            producto_id_int = int(producto_id)
        
            self.query.buscar_producto(producto_id_int)
        except Exception as e:
            alerta = ft.AlertDialog(
                title=ft.Text("ERROR", color="red"),
                content=ft.Text(f"Error al buscar producto: {e}"),
                actions=[
                    ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                ]
            )
            self.page.show_dialog(alerta)
            self.page.update()
        finally:
            self.menu.buscar_id.value = ""
            
                
    
    # funcion para eliminar productos del inventario
    def eliminar_los_productos(self, e):
        try:
            self.db.actualizar_tabla()
            eliminar_id = self.menu.id_eliminar.value.strip()
        
            if eliminar_id == "":
                alerta = ft.AlertDialog(
                    title=ft.Text("ERROR", color="red"),
                    content=ft.Text("Por favor, ingrese un ID para eliminar.", color="red"),
                    alignment=ft.Alignment.CENTER,
                    actions=[
                        ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                    ]
                )
                self.page.show_dialog(alerta)
                return
            if not eliminar_id.isdigit():
                alerta = ft.AlertDialog(
                    title=ft.Text("ERROR", color="red"),
                    content=ft.Text("El ID debe ser un numero valido"),
                    actions=[
                        ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                    ]
                )
                self.page.show_dialog(alerta)
                return
        
            eliminar_id_int = int(eliminar_id)
        
            self.query.eliminar_producto(eliminar_id_int)
            self.db.actualizar_tabla()
        except Exception as e:
            alerta = ft.AlertDialog(
                title=ft.Text("ERROR", color="red"),
                content=ft.Text(f"Ocurrio un error al eliminar el producto: {e}"),
                actions=[
                    ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                ]
            )
            self.page.show_dialog(alerta)
            self.page.update()
        finally:
            self.menu.id_eliminar.value = ""
    
    # funcion para ver la tabla        
    def stock_tabla(self):
        self.db.actualizar_tabla()
        return self.db.contenedor_tabla
    
    # funcion para actualizar producto
    def actualizar_producto(self, e):
        try:
            actualizar_id = self.menu.modificar_id.value.strip()
            actualizar_tipo = self.menu.tipo.value.strip().lower()
            actualizar_cantidad = self.menu.modificar_cantidad.value.strip()
            
            if not actualizar_id or not actualizar_tipo or not actualizar_cantidad:
                alerta = ft.AlertDialog(
                    title=ft.Text("ERROR", color="red"),
                    content=ft.Text("Todos los campos son obligatorios.", color="red"),
                    actions=[
                        ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                    ]
                )
                self.page.show_dialog(alerta)
                return
            try:
                actualizar_id_int = int(actualizar_id)
                actualizar_cantidad_int = int(actualizar_cantidad)
            except ValueError:
                alerta = ft.AlertDialog(
                    title=ft.Text("ERROR", color="red"),
                    content=ft.Text("Los campos ID y cantidad deben ser numeros enteros.", color="red"),
                    actions=[
                        ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                    ]
                ) 
                self.page.show_dialog(alerta)
                return

            if actualizar_tipo not in ["entrada", "salida"]:
                alerta = ft.AlertDialog(
                    title=ft.Text("ERROR", color="red"),
                    content=ft.Text("el tipo de movimiento debe ser 'entrada' o 'salida'."),
                    actions=[
                        ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                    ]
                )
                self.page.show_dialog(alerta)
                return
            
            if actualizar_id_int <= 0:
                alerta = ft.AlertDialog(
                    title=ft.Text("ERROR", color="red"),
                    content=ft.Text("El ID del producto debe ser un valor positivo.", color="red"),
                    actions=[
                        ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                    ]
                )
                self.page.show_dialog(alerta)
                return
            
            if not self.query.validar_id_existe(actualizar_id_int):
                alerta = ft.AlertDialog(
                    title=ft.Text("ERROR", color="red"),
                    content=ft.Text("El ID del producto no existe.", color="red"),
                    actions=[
                        ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                    ]
                )
                self.page.show_dialog(alerta)
                return
            
            if actualizar_tipo == "salida":
                stock_actual = self.query.validar_stock_actual(actualizar_id_int)
                if actualizar_cantidad_int > stock_actual:
                    alerta = ft.AlertDialog(
                        title=ft.Text("ERROR", color="red"),
                        content=ft.Text(f"No hay suficiente stock. stock actual {stock_actual}."),
                        actions=[
                            ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                        ]
                    )
                    self.page.show_dialog(alerta)
                    return
            
            self.query.editar_producto(actualizar_id_int, actualizar_tipo, actualizar_cantidad_int)
            self.db.actualizar_tabla()
        except Exception as e:
            mesage_error = ft.AlertDialog(
                title=ft.Text("ERROR: 4000", color="red"),
                content=ft.Text(f"Ocurrio un error tipo. {e}"),
                actions=[
                    ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                ]
            )
            self.page.show_dialog(mesage_error)
        finally:
            self.menu.modificar_id.value = ""
            self.menu.tipo.value = ""
            self.menu.modificar_cantidad.value = ""
            
