
import threading
from kivy.clock import mainthread
import time
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty,StringProperty
from kivymd.uix.datatables import MDDataTable
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton, MDIconButton
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp
from all_requests import request_utils, request_etudiants

from typing import Any

class ReinscriptionScreen(Screen):
    screenManager = ObjectProperty(None)
    dialog = None
    def init_data(self):
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

        self.annee = MDLabel(text=MDApp.get_running_app().ANNEE,
            pos_hint={'center_y': 0.95, 'center_x': 0.61},
            text_size="12dp",
            halign= "center"
        )

        self.edit_etudiant = MDIconButton(
            icon="account-edit",
            pos_hint={'center_y': 0.95, 'center_x': 0.9},
            opacity = 0,
            disabled=True
        )

        self.spinner = MDSpinner(
            pos_hint={'center_y': 0.5, 'center_x': 0.5},
            size = (dp(46), dp(46)),
            active = False
        )

        self.delete_etudiant = MDIconButton(
            icon="delete",
            opacity=0,
            pos_hint={'center_y': 0.95, 'center_x': 0.95},
            on_release = self.show_dialog
        )

        self.add_widget(self.titre)
        self.add_widget(self.annee)
        self.add_widget(self.edit_etudiant)
        self.add_widget(self.delete_etudiant)
        self.add_widget(self.spinner)

    def load_table(self):
        layout = AnchorLayout()
        self.data_tables = MDDataTable(
            pos_hint={'center_y': 0.55, 'center_x': 0.5},
            size_hint=(0.98, 0.75),
            use_pagination=True,
            rows_num = 8,
            column_data=[
                ("N°", dp(20)),
                ("CE", dp(30)),
                ("Nom et prénom", dp(100)),
                ("Parcours", dp(30))],
            )
        self.data_tables.bind(on_row_press = self.row_selected)
        # self.add_widget(self.semestre)
        # self.add_widget(self.semestre_label)
        self.add_widget(self.data_tables)
        return layout

    def active_button(self, *args):
        self.edit_etudiant.opacity = 1
        self.edit_etudiant.disabled = False
        self.edit_etudiant.md_bg_color=(0,0,0,0)
        self.delete_etudiant.opacity = 1
        self.delete_etudiant.disabled = False
        self.delete_etudiant.md_bg_color=(0,0,0,0)

    def on_enter(self):
        if not MDApp.get_running_app().IS_INITIALISE:
            self.load_table()
            self.init_data()
            MDApp.get_running_app().IS_INITIALISE = True


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
        MDApp.get_running_app().MENTION = MDApp.get_running_app().ALL_MENTIONS[i-1]
        if self.annee.text != "":
            self.spinner_toggle()
            self.process_spiner()
            self.spinner_toggle()
        self.ids.mention_label.text = text_item
        self.menu_mention.dismiss()

    
    @mainthread
    def spinner_toggle(self):
        print('Spinner Toggle')
        if self.spinner.active == False:
            self.spinner.active = True
        else:
            self.spinner.active = False

    def insert_data(self): 
        time.sleep(3)
        response=self.get_data()
        self.data_tables.row_data=response
        self.spinner_toggle()

    def get_data(self):
        data = []
        host = MDApp.get_running_app().HOST
        token = MDApp.get_running_app().TOKEN
        uuid_mention = MDApp.get_running_app().MENTION
        url_etudiant:str = f'http://{host}/api/v1/ancien_etudiants/by_mention/'
        response = request_etudiants.get_ancien_by_mention(url_etudiant, self.annee.text, uuid_mention, token)
        k:int = 0
        for un_et in response:
            etudiant = (k,un_et["num_carte"],f'{un_et["nom"]} {un_et["prenom"]}',(un_et["parcours"]).upper())
            data.append(etudiant)
            k += 1
        return data

    def process_spiner(self):
        self.spinner_toggle()
        threading.Thread(target=(
        self.insert_data())).start()

    def menu_calback_parcours(self,i, text_item):
        self.ids.parcours_label.text = text_item
        # self.menu_semestre.items = self.all_semestre[i]
        self.menu_parcours.dismiss()

    def menu_calback_semestre(self, text_item):
        self.ids.semestre_label.text = text_item
        self.menu_semestre.dismiss()

    def menu_calback_annee(self, text_item):
        self.annee.text = f"{text_item}"
        self.menu_annee_univ.dismiss()

    
    def calback(self, button):
        self.menu_mention.open()

    def add_new_etudiant(self):
        MDApp.get_running_app().root.current = 'Reinscription_add'

    def row_selected(self, table, row):
        start_index, end_index = row.table.recycle_data[row.index]["range"]
        print(row.table.recycle_data[start_index+1]["text"])
        self.data_tables.background_color_selected_cell = (1,1,1)
        self.active_button()

    def show_dialog(self,*args):
        if not self.dialog:
                # create dialog
            self.dialog = MDDialog(
                title="Log In",
                text="text",
                buttons=[
                    MDFlatButton(
                        text="Ok", 
                        on_release=self.delete_etudiant_
                    ),
                    MDFlatButton(
                        text="Annuler",
                        # on_release=root.delete_etudiant()
                    ),
                ],
                )
        self.dialog.open()

    def delete_etudiant_(self, *args):
        print("etudiant supprimé")
        self.dialog.dismiss()

    
