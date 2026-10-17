from kivy.app import App
from kivy.properties import BooleanProperty, ColorProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

from app.models.nota_editor import NotaEditor


class ItemMenu(ButtonBehavior, BoxLayout):
    """Fila del menú de 3 puntos (icono + texto). El diseño está en editor.kv."""
    icono = StringProperty("")
    texto = StringProperty("")
    color_item = ColorProperty([0, 0, 0, 1])


class EditorScreen(Screen):
    # Propiedades que usa editor.kv
    puede_deshacer = BooleanProperty(False)
    puede_rehacer = BooleanProperty(False)
    menu_abierto = BooleanProperty(False)

    def __init__(self, **kwargs):
        # Se definen ANTES de super().__init__ por si on_text se dispara al construir la UI
        self.editor_historico = NotaEditor(max_history=100)
        self.bloqueo_edicion = False       # True mientras se aplica deshacer/rehacer por código
        self.nota_id_actual = None
        super().__init__(**kwargs)

    # ------------- Entrada ---------------

    def cargar_nota(self, id_nota: str) -> None:
        lista = App.get_running_app().lista_nota
        nota = lista.buscar_nota_por_id(id_nota)
        if not nota:
            return
        self.nota_id_actual = id_nota
        self.ids.titulo_nota.text = nota.titulo
        self._set_contenido(nota.contenido)
        self.editor_historico.iniciar(nota.contenido)
        self._reiniciar_estado()

    def crear_nueva_nota(self) -> None:
        self.nota_id_actual = None
        self.ids.titulo_nota.text = ""
        self._set_contenido("")
        self.editor_historico.iniciar("")
        self._reiniciar_estado()

    def _reiniciar_estado(self) -> None:
        self.menu_abierto = False
        self._actualizar_botones()

    # ------------- Historial (deshacer / rehacer) ---------------

    def _set_contenido(self, texto: str) -> None:
        """Cambia el texto sin que cuente como una edición del usuario."""
        self.bloqueo_edicion = True
        try:
            caja = self.ids.contenido_nota
            caja.text = texto
            caja.cursor = caja.get_cursor_from_index(len(texto))   # cursor al final
        finally:
            self.bloqueo_edicion = False

    def _actualizar_botones(self) -> None:
        """Apaga los iconos de deshacer/rehacer cuando no hay nada que deshacer/rehacer."""
        self.puede_deshacer = self.editor_historico.undo_stack.actual_size > 1
        self.puede_rehacer = not self.editor_historico.redo_stack.es_vacia()

    def registrar_cambio(self, texto: str) -> None:
        if self.bloqueo_edicion:
            return
        self.editor_historico.guardar_estado(texto)
        self._actualizar_botones()

    def deshacer_cambio(self) -> None:
        texto = self.editor_historico.deshacer()
        if texto is not None:
            self._set_contenido(texto)
        self._actualizar_botones()

    def rehacer_cambio(self) -> None:
        texto = self.editor_historico.rehacer()
        if texto is not None:
            self._set_contenido(texto)
        self._actualizar_botones()

    # ------------- Menú de 3 puntos ---------------

    def toggle_menu(self) -> None:
        self.menu_abierto = not self.menu_abierto

    def cerrar_menu(self) -> None:
        self.menu_abierto = False

    def on_touch_down(self, touch):
        # Un toque fuera del menú abierto solo lo cierra (no activa lo que hay debajo)
        if self.menu_abierto:
            x, y = self.to_local(*touch.pos)
            if not self.ids.menu_desplegable.collide_point(x, y):
                self.cerrar_menu()
                return True
        return super().on_touch_down(touch)

    def on_pre_leave(self, *args) -> None:
        self.cerrar_menu()

    # ------------- Guardar / eliminar ---------------

    def guardar_nota(self) -> None:
        self.cerrar_menu()
        titulo = self.ids.titulo_nota.text.strip()
        contenido = self.ids.contenido_nota.text

        # Una nota nueva totalmente vacía no se guarda
        if self.nota_id_actual is None and not titulo and not contenido.strip():
            self.regresar_home()
            return

        lista = App.get_running_app().lista_nota
        titulo = titulo or "Sin título"
        if self.nota_id_actual is None:
            self.nota_id_actual = lista.crear_nota(titulo, contenido)
        else:
            lista.editar_nota(self.nota_id_actual, titulo, contenido)
        self.regresar_home()

    def eliminar_nota(self) -> None:
        self.cerrar_menu()
        if self.nota_id_actual is not None:      # si es nota nueva, simplemente se descarta
            App.get_running_app().lista_nota.eliminar_nota(self.nota_id_actual)
            self.nota_id_actual = None
        self.regresar_home()

    def regresar_home(self) -> None:
        self.manager.current = "home"