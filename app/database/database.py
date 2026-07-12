import flet as ft
import json
import os

class DataBase:
    def __init__(self, page: ft.Page):
        self.page = page
        # asignamos a la variable self.inventario la funcion cargar_inventario
        self.inventario = self.cargar_inventario()
        # declaramos la variable tabla_productos para mostrar los productos en una tabla
        self.tabla_productos = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID", color="green")),
                ft.DataColumn(ft.Text("Nombre", color="green")),
                ft.DataColumn(ft.Text("Cantidad", color="green")),
                ft.DataColumn(ft.Text("Precio", color="green"))
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
    
    # funcion para actualizar la tabla de productos
    def actualizar_tabla(self):
        self.tabla_productos.rows.clear()

        for nombre, datos in self.inventario.items():
            fila = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(datos["ID"], color="green")),
                    ft.DataCell(ft.Text(nombre, color="green")),
                    ft.DataCell(ft.Text(str(datos["Cantidad"]), color="green")),
                    ft.DataCell(ft.Text(str(datos["Precio"]), color="green"))
                ]
            )
            self.tabla_productos.rows.append(fila)

        self.page.update()
    
    # declaramos la funcion guardar_inventario para guardar los productos en el inventario
    def cargar_inventario(self):
        if not os.path.exists("inventario.json") or os.path.getsize("inventario.json") == 0:
            return {}
        
        with open("inventario.json", "r") as archivo:
            return json.load(archivo) 
        