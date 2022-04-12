import threading
import time
import urllib
from typing import Any

from kivy.clock import mainthread
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton, MDIconButton
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.spinner import MDSpinner
from kivymd.toast import toast

from all_requests import request_utils
from concurrent.futures import ThreadPoolExecutor, as_completed


def transforme_data(all_data: list):
    data = []
    k: int = 1
    for un_et in all_data:
        if un_et["sexe"] == "MASCULIN":
            if un_et["etat"] == "Passant":
                logo = ("face-profile",
                        [39 / 256, 174 / 256, 96 / 256, 1], un_et["num_carte"])
            else:
                logo = ("face-profile", [1, 0, 0, 1], un_et["num_carte"])
        else:
            if un_et["etat"] == "Passant":
                logo = ("face-woman",
                        [39 / 256, 174 / 256, 96 / 256, 1], un_et["num_carte"])
            else:
                logo = ("face-woman", [1, 0, 0, 1], un_et["num_carte"])
        etudiant = (k, logo, f'{un_et["nom"]} {un_et["prenom"]}', (un_et["parcours"]).upper())

        data.append(etudiant)
        k += 1
    data.append(("", "", "", ""))
    return data


def read_by_semestre_and_parcours(data: list, parcours: str, semestre: str):
    return list(filter(lambda etudiant: etudiant["parcours"].lower() == parcours.lower() and (
            etudiant["semestre_petit"] == semestre or etudiant["semestre_grand"] == semestre), data))


def find_key(lettre: str, key: str):
    value = lettre.lower()
    key_value = key.lower()
    return value.find(key_value)


class ReinscriptionScreen(Screen):
    screenManager = ObjectProperty(None)
    dialog = None

    def __init__(self, **kw):
        super().__init__(**kw)
        self.initialise_table = True
        self.all_parcours = []
        self.spinner = None
        self.menu_etat = None
        self.menu_nation = None
        self.menu_sexe = None
        self.menu_list = None
        self.menu_carte = None
        self.semestre = None
        self.all_semestre = None
        self.data_tables = None
        self.delete_etudiant = None
        self.edit_etudiant = None
        self.annee = None
        self.menu_semestre = None
        self.menu_annee_univ = None
        self.titre = None
        self.menu_mention = None
        self.menu_parcours = None
        self.initialise = True

        # self.search = MDTextField(
        #     hint_text="Recherche",
        #     size_hint_x=None,
        #     pos=(20, 125),
        #     width=250,
        #     pos_hint={'center_y': 0.95, 'center_x': 0.18},
        # )

    def init_data(self):

        self.menu_mention = MDDropdownMenu(
            caller=self.ids.mention_button,
            items=self.get_all_mention(),
            width_mult=4,
        )

        self.menu_semestre = MDDropdownMenu(
            caller=self.ids.semestre_button,
            items=self.get_all_semestre(),
            width_mult=4,
        )
        self.menu_parcours = MDDropdownMenu(
            caller=self.ids.parcours_button,
            items=self.get_all_parcours(),
            width_mult=4,
        )

        self.menu_annee_univ = MDDropdownMenu(
            caller=self.ids.annee_button,
            items=self.get_annee_univ(),
            width_mult=4,
        )
        carte = ['Face carte', 'Arriere carte']
        menu_carte = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{i}",
                "height": dp(50),
                "on_release": lambda x=f"{i}": self.menu_calback_carte(x),
            } for i in carte
        ]
        titre = ['Étudiant inscrit', 'Bourse passant', 'Bourse rédoublant']
        menu_list = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{i}",
                "height": dp(50),
                "on_release": lambda x=f"{i}": self.menu_calback_list(x),
            } for i in titre
        ]

        self.menu_carte = MDDropdownMenu(
            items=menu_carte,
            width_mult=4,
        )

        self.menu_list = MDDropdownMenu(
            items=menu_list,
            width_mult=4,
        )

        self.titre = MDLabel(text="Liste des étudiants:",
                             pos_hint={'center_y': 0.95, 'center_x': 0.5},
                             text_size="12dp",
                             halign="center"
                             )

        self.annee = MDLabel(text=MDApp.get_running_app().ANNEE,
                             pos_hint={'center_y': 0.95, 'center_x': 0.61},
                             text_size="12dp",
                             halign="center"
                             )

        self.edit_etudiant = MDIconButton(
            icon="account-edit",
            pos_hint={'center_y': 0.95, 'center_x': 0.9},
            opacity=0,
            disabled=True,
            on_release=self.update_etudiant
        )

        self.spinner = MDSpinner(
            pos_hint={'center_y': 0.5, 'center_x': 0.5},
            size_hint=(None, None),
            size=(dp(30), dp(30)),
            active=False
        )

        self.delete_etudiant = MDIconButton(
            icon="delete",
            opacity=0,
            pos_hint={'center_y': 0.95, 'center_x': 0.95},
            on_release=self.show_dialog
        )
        # self.add_widget(self.search)
        self.add_widget(self.titre)
        self.add_widget(self.annee)
        self.add_widget(self.edit_etudiant)
        self.add_widget(self.delete_etudiant)
        self.add_widget(self.spinner)

    def load_table(self):
        layout = AnchorLayout()
        self.data_tables = MDDataTable(
            pos_hint={'center_y': 0.55, 'center_x': 0.5},
            size_hint=(0.98, 0.75),
            use_pagination=True,
            rows_num=7,
            column_data=[
                ("N°", dp(20)),
                ("CE", dp(30)),
                ("Nom et prénom", dp(120)),
                ("Parcours", dp(20))],
        )
        self.data_tables.bind(on_row_press=self.row_selected)
        self.add_widget(self.data_tables)
        return layout

    def active_button(self, *args):
        self.edit_etudiant.opacity = 1
        self.edit_etudiant.disabled = False
        self.edit_etudiant.md_bg_color = (0, 0, 0, 0)
        self.delete_etudiant.opacity = 1
        self.delete_etudiant.disabled = False
        self.delete_etudiant.md_bg_color = (0, 0, 0, 0)

    def inactive_button(self, *args):
        self.edit_etudiant.opacity = 0
        self.edit_etudiant.disabled = True
        self.edit_etudiant.md_bg_color = (0, 0, 0, 0)
        self.delete_etudiant.opacity = 0
        self.delete_etudiant.disabled = True
        self.delete_etudiant.md_bg_color = (0, 0, 0, 0)

    def on_enter(self):
        if self.initialise:
            if self.initialise_table:
                self.load_table()
                self.initialise_table = False
            self.init_data()
            self.initialise = False
            self.inactive_button()
        else:
            MDApp.get_running_app().NUM_CARTE = ""

        self.data_tables.row_data = transforme_data(MDApp.get_running_app().ALL_ETUDIANT)

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

    def get_all_parcours(self, *args):
        """
        add al parcours in menu
        :return:
        """
        parcours = MDApp.get_running_app().get_list_parcours()

        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{parcours[i].upper()}",
                "height": dp(50),
                "on_release": lambda x=f"{parcours[i].upper()}": self.menu_calback_parcours(i, x),
            } for i in range(len(parcours))
        ]
        return menu_items

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

    def menu_calback_mention(self, text_item):
        mention = MDApp.get_running_app().read_by_key(
            MDApp.get_running_app().ALL_MENTION, 'title', text_item)[0]['uuid']
        if (MDApp.get_running_app().MENTION != mention or not self.initialise) and self.annee.text != "":
            start = time.time()
            MDApp.get_running_app().MENTION = mention
            self.spinner_toggle()
            self.process_spinner_toogle()
            self.spinner_toggle()

            self.menu_parcours = MDDropdownMenu(
                caller=self.ids.parcours_button,
                items=self.get_all_parcours(),
                width_mult=4,
            )
            self.initialise = True
            self.ids.mention_label.text = text_item
            self.menu_mention.dismiss()
            print(f'Time taken: {time.time() - start}')
        self.menu_mention.dismiss()

    @mainthread
    def spinner_toggle(self):
        print(self.spinner.active)
        if not self.spinner.active:
            self.spinner.active = True
        else:
            self.spinner.active = False

    def insert_data(self):
        self.data_tables.row_data = []
        self.data_tables.row_data = transforme_data(MDApp.get_running_app().ALL_ETUDIANT)

    def get_data(self):
        self.initialise = False
        annee = MDApp.get_running_app().ANNEE
        schemas = "anne_" + annee[0:4] + "_" + annee[5:9]
        host = MDApp.get_running_app().HOST
        token = MDApp.get_running_app().TOKEN
        uuid_mention = MDApp.get_running_app().MENTION
        url_etudiant: str = f'http://{host}/api/v1/ancien_etudiants/by_mention/'
        list_key = ["schema", "uuid_mention"]
        list_value = [schemas, uuid_mention]
        response = request_utils.get_with_params(url_etudiant, list_key, list_value, token)
        if response:
            if response[1] == 200:
                MDApp.get_running_app().ALL_ETUDIANT = response[0]
            elif response[1] == 400:
                toast(str(response[0]))
            else:
                toast(str(response))

    def process_spiner(self):
        processes = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            processes.append(executor.submit(get_parcours))
            processes.append(executor.submit(self.get_data))
        self.insert_data()
        self.spinner_toggle()

    def process_spinner_toogle(self):
        self.spinner_toggle()
        threading.Thread(target=(
            self.process_spiner)).start()

    def menu_calback_parcours(self, i, text_item):
        self.ids.parcours_label.text = text_item
        all_etudiant = MDApp.get_running_app().read_by_key(MDApp.get_running_app().ALL_ETUDIANT, "parcours", text_item)
        self.data_tables.row_data = transforme_data(all_etudiant)
        self.menu_parcours.dismiss()

    def menu_calback_semestre(self, text_item):
        self.ids.semestre_label.text = text_item
        parcours = self.ids.parcours_label.text
        all_etudiant = read_by_semestre_and_parcours(MDApp.get_running_app().ALL_ETUDIANT, parcours, text_item)
        self.data_tables.row_data = transforme_data(all_etudiant)
        self.menu_semestre.dismiss()

    def menu_calback_annee(self, text_item):
        self.annee.text = f"{text_item}"
        MDApp.get_running_app().ANNEE = text_item
        self.menu_annee_univ.dismiss()

    def menu_calback_carte(self, text_item):
        self.menu_carte.dismiss()
        MDApp.get_running_app().TITRE_FILE = f"{text_item}"
        annee = MDApp.get_running_app().ANNEE
        schemas = "anne_" + annee[0:4] + "_" + annee[5:9]
        values = {'schema': f'{schemas}', 'uuid_mention': f'{MDApp.get_running_app().MENTION}'}
        params = urllib.parse.urlencode(values)
        host = MDApp.get_running_app().HOST
        if text_item == "Face carte":
            url = f"http://{host}/api/v1/carte/carte_etudiant/"
        else:
            url = f"http://{host}/api/v1/carte/carte_etudiant_ariere/"
        MDApp.get_running_app().URL_DOWNLOAD = f"{url}?{params}"
        MDApp.get_running_app().NAME_DOWNLOAD = f"{text_item}_{self.ids.mention_label.text}.pdf"
        MDApp.get_running_app().PARENT = "Reinscription"
        if len(annee) != 0:
            MDApp.get_running_app().root.current = 'download_file'

    def calback_carte(self, button):
        self.menu_carte.caller = button
        self.menu_carte.open()

    def menu_calback_list(self, text_item):
        self.menu_list.dismiss()
        MDApp.get_running_app().TITRE_FILE = text_item
        annee = MDApp.get_running_app().ANNEE
        mention = MDApp.get_running_app().MENTION
        parcours = MDApp.get_running_app().read_by_key(MDApp.get_running_app().ALL_PARCOURS, "abreviation",
                                                       self.ids.parcours_label.text)
        uuid_parcours = ""
        if parcours:
            uuid_parcours = parcours[0]['uuid']
        semestre = self.ids.semestre_label.text
        schemas = "anne_" + annee[0:4] + "_" + annee[5:9]
        host = MDApp.get_running_app().HOST
        MDApp.get_running_app().NAME_DOWNLOAD = f"{text_item}_{self.ids.mention_label.text}.pdf"
        if text_item == "Étudiant inscrit":
            url = f"http://{host}/api/v1/liste/list_inscrit/"
            values = {'schema': f'{schemas}', 'uuid_mention': f'{mention}', 'uuid_parcours': uuid_parcours,
                      'semestre': semestre}
            MDApp.get_running_app().NAME_DOWNLOAD = f"{text_item}_{self.ids.parcours_label.text}_{semestre}.pdf"
        elif text_item == "Bourse passant":
            url = f"http://{host}/api/v1/liste/list_bourse_passant/"
            values = {'schema': f'{schemas}', 'uuid_mention': f'{mention}'}
        else:
            url = f"http://{host}/api/v1/liste/list_bourse_redoublant/"
            values = {'schema': f'{schemas}', 'uuid_mention': f'{mention}'}

        params = urllib.parse.urlencode(values)
        MDApp.get_running_app().URL_DOWNLOAD = f"{url}?{params}"
        MDApp.get_running_app().PARENT = "Reinscription"
        if len(annee) != 0 and len(mention) != 0 and len(semestre) != 0 and len(uuid_parcours) != 0:
            MDApp.get_running_app().root.current = 'download_file'

    def calback_list(self, button):
        self.menu_list.caller = button
        self.menu_list.open()

    def row_selected(self, table, row):
        start_index, end_index = row.table.recycle_data[row.index]["range"]
        num_carte = row.table.recycle_data[start_index + 1]["text"]
        if len(num_carte) != 0:
            MDApp.get_running_app().NUM_CARTE = num_carte
            self.active_button()
        else:
            self.inactive_button()

    def show_dialog(self, *args):
        # if not self.dialog:
        # create dialog
        self.dialog = MDDialog(
            title="Attention!",
            text=f"Voulez-vous supprimer {MDApp.get_running_app().NUM_CARTE} ?",
            buttons=[
                MDFlatButton(
                    text="Ok",
                    on_release=self.delete_etudiant_
                ),
                MDFlatButton(
                    text="Annuler",
                    on_release=self.cancel_dialog
                ),
            ],
        )
        self.dialog.open()

    def delete_etudiant_(self, *args):
        host = MDApp.get_running_app().HOST
        token = MDApp.get_running_app().TOKEN
        annee = MDApp.get_running_app().ANNEE
        num_carte = MDApp.get_running_app().NUM_CARTE

        url = f"http://{host}/api/v1/ancien_etudiants/"
        if num_carte != "":
            schemas = "anne_" + annee[0:4] + "_" + annee[5:9]
            list_key = ["shemas", "num_carte"]
            list_value = [schemas, num_carte]
            response = request_utils.delete_with_params(url, list_key, list_value, token)
            if response:
                if response[1] == 200:
                    self.reset_champs()
                    MDApp.get_running_app().ALL_ETUDIANT = response[0]
                    toast(f"{num_carte} bien supprimé")
                    MDApp.get_running_app().NUM_CARTE = ""
                    self.data_tables.row_data = transforme_data(MDApp.get_running_app().ALL_ETUDIANT)
                elif response[1] == 400:
                    toast(str(response[0]))
                else:
                    toast(str(response))
            self.dialog.dismiss()

    def cancel_dialog(self, *args):
        self.dialog.dismiss()

    def back_main(self):
        MDApp.get_running_app().root.current = 'Main'
        MDApp.get_running_app().IS_INITIALISE = False

    def add_new_etudiant(seld):
        MDApp.get_running_app().REINSCRIPTION_ACTION_TYPE = "ADD"
        MDApp.get_running_app().root.current = 'Reinscription_add'

    def update_etudiant(self, *args):
        MDApp.get_running_app().REINSCRIPTION_ACTION_TYPE = "UPDATE"
        MDApp.get_running_app().root.current = 'Reinscription_add'

    def search_etudiant(self, titre: str):
        data = MDApp.get_running_app().ALL_ETUDIANT
        value = list(
            filter(lambda mention: find_key(mention["num_carte"], titre) != -1 or
                                   find_key(mention["nom"], titre) != -1 or
                                   find_key(mention["prenom"], titre) != -1 or
                                   find_key(mention["adresse"], titre) != -1 or
                                   find_key(mention["sexe"], titre) != -1 or
                                   find_key(mention["etat"], titre) != -1 or
                                   find_key(mention["parcours"], titre) != -1,
                   data))
        self.data_tables.row_data = transforme_data(value)


def get_parcours():
    MDApp.get_running_app().get_list_parcours()
