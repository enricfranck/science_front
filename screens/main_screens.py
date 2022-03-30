from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty


class MainScreen(Screen):
    screenManager = ObjectProperty(None)

    def login(self):
        email = self.ids.email.text
        password = self.ids.password.text
        print(email, password)

    def back_select(self):
        MDApp.get_running_app().root.current = 'Selection'

    def back_reins(self):
        MDApp.get_running_app().root.current = 'Reinscription'

    def back_notes(self):
        MDApp.get_running_app().root.current = 'Note'

