import os

from kivy.config import Config
from kivy.lang.builder import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

from screens.login_screens import LoginScreen
from screens.main_screens import MainScreen
from screens.reinscription_add_screen import ReinscriptionAddScreen
from screens.reinscription_screen import ReinscriptionScreen
from screens.reinscription_update_screen import ReinscriptionUpdateScreen

Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'width', 1000)
Config.set('graphics', 'height', 650)
Config.write()


class MainScreen(MainScreen):
    pass


class LoginScreen(LoginScreen):
    pass


class ReinscriptionScreen(ReinscriptionScreen):
    pass


class ReinscriptionAddScreen(ReinscriptionAddScreen):
    pass


class ReinscriptionUpdateScreen(ReinscriptionUpdateScreen):
    pass


class ScienceApp(MDApp):
    dialog = None
    TOKEN: str = ""
    ALL_MENTION: list = []
    ALL_PARCOURS: list = []
    ALL_ETUDIANT: list = []
    NUMERO_CARTE: str = ""
    MENTION: str = ""
    HOST: str = os.getenv("host")
    IS_INITIALISE = False
    ANNEE: str = ""

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.accent_palette = "Green"
        screen = Builder.load_file('kv_file/all_screen.kv')
        return screen

    def show_dialog(self, text: str):
        if not self.dialog:
            # create dialog
            self.dialog = MDDialog(
                title="Log In",
                text=f"{text}",
                buttons=[
                    MDFlatButton(
                        text="Ok",
                        text_color=self.theme_cls.primary_color,
                        # on_release=""
                    ),
                ],
            )

        self.dialog.open()

    def close(self, *args):
        self.dialog.dismiss()


ScienceApp().run()
