from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextFieldRound
from kivy.properties import BooleanProperty
from kivy.core.window import Window
from dotenv import load_dotenv
import os
from os.path import join, dirname
from pathlib import Path
from urllib import parse
import dp
import requests
# set window size
Window.size=(1000,600)

dotenv_path = join(dirname(__file__), ".env")
if dotenv_path:
    load_dotenv(dotenv_path)
else:
    print(".env not found")


class LoginApp(MDApp):
    dialog = None
    def build(self):
        # define theme colors
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.accent_palette = "Blue"
        self.host = os.getenv("host")
        # load and return kv string
        return Builder.load_file('login.kv')
    
    def login(self):
        # check entered username and password
        url_login:str = f"http://{self.host}/api/v1/login/access-token"
        session = requests.Session()
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        if len(self.root.ids.user.text) != 0 and len(self.root.ids.password.text) != 0:
            payload = {'username':self.root.ids.user.text,
                        'password':self.root.ids.password.text
                        }
            payload = parse.urlencode(payload)
            res = session.post(url_login,headers=headers, data=payload,verify=False)
            print(res.json())
            if not self.dialog:
                # create dialog
                self.dialog = MDDialog(
                    title="Log In",
                    text=f"Welcome {self.root.ids.user.text}! {self.host}",
                    buttons=[
                        MDFlatButton(
                            text="Ok", text_color=self.theme_cls.primary_color,
                            on_release=self.close
                        ),
                    ],
                )
            # open and display dialog
            self.dialog.open()

    def close(self, instance):
        # close dialog
        self.dialog.dismiss()
# run app    
LoginApp().run()