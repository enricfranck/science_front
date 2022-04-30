import json
import os.path
import secrets
import string
import threading
from kivy.clock import mainthread

from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty, get_color_from_hex
from kivymd.material_resources import dp
from kivymd.toast import toast
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.picker import MDDatePicker
from all_requests.request_etudiants import save_etudiant, post_photo, update_etudiant
from all_requests.request_utils import create_json, create_with_params, create_json_update, update_with_params


class ReinscriptionAddScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.photo = None
        self.menu_etat = None
        self.menu_sexe = None
        self.menu_nation = None
        self.host = None
        self.master_two = None
        self.master_one = None
        self.license = None
        self.s9 = None
        self.s8 = None
        self.s6 = None
        self.s4 = None
        self.s7 = None
        self.s5 = None
        self.s1 = None
        self.s10 = None
        self.s3 = None
        self.s2 = None
        self.check_box = []
        self.menu_mention = None
        self.menu_parcours = None
        self.path = ""
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            # preview=True,
        )

        self.selected_mention = ""
        self.selected_parcours = ""
        self.list_semestre = ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10"]
        self.selected_semestre = []

        # self.ids.s7_check.bind(
        #     on_active=self.disabled_check_licence()
        # )

    screenManager = ObjectProperty(None)

    @mainthread
    def spinner_toggle(self):
        if not self.ids.spinner.active:
            self.ids.spinner.active = True
        else:
            self.ids.spinner.active = False

    def process_enreg_toggle(self):
        self.spinner_toggle()
        threading.Thread(target=(
            self.enreg_etudiant)).start()

    def on_enter(self):
        menu_etat = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{i}",
                "height": dp(50),
                "on_release": lambda x=f"{i}": self.menu_calback_etat(x),
            } for i in MDApp.get_running_app().ALL_ETAT
        ]

        self.menu_etat = MDDropdownMenu(
            caller=self.ids.etat,
            items=menu_etat,
            width_mult=4,
        )
        menu_sexe = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{i}",
                "height": dp(50),
                "on_release": lambda x=f"{i}": self.menu_calback_sexe(x),
            } for i in MDApp.get_running_app().ALL_SEXE
        ]

        self.menu_sexe = MDDropdownMenu(
            caller=self.ids.sexe,
            items=menu_sexe,
            width_mult=4,
        )

        menu_nation = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{i}",
                "height": dp(50),
                "on_release": lambda x=f"{i}": self.menu_calback_nation(x),
            } for i in MDApp.get_running_app().ALL_NATION
        ]

        self.menu_nation = MDDropdownMenu(
            caller=self.ids.nation,
            items=menu_nation,
            width_mult=4,
        )
        self.s1 = self.ids.s1_check
        self.s2 = self.ids.s2_check
        self.s3 = self.ids.s3_check
        self.s4 = self.ids.s4_check
        self.s5 = self.ids.s5_check
        self.s6 = self.ids.s6_check
        self.s7 = self.ids.s7_check
        self.s8 = self.ids.s8_check
        self.s9 = self.ids.s9_check
        self.s10 = self.ids.s10_check

        self.license = [self.s1, self.s2, self.s3, self.s4, self.s5, self.s6]
        self.master_one = [self.s7, self.s8]
        self.master_two = [self.s9, self.s10]

        self.check_box = self.license + self.master_one + self.master_two
        for check in self.check_box:
            check.active = False
        self.menu_mention = MDDropdownMenu(
            caller=self.ids.mention_field,
            items=self.get_all_mention(),
            width_mult=4,
        )

        self.menu_parcours = MDDropdownMenu(
            caller=self.ids.mention_field,
            items=self.get_all_parcours(),
            width_mult=4,
        )
        if MDApp.get_running_app().REINSCRIPTION_ACTION_TYPE == "UPDATE":
            num_carte = MDApp.get_running_app().NUM_CARTE
            self.host = MDApp.get_running_app().HOST
            if num_carte != "":
                un_etudiant = self.read_by_num_carte(MDApp.get_running_app().ALL_ETUDIANT, num_carte)[0]
                self.photo = str(un_etudiant["photo"])
                self.ids.num_ce.text = str(un_etudiant["num_carte"])
                self.ids.nom.text = str(un_etudiant["nom"])
                self.ids.prenom.text = str(un_etudiant["prenom"])
                self.ids.sexe.text = str(un_etudiant["sexe"])
                self.ids.date_naiss.text = str(un_etudiant["date_naiss"])
                self.ids.lieu_naiss.text = str(un_etudiant["lieu_naiss"])
                self.ids.addresse.text = str(un_etudiant["adresse"])
                self.ids.num_cin.text = str(un_etudiant["num_cin"])
                self.ids.date_cin.text = str(un_etudiant["date_cin"])
                self.ids.lieu_cin.text = str(un_etudiant["lieu_cin"])
                self.ids.num_quintance.text = str(un_etudiant["num_quitance"])
                self.ids.date_quintance.text = str(un_etudiant["date_quitance"])
                self.ids.montant.text = str(un_etudiant["montant"])
                self.ids.etat.text = str(un_etudiant["etat"])
                self.ids.nation.text = str(un_etudiant["nation"])
                self.ids.moyenne.text = str(un_etudiant["moyenne"])
                self.ids.bacc_annee.text = str(un_etudiant["bacc_anne"])
                self.ids.parcours_field.text = str(un_etudiant["parcours"]).upper()
                self.ids.mention_field.text = \
                    MDApp.get_running_app().read_by_key(MDApp.get_running_app().ALL_MENTION, "uuid",
                                                        MDApp.get_running_app().MENTION)[0]["title"]
                self.selected_parcours = \
                    MDApp.get_running_app().read_by_key(MDApp.get_running_app().ALL_PARCOURS,
                                                        "abreviation", un_etudiant["parcours"])[0]["uuid"]
                self.selected_mention = MDApp.get_running_app().MENTION
                self.set_semestre([un_etudiant["semestre_petit"], un_etudiant["semestre_grand"]])
                try:
                    self.ids.ellipse.source = \
                        StringProperty(''+str(f'http://{self.host}/api/v1/ancien_etudiants/photo?name_file='
                                       f'{str(un_etudiant["photo"])}.jpg'))
                    print(self.ids.ellipse.source)
                except Exception as e:
                    print(e)
                    pass

    def back_home(self):
        MDApp.get_running_app().root.current = 'Reinscription'

    def read_by_num_carte(self, data: list, num_carte: str):
        return list(filter(lambda etudiant: etudiant["num_carte"] == num_carte, data))

    def menu_calback_sexe(self, text_item):
        self.ids.sexe.text = text_item
        self.menu_sexe.dismiss()

    def menu_calback_nation(self, text_item):
        self.ids.nation.text = text_item
        self.menu_nation.dismiss()

    def menu_calback_etat(self, text_item):
        self.ids.etat.text = text_item
        self.menu_etat.dismiss()

    def file_manager_open(self):
        self.file_manager.show('/')  # output manager to the screen
        self.manager_open = True

    def select_path(self, path):
        """It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        """
        if os.path.isfile(path):
            self.path = path
            try:
                self.ids.ellipse.source = f"{path}"
                toast(self.ids.ellipse.source)
            except Exception as e:
                toast(e)
        self.exit_manager()

    def exit_manager(self, *args):
        """Called when the user reaches the root of the directory tree."""

        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        """Called when buttons are pressed on the mobile device."""

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True

    def on_cancel(self, instance, value):
        """Events called when the "CANCEL" dialog box button is clicked."""

    def on_save_cin(self, instance, value, date_range):
        """
        """
        self.ids.date_cin.text = str(value)

    def show_date_picker_cin(self, ):
        date_dialog = MDDatePicker(min_year=1980,
                                   max_year=2030,
                                   primary_color=get_color_from_hex("#72225b"),
                                   accent_color=get_color_from_hex("#5d1a4a"),
                                   selector_color=get_color_from_hex("#e93f39"),
                                   text_toolbar_color=get_color_from_hex("#cccccc"),
                                   text_color="#ffffff",
                                   text_current_color=get_color_from_hex("#e93f39"),
                                   input_field_background_color=(1, 1, 1, 0.2), )
        date_dialog.bind(on_save=self.on_save_cin, on_cancel=self.on_cancel)
        date_dialog.open()

    def on_save_naiss(self, instance, value, date_range):
        """
        """
        self.ids.date_naiss.text = str(value)

    def show_date_picker_naiss(self):
        date_dialog = MDDatePicker(min_year=1980,
                                   max_year=2030,
                                   primary_color=get_color_from_hex("#72225b"),
                                   accent_color=get_color_from_hex("#5d1a4a"),
                                   selector_color=get_color_from_hex("#e93f39"),
                                   text_toolbar_color=get_color_from_hex("#cccccc"),
                                   text_color="#ffffff",
                                   text_current_color=get_color_from_hex("#e93f39"),
                                   input_field_background_color=(1, 1, 1, 0.2), )
        date_dialog.bind(on_save=self.on_save_naiss, on_cancel=self.on_cancel)
        date_dialog.open()

    def on_save_quint(self, instance, value, date_range):
        """
        """
        self.ids.date_quintance.text = str(value)

    def show_date_picker_quint(self):
        date_dialog = MDDatePicker(min_year=1980,
                                   max_year=2030,
                                   primary_color=get_color_from_hex("#72225b"),
                                   accent_color=get_color_from_hex("#5d1a4a"),
                                   selector_color=get_color_from_hex("#e93f39"),
                                   text_toolbar_color=get_color_from_hex("#cccccc"),
                                   text_color="#ffffff",
                                   text_current_color=get_color_from_hex("#e93f39"),
                                   input_field_background_color=(1, 1, 1, 0.2), )
        date_dialog.bind(on_save=self.on_save_quint, on_cancel=self.on_cancel)
        date_dialog.open()

    @mainthread
    def enreg_etudiant(self):
        self.selected_semestre = self.get_semestre()
        annee = MDApp.get_running_app().ANNEE
        schemas = "anne_" + annee[0:4] + "_" + annee[5:9]
        num_carte = self.ids.num_ce.text
        if len(annee) != 0:
            if len(self.selected_semestre) != 0:
                photo = num_carte
                response = None
                nom = self.ids.nom.text
                prenom = self.ids.prenom.text
                sexe = self.ids.sexe.text
                date_naiss = self.ids.date_naiss.text
                lieu_naiss = self.ids.lieu_naiss.text
                adresse = self.ids.addresse.text
                num_cin = self.ids.num_cin.text
                date_cin = self.ids.date_cin.text
                lieu_cin = self.ids.lieu_cin.text
                quintance = self.ids.num_quintance.text
                date_quintance = self.ids.date_quintance.text
                montant = self.ids.montant.text
                etat = self.ids.etat.text
                nation = self.ids.nation.text
                moyenne = self.ids.moyenne.text
                bacc_anne = self.ids.bacc_annee.text

                host = MDApp.get_running_app().HOST
                token = MDApp.get_running_app().TOKEN
                uuid_mention = self.selected_mention
                uuid_parcours = self.selected_parcours
                semestre_petit = MDApp.get_running_app().get_semestre_petit(self.selected_semestre)
                semestre_grand = MDApp.get_running_app().get_semestre_grand(self.selected_semestre)
                list_key = ["num_carte", "nom", "prenom", "sexe", "date_naiss", "lieu_naiss",
                            "nation", "adresse", "num_cin", "date_cin", "lieu_cin", "num_quitance",
                            "date_quitance", "montant", "photo", "etat", "moyenne", "uuid_mention",
                            "uuid_parcours", "bacc_anne", "semestre_petit", "semestre_grand"]
                list_value = [num_carte, nom, prenom, sexe, date_naiss, lieu_naiss, nation, adresse,
                              num_cin, date_cin, lieu_cin, quintance, date_quintance, montant, photo,
                              etat, moyenne, uuid_mention, uuid_parcours, bacc_anne, semestre_petit,
                              semestre_grand]

                key_params = ["schema"]
                value_params = [schemas]
                if MDApp.get_running_app().REINSCRIPTION_ACTION_TYPE == "ADD":
                    test_num = MDApp.get_running_app().read_by_key(
                        MDApp.get_running_app().ALL_ETUDIANT, "num_carte", num_carte)
                    if len(test_num) == 0:
                        url_enreg: str = f'http://{host}/api/v1/ancien_etudiants/'
                        etudiant = create_json(list_key, list_value)
                        payload = json.dumps(etudiant)
                        if self.path != "":
                            photo = self.post_photo(num_carte, self.path)["filename"]
                            if 'detail' not in photo:
                                response = create_with_params(url_enreg, key_params, value_params, token, payload)
                            else:
                                toast(photo)
                        else:
                            response = create_with_params(url_enreg, key_params, value_params, token, payload)

                    else:
                        toast("Numéro carte déjà inscrit")

                else:
                    url_enreg: str = f'http://{host}/api/v1/ancien_etudiants/update_etudiant/'
                    etudiant = create_json_update(list_key, list_value)
                    payload = json.dumps(etudiant)

                    key_params = ["schema", "num_carte"]
                    value_params = [schemas, num_carte]
                    if self.path != "":
                        photo = self.post_photo(num_carte, self.path)["filename"]
                        if 'detail' not in photo:
                            response = update_with_params(url_enreg, key_params, value_params, token, payload)
                        else:
                            toast(photo)
                    else:
                        response = update_with_params(url_enreg, key_params, value_params, token, payload)
                if response:
                    if response[1] == 200:
                        self.reset_champs()
                        MDApp.get_running_app().ALL_ETUDIANT = response[0]
                        self.path = ""
                    elif response[1] == 400:
                        toast(str(response[0]))
                    else:
                        toast(str(response))
            else:
                toast("Sélectioner d'abord le(s) semestre(s)")
        else:
            toast("Sélectioner d'abord l'année universitaires")
        self.spinner_toggle()

    def post_photos(self, num_carte: str):
        photo = {}
        try:
            photo = self.post_photo(num_carte, self.path)["filename"]
        except Exception as e:
            toast(photo)
        return photo

    def get_all_mention(self):
        mention = MDApp.get_running_app().ALL_MENTION
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{mention[i]['title']}",
                "height": dp(50),
                "on_release": lambda x=f"{mention[i]['title']}": self.menu_calback_mention(x),
            } for i in range(len(mention))
        ]
        return menu_items

    def menu_calback_mention(self, text_item):
        self.selected_mention = \
            MDApp.get_running_app().read_by_key(MDApp.get_running_app().ALL_MENTION, "title", text_item)[0]['uuid']
        if MDApp.get_running_app().MENTION != self.selected_mention:
            MDApp.get_running_app().MENTION = self.selected_mention
            MDApp.get_running_app().get_list_parcours()
            self.menu_parcours = MDDropdownMenu(
                caller=self.ids.mention_field,
                items=self.get_all_parcours(),
                width_mult=4,
            )
        self.ids.mention_field.text = text_item
        self.menu_mention.dismiss()

    def get_all_parcours(self):
        parcours = MDApp.get_running_app().ALL_PARCOURS
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{parcours[i]['abreviation'].upper()}",
                "height": dp(50),
                "on_release": lambda x=f"{parcours[i]['abreviation'].upper()}": self.menu_calback_parcours(x),
            } for i in range(len(parcours))
        ]
        return menu_items

    def menu_calback_parcours(self, text_item):
        self.selected_parcours = MDApp.get_running_app().read_by_key(
            MDApp.get_running_app().ALL_PARCOURS, "abreviation", text_item)[0]['uuid']
        self.ids.parcours_field.text = text_item
        self.menu_parcours.dismiss()

    # def read_parcours_by_title(self, data: list, titre: str):
    #     return list(filter(lambda parcours: parcours["abreviation"].lower() == titre.lower(), data))

    # def read_mention_by_title(self, data: list, titre: str):
    #     return list(filter(lambda mention: mention["title"].lower() == titre.lower(), data))

    def auto_complete(self):
        self.ids.num_ce.text = MDApp.get_running_app().create_secret(5)
        self.ids.nom.text = MDApp.get_running_app().create_secret(20)
        self.ids.prenom.text = MDApp.get_running_app().create_secret(5)
        self.ids.sexe.text = "MASCULIN"
        self.ids.date_naiss.text = "1993-12-10"
        self.ids.lieu_naiss.text = MDApp.get_running_app().create_secret(12)
        self.ids.addresse.text = MDApp.get_running_app().create_secret(8)
        self.ids.num_cin.text = MDApp.get_running_app().create_secret(12)
        self.ids.date_cin.text = "2012-02-13"
        self.ids.lieu_cin.text = MDApp.get_running_app().create_secret(4)
        self.ids.num_quintance.text = MDApp.get_running_app().create_secret(13)
        self.ids.date_quintance.text = "2020-13-04"
        self.ids.montant.text = "205000"
        self.ids.etat.text = "Passant"
        self.ids.nation.text = "Malagasy"
        self.ids.moyenne.text = "12"
        self.ids.bacc_annee.text = "2013"

    def reset_champs(self):
        self.ids.num_ce.text = ""
        self.ids.nom.text = ""
        self.ids.prenom.text = ""
        self.ids.sexe.text = ""
        self.ids.date_naiss.text = ""
        self.ids.lieu_naiss.text = ""
        self.ids.addresse.text = ""
        self.ids.num_cin.text = ""
        self.ids.date_cin.text = ""
        self.ids.lieu_cin.text = ""
        self.ids.num_quintance.text = ""
        self.ids.date_quintance.text = ""
        self.ids.montant.text = ""
        self.ids.etat.text = ""
        self.ids.nation.text = ""
        self.ids.moyenne.text = ""
        self.ids.bacc_annee.text = ""
        for check in self.check_box:
            check.active = False

    def read_mention_by_uuid(self, data: list, uuid: str):
        return list(filter(lambda mention: mention["uuid"] == uuid, data))

    def post_photo(self, num_carte: str, path: str):
        host = MDApp.get_running_app().HOST
        token = MDApp.get_running_app().TOKEN
        url = f"http://{host}/api/v1/ancien_etudiants/upload_photo/"
        response = post_photo(url, num_carte, token, path)
        return response

    def disabled_check_licence_master_two(self):
        if self.ids.s7_check.active or self.ids.s8_check.active:
            for check_licence in self.license:
                check_licence.disabled = True
            for check_master in self.master_two:
                check_master.disabled = True
        else:
            for check_licence in self.license:
                check_licence.disabled = False
            for check_master_two in self.master_two:
                check_master_two.disabled = False

    def disabled_check_licence_master_one(self):
        if self.ids.s9_check.active or self.ids.s10_check.active:
            for check_licence in self.license:
                check_licence.disabled = True
            for check_master_one in self.master_one:
                check_master_one.disabled = True
        else:
            for check_licence in self.license:
                check_licence.disabled = False
            for check_master_one in self.master_one:
                check_master_one.disabled = False

    def disabled_check_master_one_two(self):
        if (self.ids.s1_check.active or self.ids.s2_check.active or self.ids.s3_check.active or
                self.ids.s4_check.active or self.ids.s5_check.active or self.ids.s6_check.active):

            for check_master_one in self.master_one:
                check_master_one.disabled = True
            for check_master_two in self.master_two:
                check_master_two.disabled = True
        else:
            for check_master_one in self.master_one:
                check_master_one.disabled = False
            for check_master_two in self.master_two:
                check_master_two.disabled = False
        self.enable_two_check()

    def enable_two_check(self):
        nbr_check: int = 1
        for check_one in self.license:
            if check_one.active:
                nbr_check += 1
            else:
                nbr_check -= 1
        if nbr_check == -1:
            for check_one in self.license:
                if check_one.active:
                    check_one.disabled = False
                else:
                    check_one.disabled = True
        else:
            for check_one in self.license:
                check_one.disabled = False

    def get_semestre(self) -> list:
        self.selected_semestre = []
        for index, check in enumerate(self.check_box):
            if check.active:
                self.selected_semestre.append(self.list_semestre[index])
        return self.selected_semestre

    def set_semestre(self, semestre: list):
        self.check_box = self.license + self.master_one + self.master_two
        if len(semestre) != 0:
            for sems in semestre:
                if len(sems) != 0:
                    indice: int = int(sems[1:len(sems)])
                    print(indice)
                    self.check_box[indice - 1].active = True
