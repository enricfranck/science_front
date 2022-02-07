
from dotenv import load_dotenv
import os
import sys
from pathlib import Path
from time import sleep, time

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty,StringProperty, BooleanProperty
from kivymd.uix.textfield import MDTextField
from kivy.clock import Clock
from functools import partial
from kivymd.uix.datatables import MDDataTable
from kivy.uix.anchorlayout import AnchorLayout

from all_requests import request_login
from kivy.metrics import dp


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
                    self.cursor = (0,0)
                    Clock.schedule_once(partial(self.set_cursor, cursor))
        return super(MyMDTextField, self).on_touch_down(touch)

    def set_cursor(self, pos, dt):
        self.cursor = pos

class LoginScreen(Screen):
    screenManager = ObjectProperty(None)
    def login(self):
        host = MDApp.get_running_app().HOST
        email = self.ids.email.text
        password = self.ids.password.text
        url_login:str = f"http://{host}/api/v1/login/access-token"

        if len(email) != 0 and len(password) != 0:
            self.ids.spinner.active = True
            response = {}
            response = request_login.login_post(url_login, email, password)
            # response["access_token"] = "blablabla"
            sleep(1)
            if "access_token" in response:
                self.ids.spinner.active = False
                MDApp.get_running_app().root.current = 'Reinscription'
                MDApp.get_running_app().TOKEN = response["access_token"]
                MDApp.get_running_app().ALL_MENTIONS = response["mention"]
                MDApp.get_running_app().MENTION = MDApp.get_running_app().ALL_MENTIONS[0]
                self.ids.email.text = ""
                self.ids.password.text = ""
            else:
                self.ids.spinner.active = False
                MDApp.get_running_app().show_dialog(str(response['detail']))
        else:
            self.ids.password.require = True

    def auto_remplir(self):
        self.ids.email.text = "franck@example.com"
        self.ids.password.text = "123"
        # self.ids.email.text = "admin@science.com"
        # self.ids.password.text = "aze135azq35sfsnf6353sfh3xb68yyp31gf68k5sf6h3s5d68jd5"

