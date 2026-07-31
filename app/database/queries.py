import flet as ft         
import config.conexion
from mysql.connector import Error
from utils.logger import Logger
import traceback

class Queries:
    def __init__(self,page: ft.Page):
        self.page = page
        self.conn = config.conexion.conectar()
        
    def guardar_producto(self, nombre, precio, cantidad, stock):
        cursor = None
        try:
            cursor = self.conn.cursor()
        
            sql = "INSERT INTO productos (nombre, precio, cantidad, stock) VALUES (%s, %s, %s, %s)"
            values = (nombre, precio, cantidad, stock)
        
            cursor.execute(sql, values)
            self.conn.commit()
            alerta = ft.AlertDialog(
                title=ft.Text("Producto Guardado"),
                content=ft.Text(f"El producto {nombre} ha sido guardado exitosamente."),
                actions=[
                    ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                ]
            )
            self.page.show_dialog(alerta)
            self.page.update()
        except Error as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            sql_error = ft.AlertDialog(
                title=ft.Text("ERROR SQL", color="red"),
                content=ft.Text("Error al guardar producto."),
                actions=[
                    ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                ]
            )
            self.page.show_dialog(sql_error)
            self.page.update()
        finally:
            if cursor is not None:
                cursor.close()
        
    def buscar_producto(self, id_buscar):
        cursor = None
        try:
            cursor = self.conn.cursor()
            sql = "SELECT * FROM productos WHERE id = %s"
            values = (id_buscar,)
        
            cursor.execute(sql, values)
            resultado = cursor.fetchone()
            if resultado:
                visualizar = ft.AlertDialog(
                    title=ft.Text("Producto Encontrado"),
                    content=ft.Column([
                        ft.Text(f"ID: {resultado[0]}"),
                        ft.Text(f"Nombre: {resultado[1]}"),
                        ft.Text(f"Precio: {resultado[2]}"),
                        ft.Text(f"Cantidad: {resultado[3]}"),
                        ft.Text(f"Stock: {resultado[4]}")
                    ]),
                    actions=[
                        ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                    ]
                )
                self.page.show_dialog(visualizar)
                self.page.update()
            else:
                alerta = ft.AlertDialog(
                    title=ft.Text("Producto No Encontrado"),
                    content=ft.Text("El producto no fue encontrado."),
                    actions=[
                        ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                    ]
                )
                self.page.show_dialog(alerta)
                self.page.update()
            self.page.update()
        except Error as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            sql_error = ft.AlertDialog(
                title=ft.Text("ERROR SQL", color="red"),
                content=ft.Text("Error al buscar producto."),
                actions=[
                    ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                ]
            )
            self.page.show_dialog(sql_error)
            self.page.update()
        finally:
            if cursor is not None:
                cursor.close()
            
            
    def eliminar_producto(self, id_eliminar):
        cursor = None
        try:
            cursor = self.conn.cursor()
            
            sql_mov = "DELETE FROM movimientos WHERE producto_id = %s"
            cursor.execute(sql_mov, (id_eliminar,))
            
            sql = "DELETE FROM productos WHERE id = %s"
            values = (id_eliminar,)
        
            cursor.execute(sql, values)
            self.conn.commit()
        
            if cursor.rowcount > 0:
                alerta = ft.AlertDialog(
                    title=ft.Text("Producto Eliminado"),
                    content=ft.Text(f"El producto con ID {id_eliminar} ha sido eliminado exitosamente."),
                    actions=[
                        ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                    ]
                )
                self.page.show_dialog(alerta)
            else:
                alerta = ft.AlertDialog(
                    title=ft.Text("ERROR", color="red"),
                    content=ft.Text(f"El ID {id_eliminar} no existe."),
                    actions=[
                        ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                    ]
                )
                self.page.show_dialog(alerta)
            self.page.update()
        except Error as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            sql_error = ft.AlertDialog(
                title=ft.Text("ERROR SQL", color="red"),
                content=ft.Text("Error al eliminar producto."),
                actions=[
                    ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                ]
            )
            self.page.show_dialog(sql_error)
            self.page.update()
        finally:
            if cursor is not None:
                cursor.close()
        
    def editar_producto(self, id_editar, tipo, cantidad):
        cursor = None
        try:
            cursor = self.conn.cursor()

            #if tipo == "entrada":
             #   sql_stock = "UPDATE productos SET stock = stock + %s WHERE id = %s"
            #else:
              #  sql_stock = "UPDATE productos SET stock = stock - %s WHERE id = %s"
            #cursor.execute(sql_stock, (cantidad, id_editar))
            if tipo == "entrada":
                sql_cantidad = """
                UPDATE productos
                SET cantidad = cantidad + %s
                WHERE id = %s
                """
            else:
                sql_cantidad = """
                UPDATE productos
                SET cantidad = cantidad - %s
                WHERE id = %s
                """
            cursor.execute(sql_cantidad, (cantidad, id_editar))

            sql_mov = """
            INSERT INTO movimientos (producto_id, tipo, cantidad) 
            VALUES (%s, %s, %s)"""
            cursor.execute(sql_mov, (id_editar, tipo, cantidad))

            self.conn.commit()
            alerta = ft.AlertDialog(
                title=ft.Text("Movimiento Registrado"),
                content=ft.Text(f"El movimiento {tipo} ha sido registrado exitosamente."),
                actions=[
                    ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                ]
            )
            self.page.show_dialog(alerta)
            self.page.update()
        except Error as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            sql_error = ft.AlertDialog(
                title=ft.Text("ERROR SQL", color="red"),
                content=ft.Text("Error al editar producto."),
                actions=[
                    ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                ]
            )
            self.page.show_dialog(sql_error)
            self.page.update()
        finally:
            if cursor is not None:
                cursor.close()
        
    def validar_id_existe(self, id_validar):
        cursor = None
        try:
            cursor = self.conn.cursor()
        
            sql = "SELECT id FROM productos WHERE id = %s"
            values = (id_validar,)
            cursor.execute(sql, values)
            resultado = cursor.fetchone()
            return resultado is not None
        except Error as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            sql_error = ft.AlertDialog(
                title=ft.Text("ERROR SQL", color="red"),
                content=ft.Text("Error al validar ID del producto."),
                actions=[
                    ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                ]
            )
            self.page.show_dialog(sql_error)
            self.page.update()
            return False
        finally:
            if cursor is not None:
                cursor.close()
    
    def validar_stock_actual(self, id_validar):
        cursor = None
        try:
            cursor = self.conn.cursor()
            sql = "SELECT stock FROM productos WHERE id = %s"
            values = (id_validar,)
        
            cursor.execute(sql, values)
            resultado = cursor.fetchone()
            if resultado:
                return resultado[0]
            else:
                return None
        except Error as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            sql_error = ft.AlertDialog(
                title=ft.Text("ERROR SQL", color="red"),
                content=ft.Text("Error al validar stock del producto."),
                actions=[
                    ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                ]
            )
            self.page.show_dialog(sql_error)
            self.page.update()
            return 0
        finally:
            if cursor is not None:
                cursor.close()
        
