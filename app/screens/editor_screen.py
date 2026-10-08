from kivy.uix.screenmanager import Screen
from kivy.app import App

from app.models.nota_editor import NotaEditor
from app.models.lista_nota import ListaNota

class EditorScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.editor_historico = NotaEditor(max_history=100)
        self.bloqueo_edicion = False   # Variable para bloquear la edición durante deshacer/rehacer

    def on_enter(self):
        self.editor_historico.clear_historial()  # Limpiar el historial al entrar a la pantalla
        # Guardar el contenido inicial de la nota en el historial
        contenido_inicial = self.ids.contenido_nota.text
        self.editor_historico.iniciar(contenido_inicial)

    def registrar_cambio(self, texto):
        if self.bloqueo_edicion:
            return  # No registrar cambios si estamos en medio de un deshacer/rehacer
        self.editor_historico.guardar_estado(texto)

    def deshacer_cambio(self):
        self.bloqueo_edicion = True
        texto_anterior = self.editor_historico.deshacer()
        # Si hay un estado anterior, actualizar el contenido de la nota
        if texto_anterior is not None:
            self.ids.contenido_nota.text = texto_anterior
        self.bloqueo_edicion = False

    def rehacer_cambio(self):
        self.bloqueo_edicion = True
        texto_siguiente = self.editor_historico.rehacer()
        # Si hay un estado rehecho, actualizar el contenido de la nota
        if texto_siguiente is not None:
            self.ids.contenido_nota.text = texto_siguiente
        self.bloqueo_edicion = False

    def regresar_home(self):
        self.manager.current = 'home'