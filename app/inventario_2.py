import flet as ft   
import menu_logica as menus  
import logica_funcional as lg
import database as datos

def main(page: ft.Page):
    page.title = "Sistema de Inventario"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "black"
    page.window.icon = "portada_sistema.ico"
    
    db = datos.DataBase(page)
    logica = lg.LogicaFuncional(page, db)
    menu_interfaz = menus.MenuLogica(page, logica)

    logica.menu = menu_interfaz
    page.add(menu_interfaz.campos_entrada())


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")