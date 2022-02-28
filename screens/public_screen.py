from kivy.uix.anchorlayout import AnchorLayout
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivymd.material_resources import dp
from kivymd.uix.button import MDIconButton
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.spinner import MDSpinner


class PublicScreen(Screen):
    screenManager = ObjectProperty(None)

    def __init__(self, **kw):
        super().__init__(**kw)
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
        self.key_droit = ["niveau", "montant", "annee", "mention"]
        self.key_users = ["email", "prenom", "role", "mention"]
        self.initialise = True
        self.uuid_selected = ""

    def init_data(self):
        self.edit = MDIconButton(
            icon="pen",
            pos_hint={'center_y': 0.95, 'center_x': 0.9},
            opacity=0,
            disabled=True,
            # on_release=self.update_etudiant
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
            # on_release=self.show_dialog
        )

        self.add_widget(self.edit)
        self.add_widget(self.delete)

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
        print(title)
        if title != "":

            if MDApp.get_running_app().PUBLIC_TITRE == "Montant":
                anne = row.table.recycle_data[start_index + 3]["text"]
                mention = row.table.recycle_data[start_index + 4]["text"]
                data = MDApp.get_running_app().ALL_DROIT
                MDApp.get_running_app().UUID_SELECTED = \
                    MDApp.get_running_app().read_by_key_multiple(data, 'niveau', "annee", "mention",
                                                                 title, anne, mention)[0]['uuid']
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
                MDApp.get_running_app().UUID_SELECTED = MDApp.get_running_app().read_by_key(
                    data, key, title)[0]['uuid']

            print(MDApp.get_running_app().UUID_SELECTED)
            self.active_button()
        else:
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
        if self.initialise:
            self.load_table()
            self.init_data()
            self.initialise = False
        self.inactive_button()

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
            data = MDApp.get_running_app().transform_data(self.key_mention, MDApp.get_running_app().ALL_MENTION)
            self.transform_table([
                ('N°', dp(10)),
                ('title', dp(80)),
                ('Abréviation', dp(20)),
                ('branche', dp(50)),
                ('Dérnière CE', dp(20)),
            ], data)

        elif text_item == "Parcours":
            MDApp.get_running_app().PUBLIC_TITRE = "Titre parcours"
            data = MDApp.get_running_app().transform_data(self.key_parcours, MDApp.get_running_app().ALL_PARCOURS)
            self.transform_table([
                ('N°', dp(10)),
                ('title', dp(100)),
                ('Abréviation', dp(20)),
                ('Semestre', dp(50)),
            ], data)

        elif text_item == "Droit":
            MDApp.get_running_app().PUBLIC_TITRE = "Montant"
            data = MDApp.get_running_app().transform_data(self.key_droit, MDApp.get_running_app().ALL_DROIT)
            self.transform_table([
                ('N°', dp(10)),
                ('Niveau', dp(20)),
                ('Montant', dp(30)),
                ('Année universitaire', dp(40)),
                ('Mention', dp(80)),
            ], data)

        elif text_item == "Role":
            MDApp.get_running_app().PUBLIC_TITRE = "Titre role"
            data = MDApp.get_running_app().transform_data(self.key_role, MDApp.get_running_app().ALL_ROLE)
            self.transform_table([
                ('N°', dp(10)),
                ('Titre', dp(160)),
            ], data)

        elif text_item == "Année universitaire":
            MDApp.get_running_app().PUBLIC_TITRE = "Titre année"
            data = MDApp.get_running_app().transform_data(self.key_anne, MDApp.get_running_app().ALL_ANNEE)
            self.transform_table([
                ('N°', dp(10)),
                ('Titre', dp(90)),
                ('Moyenne', dp(80)),
            ], data)

        elif text_item == "Users":
            MDApp.get_running_app().PUBLIC_TITRE = "Email"
            data = MDApp.get_running_app().transform_data(self.key_users, MDApp.get_running_app().ALL_USERS)
            self.transform_table([
                ('N°', dp(10)),
                ('Email', dp(50)),
                ('Prénom', dp(40)),
                ('Role', dp(20)),
                ('Mention', dp(65)),
            ], data)
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
        MDApp.get_running_app().root.current = 'Public_add'
