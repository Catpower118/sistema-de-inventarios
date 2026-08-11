import flet as ft
import config.conexion
from utils.logger import Logger
from mysql.connector import Error
import traceback

class DataBase:
    def __init__(self, page: ft.Page):
        self.page = page
        # declaramos la variable tabla_productos para mostrar los productos en una tabla
        self.tabla_productos = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID", color="green")),
                ft.DataColumn(ft.Text("Nombre", color="green")),
                ft.DataColumn(ft.Text("precio", color="green")),
                ft.DataColumn(ft.Text("cantidad", color="green")),
                ft.DataColumn(ft.Text("Stock", color="green"))
            ],
            rows=[]
        )
        self.tabla_productos.expand = True
        # creamos el contenedor para mostrar la tabla de productos
        self.contenedor_tabla = ft.Container(
            content=ft.Column(
                controls=[self.tabla_productos],
                scroll="auto",
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.START,
                expand=True,
                scroll_interval=20
            ),
            width=600,
            height=400,
            border=ft.border.all(1, "blue"),
            padding=10,
            margin=10,
            bgcolor="black",
            border_radius=10
        )
        self.tabla_movimientos = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID", color="green")),
                ft.DataColumn(ft.Text("producto_id", color="green")),
                ft.DataColumn(ft.Text("tipo", color="green")),
                ft.DataColumn(ft.Text("cantidad", color="green")),
                ft.DataColumn(ft.Text("fecha", color="green"))
            ],
            rows=[]
        )
        self.tabla_movimientos.expand = True
        self.contenedor_tabla_movimientos = ft.Container(
            content=ft.Column(
                controls=[self.tabla_movimientos],
                scroll="auto",
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.START,
                expand=True,
                scroll_interval=20
            ),
            width=600,
            height=400,
            border=ft.border.all(1, "blue"),
            padding=10,
            margin=10,
            bgcolor="black",
            border_radius=10
        )
    
    # funcion para actualizar la tabla de productos
    def actualizar_tabla(self):
        cursor = None
        conn = None
        try:
            conn = config.conexion.conectar()
            cursor = conn.cursor()
            self.tabla_productos.rows.clear()
            cursor.execute("SELECT * FROM productos")
            productos = cursor.fetchall()

            for producto in productos:
                fila = ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(producto[0]), color="green")),
                        ft.DataCell(ft.Text(producto[1], color="green")),
                        ft.DataCell(ft.Text(str(producto[2]), color="green")),
                        ft.DataCell(ft.Text(str(producto[3]), color="green")),
                        ft.DataCell(ft.Text(str(producto[4]), color="green"))
                    ]
                )
                self.tabla_productos.rows.append(fila)

            cursor.close()
            conn.close()
            self.page.update()
            
        except Error as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            sql_error = ft.AlertDialog(
                title=ft.Text("ERROR SQL", color="red"),
                content=ft.Text("Error de MySQL."),
                actions=[
                    ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                ]
            )
            self.page.show_dialog(sql_error)
            self.page.update()
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()
    
    def actualizar_tabla_movimientos(self):
        cursor = None
        conn = None
        try:
            conn = config.conexion.conectar()
            cursor = conn.cursor()
            self.tabla_movimientos.rows.clear()
            cursor.execute("SELECT * FROM movimientos")
            movimientos = cursor.fetchall()

            for movimiento in movimientos:
                fila = ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(movimiento[0]), color="green")),
                        ft.DataCell(ft.Text(str(movimiento[1]), color="green")),
                        ft.DataCell(ft.Text(movimiento[2], color="green")),
                        ft.DataCell(ft.Text(str(movimiento[3]), color="green")),
                        ft.DataCell(ft.Text(str(movimiento[4]), color="green"))
                    ]
                )
                self.tabla_movimientos.rows.append(fila)

            cursor.close()
            conn.close()
            self.page.update()
            
        except Error as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            sql_error = ft.AlertDialog(
                title=ft.Text("ERROR SQL", color="red"),
                content=ft.Text("Error de MySQL."),
                actions=[
                    ft.TextButton("Cerrar", on_click=lambda e: self.page.pop_dialog())
                ]
            )
            self.page.show_dialog(sql_error)
            self.page.update()
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()
                
    