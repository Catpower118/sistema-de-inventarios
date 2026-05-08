import flet as ft
import json
import os

class DataBase:
    def __init__(self, page: ft.Page):
        self.page = page
        self.inventario = self.cargar_inventario()
        self.tabla_productos = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID", color="green")),
                ft.DataColumn(ft.Text("Nombre", color="green")),
                ft.DataColumn(ft.Text("Cantidad", color="green")),
                ft.DataColumn(ft.Text("Precio", color="green"))
            ],
            rows=[]
        )
    
        self.contenedor_tabla = ft.Container(
            content=ft.Column(
                controls=[self.tabla_productos],
            scroll="auto"),
            width=600,
            height=400,
            border=ft.border.all(1, "blue"),
            padding=10,
            margin=10,
            bgcolor="black"
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
    
    def cargar_inventario(self):
        if not os.path.exists("inventario.json") or os.path.getsize("inventario.json") == 0:
            return {}
        
        with open("inventario.json", "r") as archivo:
            return json.load(archivo) 
        