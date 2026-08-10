import flet as ft         
import config.conexion
from mysql.connector import Error
from utils.logger import Logger
import traceback

def error_sql(page, texto):
    alerta = ft.AlertDialog(
        title=ft.Text("ERROR SQL", color="red"),
        content=ft.Text(texto, color="red"),
        actions=[
            ft.TextButton("Cerrar", on_click=lambda e: page.pop_dialog())
        ]
    )
    page.show_dialog(alerta)

def dialog_exit(page, texto, texto_2):
    alerta = ft.AlertDialog(
        title=ft.Text(texto, color="green"),
        content=ft.Text(texto_2, color="green"),
        actions=[
            ft.TextButton("Cerrar", on_click=lambda e: page.pop_dialog())
        ]
    )
    page.show_dialog(alerta)

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
            dialog_exit(self.page, "Producto Guardado", f"El producto {nombre} ha sido guardado exitosamente.")
        except Error as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            error_sql(self.page, "Error al guardar producto.")
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
                dialog_exit(self.page, "Producto No Encontrado", f"No se encontró ningún producto con ID {id_buscar}.")
        except Error as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            error_sql(self.page, "Error al buscar producto.")
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
                dialog_exit(self.page, "Producto Eliminado", f"El producto con ID {id_eliminar} ha sido eliminado exitosamente.")
            else:
                dialog_exit(self.page, "Producto No Encontrado", f"No se encontró ningún producto con ID {id_eliminar}.")
        except Error as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            error_sql(self.page, "Error al eliminar producto.")
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
            dialog_exit(self.page, "Producto Editado", f"El producto con ID {id_editar} ha sido editado exitosamente.")
        except Error as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            error_sql(self.page, "Error al editar producto.")
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
            error_sql(self.page, "Error al validar ID del producto.")
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
            error_sql(self.page, "Error al validar stock del producto.")
            return 0
        finally:
            if cursor is not None:
                cursor.close()
        
