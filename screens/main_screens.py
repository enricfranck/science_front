from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem


class MainScreen(Screen):
    screenManager = ObjectProperty(None)

    def login(self):
        email = self.ids.email.text
        password = self.ids.password.text
        print(email, password)

    def on_enter(self, *args):
        self.ids.list_email.text = MDApp.get_running_app().USER_EMAIL
        self.ids.list_role.text = MDApp.get_running_app().USER_ROLE

    def back_select(self):
        MDApp.get_running_app().root.current = 'Selection'

    def back_reins(self):
        MDApp.get_running_app().root.current = 'Reinscription'

    def back_notes(self):
        MDApp.get_running_app().root.current = 'Note'

    def back_scola(self):
        MDApp.get_running_app().root.current = 'Scola'
