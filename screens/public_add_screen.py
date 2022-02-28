import json

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivymd.material_resources import dp
from kivymd.toast import toast
from kivymd.uix.menu import MDDropdownMenu

from all_requests.request_utils import create_json, create


class PublicAddScreen(Screen):
    screenManager = ObjectProperty(None)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.selected_role = None
        self.token = None
        self.host = None
        self.selected_mention = None
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

            self.nom.hint_text = "Nom"
            self.password.hint_text = "Password"
            self.prenom.hint_text = "Prénom"

            self.ids.save_users.opacity = 1
            self.ids.save_mention.opacity = 0
            self.ids.save_parcours.opacity = 0
            self.ids.save_role.opacity = 0
            self.ids.save_annee.opacity = 0
            self.ids.save_droit.opacity = 0

        elif self.titre == "Titre mention":
            self.role.opacity = 0
            self.role.disabled = True
            self.password.opacity = 1
            self.password.disabled = False
            self.nom.opacity = 1
            self.nom.disabled = False
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

        elif self.titre == "Titre parcours":
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

            self.nom.hint_text = "Semestre"
            self.password.hint_text = "Abréviation"

            self.ids.save_users.opacity = 0
            self.ids.save_mention.opacity = 0
            self.ids.save_parcours.opacity = 1
            self.ids.save_role.opacity = 0
            self.ids.save_annee.opacity = 0
            self.ids.save_droit.opacity = 0

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

            self.ids.save_users.opacity = 0
            self.ids.save_mention.opacity = 0
            self.ids.save_parcours.opacity = 0
            self.ids.save_role.opacity = 1
            self.ids.save_annee.opacity = 0
            self.ids.save_droit.opacity = 0

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

            self.password.hint_text = "Moyenne"

            self.ids.save_users.opacity = 0
            self.ids.save_mention.opacity = 0
            self.ids.save_parcours.opacity = 0
            self.ids.save_role.opacity = 0
            self.ids.save_annee.opacity = 1
            self.ids.save_droit.opacity = 0

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

            self.password.hint_text = "Niveau"
            self.nom.hint_text = "Année"

            self.ids.save_users.opacity = 0
            self.ids.save_mention.opacity = 0
            self.ids.save_parcours.opacity = 0
            self.ids.save_role.opacity = 0
            self.ids.save_annee.opacity = 0
            self.ids.save_droit.opacity = 1

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
        url = f'http://{self.host}/api/v1/users/get_all/'
        users_key = ["email", "is_active", "is_admin", "is_superuser", "first_name", "last_name",
                     "uuid_mention", "uuid_role", "password"]
        users_value = [self.ids.email.text, True, True, False, self.ids.nom.text, self.ids.prenom.text,
                       [self.selected_mention], self.selected_role, self.ids.password.text]

        users = create_json(users_key, users_value)
        payload = json.dumps(users)
        response = create(url, self.token, payload)
        if response:
            all_users = []
            for user in response[0]:
                if not user['is_superuser']:
                    users = {"email": user["email"], "prenom": user["last_name"],
                             "role": MDApp.get_running_app().read_by_key(MDApp.get_running_app().ALL_ROLE,
                                                                         "uuid", user["uuid_role"])[0]["title"],
                             "mention": MDApp.get_running_app().read_by_key(MDApp.get_running_app().ALL_MENTION,
                                                                            "uuid", user["uuid_mention"])[0]["title"]}
                    all_users.append(users)
            MDApp.get_running_app().ALL_USERS = all_users
            if response[1] == 400:
                toast(response[0]['detail'])

    def save_mention(self):
        url = f"http://{self.host}/api/v1/mentions/"
        mention_key = ["title", "abreviation", "branche", "last_num_carte"]
        mention_value = [self.ids.email.text, self.ids.password.text, self.ids.prenom.text, self.ids.nom.text]

        mention = create_json(mention_key, mention_value)
        payload = json.dumps(mention)
        response = create(url, self.token, payload)
        if response:
            if response[1] == 200:
                MDApp.get_running_app().ALL_MENTION = response[0]
            if response[1] == 400:
                toast(response[0]['detail'])

    def save_parcours(self):
        url = f"http://{self.host}/api/v1/parcours/"

        parcours_key = ["title", "abreviation", "uuid_mention", "semestre"]
        parcours_value = [self.ids.email.text, self.ids.password.text, self.selected_mention, list(self.ids.nom.text)]

        parcours = create_json(parcours_key, parcours_value)
        payload = json.dumps(parcours)
        response = create(url, self.token, payload)
        if response:
            if response[1] == 200:
                MDApp.get_running_app().ALL_PARCOURS = response[0]
            if response[1] == 400:
                toast(response[0]['detail'])

    def save_role(self):
        url = f"http://{self.host}/api/v1/roles/"
        role_key = ["title"]
        role_value = [self.ids.email.text]

        role = create_json(role_key, role_value)
        payload = json.dumps(role)
        response = create(url, self.token, payload)
        if response:
            if response[1] == 200:
                MDApp.get_running_app().ALL_ROLE = response[0]
            if response[1] == 400:
                toast(response[0]['detail'])

    def save_droit(self):
        url = f"http://{self.host}/api/v1/droit/"
        droit_key = ["droit", "niveau", "annee", "uuid_mention"]
        doit_value = [str(self.ids.email.text), str(self.ids.password.text),
                      str(self.ids.nom.text), self.selected_mention]

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
                toast(response)

    def save_annee(self):
        url = f"http://{self.host}/api/v1/anne_univ/"
        anne_key = ["title", "moyenne"]
        anne_value = [str(self.ids.email.text), str(self.ids.password.text)]

        annee = create_json(anne_key, anne_value)
        payload = json.dumps(annee)
        response = create(url, self.token, payload)
        if response:
            if response[1] == 200:
                MDApp.get_running_app().ALL_ANNEE = response[0]
            elif response[1] == 400:
                toast(response[0]['detail'])
            else:
                toast(response)
