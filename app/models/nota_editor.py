from app.models.nodo_nota import NodoNota

class NodoEstado:
    """Nodo para la pila de historial, contiene el contenido de la nota."""
    def __init__(self, contenido: str) -> None:
        self.contenido: str = contenido
        self.anterior: NodoEstado | None = None
        self.siguiente: NodoEstado | None = None

class PilaHistorial:
    """Pila con lista doble enlazada y tamaño máximo."""
    def __init__(self, max_size: int) -> None:
        self.fondo: NodoEstado | None = None
        self.tope: NodoEstado | None = None
        self.max_size = max_size
        self.actual_size = 0

    def push(self, contenido: str) -> None:
        nuevo = NodoEstado(contenido)
        # Si la pila está vacía, el nuevo nodo es tanto el fondo como el tope
        if not self.fondo:
            self.fondo = self.tope = nuevo
        else:
            self.tope.siguiente = nuevo
            nuevo.anterior = self.tope
            self.tope = nuevo
        self.actual_size += 1

        if self.actual_size > self.max_size:
            self._eliminar_fondo()          # elimina el MÁS ANTIGUO

    def pop(self) -> str | None:
        """Elimina y devuelve el contenido del nodo tope de la pila."""
        if not self.tope:       # Pila vacía
            return None
        contenido = self.tope.contenido
        if self.fondo is self.tope:
            self.fondo = self.tope = None
        else:
            self.tope = self.tope.anterior
            self.tope.siguiente = None
            
        self.actual_size -= 1
        return contenido

    def _eliminar_fondo(self):
        if self.fondo is self.tope:
            self.fondo = self.tope = None
        else:
            self.fondo = self.fondo.siguiente
            self.fondo.anterior = None
        self.actual_size -= 1

    def es_vacia(self) -> bool:
        return self.fondo is None

    def clear(self) -> None:
        actual = self.fondo
        while actual:
            sig = actual.siguiente
            actual.anterior = actual.siguiente = None
            actual = sig
        self.fondo = self.tope = None
        self.actual_size = 0


class NotaEditor:
    """Maneja el historial de deshacer/rehacer para una nota."""
    def __init__(self, max_history=100) -> None:
        self.undo_stack = PilaHistorial(max_history)
        self.redo_stack = PilaHistorial(max_history)

    def iniciar(self, contenido_inicial: str) -> None:
        """Llamar al abrir una nota: el estado inicial queda como base."""
        self.clear_historial()
        self.undo_stack.push(contenido_inicial)

    def guardar_estado(self, nuevo_contenido: str) -> None:
        # evita duplicados consecutivos
        if self.undo_stack.tope and self.undo_stack.tope.contenido == nuevo_contenido:
            return
        self.undo_stack.push(nuevo_contenido)
        self.redo_stack.clear()

    def deshacer(self) -> str | None:
        if self.undo_stack.actual_size <= 1:   # solo queda el estado base
            return None
        # Mueve el estado actual a la pila de redo y devuelve el nuevo estado tope
        contenido = self.undo_stack.pop()
        self.redo_stack.push(contenido)
        return self.undo_stack.tope.contenido

    def rehacer(self) -> str | None:
        if self.redo_stack.es_vacia():
            return None
        # Mueve el contenido de la pila de redo a la pila de undo y devuelve el contenido
        contenido = self.redo_stack.pop()
        self.undo_stack.push(contenido)
        return contenido

    def clear_historial(self) -> None:
        self.undo_stack.clear()
        self.redo_stack.clear()