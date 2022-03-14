from typing import Tuple, Any, List

from kivy.uix.anchorlayout import AnchorLayout
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivymd.material_resources import dp
from kivymd.toast import toast
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.spinner import MDSpinner
from all_requests.request_utils import delete_with_params, create_with_params


class PublicScreen(Screen):
    screenManager = ObjectProperty(None)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.create_note = None
        self.delete_note = None
        self.add_etudiant = None
        self.create = None
        self.menu_session = None
        self.menu_annee = None
        self.dialog = None
        self.menu_matier = None
        self.selected_semestre = None
        self.selected_parcours = None
        self.selected_mention = None
        self.menu_semestre = None
        self.menu_parcours = None
        self.menu_mention = None
        self.edit = None
        self.spinner = None
        self.delete = None
        self.layout = AnchorLayout()
        self.menu_public = None
        self.data_tables = None
        self.key_mention = ['title', 'abreviation', 'branche', 'last_num_carte']
        self.key_parcours = ['title', 'abreviation', 'semestre']
        self.key_role = ["title"]
        self.key_anne = ["title", "moyenne"]
        self.key_ue = ["title", "credit"]
        self.key_ec = ["title", "poids", "value_ue", "utilisateur"]
        self.key_droit = ["niveau", "montant", "annee", "mention"]
        self.key_users = ["email", "prenom", "role", "mention"]
        self.initialise = True
        self.uuid_selected = ""
        self.all_column = []

    def init_data(self):
        self.edit = MDIconButton(
            icon="pen",
            pos_hint={'center_y': 0.95, 'center_x': 0.9},
            opacity=0,
            disabled=True,
            on_release=self.update
        )

        self.spinner = MDSpinner(
            pos_hint={'center_y': 0.5, 'center_x': 0.5},
            size=(dp(46), dp(46)),
            active=False
        )

        self.delete = MDIconButton(
            icon="delete",
            opacity=1,
            pos_hint={'center_y': 0.95, 'center_x': 0.95},
            on_release=self.show_dialog
        )

        self.create_note = MDIconButton(
            icon="plus-circle",
            opacity=1,
            pos_hint={'center_y': 0.14, 'center_x': 0.05},
            on_release=self.create_table_note
        )

        self.add_etudiant = MDIconButton(
            icon="playlist-edit",
            opacity=1,
            pos_hint={'center_y': 0.14, 'center_x': 0.1},
            on_release=self.add_etudiants
        )

        self.delete_note = MDIconButton(
            icon="delete",
            opacity=1,
            pos_hint={'center_y': 0.14, 'center_x': 0.15},
            on_release=self.show_dialog
        )

        self.menu_mention = MDDropdownMenu(
            caller=self.ids.mention,
            items=self.get_all_mention(),
            width_mult=4,
        )

        self.menu_annee = MDDropdownMenu(
            caller=self.ids.annee,
            items=self.get_all_annne(),
            width_mult=4,
        )

        self.menu_parcours = MDDropdownMenu(
            caller=self.ids.parcours,
            items=self.get_all_parcours(),
            width_mult=4,
        )

        self.menu_semestre = MDDropdownMenu(
            caller=self.ids.mention,
            items=self.get_all_semestre(),
            width_mult=4,
        )

        self.menu_matier = MDDropdownMenu(
            caller=self.ids.matier,
            items=self.get_all_matier(),
            width_mult=4,
        )

        self.menu_session = MDDropdownMenu(
            caller=self.ids.matier,
            items=self.get_all_session(),
            width_mult=4,
        )

        self.add_widget(self.edit)
        self.add_widget(self.delete)
        self.add_widget(self.create_note)
        self.add_widget(self.delete_note)
        self.add_widget(self.add_etudiant)

        self.ids.annee.text = MDApp.get_running_app().ALL_ANNEE[0]['title']
        MDApp.get_running_app().ANNEE = self.ids.annee.text

    def load_table(self):
        """
        This methode is use for load the data table
        :return:
        """
        self.data_tables = MDDataTable(
            pos_hint={'center_y': 0.55, 'center_x': 0.5},
            size_hint=(0.98, 0.75),
            column_data=[],
        )

        # self.data_tables.bind(on_row_press=self.row_selected)
        self.add_widget(self.data_tables)
        return self.layout

    def active_button(self, *args):
        self.edit.opacity = 1
        self.edit.disabled = False
        self.edit.md_bg_color = (0, 0, 0, 0)
        self.delete.opacity = 1
        self.delete.disabled = False
        self.delete.md_bg_color = (0, 0, 0, 0)

    def active_button_note(self, *args):
        self.create_note.opacity = 1
        self.create_note.disabled = False
        self.create_note.md_bg_color = (0, 0, 0, 0)
        self.add_etudiant.opacity = 1
        self.add_etudiant.disabled = False
        self.add_etudiant.md_bg_color = (0, 0, 0, 0)
        self.delete_note.opacity = 1
        self.delete_note.disabled = False
        self.delete_note.md_bg_color = (0, 0, 0, 0)

    def inactive_button_note(self, *args):
        self.create_note.opacity = 0
        self.create_note.disabled = True
        self.create_note.md_bg_color = (0, 0, 0, 0)
        self.add_etudiant.opacity = 0
        self.add_etudiant.disabled = True
        self.add_etudiant.md_bg_color = (0, 0, 0, 0)
        self.delete_note.opacity = 0
        self.delete_note.disabled = True
        self.delete_note.md_bg_color = (0, 0, 0, 0)

    def inactive_button(self, *args):
        self.edit.opacity = 0
        self.edit.disabled = True
        self.edit.md_bg_color = (0, 0, 0, 0)
        self.delete.opacity = 0
        self.delete.disabled = True
        self.delete.md_bg_color = (0, 0, 0, 0)

    def row_selected(self, table, row):
        start_index, end_index = row.table.recycle_data[row.index]["range"]
        title = row.table.recycle_data[start_index + 1]["text"]
        if title != "" and MDApp.get_running_app().PUBLIC_TITRE != "Note":

            if MDApp.get_running_app().PUBLIC_TITRE == "Montant":
                anne = row.table.recycle_data[start_index + 3]["text"]
                mention = row.table.recycle_data[start_index + 4]["text"]
                data = MDApp.get_running_app().ALL_DROIT
                MDApp.get_running_app().DATA_SELECTED = data
                MDApp.get_running_app().UUID_SELECTED = \
                    MDApp.get_running_app().read_by_key_multiple(data, 'niveau', "annee", "mention",
                                                                 title, anne, mention)[0]['uuid']
            elif MDApp.get_running_app().PUBLIC_TITRE == "UE":
                data = MDApp.get_running_app().ALL_UE
                if self.selected_parcours != "" and self.selected_mention != "" and self.ids.semestre.text != "":
                    MDApp.get_running_app().DATA_SELECTED = data
                    MDApp.get_running_app().UUID_SELECTED = \
                        MDApp.get_running_app().read_by_key_multiples(
                            data, 'title', "uuid_mention", "uuid_parcours",
                            "semestre", title, self.selected_mention,
                            self.selected_parcours, self.ids.semestre.text)[0]['uuid']

            elif MDApp.get_running_app().PUBLIC_TITRE == "EC":
                data = MDApp.get_running_app().ALL_EC
                if self.selected_parcours != "" and self.selected_mention != "" and self.ids.semestre.text != "":
                    MDApp.get_running_app().DATA_SELECTED = data
                    MDApp.get_running_app().UUID_SELECTED = \
                        MDApp.get_running_app().read_by_key_multiples(
                            data, 'title', "uuid_mention", "uuid_parcours",
                            "semestre", title, self.selected_mention,
                            self.selected_parcours, self.ids.semestre.text)[0]['uuid']
            else:
                key = "title"
                if MDApp.get_running_app().PUBLIC_TITRE == "Titre mention":
                    data = MDApp.get_running_app().ALL_MENTION
                elif MDApp.get_running_app().PUBLIC_TITRE == "Titre parcours":
                    data = MDApp.get_running_app().ALL_PARCOURS
                elif MDApp.get_running_app().PUBLIC_TITRE == "Titre role":
                    data = MDApp.get_running_app().ALL_ROLE
                elif MDApp.get_running_app().PUBLIC_TITRE == "Titre année":
                    data = MDApp.get_running_app().ALL_ANNEE
                else:
                    data = MDApp.get_running_app().ALL_USERS
                    key = "email"
                    print(MDApp.get_running_app().ALL_USERS)
                MDApp.get_running_app().DATA_SELECTED = data
                MDApp.get_running_app().UUID_SELECTED = MDApp.get_running_app().read_by_key(
                    data, key, title)[0]['uuid']

            if MDApp.get_running_app().UUID_SELECTED != "":
                self.active_button()
        else:
            MDApp.get_running_app().UUID_SELECTED = ""
            MDApp.get_running_app().DATA_SELECTED = []
            self.inactive_button()

    def on_enter(self, *args):
        list_menu = ["Année universitaire", "Mention", "Parcours", "Role", "Users", "Droit"]
        menu_list = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{i}",
                "height": dp(50),
                "on_release": lambda x=f"{i}": self.menu_calback_list(x),
            } for i in list_menu
        ]
        self.menu_public = MDDropdownMenu(
            items=menu_list,
            width_mult=4,
        )
        if self.ids.annee.text != MDApp.get_running_app().ANNEE:
            MDApp.get_running_app().get_all_ue(MDApp.get_running_app().ANNEE)
            MDApp.get_running_app().get_all_ec(MDApp.get_running_app().ANNEE)
        if self.initialise:
            self.load_table()
            self.init_data()
            self.initialise = False
        self.complet_table()
        self.inactive_button()
        self.inactive_button_note()

    def callback(self, button):
        """
        Use tp show the menu
        :param button:
        :return:
        """
        self.menu_public.caller = button
        self.menu_public.open()

    def menu_calback_list(self, text_item: str):
        """
        Make action for every elements in menu
        :param text_item:
        :return:
        """
        if text_item == "Mention":
            MDApp.get_running_app().PUBLIC_TITRE = "Titre mention"
            self.complet_table()

        elif text_item == "Parcours":
            MDApp.get_running_app().PUBLIC_TITRE = "Titre parcours"
            self.complet_table()

        elif text_item == "Droit":
            MDApp.get_running_app().PUBLIC_TITRE = "Montant"
            self.complet_table()

        elif text_item == "Role":
            MDApp.get_running_app().PUBLIC_TITRE = "Titre role"
            self.complet_table()

        elif text_item == "Année universitaire":
            MDApp.get_running_app().PUBLIC_TITRE = "Titre année"
            self.complet_table()

        elif text_item == "Users":
            MDApp.get_running_app().PUBLIC_TITRE = "Email"
            self.complet_table()

    def complet_table(self):
        if MDApp.get_running_app().PUBLIC_TITRE == "Titre mention":
            data = MDApp.get_running_app().transform_data(self.key_mention, MDApp.get_running_app().ALL_MENTION)
            self.transform_table([
                ('N°', dp(10)),
                ('title', dp(80)),
                ('Abréviation', dp(20)),
                ('branche', dp(50)),
                ('Dérnière CE', dp(20)),
            ], data)

        elif MDApp.get_running_app().PUBLIC_TITRE == "Titre parcours":
            data = MDApp.get_running_app().transform_data(self.key_parcours, MDApp.get_running_app().ALL_PARCOURS)
            self.transform_table([
                ('N°', dp(10)),
                ('title', dp(100)),
                ('Abréviation', dp(20)),
                ('Semestre', dp(50)),
            ], data)

        elif MDApp.get_running_app().PUBLIC_TITRE == "Montant":
            data = MDApp.get_running_app().transform_data(self.key_droit, MDApp.get_running_app().ALL_DROIT)
            self.transform_table([
                ('N°', dp(10)),
                ('Niveau', dp(20)),
                ('Montant', dp(30)),
                ('Année universitaire', dp(40)),
                ('Mention', dp(80)),
            ], data)

        elif MDApp.get_running_app().PUBLIC_TITRE == "Titre role":
            data = MDApp.get_running_app().transform_data(self.key_role, MDApp.get_running_app().ALL_ROLE)
            self.transform_table([
                ('N°', dp(10)),
                ('Titre', dp(160)),
            ], data)

        elif MDApp.get_running_app().PUBLIC_TITRE == "Titre année":
            data = MDApp.get_running_app().transform_data(self.key_anne, MDApp.get_running_app().ALL_ANNEE)
            self.transform_table([
                ('N°', dp(10)),
                ('Titre', dp(90)),
                ('Moyenne', dp(80)),
            ], data)

        elif MDApp.get_running_app().PUBLIC_TITRE == "Email":
            data = MDApp.get_running_app().transform_data(self.key_users, MDApp.get_running_app().ALL_USERS)
            self.transform_table([
                ('N°', dp(10)),
                ('Email', dp(50)),
                ('Prénom', dp(40)),
                ('Role', dp(20)),
                ('Mention', dp(65)),
            ], data)
        elif MDApp.get_running_app().PUBLIC_TITRE == "EC":
            data = MDApp.get_running_app().read_by_key_multiple(MDApp.get_running_app().ALL_EC,
                                                                "uuid_mention", "uuid_parcours", "semestre",
                                                                self.selected_mention, self.selected_parcours,
                                                                self.ids.semestre.text)
            self.return_ec(data)
        elif MDApp.get_running_app().PUBLIC_TITRE == "UE":
            data = MDApp.get_running_app().read_by_key_multiple(MDApp.get_running_app().ALL_UE,
                                                                "uuid_mention", "uuid_parcours", "semestre",
                                                                self.selected_mention, self.selected_parcours,
                                                                self.ids.semestre.text)
            self.return_ue(data)
        self.menu_public.dismiss()

    def transform_table(self, list_col: list, list_row: list):
        self.remove_widget(self.data_tables)
        """
        Use to transform the titre and number of the column in the table
        :param list_row:
        :param list_col:
        :return:
        """
        self.data_tables = MDDataTable(
            pos_hint={'center_y': 0.55, 'center_x': 0.5},
            size_hint=(0.98, 0.75),
            use_pagination=True,
            rows_num=7,
            column_data=list_col,
            row_data=list_row,
        )
        self.add_widget(self.data_tables)
        self.data_tables.bind(on_row_press=self.row_selected)
        return self.layout

    def add_new(self):
        MDApp.get_running_app().PUBLIC_ACTION_TYPE = "ADD_NEW"
        if MDApp.get_running_app().PUBLIC_TITRE != "":
            if MDApp.get_running_app().PUBLIC_TITRE == "UE" or MDApp.get_running_app().PUBLIC_TITRE == "EC":
                MDApp.get_running_app().root.current = 'Matier_add'
            else:
                MDApp.get_running_app().root.current = 'Public_add'

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

    def menu_calback_mention(self, text_item):
        self.selected_mention = \
            MDApp.get_running_app().read_by_key(MDApp.get_running_app().ALL_MENTION, "title", text_item)[0]['uuid']
        if MDApp.get_running_app().MENTION != self.selected_mention:
            MDApp.get_running_app().MENTION = self.selected_mention
            MDApp.get_running_app().get_list_parcours()
            self.menu_parcours = MDDropdownMenu(
                caller=self.ids.parcours,
                items=self.get_all_parcours(),
                width_mult=4,
            )
        self.ids.mention.text = text_item
        self.menu_mention.dismiss()
        if self.ids.matier.text == "Unité d'enseignement":
            data = MDApp.get_running_app().read_by_key(MDApp.get_running_app().ALL_UE,
                                                       "uuid_mention", self.selected_mention)
            self.return_ue(data)
        elif self.ids.matier.text == "Élément constitutif":
            data = MDApp.get_running_app().read_by_key(MDApp.get_running_app().ALL_EC,
                                                       "uuid_mention", self.selected_mention)
            self.return_ec(data)

    def get_all_parcours(self):
        parcours = MDApp.get_running_app().ALL_PARCOURS
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{parcours[i]['abreviation'].upper()}",
                "height": dp(50),
                "on_release": lambda x=f"{parcours[i]['abreviation'].upper()}": self.menu_calback_parcours(x),
            } for i in range(len(parcours))
        ]
        return menu_items

    def get_all_annne(self):
        annee = MDApp.get_running_app().ALL_ANNEE
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{annee[i]['title'].upper()}",
                "height": dp(50),
                "on_release": lambda x=f"{annee[i]['title'].upper()}": self.menu_calback_annee(x),
            } for i in range(len(annee))
        ]
        return menu_items

    def get_all_semestre(self):
        semestre = MDApp.get_running_app().ALL_SEMESTRE
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{semestre[i].upper()}",
                "height": dp(50),
                "on_release": lambda x=f"{semestre[i].upper()}": self.menu_calback_semestre(x),
            } for i in range(len(semestre))
        ]
        return menu_items

    def get_all_matier(self):
        matier = ["Unité d'enseignement", "Élément constitutif"]
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{matier[i]}",
                "height": dp(50),
                "on_release": lambda x=f"{matier[i]}": self.menu_calback_matier(x),
            } for i in range(len(matier))
        ]
        return menu_items

    def get_all_session(self):
        session = ["Normal", "Rattrapage", "Final"]
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{session[i]}",
                "height": dp(50),
                "on_release": lambda x=f"{session[i]}": self.menu_calback_session(x),
            } for i in range(len(session))
        ]
        return menu_items

    def menu_calback_annee(self, text_item):
        if MDApp.get_running_app().ANNEE != text_item:
            MDApp.get_running_app().ANNEE = text_item
            MDApp.get_running_app().ALL_UE = MDApp.get_running_app().get_all_ue(MDApp.get_running_app().ANNEE)
            MDApp.get_running_app().ALL_EC = MDApp.get_running_app().get_all_ec(MDApp.get_running_app().ANNEE)
            self.complet_table()
        self.ids.annee.text = text_item
        self.menu_annee.dismiss()

    def menu_calback_parcours(self, text_item):
        self.selected_parcours = MDApp.get_running_app().read_by_key(
            MDApp.get_running_app().ALL_PARCOURS, "abreviation", text_item)[0]['uuid']
        MDApp.get_running_app().PARCOURS_SELECTED = self.selected_parcours
        self.ids.parcours.text = text_item
        self.menu_parcours.dismiss()
        if self.ids.matier.text == "Unité d'enseignement":
            print(self.selected_parcours, self.selected_mention)
            data = MDApp.get_running_app().read_by_two_key(MDApp.get_running_app().ALL_UE,
                                                           "uuid_mention", "uuid_parcours",
                                                           self.selected_mention, self.selected_parcours)
            self.return_ue(data)
        elif self.ids.matier.text == "Élément constitutif":
            data = MDApp.get_running_app().read_by_two_key(MDApp.get_running_app().ALL_EC,
                                                           "uuid_mention", "uuid_parcours",
                                                           self.selected_mention, self.selected_parcours)
            self.return_ec(data)

    def menu_calback_semestre(self, text_item):
        MDApp.get_running_app().SEMESTRE_SELECTED = text_item
        self.ids.semestre.text = text_item
        self.menu_semestre.dismiss()
        if self.ids.matier.text == "Unité d'enseignement":
            data = MDApp.get_running_app().read_by_key_multiple(MDApp.get_running_app().ALL_UE,
                                                                "uuid_mention", "uuid_parcours", "semestre",
                                                                self.selected_mention, self.selected_parcours,
                                                                self.ids.semestre.text)
            self.return_ue(data)
        elif self.ids.matier.text == "Élément constitutif":
            data = MDApp.get_running_app().read_by_key_multiple(MDApp.get_running_app().ALL_EC,
                                                                "uuid_mention", "uuid_parcours", "semestre",
                                                                self.selected_mention, self.selected_parcours,
                                                                self.ids.semestre.text)
            self.return_ec(data)

    def menu_calback_matier(self, text_item):
        self.ids.matier.text = text_item
        self.menu_matier.dismiss()
        if text_item == "Unité d'enseignement":
            self.return_ue(MDApp.get_running_app().ALL_UE)
        else:
            self.return_ec(MDApp.get_running_app().ALL_EC)

    def menu_calback_session(self, text_item):
        self.ids.matier.text = text_item
        self.menu_session.dismiss()

    def return_ue(self, all_ue):
        data = MDApp.get_running_app().transform_data(self.key_ue, all_ue)
        MDApp.get_running_app().PUBLIC_TITRE = "UE"
        self.transform_table([
            ('N°', dp(10)),
            ('Titre', dp(90)),
            ('Credit', dp(80)),
        ], data)

    def return_ec(self, all_ec):
        data = MDApp.get_running_app().transform_data(self.key_ec, all_ec)
        MDApp.get_running_app().PUBLIC_TITRE = "EC"
        self.transform_table([
            ('N°', dp(10)),
            ('Titre', dp(50)),
            ('poids', dp(20)),
            ('UE', dp(50)),
            ('Enseignant', dp(50)),
        ], data)

    def create_list_tuple(self, list_data: list):
        response = [("N°", dp(10))]
        for index, data in enumerate(list_data):
            if index == 0:
                response.append((f"{data}", dp(len(data) * 2)))
            elif index == len(list_data) - 2:
                response.append((f"{data}", dp(len(data) * 2 + 5)))
            else:
                response.append((f"{data}", dp(len(data) * 2)))
        return response

    def create_table_note(self, *args):
        if self.ids.matier.text != "" and self.ids.parcours.text != "" and self.ids.semestre.text != "":
            annee = MDApp.get_running_app().ANNEE
            schemas = "anne_" + annee[0:4] + "_" + annee[5:9]
            host = MDApp.get_running_app().HOST
            url = f"http://{host}/api/v1/notes/"
            key_params = ["schemas", "session_", "uuid_parcours", "semestre"]
            value_params = [schemas, self.ids.matier.text,
                            MDApp.get_running_app().PARCOURS_SELECTED, MDApp.get_running_app().SEMESTRE_SELECTED]
            token = MDApp.get_running_app().TOKEN
            response = create_with_params(url, key_params, value_params, token, None)
            if response:
                if response[1] == 200:
                    self.all_column = list(response[0])
                    self.transform_table(self.create_list_tuple(self.all_column), [])
                elif response[1] == 400:
                    toast(response[0]['detail'])
                else:
                    toast(str(response))

    def add_etudiants(self, *args):
        if self.ids.matier.text != "" and self.ids.parcours.text != "" and self.ids.semestre.text != "":
            self.create_table_note()
            annee = MDApp.get_running_app().ANNEE
            schemas = "anne_" + annee[0:4] + "_" + annee[5:9]
            host = MDApp.get_running_app().HOST
            url = f"http://{host}/api/v1/notes_etudiants/insert_etudiants/"
            key_params = ["schemas", "session", "uuid_parcours", "semestre"]
            value_params = [schemas, self.ids.matier.text,
                            MDApp.get_running_app().PARCOURS_SELECTED, MDApp.get_running_app().SEMESTRE_SELECTED]
            token = MDApp.get_running_app().TOKEN
            response = create_with_params(url, key_params, value_params, token, None)
            if response:
                if response[1] == 200:
                    data = MDApp.get_running_app().transform_data(self.all_column, list(response[0]))
                    self.transform_table(self.create_list_tuple(self.all_column), data)
                elif response[1] == 400:
                    toast(response[0]['detail'])
                else:
                    toast(str(response))

    def delete_table_note(self, *args):
        if self.ids.matier.text != "" and self.ids.parcours.text != "" and self.ids.semestre.text != "":
            annee = MDApp.get_running_app().ANNEE
            schemas = "anne_" + annee[0:4] + "_" + annee[5:9]
            host = MDApp.get_running_app().HOST
            url = f"http://{host}/api/v1/notes/"
            key_params = ["schemas", "session", "uuid_parcours", "semestre"]
            value_params = [schemas, self.ids.matier.text,
                            MDApp.get_running_app().PARCOURS_SELECTED, MDApp.get_running_app().SEMESTRE_SELECTED]
            token = MDApp.get_running_app().TOKEN
            response = delete_with_params(url, key_params, value_params, token)
            if response:
                if response[1] == 200:
                    self.load_table()
                    self.dialog.dismiss()
                elif response[1] == 400:
                    toast(response[0]['detail'])
                else:
                    toast(str(response))

    def show_dialog(self, *args):
        if not self.dialog:
            # create dialog
            if MDApp.get_running_app().PUBLIC_TITRE != "Note":
                if MDApp.get_running_app().PUBLIC_TITRE == "Email":
                    key = "email"
                elif MDApp.get_running_app().PUBLIC_TITRE == "Montant":
                    key = "montant"
                else:
                    key = "title"
                value = MDApp.get_running_app().read_by_key(MDApp.get_running_app().DATA_SELECTED,
                                                            "uuid", MDApp.get_running_app().UUID_SELECTED)[0][key]
            else:
                value = f'{self.ids.semestre.text}_{self.ids.parcours.text}_{self.ids.matier.text}'
            self.dialog = MDDialog(
                title="Attention!",
                text=f"Voulez-vous supprimer {value} ?",
                buttons=[
                    MDFlatButton(
                        text="Oui",
                        on_release=self.delete_
                    ),
                    MDFlatButton(
                        text="Non",
                        on_release=self.cancel_dialog
                    ),
                ],
            )
        self.dialog.open()

    def update(self, *args):
        MDApp.get_running_app().PUBLIC_ACTION_TYPE = "UPDATE"
        if MDApp.get_running_app().PUBLIC_TITRE == "UE" or MDApp.get_running_app().PUBLIC_TITRE == "EC":
            MDApp.get_running_app().root.current = 'Matier_add'
        else:
            MDApp.get_running_app().root.current = 'Public_add'

    def cancel_dialog(self, *args):
        self.dialog.dismiss()

    def open_matier(self):
        if MDApp.get_running_app().PUBLIC_TITRE != "UE" and MDApp.get_running_app().PUBLIC_TITRE != "EC":
            self.ids.matier.hint_text = "Matier"
            self.ids.matier.text = ""
            self.inactive_button_note()
            MDApp.get_running_app().PUBLIC_TITRE = ""

    def open_note(self):
        if MDApp.get_running_app().PUBLIC_TITRE != "Note":
            self.ids.matier.hint_text = "Session"
            self.ids.matier.text = ""
            self.active_button_note()
            MDApp.get_running_app().PUBLIC_TITRE = "Note"

    def delete_(self, *args):
        host = MDApp.get_running_app().HOST
        token = MDApp.get_running_app().TOKEN
        annee = MDApp.get_running_app().ANNEE
        uuid = MDApp.get_running_app().UUID_SELECTED
        schemas = "anne_" + annee[0:4] + "_" + annee[5:9]
        if MDApp.get_running_app().PUBLIC_TITRE == "Note":
            self.delete_table_note()
        elif uuid != "":
            if MDApp.get_running_app().PUBLIC_TITRE == "UE":
                key_delete = ["schema", "uuid"]
                value_delete = [schemas, uuid]
                url = f"http://{host}/api/v1/matier_ue/delete_ue/"
                response = delete_with_params(url, key_delete, value_delete, token)
                self.get_response(response, MDApp.get_running_app().ALL_UE, self.key_ue)

            elif MDApp.get_running_app().PUBLIC_TITRE == "EC":
                key_delete = ["schema", "uuid"]
                value_delete = [schemas, uuid]
                url = f"http://{host}/api/v1/matier_ec/delete_ec/"
                response = delete_with_params(url, key_delete, value_delete, token)
                self.get_response(response, MDApp.get_running_app().ALL_EC, self.key_ec)
            else:
                key_delete = ["uuid"]
                value_delete = [uuid]
                if MDApp.get_running_app().PUBLIC_TITRE == "Email":
                    url = f"http://{host}/api/v1/users/"
                    response = delete_with_params(url, key_delete, value_delete, token)
                    self.get_response(response, "Email", self.key_users)
                elif MDApp.get_running_app().PUBLIC_TITRE == "Titre mention":
                    url = f"http://{host}/api/v1/mentions/"
                    response = delete_with_params(url, key_delete, value_delete, token)
                    self.get_response(response, "Titre mention", self.key_mention)
                elif MDApp.get_running_app().PUBLIC_TITRE == "Titre parcours":
                    url = f"http://{host}/api/v1/parcours/"
                    response = delete_with_params(url, key_delete, value_delete, token)
                    self.get_response(response, "Titre parcours", self.key_parcours)
                elif MDApp.get_running_app().PUBLIC_TITRE == "Montant":
                    url = f"http://{host}/api/v1/droit/"
                    response = delete_with_params(url, key_delete, value_delete, token)
                    self.get_response(response, "Montant", self.key_droit)
                elif MDApp.get_running_app().PUBLIC_TITRE == "Titre role":
                    url = f"http://{host}/api/v1/roles/"
                    response = delete_with_params(url, key_delete, value_delete, token)
                    self.get_response(response, "Titre role", self.key_role)
                else:
                    url = f"http://{host}/api/v1/anne_univ/"
                    response = delete_with_params(url, key_delete, value_delete, token)
                    self.get_response(response, "Année universitaire", self.key_anne)
            self.complet_table()

    def get_response(self, response, text: str, key):
        if response:
            if response[1] == 200:
                data = self.get_data(text, response[0])
                toast(f"Suppression avec succées")
                MDApp.get_running_app().PUBLIC_TITRE = ""
                self.dialog.dismiss()
                self.data_tables.row_data = MDApp.get_running_app().transform_data(key, data)
            elif response[1] == 400:
                toast(response[0]["detail"])
            else:
                toast(str(response))

    def get_data(self, text_item, response: list):
        if text_item == "UE":
            MDApp.get_running_app().ALL_UE = response
        elif text_item == "EC":
            MDApp.get_running_app().ALL_EC = response
        elif text_item == "Email":
            MDApp.get_running_app().ALL_USERS = response
        elif text_item == "Titre mention":
            MDApp.get_running_app().ALL_MENTION = response
        elif text_item == "Titre parcours":
            MDApp.get_running_app().ALL_PARCOURS = response
        elif text_item == "Montant":
            MDApp.get_running_app().ALL_DROIT = response
        elif text_item == "Titre role":
            MDApp.get_running_app().ALL_ROLE = response
        else:
            MDApp.get_running_app().ALL_ANNEE = response
        return response
