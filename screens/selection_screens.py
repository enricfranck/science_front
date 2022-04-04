import threading
import time
import urllib

from kivy.clock import mainthread
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivymd.toast import toast
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.spinner import MDSpinner

from all_requests import request_etudiants
from concurrent.futures import ThreadPoolExecutor, as_completed


class SelectionScreen(Screen):
    screenManager = ObjectProperty(None)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.spinner = None
        self.delete_etudiant = None
        self.annee = None
        self.titre = None
        self.dialog = None
        self.edit_etudiant = None
        self.menu_niveau = None
        self.initialise = True
        self.data_tables = None
        self.menu_annee_univ = None
        self.menu_mention = None
        self.menu_semestre = None

    def logout(seld):
        MDApp.get_running_app().root.current = 'Login'

    def init_data(self):

        self.menu_mention = MDDropdownMenu(
            caller=self.ids.mention_button,
            items=self.get_all_mention(),
            width_mult=4,
        )

        menu_niveau = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{i}",
                "height": dp(50),
                "on_release": lambda x=f"{i}": self.menu_calback_niveau(x),
            } for i in MDApp.get_running_app().ALL_NIVEAU_SELECT
        ]

        self.menu_niveau = MDDropdownMenu(
            caller=self.ids.niveau_button,
            items=menu_niveau,
            width_mult=4,
        )

        self.menu_annee_univ = MDDropdownMenu(
            caller=self.ids.annee_button,
            items=self.get_annee_univ(),
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
                ("selectioné", dp(20))],
        )
        self.data_tables.bind(on_row_press=self.row_selected)
        self.add_widget(self.data_tables)
        return layout

    def on_enter(self):
        if self.initialise:
            self.load_table()
            self.init_data()
            self.initialise = False
        else:
            MDApp.get_running_app().NUM_CARTE = ""
            self.inactive_button()
        self.data_tables.row_data = self.transforme_data(MDApp.get_running_app().ALL_ETUDIANT_SELECTIONNER)

    def back_main(self):
        MDApp.get_running_app().root.current = 'Main'

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

    def row_selected(self, table, row):
        start_index, end_index = row.table.recycle_data[row.index]["range"]
        num_select = row.table.recycle_data[start_index + 1]["text"]
        if num_select != "":
            MDApp.get_running_app().NUM_SELECT = num_select
            self.active_button()
        else:
            MDApp.get_running_app().NUM_SELECT = num_select
            self.inactive_button()

    def get_all_mention(self):
        mention = MDApp.get_running_app().ALL_MENTION
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{mention[i]['title']}",
                "height": dp(50),
                "on_release": lambda x=f"{mention[i]['title']}": self.menu_calback_mention(x),
            } for i in range(len(mention))
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

    def update_etudiant(self, *args):
        MDApp.get_running_app().root.current = 'SelectionUpdate'

    def show_dialog(self):
        pass

    def transforme_data(self, all_data: list):
        data = []
        k: int = 1
        for un_et in all_data:
            if un_et["select"]:
                logo = ("checkbox-marked-circle",
                        [39 / 256, 174 / 256, 96 / 256, 1], "Oui")
            else:
                logo = ("alert", [1, 0, 0, 1], "Non")

            etudiant = (k, ("human-female",
                            [39 / 256, 174 / 256, 96 / 256, 1], un_et["num_select"]),
                        f'{un_et["nom"]} {un_et["prenom"]}', logo)

            data.append(etudiant)
            k += 1
        data.append(("", "", "", ""))
        return data

    def menu_calback_mention(self, text_item):
        mention = MDApp.get_running_app().read_by_key(
            MDApp.get_running_app().ALL_MENTION, 'title', text_item)[0]['uuid']
        if (MDApp.get_running_app().MENTION != mention or not self.initialise) and self.annee.text != "":
            start = time.time()
            MDApp.get_running_app().MENTION = mention
            self.spinner_toggle()
            self.process_spinner_toogle()
            self.spinner_toggle()
            self.initialise = True
            self.ids.mention_label.text = text_item
            self.menu_mention.dismiss()
            print(f'Time taken: {time.time() - start}')
        self.menu_mention.dismiss()

    def read_mention_by_title(self, data: list, titre: str):
        return list(filter(lambda mention: mention["title"].lower() == titre.lower(), data))

    def insert_data(self):
        self.data_tables.row_data = self.transforme_data(MDApp.get_running_app().ALL_ETUDIANT_SELECTIONNER)

    @mainthread
    def spinner_toggle(self):
        if not self.spinner.active:
            self.spinner.active = True
        else:
            self.spinner.active = False

    def process_spiner(self):
        time.sleep(2)
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

    def get_data(self):
        self.initialise = False
        host = MDApp.get_running_app().HOST
        token = MDApp.get_running_app().TOKEN
        uuid_mention = MDApp.get_running_app().MENTION
        url_etudiant: str = f'http://{host}/api/v1/nouveau_etudiants/by_mention/'
        MDApp.get_running_app().ALL_ETUDIANT_SELECTIONNER = request_etudiants.get_by_mention(
            url_etudiant,
            self.annee.text,
            uuid_mention, token)

    def menu_calback_annee(self, text_item):
        self.annee.text = f"{text_item}"
        MDApp.get_running_app().ANNEE = text_item
        self.menu_annee_univ.dismiss()

    def menu_calback_niveau(self, text_item):
        self.ids.niveau_label.text = text_item
        ALL_ETUDIANT_SELECTIONNER = MDApp.get_running_app().read_by_key(
            MDApp.get_running_app().ALL_ETUDIANT_SELECTIONNER, "niveau", text_item)
        self.data_tables.row_data = self.transforme_data(ALL_ETUDIANT_SELECTIONNER)
        self.menu_niveau.dismiss()

    # def read_by_niveau(self, data: list, key: str, niveau: str):
    #     return list(filter(lambda etudiant: etudiant[f"{key}"].lower() == niveau.lower(), data))

    def add_new_etudiant(self):
        MDApp.get_running_app().root.current = 'SelectionAdd'

    def find_key(self, lettre: str, key: str):
        value = lettre.lower()
        key_value = key.lower()
        return value.find(key_value)

    def serch_etudiant(self, titre: str):
        data = MDApp.get_running_app().ALL_ETUDIANT_SELECTIONNER
        value = list(
            filter(lambda mention: self.find_key(mention["num_select"], titre) != -1 or
                                   self.find_key(mention["nom"], titre) != -1 or
                                   self.find_key(mention["prenom"], titre) != -1 or
                                   self.find_key(mention["adresse"], titre) != -1 or
                                   self.find_key(mention["sexe"], titre) != -1,
                   data))
        self.data_tables.row_data = self.transforme_data(value)

    def menu_calback_list(self, *args):
        text_item = "Sélection de dossier"
        MDApp.get_running_app().TITRE_FILE = text_item
        annee = MDApp.get_running_app().ANNEE
        mention = MDApp.get_running_app().MENTION
        schemas = "anne_" + annee[0:4] + "_" + annee[5:9]
        host = MDApp.get_running_app().HOST
        MDApp.get_running_app().NAME_DOWNLOAD = f"{text_item}_{self.ids.mention_label.text}.pdf"
        url = f"http://{host}/api/v1/liste/list_selection/"
        values = {'schema': f'{schemas}', 'uuid_mention': f'{mention}'}
        params = urllib.parse.urlencode(values)
        MDApp.get_running_app().URL_DOWNLOAD = f"{url}?{params}"
        MDApp.get_running_app().PARENT = "Selection"
        if len(annee) != 0 and len(mention) != 0:
            MDApp.get_running_app().root.current = 'download_file'

    def show_dialog(self, *args):
        if not self.dialog:
            # create dialog
            self.dialog = MDDialog(
                title="Attention!",
                text=f"Voulez-vous supprimer {MDApp.get_running_app().NUM_SELECT} ?",
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
        num_select = MDApp.get_running_app().NUM_SELECT
        etudiant = MDApp.get_running_app().read_by_key(MDApp.get_running_app().ALL_ETUDIANT_SELECTIONNER, "num_select",
                                                       num_select)[0]["num_quitance"]
        url = f"http://{host}/api/v1/nouveau_etudiants/"
        if str(etudiant) == "" or str(etudiant) == "None":
            if num_select != "":
                response = request_etudiants.delete(url, annee, "num_select", num_select, token)
                if response:
                    self.dialog.dismiss()
                    MDApp.get_running_app().ALL_ETUDIANT_SELECTIONNER = response
                    toast(f"{num_select} bien supprimé")
                    MDApp.get_running_app().NUM_SELECT = ""
                    self.data_tables.row_data = self.transforme_data(MDApp.get_running_app().ALL_ETUDIANT_SELECTIONNER)
        else:
            self.dialog.dismiss()
            toast("Impossible de supprimer l'etudiant(e)")

    def cancel_dialog(self, *args):
        self.dialog.dismiss()


def get_parcours():
    MDApp.get_running_app().get_list_parcours()
