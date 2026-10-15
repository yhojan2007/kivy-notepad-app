from kivy.uix.screenmanager import Screen
from kivy.app import App

from app.models.nota_editor import NotaEditor

class EditorScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.editor_historico = NotaEditor(max_history=100)
        self.bloqueo_edicion = False   # Variable para bloquear la edición durante deshacer/rehacer
        self.nota_id_actual = None  # Variable para almacenar el ID de la nota actual

    #------------- Entrada ---------------

    def cargar_nota(self, id_nota) -> None:
        lista = App.get_running_app().lista_nota
        nota = lista.buscar_nota_por_id(id_nota)
        if not nota:
            return
        self.nota_id_actual = id_nota
        self.ids.titulo_nota.text = nota.titulo
        # bloquear el registro de cambio mientras seteamos texto
        self.bloqueo_edicion = True
        self.ids.contenido_nota.text = nota.contenido
        self.bloqueo_edicion = False
        self.editor_historico.iniciar(nota.contenido)

    def crear_nueva_nota(self):
        self.nota_id_actual = None
        self.ids.titulo_nota.text = ""
        self.bloqueo_edicion = True
        self.ids.contenido_nota.text = ""
        self.bloqueo_edicion = False
        self.editor_historico.iniciar("")

    #------------- Historial ---------------

    def registrar_cambio(self, texto) -> None:
        if self.bloqueo_edicion:
            return  # No registrar cambios si estamos en medio de un deshacer/rehacer
        self.editor_historico.guardar_estado(texto)

    def deshacer_cambio(self) -> None:
        self.bloqueo_edicion = True
        texto_anterior = self.editor_historico.deshacer()
        # Si hay un estado anterior, actualizar el contenido de la nota
        if texto_anterior is not None:
            self.ids.contenido_nota.text = texto_anterior
        self.bloqueo_edicion = False

    def rehacer_cambio(self) -> None:
        self.bloqueo_edicion = True
        texto_siguiente = self.editor_historico.rehacer()
        # Si hay un estado rehecho, actualizar el contenido de la nota
        if texto_siguiente is not None:
            self.ids.contenido_nota.text = texto_siguiente
        self.bloqueo_edicion = False

    # ---------- GUARDAR / ELIMINAR ----------

    def guardar_nota(self):
        titulo = self.ids.titulo_nota.text.strip()
        contenido = self.ids.contenido_nota.text

        if not titulo:
            titulo = "Sin título"

        lista = App.get_running_app().lista_nota

        if self.nota_id_actual is None:
            # nota nueva
            self.nota_id_actual = lista.crear_nota(titulo, contenido)
        else:
            # editar existente
            lista.editar_nota(self.nota_id_actual, titulo, contenido)

        # Volver al home (que refresca automáticamente con on_enter)
        self.manager.current = "home"

    def eliminar_nota(self):
        if self.nota_id_actual is None:
            # nota nueva sin guardar → solo limpiar
            self.nueva_nota()
            return
        lista = App.get_running_app().lista_nota
        lista.eliminar_nota(self.nota_id_actual)
        self.nota_id_actual = None
        self.manager.current = "home"

    def regresar_home(self):
        self.manager.current = "home"