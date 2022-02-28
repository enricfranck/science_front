import sys
from functools import partial
from pathlib import Path
from time import sleep

from dotenv import load_dotenv
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.textfield import MDTextField

from all_requests import request_login, request_utils

parent = Path(__file__).resolve().parent.parent / ""
sys.path.append(str(parent))

dotenv_path = Path(__file__).resolve().parent.parent / ".env"
if dotenv_path.exists():
    load_dotenv(dotenv_path)
else:
    print(".env not found")


class MyMDTextField(MDTextField):
    password_mode = BooleanProperty(True)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.icon_right:
                # icon position based on the KV code for MDTextField
                icon_x = (self.width + self.x) - (self._lbl_icon_right.texture_size[1]) - dp(8)
                icon_y = self.center[1] - self._lbl_icon_right.texture_size[1] / 2
                if self.mode == "rectangle":
                    icon_y -= dp(4)
                elif self.mode != 'fill':
                    icon_y += 8

                # not a complete bounding box test, but should be sufficient
                if touch.pos[0] > icon_x and touch.pos[1] > icon_y:
                    if self.password_mode:
                        self.icon_right = 'eye'
                        self.password_mode = False
                        self.password = self.password_mode
                    else:
                        self.icon_right = 'eye-off'
                        self.password_mode = True
                        self.password = self.password_mode

                    # try to adjust cursor position
                    cursor = self.cursor
                    self.cursor = (0, 0)
                    Clock.schedule_once(partial(self.set_cursor, cursor))
        return super(MyMDTextField, self).on_touch_down(touch)

    def set_cursor(self, pos, dt):
        self.cursor = pos


class LoginScreen(Screen):
    screenManager = ObjectProperty(None)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.host = MDApp.get_running_app().HOST
        self.token = ""

    def login(self):
        email = self.ids.email.text
        password = self.ids.password.text
        url_login: str = f"http://{self.host}/api/v1/login/access-token"

        if len(email) != 0 and len(password) != 0:
            self.ids.spinner.active = True
            response = {}
            response = request_login.login_post(url_login, email, password)
            # response["access_token"] = "blablabla"
            sleep(1)
            if "access_token" in response:
                self.ids.spinner.active = False
                MDApp.get_running_app().TOKEN = response["access_token"]
                self.token = MDApp.get_running_app().TOKEN
                MDApp.get_running_app().ALL_UUID_MENTION = response["mention"]
                # MDApp.get_running_app().MENTION = MDApp.get_running_app().ALL_UUID_MENTION[0]
                self.get_all_mention()
                self.get_annee_univ()
                self.get_all_droit()
                self.ids.email.text = ""
                self.ids.password.text = ""
                if response['role'] == "supperuser":
                    MDApp.get_running_app().root.current = 'Public'
                    self.get_all_parcours()
                    self.get_all_role()
                    self.get_all_users()
                else:
                    MDApp.get_running_app().root.current = 'Selection'
                # MDApp.get_running_app().root.current = 'Reinscription'
            else:
                self.ids.spinner.active = False
                MDApp.get_running_app().show_dialog(str(response['detail']))
        else:
            self.ids.password.require = True

    def auto_remplir(self):
        # self.ids.email.text = "enricfranck@gmail.com"
        # self.ids.password.text = "123"
        self.ids.email.text = "admin@science.com"
        self.ids.password.text = "aze135azq35sfsnf6353sfh3xb68yyp31gf68k5sf6h3s5d68jd5"

    def get_all_mention(self):
        """
        retrieve all mention from the database
        :return:
        """
        uuid_mention = MDApp.get_running_app().ALL_UUID_MENTION

        if len(uuid_mention) != 0:
            url_mention: str = f'http://{self.host}/api/v1/mentions/by_uuid'
            for uuid in uuid_mention:
                response = request_utils.get_with_params(url_mention, ["uuid"], [uuid], self.token)
                if response:
                    if response[1] == 200:
                        MDApp.get_running_app().ALL_MENTION.append(response[0])
                    elif response[1] == 400:
                        toast(response[0]["detail"])
                    else:
                        toast(response)
        else:
            url_mention: str = f'http://{self.host}/api/v1/mentions/'
        MDApp.get_running_app().ALL_MENTION = self.get_response(url_mention)

    def get_annee_univ(self):
        """
        retrieve all years from the database
        :return:
        """
        url_annee_univ: str = f'http://{self.host}/api/v1/anne_univ/'
        MDApp.get_running_app().ALL_ANNEE = self.get_response(url_annee_univ)

    def get_all_parcours(self):
        """
        retrieve all parcours from the database
        :return:
        """
        url_parcours: str = f'http://{self.host}/api/v1/parcours/'
        MDApp.get_running_app().ALL_PARCOURS = self.get_response(url_parcours)

    def get_all_role(self):
        """
        Retrieve all role from the api
        :return:
        """
        url_role: str = f"http://{self.host}/api/v1/roles/"
        MDApp.get_running_app().ALL_ROLE = self.get_response(url_role)

    def get_all_droit(self):
        """
        Retrieve all role from the api
        :return:
        """
        url_droit: str = f"http://{self.host}/api/v1/droit/"
        MDApp.get_running_app().ALL_DROIT = self.get_response(url_droit)
        all_droit = []
        for droit in MDApp.get_running_app().ALL_DROIT:
            droit_ = {"uuid": droit['uuid'], "niveau": droit["niveau"], "montant": droit["droit"], "annee": droit["annee"],
                      "mention": MDApp.get_running_app().read_by_key(MDApp.get_running_app().ALL_MENTION,
                                                                     "uuid", droit["uuid_mention"])[0]["title"]}
            all_droit.append(droit_)
        MDApp.get_running_app().ALL_DROIT = all_droit

    def get_all_users(self):
        url_user = f'http://{self.host}/api/v1/users/get_all/'
        MDApp.get_running_app().ALL_USERS = self.get_response(url_user)
        all_users = []
        for user in MDApp.get_running_app().ALL_USERS:
            if not user['is_superuser']:
                users = {"uuid": user['uuid'], "email": user["email"], "prenom": user["last_name"],
                         "role": MDApp.get_running_app().read_by_key(MDApp.get_running_app().ALL_ROLE,
                                                                     "uuid", user["uuid_role"])[0]["title"],
                         "mention": MDApp.get_running_app().read_by_key(MDApp.get_running_app().ALL_MENTION,
                                                                        "uuid", user["uuid_mention"][0])[0]["title"]}
                all_users.append(users)
        MDApp.get_running_app().ALL_USERS = all_users

    def get_response(self, url: str):
        response = request_utils.get(url, self.token)
        if response:
            if response[1] == 200:
                return response[0]
            elif response[1] == 400:
                toast(response[0]["detail"])
            else:
                toast(response)
