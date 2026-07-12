import flet as ft         
import config.conexion

class Queries:
    def __init__(self,page: ft.Page ,qu):
        self.page = page
        self.qu = qu
        self.conn = config.conexion.conectar()
        self.cursor = self.conn.cursor()
        
    def guardar_producto(self, nombre, precio, cantidad, stock):
        
        sql = "INSERT INTO productos (nombre, precio, cantidad, stock) VALUES (%s, %s, %s, %s)"
        values = (nombre, precio, cantidad, stock)
        
        self.cursor.execute(sql, values)
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
        
    def buscar_producto(self, id_buscar):
        sql = "SELECT * FROM productos WHERE id = %s"
        values = (id_buscar,)
        
        self.cursor.execute(sql, values)
        resultado = self.cursor.fetchone()
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
            
    def cerrar(self):
        self.cursor.close()
        self.conn.close()