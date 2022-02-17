from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty,StringProperty

class MainScreen(Screen):
    screenManager = ObjectProperty(None)
    def login(self):
        email = self.ids.email.text
        password = self.ids.password.text
        print(email, password)
    
    def logout(seld):
    
        MDApp.get_running_app().root.current = 'Login'
        MDApp.get_running_app().TOKEN = ""
        MDApp.get_running_app().ALL_UUID_MENTION = []
        MDApp.get_running_app().ALL_MENTION = []
        MDApp.get_running_app().ALL_PARCOURS = []
        MDApp.get_running_app().ALL_ETUDIANT = []
        MDApp.get_running_app().MENTION = ""
        MDApp.get_running_app().NUM_CARTE = ""
        MDApp.get_running_app().IS_INITIALISE = False
