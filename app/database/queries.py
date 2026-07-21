import flet as ft         
import config.conexion

class Queries:
    def __init__(self,page: ft.Page):
        self.page = page
        self.conn = config.conexion.conectar()
        
    def guardar_producto(self, nombre, precio, cantidad, stock):
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
        cursor.close()
        self.page.update()
        
    def buscar_producto(self, id_buscar):
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
        cursor.close()
        self.page.update()
            
    def eliminar_producto(self, id_eliminar):
        cursor = self.conn.cursor()
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
        cursor.close()
        self.page.update()
        
    def editar_producto(self, id_editar, tipo, cantidad):
        cursor = self.conn.cursor()

        if tipo == "entrada":
            sql_stock = "UPDATE productos SET stock = stock + %s WHERE id = %s"
        else:
            sql_stock = "UPDATE productos SET stock = stock - %s WHERE id = %s"
        cursor.execute(sql_stock, (cantidad, id_editar))

        sql_mov = """
        INSERT INTO movimientos (id_producto, tipo_movimiento, cantidad) 
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
        cursor.close()
        self.page.update()
        
    def validar_id_existe(self, id_validar):
        cursor = self.conn.cursor()
        
        sql = "SELECT id FROM productos WHERE id = %s"
        values = (id_validar,)
        cursor.execute(sql, values)
        resultado = cursor.fetchone()
        return resultado is not None
    
    def validar_stock_actual(self, id_validar):
        cursor = self.conn.cursor()
        sql = "SELECT stock FROM productos WHERE id = %s"
        values = (id_validar,)
        
        cursor.execute(sql, values)
        resultado = cursor.fetchone()
        if resultado:
            return resultado[0]
        else:
            return None
        
