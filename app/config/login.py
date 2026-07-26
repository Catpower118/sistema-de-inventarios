import flet as ft   
from config.conexion import conectar 

class Login:
    def __init__(self, page: ft.Page, callback_exito):
        self.page = page   
        self.callback_exito = callback_exito
        
        # creamos las entradas para el conector
        self.host = ft.TextField(label="Host", width=300)
        self.user = ft.TextField(label="Usuario", width=300)
        self.password = ft.TextField(label="Contraseña", width=300, password=True, can_reveal_password=True)
        self.database = ft.TextField(label="Base de Datos", width=300)
        
        self.dialogo = ft.AlertDialog(
            modal=True,
            title=ft.Text("Iniciar Sesión"),
            content=ft.Column(
                controls=[
                    self.host,
                    self.user,
                    self.password,
                    self.database
                ],
                tight=True
            ),
            actions=[
                ft.TextButton("Iniciar sesion", on_click=self.validar_conexion)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
    
    def mostrar_dialogo(self):
        self.page.show_dialog(self.dialogo)
        self.page.update()
    
    def validar_conexion(self, e):
        import config.conexion
        config.conexion.localhost_sesion = self.host.value
        config.conexion.user_sesion = self.user.value
        config.conexion.password_sesion = self.password.value
        config.conexion.database_sesion = self.database.value
        
        try:
            conn = conectar()
            conn.close()
            
            self.page.pop_dialog()
            self.page.update()
            
            self.callback_exito()
            
        except Exception as error:
            snack = ft.SnackBar(
                ft.Text(f"Error de conexión: {error}"),
                bgcolor=ft.Colors.RED
            )
            self.page.overlay.append(snack)
            snack.open = True
            self.page.update()
    