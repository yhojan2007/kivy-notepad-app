from datetime import datetime

from app.models.busqueda_titulos import IndiceTitulos
from app.models.nodo_nota import NodoNota


class ListaNota:
    def __init__(self, repositorio = None, indice = None):
        self.cabeza = None
        self.cola = None
        self.repo = repositorio

        self.indice = indice if indice is not None else IndiceTitulos()
        self.cargar_desde_repositorio()

    #---------------- Carga inicial -----------------------------

    def cargar_desde_repositorio(self) -> None:
        """ Reconstruye las lista al abrir la app."""
        if not self.repo:
            return
        for datos in self.repo.obtener_todas():
            nodo = NodoNota(
                datos["titulo"], datos["contenido"],
                id = datos["id"], fecha_modificacion = datos["fecha_modificacion"],
            )
            self._agregar_al_final(nodo)
            self.indice.indexar(nodo.id, nodo.titulo)

    def _agregar_al_final(self, nodo: NodoNota) -> None:
        if not self.cola:
            self.cabeza = self.cola = nodo
        else:
            nodo.anterior = self.cola
            self.cola.siguiente = nodo
            self.cola = nodo

    # ------------------- Operaciones ------------------

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
        self.indice.indexar(nueva_nota.id, nueva_nota.titulo)
        if self.repo:
            self.repo.guardar(nueva_nota)
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
            if nota.titulo == nuevo_titulo and nota.contenido == nuevo_contenido:
                return True      # sin cambios: no se toca la fecha ni el orden
            nota.titulo = nuevo_titulo
            nota.contenido = nuevo_contenido
            nota.fecha_modificacion = datetime.now()
            self._mover_nota_a_inicio(nota)  # Mueve la nota editada al inicio de la lista
            self.indice.indexar(nota.id, nota.titulo)   # el título pudo cambiar
            if self.repo:
                self.repo.guardar(nota)
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

    def eliminar_nota(self, id_nota) -> bool:
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
        self.indice.quitar(id_nota)
        if self.repo:
            self.repo.eliminar(id_nota)

        return True

    def obtener_todas_las_notas(self):
        notas = []
        actual = self.cabeza
        while actual:
            notas.append(actual.to_dict())
            actual = actual.siguiente
        return notas

    def buscar_por_titulo(self, consulta: str) -> list[dict]:
        """Notas cuyo título coincide con la consulta (más reciente primero). Consulta vacía = todas."""
        ids = self.indice.buscar(consulta)
        if ids is None:
            return self.obtener_todas_las_notas()
        coincidencias = []
        actual = self.cabeza
        while actual:
            if actual.id in ids:
                coincidencias.append(actual.to_dict())
            actual = actual.siguiente
        return coincidencias