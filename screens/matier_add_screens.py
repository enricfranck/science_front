import json

from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.material_resources import dp
from kivymd.toast import toast
from kivymd.uix.menu import MDDropdownMenu

from all_requests.request_utils import create_json, create_with_params, update_with_params, create_json_update


class MatierAddScreen(Screen):
    screenManager = ObjectProperty(None)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.token = None
        self.host = None
        self.semestre = None
        self.parcours = None
        self.mention = None
        self.menue_ue = None

    def on_enter(self, *args):
        self.host = MDApp.get_running_app().HOST
        self.token = MDApp.get_running_app().TOKEN
        self.mention = MDApp.get_running_app().MENTION

        self.parcours = MDApp.get_running_app().PARCOURS_SELECTED
        self.semestre = MDApp.get_running_app().SEMESTRE_SELECTED

        self.menue_ue = MDDropdownMenu(
            caller=self.ids.value_ue,
            items=self.get_all_ue(),
            width_mult=4,
        )
        if MDApp.get_running_app().PUBLIC_TITRE == "UE":
            self.ids.title.hint_text = "Unité d'enseingement"
            self.ids.value.hint_text = "Credit"
            self.ids.value_ue.opacity = 0
            self.ids.value_ue.disabled = True
            self.ids.enseignant.opacity = 0
            self.ids.enseignant.disabled = True
            self.ids.save_ec.opacity = 0
            self.ids.save_ue.opacity = 1
            if MDApp.get_running_app().PUBLIC_ACTION_TYPE == "UPDATE":
                self.ids.title.text = MDApp.get_running_app().read_by_key(MDApp.get_running_app().ALL_UE, "uuid",
                                                                          MDApp.get_running_app().UUID_SELECTED
                                                                          )[0]["title"]
                self.ids.title.readonly = True
                self.ids.value.text = str(MDApp.get_running_app().read_by_key(
                    MDApp.get_running_app().ALL_UE, "uuid", MDApp.get_running_app().UUID_SELECTED)[0]["credit"])
            else:
                self.ids.title.text = ""
                self.ids.title.readonly = False
                self.ids.value.text = ""

        elif MDApp.get_running_app().PUBLIC_TITRE == "EC":
            self.ids.title.hint_text = "Élément constitutif"
            self.ids.value.hint_text = "Poids"
            self.ids.value_ue.opacity = 1
            self.ids.value_ue.disabled = False
            self.ids.enseignant.opacity = 1
            self.ids.enseignant.disabled = False
            self.ids.save_ec.opacity = 1
            self.ids.save_ue.opacity = 0
            if MDApp.get_running_app().PUBLIC_ACTION_TYPE == "UPDATE":
                self.ids.title.text = MDApp.get_running_app().read_by_key(MDApp.get_running_app().ALL_EC, "uuid",
                                                                          MDApp.get_running_app().UUID_SELECTED
                                                                          )[0]["title"]
                self.ids.title.readonly = True
                self.ids.value.text = str(MDApp.get_running_app().read_by_key(
                    MDApp.get_running_app().ALL_EC, "uuid", MDApp.get_running_app().UUID_SELECTED)[0]["poids"])
                self.ids.value_ue.text = str(MDApp.get_running_app().read_by_key(
                    MDApp.get_running_app().ALL_EC, "uuid", MDApp.get_running_app().UUID_SELECTED)[0]["value_ue"])
                self.ids.enseignant.text = MDApp.get_running_app().read_by_key(
                    MDApp.get_running_app().ALL_EC, "uuid", MDApp.get_running_app().UUID_SELECTED)[0]["utilisateur"]
            else:
                self.ids.title.text = ""
                self.ids.title.readonly = False
                self.ids.value.text = ""
                self.ids.value_ue.text = ""
                self.ids.enseignant.text = ""

    def back_home(self):
        """
        navigate to the datatable screens
        :return:
        """
        MDApp.get_running_app().root.current = 'Public'

    def get_all_ue(self):
        value_ue = []
        data = MDApp.get_running_app().read_by_key_multiple(MDApp.get_running_app().ALL_UE,
                                                            "uuid_mention", "uuid_parcours", "semestre",
                                                            self.mention, self.parcours,
                                                            self.semestre)
        for one_mention in data:
            value_ue.append(one_mention["value"])
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{value_ue[i]}",
                "height": dp(50),
                "on_release": lambda x=f"{value_ue[i]}": self.menu_calback_value_ue(x),
            } for i in range(len(value_ue))
        ]
        return menu_items

    def menu_calback_value_ue(self, text_item):
        self.ids.value_ue.text = text_item
        self.menue_ue.dismiss()

    def enreg_ue(self):
        """
        Save matier
        :return:
        """

        annee = MDApp.get_running_app().ANNEE
        schemas = "anne_" + annee[0:4] + "_" + annee[5:9]
        if MDApp.get_running_app().PUBLIC_ACTION_TYPE == "UPDATE":
            ue_key_up = ["credit"]
            ue_value_up = [self.ids.value.text]
            uuid = MDApp.get_running_app().UUID_SELECTED
            params_key = ["schema", "uuid"]
            params_value = [schemas, uuid]
            url = f"http://{self.host}/api/v1/matier_ue/update_ue/"
            ue = create_json_update(ue_key_up, ue_value_up)
            payload = json.dumps(ue)
            response = update_with_params(url, params_key, params_value, self.token, payload)
        else:
            ue_key = ["uuid", "title", "credit", "uuid_mention", "uuid_parcours", "semestre"]
            uuid = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
            ue_value = [uuid, self.ids.title.text, self.ids.value.text, self.mention, self.parcours, self.semestre]
            params_key = ["schema"]
            params_value = [schemas]
            url = f"http://{self.host}/api/v1/matier_ue/"
            ue = create_json(ue_key, ue_value)
            payload = json.dumps(ue)
            response = create_with_params(url, params_key, params_value, self.token, payload)
        if response:
            if response[1] == 200:
                MDApp.get_running_app().ALL_UE = response[0]
            if response[1] == 400:
                toast(response[0]['detail'])

    def enreg_ec(self):
        """
        Save matier
        :return:
        """
        annee = MDApp.get_running_app().ANNEE
        schemas = "anne_" + annee[0:4] + "_" + annee[5:9]

        if MDApp.get_running_app().PUBLIC_ACTION_TYPE == "UPDATE":
            url = f"http://{self.host}/api/v1/matier_ec/update_ec/"
            ec_key = ["poids", "value_ue", "utilisateur"]
            ec_value = [self.ids.value.text, self.ids.value_ue.text, self.ids.enseignant.text]
            params_key = ["schema", "uuid"]
            uuid = MDApp.get_running_app().UUID_SELECTED
            print(uuid)
            params_value = [schemas, uuid]
            ec = create_json_update(ec_key, ec_value)
            payload = json.dumps(ec)
            response = update_with_params(url, params_key, params_value, self.token, payload)
        else:
            url = f"http://{self.host}/api/v1/matier_ec/"
            ec_key = ["uuid", "title", "poids", "value_ue", "uuid_mention", "uuid_parcours", "semestre", "utilisateur"]
            uuid = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
            ec_value = [uuid, self.ids.title.text, self.ids.value.text, self.ids.value_ue.text, self.mention,
                        self.parcours,
                        self.semestre, self.ids.enseignant.text]
            params_key = ["schema"]
            params_value = [schemas]
            ec = create_json(ec_key, ec_value)
            payload = json.dumps(ec)
            response = create_with_params(url, params_key, params_value, self.token, payload)

        if response:
            if response[1] == 200:
                MDApp.get_running_app().ALL_EC = response[0]
            if response[1] == 400:
                toast(response[0]['detail'])
