from datetime import datetime

from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from app.models.busqueda_titulos import tokenizar

MAX_SUGERENCIAS = 4


def formatear_fecha(fecha: datetime) -> str:
    """fecha: 16/10/2026 22:56"""
    return f"fecha: {fecha:%d/%m/%Y %H:%M}"


class NotaItem(ButtonBehavior, BoxLayout):
    """Tarjeta (píldora) de una nota en la lista. El diseño está en home.kv."""
    nota_id = StringProperty("")
    titulo = StringProperty("")
    fecha = StringProperty("")


class SugerenciaItem(ButtonBehavior, BoxLayout):
    """Fila del autocompletado. El diseño está en home.kv."""
    texto = StringProperty("")


class HomeScreen(Screen):

    # ---------- Ciclo de vida ----------

    def on_enter(self) -> None:
        # Al volver del editor se refresca la lista (título nuevo, nota borrada, nuevo orden...)
        self._limpiar_sugerencias()
        self.mostrar_notas(self.ids.buscador.text)

    # ---------- Lista de notas ----------

    def mostrar_notas(self, filtro: str = "") -> list[dict]:
        """Pinta las notas cuyo título coincide con `filtro` y devuelve esas coincidencias."""
        lista = App.get_running_app().lista_nota
        coincidencias = lista.buscar_por_titulo(filtro)
        self._pintar_notas(coincidencias, hay_filtro=bool(tokenizar(filtro)))
        return coincidencias

    def _pintar_notas(self, notas: list[dict], hay_filtro: bool) -> None:
        contenedor = self.ids.notas_container
        contenedor.clear_widgets()

        for nota in notas:
            item = NotaItem(
                nota_id=nota["id"],
                titulo=nota["titulo"],
                fecha=formatear_fecha(nota["fecha_modificacion"]),
            )
            item.bind(on_release=lambda w: self.abrir_nota(w.nota_id))
            contenedor.add_widget(item)

        if not notas:
            mensaje = ("No hay notas que coincidan." if hay_filtro
                       else "Aún no tienes notas.\nToca + para crear la primera.")
            vacio = Label(
                text=mensaje,
                size_hint_y=None,
                height=120,
                color=(0.52, 0.55, 0.60, 1),
                halign="center",
            )
            vacio.bind(size=lambda w, s: setattr(w, "text_size", s))
            contenedor.add_widget(vacio)

    # ---------- Buscador y notas sugeridas ----------

    def al_escribir(self, texto: str) -> None:
        """Se llama en cada cambio del buscador: filtra la lista y actualiza las sugerencias."""
        coincidencias = self.mostrar_notas(texto)
        self._pintar_sugerencias(texto, coincidencias)

    def al_cambiar_foco(self, con_foco: bool) -> None:
        if con_foco:
            texto = self.ids.buscador.text
            lista = App.get_running_app().lista_nota
            self._pintar_sugerencias(texto, lista.buscar_por_titulo(texto))
        else:
            self._limpiar_sugerencias()

    def _pintar_sugerencias(self, texto: str, coincidencias: list[dict]) -> None:
        """Muestra hasta MAX_SUGERENCIAS títulos que completan lo que se va escribiendo."""
        self._limpiar_sugerencias()
        consulta = " ".join(tokenizar(texto))
        if not consulta or not self.ids.buscador.focus:
            return

        panel = self.ids.panel_sugerencias
        vistos = set()
        for nota in coincidencias:               # ya vienen de la más reciente a la más antigua
            clave = " ".join(tokenizar(nota["titulo"]))
            if clave == consulta or clave in vistos:   # nada que completar / título repetido
                continue
            vistos.add(clave)
            item = SugerenciaItem(texto=nota["titulo"])
            item.bind(on_release=lambda w: self.seleccionar_sugerencia(w.texto))
            panel.add_widget(item)
            if len(vistos) >= MAX_SUGERENCIAS:
                break

    def _limpiar_sugerencias(self) -> None:
        self.ids.panel_sugerencias.clear_widgets()

    def seleccionar_sugerencia(self, titulo: str) -> None:
        caja = self.ids.buscador
        caja.text = titulo        # dispara al_escribir y filtra la lista
        caja.focus = False        # cierra el teclado y las sugerencias

    # ---------- Navegación ----------

    def abrir_nota(self, nota_id: str) -> None:
        editor = self.manager.get_screen("editor")
        editor.cargar_nota(nota_id)
        self.manager.current = "editor"

    def crear_nueva_nota(self) -> None:
        editor = self.manager.get_screen("editor")
        editor.crear_nueva_nota()
        self.manager.current = "editor"