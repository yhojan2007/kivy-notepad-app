from kivy.uix.screenmanager import Screen
from app.services.auth_service import AuthService

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auth_service = AuthService()

    def iniciar_sesion(self):
        username = self.ids.username.text
        password = self.ids.password.text

        if self.auth_service.authenticate(username, password):
            self.ids.mensaje.text = "Inicio de sesión exitoso"
            # Aquí puedes cambiar a la pantalla principal de la aplicación
        else:
            self.ids.mensaje.text = "Nombre de usuario o contraseña incorrectos"