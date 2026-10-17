import uuid
from datetime import datetime

class NodoNota:
    def __init__(self, titulo, contenido, id=None, fecha_modificacion=None):
        self.id = id or str(uuid.uuid4())[:8]  # Genera un ID único de 8 caracteres
        self.titulo = titulo
        self.contenido = contenido
        self.fecha_modificacion = fecha_modificacion or datetime.now()
        self.anterior = None
        self.siguiente = None

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "contenido": self.contenido,
            "fecha_modificacion": self.fecha_modificacion
        }