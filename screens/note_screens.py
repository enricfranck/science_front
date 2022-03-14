import urllib

from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivymd.toast import toast
from kivymd.uix.button import MDIconButton
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.spinner import MDSpinner

from all_requests.request_utils import create_with_params, get_with_params


class NoteScreen(Screen):
    screenManager = ObjectProperty(None)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.data = None
        self.nombre = None
        self.selected_mention = None
        self.selected_parcours = None
        self.all_column = None
        self.menu_session = None
        self.menu_semestre = None
        self.menu_parcours = None
        self.menu_matier = None
        self.menu_annee = None
        self.menu_mention = None
        self.spinner = None
        self.layout = AnchorLayout()
        self.initialise = True
        self.data_tables = None

    def on_enter(self, *args):
        if self.initialise:
            self.load_table()
            self.init_data()
            self.initialise = False
        pass

    def init_data(self):
        self.spinner = MDSpinner(
            pos_hint={'center_y': 0.5, 'center_x': 0.5},
            size=(dp(46), dp(46)),
            active=False
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
            caller=self.ids.session,
            items=self.get_all_session(),
            width_mult=4,
        )

        self.menu_condition = MDDropdownMenu(
            caller=self.ids.condition,
            items=self.get_all_condition(),
            width_mult=4,
        )

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

    def transform_table(self, list_col: list, list_row: list):
        """
        Use to transform the titre and number of the column in the table
        :param list_row:
        :param list_col:
        :return:
        """

        self.remove_widget(self.data_tables)
        self.data_tables = MDDataTable(
            pos_hint={'center_y': 0.55, 'center_x': 0.5},
            size_hint=(0.98, 0.75),
            use_pagination=True,
            rows_num=7,
            column_data=list_col,
            row_data=list_row,
        )
        self.add_widget(self.data_tables)
        # self.data_tables.bind(on_row_press=self.row_selected)
        return self.layout

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

    def get_all_condition(self):
        condition = ["Inférieur à", "Égale à", "Supérieur à"]
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{condition[i]}",
                "height": dp(50),
                "on_release": lambda x=f"{condition[i]}": self.menu_calback_condition(x),
            } for i in range(len(condition))
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

    def menu_calback_annee(self, text_item):
        if MDApp.get_running_app().ANNEE != text_item:
            MDApp.get_running_app().ANNEE = text_item
            MDApp.get_running_app().ALL_UE = MDApp.get_running_app().get_all_ue(MDApp.get_running_app().ANNEE)
            MDApp.get_running_app().ALL_EC = MDApp.get_running_app().get_all_ec(MDApp.get_running_app().ANNEE)
            self.complet_table()
        self.ids.annee.text = text_item
        self.menu_annee.dismiss()

    def get_all_colums(self):
        if self.ids.parcours.text != "" and self.ids.semestre.text != "":
            annee = MDApp.get_running_app().ANNEE
            schemas = "anne_" + annee[0:4] + "_" + annee[5:9]
            host = MDApp.get_running_app().HOST
            url = f"http://{host}/api/v1/notes/"
            key_params = ["schemas", "session", "uuid_parcours", "semestre"]
            value_params = [schemas, self.ids.session.text,
                            MDApp.get_running_app().PARCOURS_SELECTED, MDApp.get_running_app().SEMESTRE_SELECTED]
            token = MDApp.get_running_app().TOKEN
            response = get_with_params(url, key_params, value_params, token)
            if response:
                if response[1] == 200:
                    self.ids.matier.text = ""
                    self.ids.nombre.text = ""
                    self.ids.disabled = True
                    self.all_column = list(response[0])
                    self.menu_matier = MDDropdownMenu(
                        caller=self.ids.matier,
                        items=self.get_all_matier(),
                        width_mult=4,
                    )
                elif response[1] == 400:
                    toast(response[0]['detail'])
                    self.all_column = []
                else:
                    toast(str(response))

    def get_etudiants(self, *args):
        if self.ids.parcours.text != "" and self.ids.semestre.text != "":
            self.get_all_colums()
            annee = MDApp.get_running_app().ANNEE
            schemas = "anne_" + annee[0:4] + "_" + annee[5:9]
            host = MDApp.get_running_app().HOST
            url = f"http://{host}/api/v1/notes_etudiants/get_all_notes/"
            key_params = ["schemas", "session", "uuid_parcours", "semestre"]
            value_params = [schemas, self.ids.session.text,
                            MDApp.get_running_app().PARCOURS_SELECTED, MDApp.get_running_app().SEMESTRE_SELECTED]
            token = MDApp.get_running_app().TOKEN
            response = get_with_params(url, key_params, value_params, token)
            if response:
                if response[1] == 200:
                    self.data = list(response[0])
                    data = MDApp.get_running_app().transform_data(self.all_column, self.data)
                    self.transform_table(self.create_list_tuple(self.all_column), data)
                elif response[1] == 400:
                    toast(response[0]['detail'])
                else:
                    toast(str(response))

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

    def menu_calback_semestre(self, text_item):
        MDApp.get_running_app().SEMESTRE_SELECTED = text_item
        self.ids.semestre.text = text_item
        if self.ids.parcours.text != "" and self.ids.semestre.text != "":
            self.get_etudiants()
        self.menu_semestre.dismiss()

    def menu_calback_condition(self, text_item):
        self.ids.condition.text = text_item
        if text_item == "Inférieur à":
            value = MDApp.get_running_app().read_note_inferieur(
                self.data, self.ids.matier.text, float(self.ids.nombre.text))
            value = MDApp.get_running_app().transform_data(self.all_column, value)
            self.transform_table(self.create_list_tuple(self.all_column), value)

        elif text_item == "Supérieur à":
            value = MDApp.get_running_app().read_note_superieur(
                self.data, self.ids.matier.text, float(self.ids.nombre.text))
            value = MDApp.get_running_app().transform_data(self.all_column, value)
            self.transform_table(self.create_list_tuple(self.all_column), value)

        if text_item == "Égale à":
            value = MDApp.get_running_app().read_note_egale(
                self.data, self.ids.matier.text, float(self.ids.nombre.text))
            value = MDApp.get_running_app().transform_data(self.all_column, value)
            self.transform_table(self.create_list_tuple(self.all_column), value)
        self.menu_condition.dismiss()

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

    def menu_calback_parcours(self, text_item):
        self.selected_parcours = MDApp.get_running_app().read_by_key(
            MDApp.get_running_app().ALL_PARCOURS, "abreviation", text_item)[0]['uuid']
        MDApp.get_running_app().PARCOURS_SELECTED = self.selected_parcours
        self.ids.parcours.text = text_item
        if self.ids.parcours.text != "" and self.ids.semestre.text != "":
            self.get_etudiants()
        self.menu_parcours.dismiss()

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

    def get_all_matier(self):
        matier = []
        if self.all_column is not None:
            for inedex, items in enumerate(self.all_column):
                if inedex != 0:
                    matier.append(self.all_column[inedex])
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{matier[i]}",
                "height": dp(50),
                "on_release": lambda x=f"{matier[i]}": self.menu_calback_matier(x),
            } for i in range(len(matier))
        ]
        return menu_items

    def menu_calback_session(self, text_item):
        self.ids.session.text = text_item
        self.menu_session.dismiss()

    def menu_calback_matier(self, text_item):
        self.ids.matier.text = text_item
        self.ids.nombre.disabled = False
        self.menu_matier.dismiss()

    def test_number(self):
        if self.ids.nombre.text != '':
            try:
                self.nombre = float(self.ids.nombre.text)
                self.ids.condition.disabled = False
            except Exception as e:
                self.ids.condition.text = ""
                self.ids.condition.disabled = True

    def view_rattrapage(self):
        str_ = self.ids.matier.text
        if str_ != '' and str_[0:1] == 'e':
            self.ids.rattrapage.disabled = False
            self.ids.rattrapage.opacity = 1
            self.ids.download.disable = True
            self.ids.download.opacity = 0
        elif str_[0:1] == "u":
            self.ids.download.disable = False
            self.ids.download.opacity = 1
            self.ids.rattrapage.disabled = True
            self.ids.rattrapage.opacity = 0
        else:
            self.ids.rattrapage.disabled = True
            self.ids.rattrapage.opacity = 0
            self.ids.download.disable = True
            self.ids.download.opacity = 0

    def list_rattrapage(self):
        value_ec = self.ids.matier.text[3:len(self.ids.matier.text)]
        data = MDApp.get_running_app().ALL_EC
        value_ue = \
            MDApp.get_running_app().read_by_key_multiples(
                data, 'value', "uuid_mention", "uuid_parcours",
                "semestre", value_ec, self.selected_mention,
                self.selected_parcours, self.ids.semestre.text)[0]['value_ue']
        value = MDApp.get_running_app().read_rattrapage(
            self.data, f'ec_{value_ec}', f'ue_{value_ue}')
        value = MDApp.get_running_app().transform_data(self.all_column, value)
        self.transform_table(self.create_list_tuple(self.all_column), value)

    def download_resultat(self):
        MDApp.get_running_app().TITRE_FILE = \
            f"Resultat_{self.ids.matier.text}_{self.ids.parcours.text}_{self.ids.semestre.text}_{self.ids.session.text}"
        annee = MDApp.get_running_app().ANNEE
        schemas = "anne_" + annee[0:4] + "_" + annee[5:9]
        values = {'schema': f'{schemas}', 'session': f'{self.ids.session.text}',
                  'semestre': f'{self.ids.semestre.text}', 'uuid_parcours': MDApp.get_running_app().PARCOURS_SELECTED,
                  'value_ue': f'{self.ids.matier.text[3:len(self.ids.matier.text)]}'}
        params = urllib.parse.urlencode(values)
        host = MDApp.get_running_app().HOST
        url = f"http://{host}/api/v1/resultat/get_by_matier_pdf"
        MDApp.get_running_app().URL_DOWNLOAD = f"{url}?{params}"
        MDApp.get_running_app().NAME_DOWNLOAD = f"{MDApp.get_running_app().TITRE_FILE}.pdf"
        MDApp.get_running_app().PARENT = "Note"
        if len(annee) != 0:
            MDApp.get_running_app().root.current = 'download_file'
