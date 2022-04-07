from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp


class ScolaScreen(Screen):
    screenManager = ObjectProperty(None)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.menu_semestre = None
        self.menu_annee_univ = None
        self.menu_list = None

    def back_home(self):
        MDApp.get_running_app().root.current = 'Main'

    def init_data(self):
        self.menu_semestre = MDDropdownMenu(
            caller=self.ids.semestre,
            items=self.get_all_semestre(),
            width_mult=4,
        )

        self.menu_annee_univ = MDDropdownMenu(
            caller=self.ids.annee,
            items=self.get_annee_univ(),
            width_mult=4,
        )
        titre = ["Certificat de Scolarité",
                 "Certificat d'asuidité",
                 "Attestation d'inscription",
                 ""]
        menu_lists = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{i}",
                "height": dp(50),
                "on_release": lambda x=f"{i}": self.menu_calback_list(x),
            } for i in titre
        ]

        self.menu_list = MDDropdownMenu(
            items=menu_lists,
            width_mult=4,
        )

    def on_enter(self, *args):
        self.init_data()

    def get_annee_univ(self):
        annee_univ = MDApp.get_running_app().ALL_ANNEE

        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{annee_univ[i]['title']}",
                "height": dp(50),
                "on_release": lambda x=f"{annee_univ[i]['title']}": self.menu_calback_annee(x),
            } for i in range(len(annee_univ))
        ]
        return menu_items

    def menu_calback_annee(self, text_item):
        self.ids.annee.text = f"{text_item}"
        MDApp.get_running_app().ANNEE = text_item
        self.menu_annee_univ.dismiss()

    def get_all_semestre(self):
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"S{i + 1}",
                "height": dp(50),
                "on_release": lambda x=f"S{i + 1}": self.menu_calback_semestre(x),
            } for i in range(9)
        ]
        return menu_items

    def menu_calback_semestre(self, text_item):
        self.ids.semestre.text = text_item
        self.menu_semestre.dismiss()

    def menu_calback_list(self, text_item):
        self.menu_list.dismiss()
        MDApp.get_running_app().TITRE_FILE = text_item

    def calback_list(self, button):
        self.menu_list.caller = button
        self.menu_list.open()

    def active_semestre(self):
        self.ids.semestre.disable = False
        self.ids.save.disable = True
        self.ids.save_relever.disable = False
        self.ids.save_relever.opacity = 1
        self.ids.save.opacity = 0

    def inactive_semestre(self):
        self.ids.semestre.disable = True
        self.ids.save.disable = False
        self.ids.save_relever.disable = True
        self.ids.save_relever.opacity = 0
        self.ids.save.opacity = 1
