from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
import urllib


class ScolaScreen(Screen):
    screenManager = ObjectProperty(None)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.menu = None
        self.menu_mention = None
        self.list_menu = None
        self.menu_list_stats = None
        self.values = None
        self.url = None
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
                 "Certificat d'assiduité",
                 "Attestation d'inscription",
                 "Validation de credit",
                 "Relever des notes"]
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
            caller=self.ids.type,
        )

        titre_stat = ["Statistique total",
                      "Statistique par âge",
                      "Statistique par nationalité",
                      "Etudiant diplomé",
                      "Renseignement",
                      "Etudiant bachelier"]
        menu_list_stats_ = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{i}",
                "height": dp(50),
                "on_release": lambda x=f"{i}": self.menu_calback_list_stats(x),
            } for i in titre_stat
        ]

        self.menu_list_stats = MDDropdownMenu(
            items=menu_list_stats_,
            width_mult=4,
            caller=self.ids.stats,
        )

        menu = ["Statistique", "Certificat"]
        menu_list = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{i}",
                "height": dp(50),
                "on_release": lambda x=f"{i}": self.calback_list_menu(x),
            } for i in menu
        ]

        self.list_menu = MDDropdownMenu(
            items=menu_list,
            width_mult=4,
        )

        self.menu_mention = MDDropdownMenu(
            caller=self.ids.mention,
            items=self.get_all_mention(),
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
        self.reset_champs()
        MDApp.get_running_app().ANNEE = text_item
        if self.menu == "Statistique":
            self.ids.mention.disabled = False
            self.ids.mention.opacity = 1
            self.ids.num_carte.disabled = True
            self.ids.num_carte.opacity = 0
            self.ids.type.disabled = True
            self.ids.type.opacity = 0
            self.ids.stats.disabled = False
            self.ids.stats.opacity = 1
            self.ids.download.opacity = 1

        elif self.menu == "Certificat":
            self.ids.mention.disabled = True
            self.ids.mention.opacity = 0
            self.ids.num_carte.disabled = False
            self.ids.num_carte.opacity = 1
            self.ids.type.disabled = False
            self.ids.type.opacity = 1
            self.ids.save_relever.opacity = 0
            self.ids.save.opacity = 0
            self.ids.stats.disabled = True
            self.ids.stats.opacity = 0
            self.ids.download.opacity = 0
            
        else:
            self.ids.mention.disabled = True
            self.ids.mention.opacity = 0
            self.ids.num_carte.disabled = True
            self.ids.num_carte.opacity = 0
            self.ids.type.disabled = True
            self.ids.save_relever.opacity = 0
            self.ids.save.opacity = 0
            self.ids.type.opacity = 0
            self.ids.stats.disabled = True
            self.ids.stats.opacity = 0
            self.ids.download.opacity = 0
        self.menu_annee_univ.dismiss()

    def get_all_semestre(self):
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"S{i + 1}",
                "height": dp(50),
                "on_release": lambda x=f"S{i + 1}": self.menu_calback_semestre(x),
            } for i in range(10)
        ]
        return menu_items
    
    def get_all_mention(self):
        mention = []
        for titre in MDApp.get_running_app().ALL_MENTION:
            mention.append(titre['title'])
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{mention[i]}",
                "height": dp(50),
                "on_release": lambda x=f"{mention[i]}": self.menu_calback_mention(x),
            } for i in range(len(mention))
        ]
        return menu_items

    def menu_calback_semestre(self, text_item):
        self.ids.semestre.text = text_item
        self.menu_semestre.dismiss()

    def calback_list_menu(self, text_item):
        self.menu = text_item
        self.reset_champs()
        if self.menu == "Statistique" and self.ids.annee.text != "":
            self.ids.mention.disabled = False
            self.ids.mention.opacity = 1
            self.ids.num_carte.disabled = True
            self.ids.num_carte.opacity = 0
            self.ids.type.disabled = True
            self.ids.type.opacity = 0
            self.ids.semestre.opacity = 0
            self.ids.save.opacity = 0
            self.ids.stats.disabled = False
            self.ids.stats.opacity = 1
            self.ids.save_relever.opacity = 0
            self.ids.download.opacity = 1

        elif self.menu == "Certificat" and self.ids.annee.text != "":
            self.ids.mention.disabled = True
            self.ids.mention.opacity = 0
            self.ids.num_carte.disabled = False
            self.ids.num_carte.opacity = 1
            self.ids.type.disabled = False
            self.ids.type.opacity = 1
            self.ids.stats.disabled = True
            self.ids.stats.opacity = 0
            self.ids.download.opacity = 0

        else:
            self.ids.mention.disabled = True
            self.ids.mention.opacity = 0
            self.ids.num_carte.disabled = True
            self.ids.num_carte.opacity = 0
            self.ids.type.disabled = True
            self.ids.type.opacity = 0
            self.ids.stats.disabled = True
            self.ids.stats.opacity = 0
            self.ids.download.opacity = 0
        self.list_menu.dismiss()

    def menu_calback_mention(self, text_item):
        self.ids.mention.text = f"{text_item}"
        mention = MDApp.get_running_app().read_by_key(
            MDApp.get_running_app().ALL_MENTION, 'title', text_item)[0]['uuid']

        MDApp.get_running_app().MENTION = mention
        self.menu_mention.dismiss()

    def menu_calback_list(self, text_item):
        MDApp.get_running_app().TITRE_FILE = text_item
        self.ids.type.text = text_item
        if text_item == "Relever des notes":
            self.ids.semestre.hint_text = "Semestre"
            self.active_semestre()
        elif text_item == "Certificat de Scolarité":
            self.inactive_semestre()
        elif text_item == "Certificat d'assiduité":
            self.ids.semestre.hint_text = "Date d'entrer"
            self.active_semestre()
        elif text_item == "Validation de credit":
            self.ids.semestre.hint_text = "Niveau"
            self.active_semestre()
        else:
            self.inactive_semestre()
        self.menu_list.dismiss()

    def menu_calback_list_stats(self, text_item):
        MDApp.get_running_app().TITRE_FILE = text_item
        self.ids.stats.text = text_item
        self.menu_list_stats.dismiss()

    def calback_menu(self, button):
        self.list_menu.caller = button
        self.list_menu.open()

    def active_semestre(self):
        self.ids.semestre.opacity = 1
        self.ids.semestre.disabled = False
        self.ids.save_relever.opacity = 1
        self.ids.save.opacity = 0

    def inactive_semestre(self):
        self.ids.semestre.opacity = 0
        self.ids.semestre.disabled = True
        self.ids.save_relever.opacity = 0
        self.ids.save.opacity = 1

    def enreg_releve(self):
        annee = MDApp.get_running_app().ANNEE
        schemas = "anne_" + annee[0:4] + "_" + annee[5:9]
        host = MDApp.get_running_app().HOST
        text_item = self.ids.type.text
        MDApp.get_running_app().NAME_DOWNLOAD = f"{text_item}_{self.ids.num_carte.text}.pdf"
        if text_item == "Relever des notes":
            self.values = {'schemas': f'{schemas}', 'num_carte': f'{self.ids.num_carte.text}',
                           "semestre": f'{self.ids.semestre.text.upper()}'}
            self.url = f"http://{host}/api/v1/scolarites/relever"
        elif text_item == "Certificat d'assiduité":
            self.values = {'schema': f'{schemas}', 'num_carte': f'{self.ids.num_carte.text}',
                           "rentrer": f'{self.ids.semestre.text}'}
            self.url = f"http://{host}/api/v1/scolarites/assiduite"
        elif text_item == "Validation de credit":
            self.values = {'schema': f'{schemas}', 'num_carte': f'{self.ids.num_carte.text}',
                           "niveau": f'{self.ids.semestre.text.upper()}'}
            self.url = f"http://{host}/api/v1/scolarites/validation_credit"
        params = urllib.parse.urlencode(self.values)
        MDApp.get_running_app().URL_DOWNLOAD = f"{self.url}?{params}"
        MDApp.get_running_app().PARENT = "Scola"
        MDApp.get_running_app().root.current = 'download_file'
        self.reset_champs()

    def enreg(self):
        annee = MDApp.get_running_app().ANNEE
        schemas = "anne_" + annee[0:4] + "_" + annee[5:9]
        host = MDApp.get_running_app().HOST
        text_item = self.ids.type.text
        MDApp.get_running_app().NAME_DOWNLOAD = f"{text_item}_{self.ids.num_carte.text}.pdf"
        self.values = {'schema': f'{schemas}', 'num_carte': f'{self.ids.num_carte.text}'}
        if text_item == "Certificat de Scolarité":
            self.url = f"http://{host}/api/v1/scolarites/certificat"
        elif text_item == "Attestation d'inscription":
            self.url = f"http://{host}/api/v1/scolarites/attestation_inscription"
        params = urllib.parse.urlencode(self.values)
        MDApp.get_running_app().URL_DOWNLOAD = f"{self.url}?{params}"
        MDApp.get_running_app().PARENT = 'Scola'
        MDApp.get_running_app().root.current = 'download_file'
        self.reset_champs()

    def enreg_stats(self):
        annee = MDApp.get_running_app().ANNEE
        schemas = "anne_" + annee[0:4] + "_" + annee[5:9]
        host = MDApp.get_running_app().HOST
        text_item = self.ids.stats.text
        MDApp.get_running_app().NAME_DOWNLOAD = f"{text_item}_{self.ids.num_carte.text}.pdf"

        self.values = {'schemas': f'{schemas}', 'uuid_mention': MDApp.get_running_app().MENTION}
        if text_item == "Statistique total":
            self.url = f"http://{host}/api/v1/statistic/all_statistic/"
        elif text_item == "Statistique par âge":
            self.url = f"http://{host}/api/v1/statistic/statistic_by_years/"
        elif text_item == "Statistique par nationalité":
            self.url = f"http://{host}/api/v1/statistic/statistic_by_nation/"
        elif text_item == "Etudiant diplomé":
            self.url = f"http://{host}/api/v1/statistic/statistic_by_diplome/"
        elif text_item == "Renseignement":
            self.url = f"http://{host}/api/v1/statistic/renseignement/"
        else:
            self.url = f"http://{host}/api/v1/statistic/bachelier/"

        params = urllib.parse.urlencode(self.values)
        MDApp.get_running_app().URL_DOWNLOAD = f"{self.url}?{params}"
        MDApp.get_running_app().PARENT = 'Scola'
        MDApp.get_running_app().root.current = 'download_file'
        self.reset_champs()

    def reset_champs(self):
        self.ids.num_carte.text = ""
        self.ids.type.text = ""
        self.ids.semestre.text = ""
        self.ids.mention.text = ""
