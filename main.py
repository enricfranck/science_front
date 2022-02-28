import os
import secrets
import string

from kivy.config import Config
from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import AsyncImage
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.picker import MDDatePicker

from all_requests import request_utils
from screens.download_screen import DownloadScreen
from screens.login_screens import LoginScreen
from screens.main_screens import MainScreen
from screens.public_add_screen import PublicAddScreen
from screens.public_screen import PublicScreen
from screens.reinscription_add_screen import ReinscriptionAddScreen
from screens.reinscription_screen import ReinscriptionScreen
from screens.reinscription_update_screen import ReinscriptionUpdateScreen
from screens.selection_add_screens import SelectionAddScreen
from screens.selection_screens import SelectionScreen
from screens.selection_update_screens import SelectionUpdateScreen

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


class PublicScreen(PublicScreen):
    pass


class FloatLayout_(FloatLayout):
    source = StringProperty()


class ImageButton(ButtonBehavior, AsyncImage):
    pass


class DownloadScreen(DownloadScreen):
    pass


class SelectionScreen(SelectionScreen):
    pass


class SelectionAddScreen(SelectionAddScreen):
    pass


class SelectionUpdateScreen(SelectionUpdateScreen):
    pass


class PublicAddScreen(PublicAddScreen):
    pass


class ScienceApp(MDApp):
    dialog = None
    TOKEN: str = ""
    URL_DOWNLOAD: str = ""
    ALL_UUID_MENTION: list = []
    ALL_MENTION: list = []
    ALL_PARCOURS: list = []
    ALL_ETUDIANT: list = []
    ALL_ETUDIANT_PRE_SELECTIONNER: list = []
    ALL_ETUDIANT_SELECTIONNER: list = []
    ALL_NIVEAU_SELECT: list = ['L1', 'M1', 'M2']
    AL_NIVEAU: list = ['L1', 'L2', 'L3', 'M1', 'M2']
    NUM_CARTE: str = ""
    NUM_SELECT: str = ""
    MENTION: str = ""
    HOST: str = os.getenv("host")
    IS_INITIALISE = False
    TITRE_FILE: str = ""
    PARENT: str = ""
    ANNEE: str = ""
    ALL_ANNEE: str = ""
    NAME_DOWNLOAD: str = ""
    ALL_SEXE: list = ["MASCULIN", "FEMININ"]
    ALL_ETAT: list = ["Passant", "Redoublant", "Triplant ou plus"]
    ALL_NATION: list = ["Malagasy", "Asiatique", "Africaine", "Comorienne", "Européene"]
    DATE_TEXTE: str = ""
    ERROR: str = ""
    PUBLIC_TITRE: str = ""
    ALL_ROLE: list = []
    ALL_DROIT: list = []
    ALL_USERS: list = []
    UUID_SELECTED: str = ""

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

    def create_secret(self, nbr: int):
        """
        To create a random string
        :param nbr: number of character to the random string
        :return:
        """
        res = "".join(secrets.choice(string.ascii_letters + string.digits) for x in range(nbr))
        return res

    def read_by_key_multiple(self, data: list, key_1: str, key_2: str, key_3: str,
                             value_1: str, value_2: str, value_3: str):
        return list(filter(lambda elements: elements[f"{key_1}"].lower() == value_1.lower() and
                                            elements[f"{key_2}"].lower() == value_2.lower() and
                                            elements[f"{key_3}"].lower() == value_3.lower(), data))

    def read_by_key(self, data: list, key: str, value: str):
        return list(filter(lambda elements: elements[f"{key}"].lower() == value.lower(), data))

    def get_semestre_grand(self, semestre: list) -> str:
        if len(semestre) == 1:
            return semestre[0]
        return semestre[1]

    def get_semestre_petit(self, semestre: list) -> str:
        if len(semestre) == 1:
            return ""
        return semestre[0]

    def on_cancel(self, instance, value):
        """Events called when the "CANCEL" dialog box button is clicked."""

    def on_save_cin(self, instance, value, date_range):
        MDApp.get_running_app().DATE_TEXTE = value

    def show_date_picker_cin(self):
        date_dialog = MDDatePicker(min_year=1980, max_year=2030)
        date_dialog.bind(on_save=self.on_save_cin, on_cancel=self.on_cancel)
        date_dialog.open()

    def test_string(self, text: str = "") -> str:
        if text == "" or text == "None":
            return ""
        return text

    def get_list_parcours(self) -> list:
        parcours = []
        host = MDApp.get_running_app().HOST
        token = MDApp.get_running_app().TOKEN
        uuid_mention = MDApp.get_running_app().MENTION
        url_parcours: str = f'http://{host}/api/v1/parcours/by_mention/'
        response = request_utils.get_with_params(url_parcours, ["uuid_mention"], [uuid_mention], token)
        if response:
            MDApp.get_running_app().ALL_PARCOURS = response
            for rep in response:
                parcours.append(str(rep['abreviation']))
        return parcours

    def transform_data(self, list_key: list, all_data: list):
        data = []
        k: int = 1
        if len(all_data) != 0:
            for on_data in all_data:
                data_value = [k]
                for key in list_key:
                    data_value.append(on_data[key])
                data.append(tuple(data_value))
                k += 1
        data_vide = [""]
        for key in list_key:
            data_vide.append("")
        data.append(tuple(data_vide))
        return data

    def logout(seld):
        MDApp.get_running_app().root.current = 'Login'
        MDApp.get_running_app().TOKEN = ""
        MDApp.get_running_app().TITRE_FILE = ""
        MDApp.get_running_app().PARENT = ""
        MDApp.get_running_app().ALL_UUID_MENTION = []
        MDApp.get_running_app().ALL_MENTION = []
        MDApp.get_running_app().ALL_PARCOURS = []
        MDApp.get_running_app().ALL_ETUDIANT = []
        MDApp.get_running_app().MENTION = ""
        MDApp.get_running_app().NUM_CARTE = ""
        MDApp.get_running_app().URL_DOWNLOAD = ""
        MDApp.get_running_app().NAME_DOWNLOAD = ""
        MDApp.get_running_app().IS_INITIALISE = False
        MDApp.get_running_app().PUBLIC_TITRE = ""


ScienceApp().run()
