from kivy.uix.anchorlayout import AnchorLayout
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivymd.material_resources import dp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.menu import MDDropdownMenu


class PublicScreen(Screen):
    screenManager = ObjectProperty(None)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.layout = AnchorLayout()
        self.menu_public = None
        self.data_tables = None

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
        self.load_table()

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
            self.transform_table([
                ('title', dp(80)),
                ('Abréviation', dp(30)),
                ('branche', dp(50)),
                ('Dérnière CE', dp(20)),
            ])

        elif text_item == "Parcours":
            MDApp.get_running_app().PUBLIC_TITRE = "Titre parcours"
            self.transform_table([
                ('title', dp(70)),
                ('Abréviation', dp(20)),
                ('Mention', dp(60)),
                ('Semestre', dp(40)),
            ])

        elif text_item == "Droit":
            MDApp.get_running_app().PUBLIC_TITRE = "Montant"
            self.transform_table([
                ('Niveau', dp(30)),
                ('Montant', dp(30)),
                ('Année universitaire', dp(40)),
                ('Mention', dp(80)),
            ])

        elif text_item == "Role":
            MDApp.get_running_app().PUBLIC_TITRE = "Titre role"
            self.transform_table([
                ('Titre', dp(160)),
                ('', dp(20)),
            ])

        elif text_item == "Année universitaire":
            MDApp.get_running_app().PUBLIC_TITRE = "Titre année"
            self.transform_table([
                ('Titre', dp(90)),
                ('Moyenne', dp(90)),
            ])

        elif text_item == "Users":
            MDApp.get_running_app().PUBLIC_TITRE = "Email"
            self.transform_table([
                ('Email', dp(50)),
                ('Prénom', dp(40)),
                ('Role', dp(30)),
                ('Mention', dp(65)),
            ])
        self.menu_public.dismiss()

    def transform_table(self, list_col: list):
        """
        Use to transform the titre and number of the column in the table
        :param list_col:
        :return:
        """
        self.data_tables = MDDataTable(
            pos_hint={'center_y': 0.55, 'center_x': 0.5},
            size_hint=(0.98, 0.75),
            column_data=list_col,
        )
        self.remove_widget(self.data_tables)
        self.add_widget(self.data_tables)
        return self.layout

    def add_new(self):
        MDApp.get_running_app().root.current = 'Public_add'

