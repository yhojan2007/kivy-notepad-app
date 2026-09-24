from app.models.usuario import Usuario

class AuthService:
    def __init__(self):
        self.usuario = Usuario("admin", "1234") # Usuario predeterminado para autenticación

    def authenticate(self, username: str, password: str) -> bool:
        return self.usuario.username == username and self.usuario.password == password