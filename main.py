import os

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.resources import resource_add_path
from kivy.uix.screenmanager import ScreenManager
from kivy.utils import get_color_from_hex

from app.data.nota_repositorio import NotaRepositorio
from app.models.lista_nota import ListaNota
from app.screens.editor_screen import EditorScreen
from app.screens.home_screen import HomeScreen

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
resource_add_path(BASE_DIR)        # así la fuente de iconos se encuentra sin importar desde dónde se ejecute

Window.clearcolor = get_color_from_hex("#FFFFFF")
Window.softinput_mode = "resize"   # el teclado empuja el contenido en vez de taparlo
Window.size = (360, 700)         # descomenta para simular un celular en PC


class NotepadApp(App):

    def build(self) -> ScreenManager:
        # El tema va primero: define colores y componentes que usan las demás pantallas
        for nombre in ("theme.kv", "home.kv", "editor.kv"):
            Builder.load_file(os.path.join(BASE_DIR, "kv", nombre))

        # user_data_dir: carpeta privada de la app (en Android sobrevive al cerrarla)
        os.makedirs(self.user_data_dir, exist_ok=True)
        self.repo = NotaRepositorio(os.path.join(self.user_data_dir, "notas.db"))
        self.lista_nota = ListaNota(self.repo)

        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(HomeScreen(name="home"))
        self.screen_manager.add_widget(EditorScreen(name="editor"))
        return self.screen_manager

    def on_pause(self) -> bool:
        return True                    # Android: permite pausar la app sin cerrarla

    def on_stop(self) -> None:
        self.repo.cerrar()


if __name__ == "__main__":
    NotepadApp().run()