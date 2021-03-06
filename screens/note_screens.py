import json
import threading
import time
import urllib
from concurrent.futures import ThreadPoolExecutor

from kivy.clock import mainthread
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.spinner import MDSpinner

from all_requests import request_utils
from all_requests.request_utils import create_with_params, get_with_params, create_json


class Content(MDBoxLayout):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.process_spinner_toogle()

    @mainthread
    def spinner_toggle(self):
        print(self.ids.spinner.active)
        if not self.ids.spinner.active:
            self.ids.spinner.active = True
        else:
            self.ids.spinner.active = False

    def active_check(self):
        annee = MDApp.get_running_app().ANNEE
        schemas = "anne_" + annee[0:4] + "_" + annee[5:9]
        host = MDApp.get_running_app().HOST
        url = f"http://{host}/api/v1/semestre_valide/by_num_carte"
        key_params = ["schema", "num_carte"]
        value_params = [schemas, MDApp.get_running_app().NUM_CARTE]
        token = MDApp.get_running_app().TOKEN
        response = get_with_params(url, key_params, value_params, token)
        if response:
            if response[1] == 200:
                if MDApp.get_running_app().SEMESTRE_SELECTED in response[0]["semestre"]:
                    self.ids.check.active = True
            elif response[1] == 400:
                print(response[0]['detail'])
            else:
                print(str(response))

    def enreg_semestre(self):
        annee = MDApp.get_running_app().ANNEE
        schemas = "anne_" + annee[0:4] + "_" + annee[5:9]
        host = MDApp.get_running_app().HOST
        url = f"http://{host}/api/v1/semestre_valide/"
        key_params = ["schema"]
        value_params = [schemas]

        validation_key = ["uuid", "num_carte", "semestre"]
        validation_value = ["3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            MDApp.get_running_app().NUM_CARTE,
                            [MDApp.get_running_app().SEMESTRE_SELECTED]]
        token = MDApp.get_running_app().TOKEN
        validation = create_json(validation_key, validation_value)
        payload = json.dumps(validation)
        response = create_with_params(url, key_params, value_params, token, payload)
        if response:
            if response[1] == 200:
                if response[0]["semestre"] is not None:
                    if MDApp.get_running_app().SEMESTRE_SELECTED in response[0]["semestre"]:
                        self.ids.check.active = True
                    else:
                        self.ids.check.active = False
                else:
                    self.ids.check.active = False

            elif response[1] == 400:
                print(response[0]['detail'])
            else:
                print(str(response))
        self.spinner_toggle()

    def process_spinner_toogle(self):
        threading.Thread(target=(
            self.active_check)).start()

    def process_enreg_semestre(self):
        self.spinner_toggle()
        threading.Thread(target=(
            self.enreg_semestre)).start()


class ListExam(MDBoxLayout):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.ids.valider.opacity = 1
        self.ids.valider.disabled = False

    def get_info(self):
        MDApp.get_running_app().SALLE = self.ids.salle.text
        MDApp.get_running_app().START_LIST = self.ids.start.text
        MDApp.get_running_app().END_LIST = self.ids.end.text
        self.ids.valider.opacity = 0
        self.ids.valider.disabled = True


def get_list_parcours() -> list:
    parcours = []
    host = MDApp.get_running_app().HOST
    token = MDApp.get_running_app().TOKEN
    uuid_mention = MDApp.get_running_app().MENTION
    url_parcours: str = f'http://{host}/api/v1/parcours/by_mention/'
    response = request_utils.get_with_params(url_parcours, ["uuid_mention"], [uuid_mention], token)
    if response:
        if response[1] == 200:
            MDApp.get_running_app().ALL_PARCOURS = response[0]
            if len(response[0]) != 0:
                for rep in response[0]:
                    parcours.append(str(rep['abreviation']))
        else:
            toast(str(response))
    return parcours


class NoteScreen(Screen):
    screenManager = ObjectProperty(None)
    dialog = None

    def __init__(self, **kw):
        super().__init__(**kw)
        self.content = None
        self.semestre = None
        self.num = None
        self.menu_condition = None
        self.data = None
        self.nombre = None
        self.selected_mention = None
        self.selected_parcours = None
        self.all_column = []
        self.menu_session = None
        self.menu_result_final = None
        self.menu_semestre = None
        self.menu_parcours = None
        self.menu_matier = None
        self.menu_annee = None
        self.menu_mention = None
        self.spinner = None
        self.layout = AnchorLayout()
        self.initialise = True
        self.data_tables = None
        self.parcours = []

    def on_enter(self, *args):
        if self.initialise:
            self.load_table()
            self.init_data()
            self.initialise = False
        if self.ids.semestre.text != "":
            self.spinner_toggle()
            self.process_spinner_toogle()
            self.spinner_toggle()

    def init_data(self):

        self.all_column = []

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
            items=[],
            width_mult=4,
        )

        self.menu_semestre = MDDropdownMenu(
            caller=self.ids.mention,
            items=self.get_all_semestre(),
            width_mult=4,
        )

        self.menu_session = MDDropdownMenu(
            caller=self.ids.session,
            items=self.get_all_session(),
            width_mult=4,
        )

        self.menu_result_final = MDDropdownMenu(
            caller=self.ids.result,
            items=self.get_all_result(),
            width_mult=4,
        )

        self.menu_condition = MDDropdownMenu(
            caller=self.ids.condition,
            items=self.get_all_condition(),
            width_mult=4,
        )

        self.spinner = MDSpinner(
            pos_hint={'center_y': 0.5, 'center_x': 0.5},
            size_hint=(None, None),
            size=(dp(30), dp(30)),
            active=False
        )

        self.add_widget(self.spinner)

        self.ids.annee.text = MDApp.get_running_app().ALL_ANNEE[0]['title']
        MDApp.get_running_app().ANNEE = self.ids.annee.text

    def back_home(self):
        MDApp.get_running_app().root.current = 'Main'

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

        self.add_widget(self.data_tables)
        return self.layout

    def row_selected(self, table, row):
        try:
            start_index, end_index = row.table.recycle_data[row.index]["range"]
            num_carte = row.table.recycle_data[start_index + 1]["text"]
            semestre = self.ids.semestre.text
            if num_carte != "":
                MDApp.get_running_app().NUM_CARTE = num_carte
                MDApp.get_running_app().SEMESTRE_SELECTED = semestre
                self.show_confirmation_dialog()
        except Exception as e:
            toast(str(e))

    def create_list_tuple(self, list_data: list):
        response = [("N??", dp(10))]
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
        self.data_tables.bind(on_row_press=self.row_selected)
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

    def get_all_result(self):
        result = ["D??finitive", "Compens??"]
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{result[i]}",
                "height": dp(50),
                "on_release": lambda x=f"{result[i]}": self.menu_calback_result(x),
            } for i in range(len(result))
        ]
        return menu_items

    def get_all_condition(self):
        condition = ["Inf??rieur ??", "??gale ??", "Sup??rieur ??"]
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
            processes = []
            with ThreadPoolExecutor(max_workers=10) as executor:
                processes.append(executor.submit(get_ue, MDApp.get_running_app().ANNEE))
                processes.append(executor.submit(get_ec, MDApp.get_running_app().ANNEE))
            self.complet_table()
        self.ids.annee.text = text_item
        self.menu_annee.dismiss()

    def open_menu(self):
        self.menu_matier = MDDropdownMenu(
            caller=self.ids.matier,
            items=self.get_all_matier(),
            width_mult=4,
        )
        self.menu_matier.open()

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
                elif response[1] == 400:
                    toast(response[0]['detail'])
                    self.all_column = []
                else:
                    toast(str(response))
                    self.all_column = []

    def get_etudiants(self, *args):
        if self.ids.parcours.text != "" and self.ids.semestre.text != "":
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
                elif response[1] == 400:
                    toast(response[0]['detail'])
                else:
                    toast(str(response))

    @mainthread
    def insert_data(self):
        data = MDApp.get_running_app().transform_data(self.all_column, self.data)
        self.transform_table(self.create_list_tuple(self.all_column), data)

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
            self.spinner_toggle()
            self.process_spinner_toogle()
            self.spinner_toggle()
        self.menu_semestre.dismiss()

    def menu_calback_condition(self, text_item):
        self.ids.condition.text = text_item
        if text_item == "Inf??rieur ??":
            value = MDApp.get_running_app().read_note_inferieur(
                self.data, self.ids.matier.text, float(self.ids.nombre.text))
            value = MDApp.get_running_app().transform_data(self.all_column, value)
            self.transform_table(self.create_list_tuple(self.all_column), value)

        elif text_item == "Sup??rieur ??":
            value = MDApp.get_running_app().read_note_superieur(
                self.data, self.ids.matier.text, float(self.ids.nombre.text))
            value = MDApp.get_running_app().transform_data(self.all_column, value)
            self.transform_table(self.create_list_tuple(self.all_column), value)

        if text_item == "??gale ??":
            value = MDApp.get_running_app().read_note_egale(
                self.data, self.ids.matier.text, float(self.ids.nombre.text))
            value = MDApp.get_running_app().transform_data(self.all_column, value)
            self.transform_table(self.create_list_tuple(self.all_column), value)
        self.menu_condition.dismiss()

    def get_all_parcours(self):
        parcours = self.parcours
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{parcours[i].upper()}",
                "height": dp(50),
                "on_release": lambda x=f"{parcours[i].upper()}": self.menu_calback_parcours(x),
            } for i in range(len(parcours))
        ]
        return menu_items

    def menu_calback_parcours(self, text_item):
        self.selected_parcours = MDApp.get_running_app().read_by_key(
            MDApp.get_running_app().ALL_PARCOURS, "abreviation", text_item)[0]['uuid']
        MDApp.get_running_app().PARCOURS_SELECTED = self.selected_parcours
        self.ids.parcours.text = text_item
        if self.ids.parcours.text != "" and self.ids.semestre.text != "":
            self.spinner_toggle()
            self.process_spinner_toogle()
            self.spinner_toggle()
        self.menu_parcours.dismiss()

    @mainthread
    def spinner_toggle(self):
        print("avant", self.spinner.active)
        if not self.spinner.active:
            self.spinner.active = True
        else:
            self.spinner.active = False

        print("apres", self.spinner.active)

    def process_spiner(self):
        processes = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            processes.append(executor.submit(self.get_all_colums))
            processes.append(executor.submit(self.get_etudiants))
        self.insert_data()
        self.spinner_toggle()

    def process_spinner_toogle(self):
        self.spinner_toggle()
        threading.Thread(target=(
            self.process_spiner)).start()

    # def process_parcours(self):
    #     processes = []
    #     with ThreadPoolExecutor(max_workers=3) as executor:
    #         processes.append(executor.submit(self.get_parcours))
    #     self.spinner_toggle()

    def get_parcours(self):
        self.parcours = get_list_parcours()

    def process_parcours_toogle(self):
        self.spinner_toggle()
        threading.Thread(target=(
            self.get_parcours)).start()

        print("Parcours",self.parcours)

    def show_spinner_dialog(self):
        self.content = Content()

    def process_spinner_dialog(self):
        self.spinner_toggle()
        threading.Thread(target=(
            self.show_spinner_dialog)).start()

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
            self.get_parcours()
        self.ids.mention.text = text_item
        self.menu_mention.dismiss()

        self.menu_parcours = MDDropdownMenu(
            caller=self.ids.parcours,
            items=self.get_all_parcours(),
            width_mult=4,
        )

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
        if self.ids.parcours.text != "" and self.ids.semestre.text != "":
            self.spinner_toggle()
            self.process_spinner_toogle()
            self.spinner_toggle()
        self.menu_session.dismiss()

    def menu_calback_result(self, text_item):
        if text_item == "D??finitive":
            text_item = "definitive"
        else:
            text_item = "compense"
        MDApp.get_running_app().TITRE_FILE = \
            f"Resultat_final_{self.ids.parcours.text}_{self.ids.semestre.text}_{self.ids.session.text}_{text_item}"
        annee = MDApp.get_running_app().ANNEE
        schemas = "anne_" + annee[0:4] + "_" + annee[5:9]
        values = {'schema': f'{schemas}', 'session': f'{self.ids.session.text}',
                  'semestre': f'{self.ids.semestre.text}', 'uuid_parcours': MDApp.get_running_app().PARCOURS_SELECTED,
                  'type_result': text_item}
        params = urllib.parse.urlencode(values)
        host = MDApp.get_running_app().HOST
        url = f"http://{host}/api/v1/resultat/get_by_session"
        MDApp.get_running_app().URL_DOWNLOAD = f"{url}?{params}"
        MDApp.get_running_app().NAME_DOWNLOAD = f"{MDApp.get_running_app().TITRE_FILE}.pdf"
        MDApp.get_running_app().PARENT = "Note"
        if len(annee) != 0:
            MDApp.get_running_app().root.current = 'download_file'
        self.menu_result_final.dismiss()

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

    def download_note(self):
        annee = MDApp.get_running_app().ANNEE
        MDApp.get_running_app().TITRE_FILE = \
            f"note_{self.ids.parcours.text}_{self.ids.session.text}"
        schemas = "anne_" + annee[0:4] + "_" + annee[5:9]
        values = {'schema': f'{schemas}', 'session': f'{self.ids.session.text}',
                  'uuid_parcours': MDApp.get_running_app().PARCOURS_SELECTED}
        params = urllib.parse.urlencode(values)
        host = MDApp.get_running_app().HOST
        url = f"http://{host}/api/v1/save_data/get_models_notes/"
        MDApp.get_running_app().URL_DOWNLOAD = f"{url}?{params}"
        MDApp.get_running_app().NAME_DOWNLOAD = f"{MDApp.get_running_app().TITRE_FILE}.xlsx"
        MDApp.get_running_app().PARENT = "Note"
        if len(annee) != 0 and self.ids.parcours.text != "":
            MDApp.get_running_app().root.current = 'download_file'

    def upload_note(self):
        annee = MDApp.get_running_app().ANNEE
        MDApp.get_running_app().TITRE_FILE = \
            f"note_{self.ids.parcours.text}_{self.ids.session.text}"
        schemas = "anne_" + annee[0:4] + "_" + annee[5:9]
        values = {'schema': f'{schemas}', 'session': f'{self.ids.session.text}',
                  'uuid_parcours': MDApp.get_running_app().PARCOURS_SELECTED,
                  'semestre': self.ids.semestre.text}
        params = urllib.parse.urlencode(values)
        host = MDApp.get_running_app().HOST
        url = f"http://{host}/api/v1/save_data/upload_note_file/"
        MDApp.get_running_app().URL_UPLOAD = f"{url}?{params}"
        MDApp.get_running_app().PARENT = "Note"
        if len(annee) != 0 and self.ids.semestre.text != "":
            MDApp.get_running_app().root.current = 'upload_file'

    def show_confirmation_dialog(self):
        # if not self.dialog:
        self.dialog = MDDialog(
            title=f"Validation {MDApp.get_running_app().NUM_CARTE} semestre {MDApp.get_running_app().SEMESTRE_SELECTED}",
            type="custom",
            content_cls=Content(),
            buttons=[
                MDFlatButton(
                    text="T??rminer",
                    on_release=self.cancel_dialog
                ),
            ],
        )
        self.dialog.open()
        self.spinner_toggle()

    def show_dialog_list(self):
        self.dialog = MDDialog(
            title=f"Listes aux examen",
            type="custom",
            content_cls=ListExam(),
            buttons=[
                MDFlatButton(
                    text="T??rminer",
                    on_release=self.process_get_list
                ),
            ],

        )
        self.dialog.open()

    def cancel_dialog(self, *args):
        self.dialog.dismiss()

    def process_get_list(self, *args):
        # ListExam().get_info()
        annee = MDApp.get_running_app().ANNEE
        MDApp.get_running_app().TITRE_FILE = \
            f"list_{self.ids.semestre.text}_{self.ids.parcours.text}_{self.ids.session.text}"
        schemas = "anne_" + annee[0:4] + "_" + annee[5:9]
        values = {'schema': f'{schemas}',
                  'session': f'{self.ids.session.text}',
                  'semestre': f'{self.ids.semestre.text}',
                  'uuid_parcours': MDApp.get_running_app().PARCOURS_SELECTED,
                  'uuid_mention': MDApp.get_running_app().MENTION,
                  'salle': MDApp.get_running_app().SALLE,
                  'skip': MDApp.get_running_app().START_LIST,
                  'limit': MDApp.get_running_app().END_LIST
                  }
        params = urllib.parse.urlencode(values)
        host = MDApp.get_running_app().HOST
        url = f"http://{host}/api/v1/liste/list_exam/"
        MDApp.get_running_app().URL_DOWNLOAD = f"{url}?{params}"
        MDApp.get_running_app().NAME_DOWNLOAD = f"{MDApp.get_running_app().TITRE_FILE}.pdf"
        MDApp.get_running_app().PARENT = "Note"
        if len(annee) != 0 and self.ids.parcours.text != "":
            self.dialog.dismiss()
            MDApp.get_running_app().root.current = 'download_file'


def get_ue(annee):
    if len(MDApp.get_running_app().ALL_ANNEE) != 0:
        MDApp.get_running_app().ALL_UE = \
            MDApp.get_running_app().get_all_ue(annee=annee)


def get_ec(anne):
    if len(MDApp.get_running_app().ALL_ANNEE) != 0:
        MDApp.get_running_app().ALL_EC = \
            MDApp.get_running_app().get_all_ec(annee=anne)
