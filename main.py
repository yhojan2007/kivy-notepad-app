from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from app.models.lista_nota import ListaNota
from app.screens.home_screen import HomeScreen
from app.screens.editor_screen import EditorScreen



class NotepadApp(App):  
    
    def build(self) -> ScreenManager:
        Builder.load_file("kv/home.kv")
        Builder.load_file("kv/editor.kv")

        self.lista_nota = ListaNota()  # Inicializa la lista de notas

        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(HomeScreen(name="home"))
        self.screen_manager.add_widget(EditorScreen(name="editor"))

        return self.screen_manager

        
        

if __name__ == "__main__":
    NotepadApp().run()