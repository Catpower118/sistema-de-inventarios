import flet as ft
import config.conexion

class DataBase:
    def __init__(self, page: ft.Page):
        self.page = page
        # declaramos la variable tabla_productos para mostrar los productos en una tabla
        self.tabla_productos = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID", color="green")),
                ft.DataColumn(ft.Text("Nombre", color="green")),
                ft.DataColumn(ft.Text("Cantidad", color="green")),
                ft.DataColumn(ft.Text("Precio", color="green")),
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
    
    # funcion para actualizar la tabla de productos
    def actualizar_tabla(self):
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
    