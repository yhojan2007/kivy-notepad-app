"""Búsqueda por título: utilidades de texto, Trie e índice de títulos en un solo módulo."""
import re
import unicodedata

# ============================================================
#  Utilidades de texto
# ============================================================
_PALABRA = re.compile(r"\w+")


def normalizar(texto: str) -> str:
    """Minúsculas y sin tildes: 'Estadística' -> 'estadistica'."""
    descompuesto = unicodedata.normalize("NFD", texto.casefold())
    return "".join(c for c in descompuesto if unicodedata.category(c) != "Mn")


def tokenizar(texto: str) -> list[str]:
    """Separa un texto en palabras normalizadas, ignorando signos de puntuación.

    'Tarea de Estadística II!' -> ['tarea', 'de', 'estadistica', 'ii']
    """
    return _PALABRA.findall(normalizar(texto))


# ============================================================
#  Trie (árbol de prefijos)
# ============================================================
class NodoTrie:
    """Un carácter del árbol. `ids` guarda las notas cuya palabra termina exactamente aquí."""
    __slots__ = ("hijos", "ids")

    def __init__(self) -> None:
        self.hijos: dict[str, "NodoTrie"] = {}
        self.ids: set[str] = set()


class Trie:
    """Árbol de prefijos: asocia palabras con los ids de las notas que las contienen.

    Complejidad (L = largo de la palabra, k = nodos bajo el prefijo):
        insertar  O(L)      eliminar  O(L)      buscar_prefijo  O(L + k)
    """

    def __init__(self) -> None:
        self.raiz = NodoTrie()

    def insertar(self, palabra: str, id_nota: str) -> None:
        if not palabra:
            return
        nodo = self.raiz
        for caracter in palabra:
            hijo = nodo.hijos.get(caracter)
            if hijo is None:
                hijo = nodo.hijos[caracter] = NodoTrie()
            nodo = hijo
        nodo.ids.add(id_nota)

    def eliminar(self, palabra: str, id_nota: str) -> bool:
        """Quita la asociación palabra -> nota y poda los nodos que quedaron sin uso.

        Devuelve True si algo fue eliminado.
        """
        camino: list[tuple[NodoTrie, str]] = []   # (padre, carácter) de cada paso
        nodo = self.raiz
        for caracter in palabra:
            hijo = nodo.hijos.get(caracter)
            if hijo is None:
                return False
            camino.append((nodo, caracter))
            nodo = hijo

        if id_nota not in nodo.ids:
            return False
        nodo.ids.remove(id_nota)

        # Poda de abajo hacia arriba: un nodo sin ids y sin hijos ya no aporta nada.
        for padre, caracter in reversed(camino):
            hijo = padre.hijos[caracter]
            if hijo.ids or hijo.hijos:
                break
            del padre.hijos[caracter]
        return True

    def buscar_prefijo(self, prefijo: str) -> set[str]:
        """Ids de todas las notas con alguna palabra que empiece por `prefijo`."""
        nodo = self.raiz
        for caracter in prefijo:
            nodo = nodo.hijos.get(caracter)
            if nodo is None:
                return set()

        # Recorrido iterativo (pila) para no depender del límite de recursión de Python.
        encontrados: set[str] = set()
        pila = [nodo]
        while pila:
            actual = pila.pop()
            encontrados |= actual.ids
            pila.extend(actual.hijos.values())
        return encontrados


# ============================================================
#  Índice de títulos
# ============================================================
class IndiceTitulos:
    """Índice de búsqueda por título construido sobre un Trie.

    Cada palabra del título se guarda en el Trie, así 'esta' encuentra
    'Tarea de Estadística II'. Además recuerda qué palabras indexó por nota, de modo
    que actualizar o quitar una nota nunca depende de que alguien recuerde el título viejo.
    """

    def __init__(self) -> None:
        self._trie = Trie()
        self._palabras_por_id: dict[str, frozenset[str]] = {}

    def indexar(self, id_nota: str, titulo: str) -> None:
        """Alta o actualización. Es idempotente y solo toca las palabras que cambiaron."""
        nuevas = frozenset(tokenizar(titulo))
        anteriores = self._palabras_por_id.get(id_nota, frozenset())
        if nuevas == anteriores:
            return

        for palabra in anteriores - nuevas:
            self._trie.eliminar(palabra, id_nota)
        for palabra in nuevas - anteriores:
            self._trie.insertar(palabra, id_nota)

        if nuevas:
            self._palabras_por_id[id_nota] = nuevas
        else:
            self._palabras_por_id.pop(id_nota, None)

    def quitar(self, id_nota: str) -> None:
        for palabra in self._palabras_por_id.pop(id_nota, ()):
            self._trie.eliminar(palabra, id_nota)

    def buscar(self, consulta: str) -> set[str] | None:
        """Ids de las notas que contienen TODAS las palabras de la consulta (cada una como prefijo).

        Devuelve None si la consulta no tiene palabras buscables (vacía o solo símbolos):
        en ese caso no hay que filtrar nada.
        """
        palabras = tokenizar(consulta)
        if not palabras:
            return None

        resultado: set[str] | None = None
        for palabra in palabras:
            ids = self._trie.buscar_prefijo(palabra)
            resultado = ids if resultado is None else resultado & ids
            if not resultado:
                break                     # ya no puede coincidir nada más
        return resultado or set()