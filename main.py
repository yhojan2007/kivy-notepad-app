from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from app.screens.login_screen import LoginScreen



class LoginApp(App):  
    
    def build(self) -> ScreenManager:
        Builder.load_file("kv/login.kv")

        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(LoginScreen(name="login"))
    
        return self.screen_manager

        

if __name__ == "__main__":
    LoginApp().run()