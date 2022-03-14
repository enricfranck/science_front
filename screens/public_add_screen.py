import json

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivymd.material_resources import dp
from kivymd.toast import toast
from kivymd.uix.menu import MDDropdownMenu

from all_requests.request_utils import create_json, create, create_json_update, update_with_params
from utils import select_str, create_list, creat_str_from_list


class PublicAddScreen(Screen):
    screenManager = ObjectProperty(None)

    def __init__(self, **kw):
        super().__init__(**kw)

        self.semestre = None
        self.menu_semestre = None
        self.menu_role = None
        self.selected_role = None
        self.token = None
        self.host = None
        self.selected_mention = None
        self.list_mention = []
        self.menu_mention = None
        self.titre = None
        self.email = None
        self.password = None
        self.nom = None
        self.prenom = None
        self.role = None
        self.mention = None

    def back_home(self):
        MDApp.get_running_app().root.current = 'Public'

    def on_enter(self, *args):

        self.host = MDApp.get_running_app().HOST
        self.token = MDApp.get_running_app().TOKEN

        self.titre = MDApp.get_running_app().PUBLIC_TITRE
        self.ids.email.hint_text = self.titre
        self.email = self.ids.email
        self.password = self.ids.password
        self.nom = self.ids.nom
        self.prenom = self.ids.prenom
        self.mention = self.ids.mention
        self.role = self.ids.role
        self.semestre = self.ids.semestre

        self.menu_semestre = MDDropdownMenu(
            caller=self.ids.semestre,
            items=self.get_all_semestre(),
        )

        self.menu_mention = MDDropdownMenu(
            caller=self.ids.mention,
            items=self.get_all_mention(),
            width_mult=4,
        )
        self.menu_role = MDDropdownMenu(
            caller=self.ids.role,
            items=self.get_all_role(),
            width_mult=4,
        )

        if self.titre == "Email":
            self.role.opacity = 1
            self.role.disabled = False
            self.password.opacity = 1
            self.password.disabled = False
            self.nom.opacity = 1
            self.nom.disabled = False
            self.prenom.opacity = 1
            self.prenom.disabled = False
            self.mention.opacity = 1
            self.mention.disabled = False
            self.semestre.opacity = 0
            self.semestre.disabled = True

            self.nom.hint_text = "Nom"
            self.password.hint_text = "Password"
            self.prenom.hint_text = "Prénom"

            self.ids.save_users.opacity = 1
            self.ids.save_mention.opacity = 0
            self.ids.save_parcours.opacity = 0
            self.ids.save_role.opacity = 0
            self.ids.save_annee.opacity = 0
            self.ids.save_droit.opacity = 0
            if MDApp.get_running_app().PUBLIC_ACTION_TYPE == "UPDATE":
                self.email.text = str(MDApp.get_running_app().read_by_key(
                    MDApp.get_running_app().ALL_USERS, "uuid", MDApp.get_running_app().UUID_SELECTED)[0]["email"])
                self.nom.text = str(MDApp.get_running_app().read_by_key(
                    MDApp.get_running_app().ALL_USERS, "uuid", MDApp.get_running_app().UUID_SELECTED)[0]["nom"])
                self.prenom.text = str(MDApp.get_running_app().read_by_key(
                    MDApp.get_running_app().ALL_USERS, "uuid", MDApp.get_running_app().UUID_SELECTED)[0]["prenom"])
                all_mention = MDApp.get_running_app().read_by_key(
                    MDApp.get_running_app().ALL_USERS, "uuid", MDApp.get_running_app().UUID_SELECTED)[0]["mention"]
                self.mention.text = all_mention

                self.role.text = str(MDApp.get_running_app().read_by_key(
                    MDApp.get_running_app().ALL_USERS, "uuid", MDApp.get_running_app().UUID_SELECTED)[0]["role"])
                self.password.text = ""
            else:
                self.email.text = ""
                self.nom.text = ""
                self.prenom.text = ""
                self.mention.text = ""
                self.role.text = ""
                self.password.text = ""

        elif self.titre == "Titre mention":
            self.role.opacity = 0
            self.role.disabled = True
            self.password.opacity = 1
            self.password.disabled = False
            self.nom.opacity = 1
            self.nom.disabled = False
            self.semestre.opacity = 0
            self.semestre.disabled = True
            self.prenom.opacity = 1
            self.prenom.disabled = False
            self.mention.opacity = 0
            self.mention.disabled = True

            self.nom.hint_text = "Dérniere CE"
            self.password.hint_text = "Abréviation"
            self.prenom.hint_text = "Branche"

            self.ids.save_users.opacity = 0
            self.ids.save_mention.opacity = 1
            self.ids.save_parcours.opacity = 0
            self.ids.save_role.opacity = 0
            self.ids.save_annee.opacity = 0
            self.ids.save_droit.opacity = 0
            if MDApp.get_running_app().PUBLIC_ACTION_TYPE == "UPDATE":
                self.email.text = str(MDApp.get_running_app().read_by_key(
                    MDApp.get_running_app().ALL_MENTION, "uuid", MDApp.get_running_app().UUID_SELECTED)[0]["title"])
                self.nom.text = str(MDApp.get_running_app().read_by_key(
                    MDApp.get_running_app().ALL_MENTION, "uuid", MDApp.get_running_app().UUID_SELECTED)[0][
                                        "last_num_carte"])
                self.prenom.text = str(MDApp.get_running_app().read_by_key(
                    MDApp.get_running_app().ALL_MENTION, "uuid", MDApp.get_running_app().UUID_SELECTED)[0]["branche"])
                self.password.text = str(MDApp.get_running_app().read_by_key(
                    MDApp.get_running_app().ALL_MENTION, "uuid", MDApp.get_running_app().UUID_SELECTED)[0][
                                             "abreviation"])
            else:
                self.email.text = ""
                self.nom.text = ""
                self.prenom.text = ""
                self.passxord.text = ""
                self.mention.text = ""

        elif self.titre == "Titre parcours":

            self.role.opacity = 0
            self.role.disabled = True
            self.password.opacity = 1
            self.password.disabled = False
            self.nom.opacity = 0
            self.nom.disabled = True
            self.semestre.opacity = 1
            self.semestre.disabled = False
            self.prenom.opacity = 0
            self.prenom.disabled = True
            self.mention.opacity = 1
            self.mention.disabled = False

            self.password.hint_text = "Abréviation"

            self.ids.save_users.opacity = 0
            self.ids.save_mention.opacity = 0
            self.ids.save_parcours.opacity = 1
            self.ids.save_role.opacity = 0
            self.ids.save_annee.opacity = 0
            self.ids.save_droit.opacity = 0
            if MDApp.get_running_app().PUBLIC_ACTION_TYPE == "UPDATE":
                self.email.text = str(MDApp.get_running_app().read_by_key(
                    MDApp.get_running_app().ALL_PARCOURS, "uuid", MDApp.get_running_app().UUID_SELECTED)[0]["title"])
                self.nom.text = str(MDApp.get_running_app().read_by_key(
                    MDApp.get_running_app().ALL_PARCOURS, "uuid", MDApp.get_running_app().UUID_SELECTED)[0]["semestre"])
                self.password.text = str(MDApp.get_running_app().read_by_key(
                    MDApp.get_running_app().ALL_PARCOURS, "uuid", MDApp.get_running_app().UUID_SELECTED)[0][
                                             "abreviation"])
                uuid_mention = str(MDApp.get_running_app().read_by_key(
                    MDApp.get_running_app().ALL_PARCOURS, "uuid", MDApp.get_running_app().UUID_SELECTED)[0][
                                       "uuid_mention"])
                self.mention.text = str(MDApp.get_running_app().read_by_key(
                    MDApp.get_running_app().ALL_MENTION, "uuid", uuid_mention)[0][
                                            "title"])
                self.semestre.text = creat_str_from_list(
                    MDApp.get_running_app().read_by_key(
                        MDApp.get_running_app().ALL_PARCOURS, "uuid", MDApp.get_running_app().UUID_SELECTED)[0][
                            "semestre"])
            else:
                self.email.text = ""
                self.nom.text = ""
                self.prenom.text = ""
                self.password.text = ""
                self.mention.text = ""

        elif self.titre == "Titre role":
            self.role.opacity = 0
            self.role.disabled = True
            self.password.opacity = 0
            self.password.disabled = True
            self.nom.opacity = 0
            self.nom.disabled = True
            self.prenom.opacity = 0
            self.prenom.disabled = True
            self.mention.opacity = 0
            self.mention.disabled = True
            self.semestre.opacity = 0
            self.semestre.disabled = True

            self.ids.save_users.opacity = 0
            self.ids.save_mention.opacity = 0
            self.ids.save_parcours.opacity = 0
            self.ids.save_role.opacity = 1
            self.ids.save_annee.opacity = 0
            self.ids.save_droit.opacity = 0
            if MDApp.get_running_app().PUBLIC_ACTION_TYPE == "UPDATE":
                self.email.text = str(MDApp.get_running_app().read_by_key(
                    MDApp.get_running_app().ALL_ROLE, "uuid", MDApp.get_running_app().UUID_SELECTED)[0]["title"])
            else:
                self.email.text = ""
                self.nom.text = ""
                self.prenom.text = ""
                self.passxord.text = ""
                self.mention.text = ""

        elif self.titre == "Titre année":
            self.role.opacity = 0
            self.role.disabled = True
            self.password.opacity = 1
            self.password.disabled = False
            self.nom.opacity = 0
            self.nom.disabled = True
            self.prenom.opacity = 0
            self.prenom.disabled = True
            self.mention.opacity = 0
            self.mention.disabled = True
            self.semestre.opacity = 0
            self.semestre.disabled = True

            self.password.hint_text = "Moyenne"

            self.ids.save_users.opacity = 0
            self.ids.save_mention.opacity = 0
            self.ids.save_parcours.opacity = 0
            self.ids.save_role.opacity = 0
            self.ids.save_annee.opacity = 1
            self.ids.save_droit.opacity = 0
            if MDApp.get_running_app().PUBLIC_ACTION_TYPE == "UPDATE":
                self.email.text = str(MDApp.get_running_app().read_by_key(
                    MDApp.get_running_app().ALL_ANNEE, "uuid", MDApp.get_running_app().UUID_SELECTED)[0]["title"])
                self.password.text = str(MDApp.get_running_app().read_by_key(
                    MDApp.get_running_app().ALL_ANNEE, "uuid", MDApp.get_running_app().UUID_SELECTED)[0]["moyenne"])
            else:
                self.email.text = ""
                self.nom.text = ""
                self.prenom.text = ""
                self.passxord.text = ""
                self.mention.text = ""

        elif self.titre == "Montant":
            self.role.opacity = 0
            self.role.disabled = True
            self.password.opacity = 1
            self.password.disabled = False
            self.nom.opacity = 1
            self.nom.disabled = False
            self.prenom.opacity = 0
            self.prenom.disabled = True
            self.mention.opacity = 1
            self.mention.disabled = False
            self.semestre.opacity = 0
            self.semestre.disabled = True

            self.password.hint_text = "Niveau"
            self.nom.hint_text = "Année"

            self.ids.save_users.opacity = 0
            self.ids.save_mention.opacity = 0
            self.ids.save_parcours.opacity = 0
            self.ids.save_role.opacity = 0
            self.ids.save_annee.opacity = 0
            self.ids.save_droit.opacity = 1
            if MDApp.get_running_app().PUBLIC_ACTION_TYPE == "UPDATE":
                self.email.text = str(MDApp.get_running_app().read_by_key(
                    MDApp.get_running_app().ALL_DROIT, "uuid", MDApp.get_running_app().UUID_SELECTED)[0]["montant"])
                self.nom.text = str(MDApp.get_running_app().read_by_key(
                    MDApp.get_running_app().ALL_DROIT, "uuid", MDApp.get_running_app().UUID_SELECTED)[0]["annee"])
                self.password.text = str(MDApp.get_running_app().read_by_key(
                    MDApp.get_running_app().ALL_DROIT, "uuid", MDApp.get_running_app().UUID_SELECTED)[0]["niveau"])
                self.mention.text = str(MDApp.get_running_app().read_by_key(
                    MDApp.get_running_app().ALL_DROIT, "uuid", MDApp.get_running_app().UUID_SELECTED)[0]["mention"])
            else:
                self.email.text = ""
                self.nom.text = ""
                self.prenom.text = ""
                self.passxord.text = ""
                self.mention.text = ""

    def get_all_semestre(self):
        semestre = MDApp.get_running_app().ALL_SEMESTRE
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{semestre[i].upper()}",
                "height": dp(50),
                "width":dp(60),
                "on_release": lambda x=f"{semestre[i].upper()}": self.menu_calback_semestre(x),
            } for i in range(len(semestre))
        ]
        return menu_items

    def menu_calback_semestre(self, text_item):
        self.ids.semestre.text = select_str(self.ids.semestre.text, text_item)
        self.menu_semestre.dismiss()

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

    def get_all_role(self):
        role = []
        for titre in MDApp.get_running_app().ALL_ROLE:
            role.append(titre['title'])
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{role[i]}",
                "height": dp(50),
                "on_release": lambda x=f"{role[i]}": self.menu_calback_role(x),
            } for i in range(len(role))
        ]
        return menu_items

    def menu_calback_mention(self, text_item):
        if self.titre == "Email":
            self.ids.mention.text = select_str(self.ids.mention.text, text_item)
            self.ids.mention.multiline = True
            self.menu_mention.dismiss()
        else:
            self.selected_mention = \
                MDApp.get_running_app().read_by_key(MDApp.get_running_app().ALL_MENTION, "title", text_item)[0]['uuid']
            self.ids.mention.text = text_item
            self.menu_mention.dismiss()

    def menu_calback_role(self, text_item):
        self.selected_role = \
            MDApp.get_running_app().read_by_key(MDApp.get_running_app().ALL_ROLE, "title", text_item)[0]['uuid']
        self.ids.role.text = text_item
        self.menu_role.dismiss()

    def save_users(self):
        users_key = ["email", "is_active", "is_admin", "is_superuser", "first_name", "last_name",
                     "uuid_mention", "uuid_role", "password"]
        all_mention = create_list(self.ids.mention.text)
        uuid_mention = []
        for mention in all_mention:
            uuid = MDApp.get_running_app().read_by_key(MDApp.get_running_app().ALL_MENTION, "title", mention)[0]['uuid']
            uuid_mention.append(uuid)
        users_value = [self.ids.email.text, True, True, False, self.ids.nom.text, self.ids.prenom.text,
                       uuid_mention, self.selected_role, self.ids.password.text]

        if MDApp.get_running_app().PUBLIC_ACTION_TYPE == "UPDATE":
            url = f'http://{self.host}/api/v1/users/'
            params_key = ["uuid"]
            params_value = [MDApp.get_running_app().UUID_SELECTED]
            users = create_json_update(users_key, users_value)
            payload = json.dumps(users)
            response = update_with_params(url, params_key, params_value, self.token, payload)
        else:
            url = f'http://{self.host}/api/v1/users/'
            users = create_json(users_key, users_value)
            payload = json.dumps(users)
            response = create(url, self.token, payload)
        if response:
            if response[1] == 400:
                toast(response[0]['detail'])

            if response[1] == 200:
                all_users = []
                for user in response[0]:
                    if not user['is_superuser']:
                        if not user['is_superuser']:
                            all_mention = []
                            for uuid in user["uuid_mention"]:
                                all_mention.append(
                                    MDApp.get_running_app().read_by_key(MDApp.get_running_app().ALL_MENTION,
                                                                        "uuid", uuid)[0]["title"])
                                users = {"uuid": user['uuid'], "email": user["email"], "nom": user["first_name"],
                                         "prenom": user["last_name"],
                                         "role": MDApp.get_running_app().read_by_key(
                                             MDApp.get_running_app().ALL_ROLE, "uuid", user["uuid_role"])[0]["title"],
                                         "mention": creat_str_from_list(list(all_mention))}
                        all_users.append(users)
                MDApp.get_running_app().ALL_USERS = all_users
            elif response[1] == 400:
                toast(response[0]['detail'])
            else:
                toast(str(response))

    def save_mention(self):
        # create_json_update
        url = f"http://{self.host}/api/v1/mentions/"
        mention_key = ["title", "abreviation", "branche", "last_num_carte"]
        mention_value = [self.ids.email.text, self.ids.password.text, self.ids.prenom.text, self.ids.nom.text]
        if MDApp.get_running_app().PUBLIC_ACTION_TYPE == "UPDATE":
            params_key = ["uuid"]
            params_value = [MDApp.get_running_app().UUID_SELECTED]

            mention = create_json_update(mention_key, mention_value)
            payload = json.dumps(mention)

            response = update_with_params(url, params_key, params_value, self.token, payload)
        else:
            mention = create_json(mention_key, mention_value)
            payload = json.dumps(mention)

            response = create(url, self.token, payload)
        if response:
            if response[1] == 200:
                MDApp.get_running_app().ALL_MENTION = response[0]
            elif response[1] == 400:
                toast(response[0]['detail'])
            else:
                toast(str(response))

    def save_parcours(self):
        url = f"http://{self.host}/api/v1/parcours/"

        parcours_key = ["title", "abreviation", "uuid_mention", "semestre"]
        parcours_value = [self.ids.email.text, self.ids.password.text, self.selected_mention,
                          create_list(self.ids.semestre.text)]

        if MDApp.get_running_app().PUBLIC_ACTION_TYPE == "UPDATE":
            params_key = ["uuid"]
            params_value = [MDApp.get_running_app().UUID_SELECTED]
            parcours = create_json_update(parcours_key, parcours_value)
            payload = json.dumps(parcours)
            response = update_with_params(url, params_key, params_value, self.token, payload)
        else:
            parcours = create_json(parcours_key, parcours_value)
            payload = json.dumps(parcours)
            response = create(url, self.token, payload)
        if response:
            if response[1] == 200:
                MDApp.get_running_app().ALL_PARCOURS = response[0]
            elif response[1] == 400:
                toast(response[0]['detail'])
            else:
                toast(str(response))

    def save_role(self):
        url = f"http://{self.host}/api/v1/roles/"
        role_key = ["title"]
        role_value = [self.ids.email.text]

        if MDApp.get_running_app().PUBLIC_ACTION_TYPE == "UPDATE":
            params_key = ["uuid"]
            params_value = [MDApp.get_running_app().UUID_SELECTED]
            role = create_json_update(role_key, role_value)
            payload = json.dumps(role)
            response = update_with_params(url, params_key, params_value, self.token, payload)
        else:
            role = create_json(role_key, role_value)
            payload = json.dumps(role)
            response = create(url, self.token, payload)
        if response:
            if response[1] == 200:
                MDApp.get_running_app().ALL_ROLE = response[0]
            elif response[1] == 400:
                toast(response[0]['detail'])
            else:
                toast(response)

    def save_droit(self):
        url = f"http://{self.host}/api/v1/droit/"
        droit_key = ["droit", "niveau", "annee", "uuid_mention"]
        doit_value = [str(self.ids.email.text), str(self.ids.password.text),
                      str(self.ids.nom.text), self.selected_mention]

        if MDApp.get_running_app().PUBLIC_ACTION_TYPE == "UPDATE":
            params_key = ["uuid"]
            params_value = [MDApp.get_running_app().UUID_SELECTED]
            droit = create_json_update(droit_key, doit_value)
            payload = json.dumps(droit)
            response = update_with_params(url, params_key, params_value, self.token, payload)
        else:
            droit = create_json(droit_key, doit_value)
            payload = json.dumps(droit)
            response = create(url, self.token, payload)
        if response:
            if response[1] == 200:
                all_droit = []
                for droit in response[0]:
                    droit_ = {"niveau": droit["niveau"], "montant": droit["droit"], "annee": droit["annee"],
                              "mention": MDApp.get_running_app().read_by_key(MDApp.get_running_app().ALL_MENTION,
                                                                             "uuid", droit["uuid_mention"])[0]["title"]}
                    all_droit.append(droit_)
                MDApp.get_running_app().ALL_DROIT = all_droit
            elif response[1] == 400:
                toast(response[0]['detail'])
            else:
                toast(str(response))

    def save_annee(self):
        url = f"http://{self.host}/api/v1/anne_univ/"
        anne_key = ["title", "moyenne"]
        anne_value = [str(self.ids.email.text), str(self.ids.password.text)]

        if MDApp.get_running_app().PUBLIC_ACTION_TYPE == "UPDATE":
            params_key = ["uuid"]
            params_value = [MDApp.get_running_app().UUID_SELECTED]
            annee = create_json_update(anne_key, anne_value)
            payload = json.dumps(annee)
            response = update_with_params(url, params_key, params_value, self.token, payload)
        else:
            annee = create_json(anne_key, anne_value)
            payload = json.dumps(annee)
            response = create(url, self.token, payload)
        if response:
            if response[1] == 200:
                MDApp.get_running_app().ALL_ANNEE = response[0]
            elif response[1] == 400:
                toast(response[0]['detail'])
            else:
                toast(str(response))
