from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty,StringProperty
from kivymd.uix.datatables import MDDataTable
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton, MDIconButton
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp

from all_requests import request_utils

from typing import Any

class ReinscriptionScreen(Screen):
    screenManager = ObjectProperty(None)
    def load_table(self):
        layout = AnchorLayout()
        self.menu_mention = MDDropdownMenu(
            caller = self.ids.mention_button,
            items = self.get_all_mention(),
            width_mult = 4,
        )

        self.menu_parcours = MDDropdownMenu(
            caller = self.ids.parcours_button,
            items = self.get_all_parcours(),
            width_mult = 4,
        )

        self.menu_semestre = MDDropdownMenu(
            caller = self.ids.semestre_button,
            width_mult = 4,
        )

        self.menu_annee_univ = MDDropdownMenu(
            caller = self.ids.annee_button,
            items = self.get_annee_univ(),
            width_mult = 4,
        )

        self.titre = MDLabel(text="Liste des étudiants:",
            pos_hint={'center_y': 0.95, 'center_x': 0.5},
            text_size="12dp",
            halign= "center"
        )

        self.edit_etudiant = MDIconButton(
            icon="account-edit",
            pos_hint={'center_y': 0.95, 'center_x': 0.9},
            opacity = 0,
            disabled=True
        )

        self.delete_etudiant = MDIconButton(
            icon="delete",
            opacity=1,
            pos_hint={'center_y': 0.95, 'center_x': 0.95},
            on_release = self.active_button
        )

        self.data_tables = MDDataTable(
            pos_hint={'center_y': 0.55, 'center_x': 0.5},
            size_hint=(0.98, 0.75),
            use_pagination=True,
            column_data=[
                ("N°", dp(20)),
                ("CE", dp(30)),
                ("Nom et prénom", dp(100)),
                ("Parcours", dp(30))],
            )
        self.add_widget(self.titre)
        self.add_widget(self.edit_etudiant)
        self.add_widget(self.delete_etudiant)
        # self.add_widget(self.parcours_label)
        # self.add_widget(self.semestre)
        # self.add_widget(self.semestre_label)
        self.add_widget(self.data_tables)
        return layout

    def active_button(self, *args):
        self.edit_etudiant.opacity = 1
        self.edit_etudiant.disabled = False
        self.edit_etudiant.md_bg_color=(0,0,0,1)

    def on_enter(self):
        self.load_table()

    def back_main(self):
        MDApp.get_running_app().root.current = 'Main'

    def get_all_mention(self):
        host = MDApp.get_running_app().HOST
        token = MDApp.get_running_app().TOKEN
        uuid_mention = MDApp.get_running_app().ALL_MENTION
        mention = []
        mention.append("")
        response = {}
        if len(uuid_mention) != 0:
            url_mention:str = f'http://{host}/api/v1/mentions/by_uuid'
            for uuid in uuid_mention:
                response = request_utils.get_mention_uuid(url_mention, uuid, token)
                if response:
                    mention.append(str(response[0]['title']))
        else:
            url_mention:str = f'http://{host}/api/v1/mentions/'
            response = request_utils.get_mention(url_mention, token)
            if response:
                mention.append(str(response[0]['title']))

        menu_items= [
            {
                "viewclass":"OneLineListItem",
                "text":f"{mention[i]}",
                "height":dp(56),
                "on_release": lambda x = f"{mention[i]}":self.menu_calback_mention(i,x),
                } for i in range(len(mention))
            ]
        return menu_items

    def get_all_parcours(self):
        parcours = []
        self.all_semestre = []
        self.semestre = []
        host = MDApp.get_running_app().HOST
        token = MDApp.get_running_app().TOKEN
        uuid_mention = MDApp.get_running_app().MENTION
        url_parcours:str = f'http://{host}/api/v1/parcours/by_mention/'
        response = request_utils.get_parcours_by_mention(url_parcours, uuid_mention, token)
        if response: 
            for rep in response:   
                parcours.append(str(rep['abreviation']))
                self.all_semestre.append(rep["semestre"])
                
        menu_items= [
            {
                "viewclass":"OneLineListItem",
                "text":f"{parcours[i]}",
                "height":dp(56),
                "on_release": lambda x = f"{parcours[i]}":self.menu_calback_parcours(i,x),
                } for i in range(len(parcours))
            ]
        return menu_items

    def get_annee_univ(self):
        host = MDApp.get_running_app().HOST
        token = MDApp.get_running_app().TOKEN
        annee_univ = []
        url_annee_univ:str = f'http://{host}/api/v1/anne_univ/'
        response = request_utils.get_annee_univ(url_annee_univ, token)
        if response:
            print(response)
            annee_univ.append(str(response[0]['title']))


        menu_items= [
            {
                "viewclass":"OneLineListItem",
                "text":f"{annee_univ[i]}",
                "height":dp(56),
                "on_release": lambda x = f"{annee_univ[i]}":self.menu_calback_annee(x),
                } for i in range(len(annee_univ))
            ]
        return menu_items

    def get_all_semestre(self):
        menu_items= [
            {
                "viewclass":"OneLineListItem",
                "text":f"{self.semestre[i]}",
                "height":dp(56),
                "on_release": lambda x = f"{self.semestre[i]}":self.menu_calback_semestre(x),
                } for i in range(len(self.semestre))
            ]
        return menu_items

    def menu_calback_mention(self,i, text_item):
        self.data_tables.row_data=[
                (f"{i + 1}", f"M00011{i+5}", "RALAITSIMANOLAKAVANA Henri Franck", "35",)
                for i in range(8)]
        self.ids.mention_label.text = text_item
        MDApp.get_running_app().MENTION = MDApp.get_running_app().ALL_MENTIONS[i-1]
        self.menu_mention.dismiss()
    
    def menu_calback_parcours(self,i, text_item):
        self.data_tables.row_data=[
                (f"{i + 1}", f"M00011{i+5}", "RALAITSIMANOLAKAVANA Henri Franck", f"{text_item}",)
                for i in range(8)]
        self.ids.parcours_label.text = text_item
        # self.menu_semestre.items = self.all_semestre[i]
        self.menu_parcours.dismiss()

    def menu_calback_semestre(self, text_item):
        self.data_tables.row_data=[
                (f"{i + 1}", f"M00011{i+5}", "RALAITSIMANOLAKAVANA Henri Franck", f"{text_item}",)
                for i in range(8)]
        self.ids.semestre_label.text = text_item
        self.menu_semestre.dismiss()

    def menu_calback_annee(self, text_item):
        self.data_tables.row_data=[
                (f"{i + 1}", f"M00011{i+5}", "RALAITSIMANOLAKAVANA Henri Franck", f"{text_item}",)
                for i in range(8)]
        self.titre.text = f"Liste des étudiants:{text_item}"
        self.menu_annee_univ.dismiss()

    
    def calback(self, button):
        self.menu_mention.open()


    
