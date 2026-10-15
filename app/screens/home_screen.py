from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.app import App

class HomeScreen(Screen):
    def on_enter(self) -> None:
        self.mostrar_notas()

    def mostrar_notas(self, filtro=""):
        app = App.get_running_app()
        notas = app.lista_nota.obtener_todas_las_notas()

        contenedor = self.ids.notas_container
        contenedor.clear_widgets()

        filtro = (filtro or "").lower()
        for nota in notas:
            if filtro and filtro not in nota["titulo"].lower() \
               and filtro not in nota["contenido"].lower():
                continue

            btn = Button(
                text=f"{nota['titulo']}",
                size_hint_y=None,
                height=50,
            )
            btn.bind(on_release=lambda b, n=nota: self.abrir_nota(n["id"]))
            contenedor.add_widget(btn)

    def abrir_nota(self, nota_id) -> None:
        editor = self.manager.get_screen('editor')
        editor.cargar_nota(nota_id)
        self.manager.current = 'editor'

    def crear_nueva_nota(self) -> None:
        editor = self.manager.get_screen('editor')
        editor.crear_nueva_nota()
        self.manager.current = 'editor'


