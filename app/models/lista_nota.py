from datetime import datetime
from app.models.nodo_nota import NodoNota


class ListaNota:
    def __init__(self):
        self.cabeza = None
        self.cola = None

    def crear_nota(self, titulo, contenido):
        nueva_nota = NodoNota(titulo, contenido)
        if not self.cabeza:
            self.cabeza = nueva_nota
            self.cola = nueva_nota
        else:
            # Enlaza la nueva nota al inicio de la lista
            nueva_nota.siguiente = self.cabeza
            self.cabeza.anterior = nueva_nota
            self.cabeza = nueva_nota
        return nueva_nota.id  

    def buscar_nota_por_id(self, id):
        actual = self.cabeza
        while actual:
            if actual.id == id:
                return actual
            actual = actual.siguiente
        return None  # Nota no encontrada

    def editar_nota(self, id, nuevo_titulo, nuevo_contenido):
        nota = self.buscar_nota_por_id(id)
        if nota:
            nota.titulo = nuevo_titulo
            nota.contenido = nuevo_contenido
            nota.fecha_modificacion = datetime.now()
            self._mover_nota_a_inicio(nota)  # Mueve la nota editada al inicio de la lista
            return True  # Nota editada exitosamente
        return False  # Nota no encontrada

    def _mover_nota_a_inicio(self, nota: NodoNota):
        if nota is self.cabeza:
            return
        # desenlazar (nota.anterior existe porque no es cabeza)
        nota.anterior.siguiente = nota.siguiente
        if nota.siguiente:
            nota.siguiente.anterior = nota.anterior
        else:
            self.cola = nota.anterior
        # insertar al inicio
        nota.anterior = None
        nota.siguiente = self.cabeza
        self.cabeza.anterior = nota
        self.cabeza = nota

    def eliminar_nota(self, id_nota):
        nodo = self.buscar_nota_por_id(id_nota)
        if not nodo:
            return False
        if nodo.anterior:
            nodo.anterior.siguiente = nodo.siguiente
        else:
            self.cabeza = nodo.siguiente
        if nodo.siguiente:
            nodo.siguiente.anterior = nodo.anterior
        else:
            self.cola = nodo.anterior
        nodo.anterior = nodo.siguiente = None
        return True


    def obtener_todas_las_notas(self):
        notas = []
        actual = self.cabeza
        while actual:
            notas.append(actual.to_dict())
            actual = actual.siguiente
        return notas
