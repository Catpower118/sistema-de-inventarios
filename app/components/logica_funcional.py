import flet as ft         
import database.queries as qu
from utils.logger import Logger


def error_dialog(page, texto):
    alerta = ft.AlertDialog(
        title=ft.Text("ERROR", color="red"),
        content=ft.Text(texto, color="red"),
        actions=[
            ft.TextButton("Cerrar", on_click=lambda e: page.pop_dialog())
        ]
    )
    page.show_dialog(alerta)

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
                error_dialog(self.page, "Todos los campos son obligatorios, intente otra vez.")
                return

            if not nombre_val.replace(" ", "").isalpha():
                error_dialog(self.page, "El nombre del producto solo debe contener letras y espacios.")
                return
            if not cantidad_val_str.isdigit() or not stock_val_str.isdigit():
                error_dialog(self.page, "La cantidad y el stock deben ser números enteros.")
                return
            
            if precio_val_str.count('.') > 1:
                error_dialog(self.page, "El precio no puede contener más de un punto decimal.")
                return
            
            try:
                precio_val = float(precio_val_str)
                cantidad_val = int(cantidad_val_str)
                stock_val = int(stock_val_str)
            except ValueError:
                error_dialog(self.page, "La cantidad, el stock y el precio deben ser números válidos.")
                return
            
            if cantidad_val <= 0:
                error_dialog(self.page, "La cantidad debe ser un número positivo.")
                return
            
            if stock_val <= 0:
                error_dialog(self.page, "El stock debe ser un número positivo.")
                return
            
            if precio_val <= 0:
                error_dialog(self.page, "El precio debe ser un número positivo.")
                return
            
            self.query.guardar_producto(nombre_val, precio_val, cantidad_val, stock_val)
            self.db.actualizar_tabla()
            Logger.add_to_log("info", f"se anadio un nuevo producto: {nombre_val}")
               
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
        
    def ver_tabla_movimientos(self, e):
        self.db.actualizar_tabla_movimientos()
        self.tabla_movimientos = ft.AlertDialog(
            title=ft.Text("Movimientos en el inventario"),
            content=self.db.contenedor_tabla_movimientos,
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
            ]
        )
        self.page.show_dialog(self.tabla_movimientos)
        
    # funcion para buscar los productos en el inventario
    def buscar_los_productos(self, e):
        try:
            self.db.actualizar_tabla()
            producto_id = self.menu.buscar_id.value.strip()
        
            if not producto_id:
                error_dialog(self.page, "Por favor, ingrese un ID para buscar.")
                return
            if not producto_id.isdigit():
                error_dialog(self.page, "El ID debe ser un número válido.")
                return
        
            producto_id_int = int(producto_id)
        
            self.query.buscar_producto(producto_id_int)
            Logger.add_to_log("info", f"se hizo a busqueda del producto: {producto_id_int}")
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
                error_dialog(self.page, "Por favor, ingrese un ID para eliminar.")
                return
            if not eliminar_id.isdigit():
                error_dialog(self.page, "El ID debe ser un número válido.")
                return
        
            eliminar_id_int = int(eliminar_id)
        
            self.query.eliminar_producto(eliminar_id_int)
            self.db.actualizar_tabla()
            Logger.add_to_log("warn", f"se elimino del inventario el producto id: {eliminar_id_int}")
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
                error_dialog(self.page, "Todos los campos son obligatorios, intente otra vez.")
                return
            try:
                actualizar_id_int = int(actualizar_id)
                actualizar_cantidad_int = int(actualizar_cantidad)
            except ValueError:
                error_dialog(self.page, "El ID y la cantidad deben ser números válidos.")
                return

            if actualizar_tipo not in ["entrada", "salida"]:
                error_dialog(self.page, "El tipo de movimiento debe ser 'entrada' o 'salida'.")
                return
            
            if actualizar_id_int <= 0:
                error_dialog(self.page, "El ID debe ser un número positivo.")
                return
            
            if not self.query.validar_id_existe(actualizar_id_int):
                error_dialog(self.page, f"El ID {actualizar_id_int} no existe en la base de datos.")
                return
            
            if actualizar_tipo == "salida":
                stock_actual = self.query.validar_stock_actual(actualizar_id_int)
                if actualizar_cantidad_int > stock_actual:
                    error_dialog(self.page, f"No hay suficiente stock para realizar la salida. Stock actual: {stock_actual}.")
                    return
            
            self.query.editar_producto(actualizar_id_int, actualizar_tipo, actualizar_cantidad_int)
            self.db.actualizar_tabla()
            Logger.add_to_log("info", f"movimiento en el inventario tipo: {actualizar_tipo}, id: {actualizar_id_int}, cantidad: {actualizar_cantidad_int}")
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
            
