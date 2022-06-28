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

    def update(self):
        if MDApp.get_running_app().VERSION_APP != "":
            MDApp.get_running_app().TITRE_FILE = f"DataSciV{MDApp.get_running_app().VERSION_APP}"
            host = MDApp.get_running_app().HOST
            url = f"http://{host}/api/v1/resultat/get_by_session"
            MDApp.get_running_app().URL_DOWNLOAD = url
            MDApp.get_running_app().NAME_DOWNLOAD = f"{MDApp.get_running_app().TITRE_FILE}.zip"
            MDApp.get_running_app().PARENT = "Main"
            MDApp.get_running_app().root.current = 'download_file'
