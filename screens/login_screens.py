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
from kivymd.uix.textfield import MDTextField

from all_requests.request_utils import login_post

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
            response = login_post(url_login, email, password)
            # response["access_token"] = "blablabla"
            sleep(1)
            if response:
                if response[1] == 200:
                    if "access_token" in response[0]:
                        self.ids.spinner.active = False
                        MDApp.get_running_app().TOKEN = response[0]["access_token"]
                        self.token = MDApp.get_running_app().TOKEN
                        MDApp.get_running_app().ALL_UUID_MENTION = response[0]["mention"]
                        MDApp.get_running_app().get_all_mention()
                        MDApp.get_running_app().get_annee_univ()
                        MDApp.get_running_app().get_all_droit()
                        if len(MDApp.get_running_app().ALL_ANNEE) != 0:
                            MDApp.get_running_app().ALL_UE = \
                                MDApp.get_running_app().get_all_ue(annee=MDApp.get_running_app().ALL_ANNEE[0]['title'])
                            MDApp.get_running_app().ALL_EC = \
                                MDApp.get_running_app().get_all_ec(annee=MDApp.get_running_app().ALL_ANNEE[0]['title'])
                        self.ids.email.text = ""
                        self.ids.password.text = ""
                        if response[0]['role'] == "supperuser":
                            MDApp.get_running_app().root.current = 'Public'
                            MDApp.get_running_app().get_all_parcours()
                            MDApp.get_running_app().get_all_role()
                            MDApp.get_running_app().get_all_users()
                        else:
                            # MDApp.get_running_app().root.current = 'Selection'
                            MDApp.get_running_app().root.current = 'Reinscription'
                            # MDApp.get_running_app().root.current = 'NoteAdd'
                elif response[1] == 400:
                    self.ids.spinner.active = False
                    MDApp.get_running_app().show_dialog(str(response[0]['detail']))
                else:
                    self.ids.spinner.active = False
                    MDApp.get_running_app().show_dialog(str(response))
        else:
            self.ids.password.require = True

    def auto_remplir(self):
        self.ids.email.text = "enricfranck@gmail.com"
        self.ids.password.text = "123"
        # self.ids.email.text = "admin@science.com"
        # self.ids.password.text = "aze135azq35sfsnf6353sfh3xb68yyp31gf68k5sf6h3s5d68jd5"
