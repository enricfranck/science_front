import sys
from kivy.clock import mainthread, Clock
from functools import partial
from pathlib import Path
from time import sleep, time
import threading
from dotenv import load_dotenv
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu

from all_requests.request_utils import login_post
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils import get_data_from_json, get_item_by_title_from_json

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
        self.menu_server = None
        self.response = None
        self.host = ""
        self.token = ""
        self.menu_server = MDDropdownMenu(
            items=self.get_all_server(),
            width_mult=4,
        )

    def callback(self, button):
        self.menu_server.caller = button
        self.menu_server.open()

    def get_all_server(self):
        server = get_data_from_json('server', "server")
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{server[i]['title']}",
                "height": dp(50),
                "on_release": lambda x=f"{server[i]['title']}": self.menu_calback_server(x),
            } for i in range(len(server))
        ]
        return menu_items

    def menu_calback_server(self, text_item):
        self.ids.server.text = text_item
        server = get_item_by_title_from_json(text_item, "server", "server")
        MDApp.get_running_app().HOST = server['address']
        self.ids.adress.text = f"Adresse:{MDApp.get_running_app().HOST}"
        self.menu_server.dismiss()

    def thread_login_(self):
        self.spinner_toggle()
        self.login()

    @mainthread
    def reset_champ(self):
        self.ids.email.text = ""
        self.ids.password.text = ""

    @mainthread
    def spinner_toggle(self, *args):
        if not self.ids.spinner.active:
            self.ids.spinner.active = True
        else:
            self.ids.spinner.active = False

    def thread_login(self):
        self.spinner_toggle()
        threading.Thread(target=(
            self.login)).start()

    @mainthread
    def navigate_screen(self, name: str):
        MDApp.get_running_app().root.current = name

    @mainthread
    def show_dialog(self, message: str):
        MDApp.get_running_app().show_dialog(message)

    def login(self):
        self.host = MDApp.get_running_app().HOST
        email = self.ids.email.text
        password = self.ids.password.text
        url_login: str = f"http://{self.host}/api/v1/login/access-token"
        if len(email) != 0 and len(password) != 0:
            response = login_post(url_login, email, password)
            if response:
                if response[1] == 200:
                    if "access_token" in response[0]:
                        MDApp.get_running_app().TOKEN = response[0]["access_token"]
                        self.token = MDApp.get_running_app().TOKEN
                        MDApp.get_running_app().ALL_UUID_MENTION = response[0]["mention"]
                        start = time()
                        get_anne()
                        processes = []
                        with ThreadPoolExecutor(max_workers=10) as executor:
                            processes.append(executor.submit(get_mention))
                            processes.append(executor.submit(get_droit))
                            if len(MDApp.get_running_app().ALL_ANNEE) != 0:
                                processes.append(executor.submit(get_ue, MDApp.get_running_app().ALL_ANNEE[0]['title']))
                                processes.append(executor.submit(get_ec, MDApp.get_running_app().ALL_ANNEE[0]['title']))

                        print(f'Time taken: {time() - start}')
                        if response[0]['role'] == "supperuser":
                            start = time()
                            processes = []
                            with ThreadPoolExecutor(max_workers=10) as executor:
                                processes.append(executor.submit(MDApp.get_running_app().get_all_parcours()))
                                processes.append(executor.submit(MDApp.get_running_app().get_all_role()))
                                processes.append(executor.submit(MDApp.get_running_app().get_all_users()))
                            print(f'Time taken: {time() - start}')
                            self.navigate_screen("Public")
                        else:
                            MDApp.get_running_app().USER_EMAIL = email
                            MDApp.get_running_app().USER_ROLE = response[0]['role']
                            MDApp.get_running_app().root.current = 'Main'
                    self.reset_champ()
                elif response[1] == 400:
                    self.show_dialog(str(response[0]['detail']))
                    self.ids.spinner.active = False
                else:
                    self.show_dialog(str(response))
                    self.ids.spinner.active = False
        self.spinner_toggle()

    def auto_remplir(self):
        # self.ids.email.text = "enricfranck@gmail.com"
        # self.ids.password.text = "123"
        self.ids.email.text = "admin@science.com"
        self.ids.password.text = "aze135azq35sfsnf6353sfh3xb68yyp31gf68k5sf6h3s5d68jd5"

    def active_spinner(self):
        self.ids.spinner.active = True


def get_mention():
    MDApp.get_running_app().get_all_mention()


def get_anne():
    MDApp.get_running_app().get_annee_univ()


def get_droit():
    MDApp.get_running_app().get_all_droit()


def get_ue(annee):
    if len(MDApp.get_running_app().ALL_ANNEE) != 0:
        MDApp.get_running_app().ALL_UE = \
            MDApp.get_running_app().get_all_ue(annee=annee)


def get_ec(anne):
    if len(MDApp.get_running_app().ALL_ANNEE) != 0:
        MDApp.get_running_app().ALL_EC = \
            MDApp.get_running_app().get_all_ec(annee=anne)
