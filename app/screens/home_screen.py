from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.app import App

from app.models.lista_nota import ListaNota
from app.models.nota_editor import NotaEditor

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lista_nota = ListaNota()  # Inicializa la lista de notas

    def mostrar_notas(self):
        notas = self.lista_nota.obtener_todas_las_notas()
        self.ids.lista_notas.clear_widgets()  # Limpiar la lista antes de mostrar las notas

        for nota in notas:
            boton_nota = Button(
                text=nota["titulo"],
                size_hint_y=None,
                height=40
            )
            boton_nota.bind(on_release=lambda btn, n=nota: self.cargar_nota(n))
            self.ids.lista_notas.add_widget(boton_nota)

    def crear_nueva_nota(self):
        
        self.manager.current = "editor"