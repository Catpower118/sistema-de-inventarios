import flet as ft   
import view.menu_logica as menus  
import components.logica_funcional as lg
import database.database as datos
from config.login import Login

def cargar_ventana_principal(page: ft.Page):
    
    db = datos.DataBase(page)
    logica = lg.LogicaFuncional(page, db)
    menu_interfaz = menus.MenuLogica(page, logica)
    
    logica.menu = menu_interfaz
    page.controls.clear()
    
    page.add(
    ft.Stack(
        expand=True,
        controls=[
            ft.Container(
                expand=True,
                image=ft.DecorationImage(
                    src="fondo.jpg",
                    fit="cover",
                    opacity=0.6
                )
            ),
            ft.Container(
                expand=True,
                bgcolor="transparent",
                content=menu_interfaz.pestanas_division()
            )
        ]
    ))

def main(page: ft.Page):
    page.title = "Sistema de Inventario"
    page.padding = 0
    page.bgcolor = "#000000"
    page.window.icon = "portada_sistema.ico"
    
    login = Login(page, lambda: cargar_ventana_principal(page))
    login.mostrar_dialogo()


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
    
    