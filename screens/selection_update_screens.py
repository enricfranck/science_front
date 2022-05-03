import threading

from kivy.clock import mainthread
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivymd.toast import toast
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.picker import MDDatePicker

from all_requests import request_etudiants


class SelectionUpdateScreen(Screen):
    screenManager = ObjectProperty(None)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.button = None
        self.menu_serie = None
        self.menu_parcours = None
        self.menu_sexe = None
        self.menu_nation = None
        self.selected_parcours = None
        self.host = None
        self.selected_mention = None
        self.menu_niveau = None
        self.menu_mention = None

    def on_enter(self, *args):
        self.menu_mention = MDDropdownMenu(
            caller=self.ids.mention_field,
            items=self.get_all_mention(),
            width_mult=4,
        )
        menu_niveau = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{i}",
                "height": dp(50),
                "on_release": lambda x=f"{i}": self.menu_calback_niveau(x),
            } for i in MDApp.get_running_app().ALL_NIVEAU_SELECT
        ]

        self.menu_niveau = MDDropdownMenu(
            caller=self.ids.niveau_field,
            items=menu_niveau,
            width_mult=4,
        )

        self.menu_parcours = MDDropdownMenu(
            caller=self.ids.parcours_field,
            items=self.get_all_parcours(),
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

        menu_serie = ["Serie A1", "Serie A2", "Serie C", "Serie D", "Technique Génie civile",
                      "Technique Industrielle", "Technique Tertiaire",
                      "Technique Agricole", "Technologique", "Autre"]

        menu_serie_list = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{i}",
                "height": dp(50),
                "on_release": lambda x=f"{i}": self.menu_calback_serie(x),
            } for i in menu_serie
        ]
        self.menu_serie = MDDropdownMenu(
            caller=self.ids.serie_bacc,
            items=menu_serie_list,
            width_mult=4,
        )

        num_select = MDApp.get_running_app().NUM_SELECT
        self.host = MDApp.get_running_app().HOST
        if num_select != "":
            un_etudiant = MDApp.get_running_app().read_by_key(
                MDApp.get_running_app().ALL_ETUDIANT_SELECTIONNER, "num_select", num_select)[0]
            self.ids.num_select.text = str(un_etudiant["num_select"])
            self.ids.nom.text = MDApp.get_running_app().test_string(str(un_etudiant["nom"]))
            self.ids.prenom.text = MDApp.get_running_app().test_string(str(un_etudiant["prenom"]))
            self.ids.sexe.text = MDApp.get_running_app().test_string(str(un_etudiant["sexe"]))
            self.ids.date_naiss.text = MDApp.get_running_app().test_string(str(un_etudiant["date_naiss"]))
            self.ids.lieu_naiss.text = MDApp.get_running_app().test_string(str(un_etudiant["lieu_naiss"]))
            self.ids.addresse.text = MDApp.get_running_app().test_string(str(un_etudiant["adresse"]))
            self.ids.num_cin.text = MDApp.get_running_app().test_string(str(un_etudiant["num_cin"]))
            self.ids.date_cin.text = MDApp.get_running_app().test_string(str(un_etudiant["date_cin"]))
            self.ids.lieu_cin.text = MDApp.get_running_app().test_string(str(un_etudiant["lieu_cin"]))
            self.ids.num_quintance.text = MDApp.get_running_app().test_string(str(un_etudiant["num_quitance"]))
            self.ids.date_quintance.text = MDApp.get_running_app().test_string(str(un_etudiant["date_quitance"]))
            self.ids.montant.text = MDApp.get_running_app().test_string(str(un_etudiant["montant"]))
            self.ids.nation.text = MDApp.get_running_app().test_string(str(un_etudiant["nation"]))
            self.ids.prof_et.text = MDApp.get_running_app().test_string(str(un_etudiant["proffession"]))
            self.ids.annee_bacc.text = MDApp.get_running_app().test_string(str(un_etudiant["bacc_anne"]))
            self.ids.niveau_field.text = MDApp.get_running_app().test_string(str(un_etudiant["niveau"]))
            self.ids.serie_bacc.text = MDApp.get_running_app().test_string(str(un_etudiant["bacc_serie"]))
            self.ids.centre_bacc.text = MDApp.get_running_app().test_string(str(un_etudiant["bacc_centre"]))
            self.ids.num_bacc.text = MDApp.get_running_app().test_string(str(un_etudiant["bacc_num"]))
            self.ids.situation.text = MDApp.get_running_app().test_string(str(un_etudiant["situation"]))
            self.ids.phone.text = MDApp.get_running_app().test_string(str(un_etudiant["telephone"]))
            self.ids.nom_pere.text = MDApp.get_running_app().test_string(str(un_etudiant["nom_pere"]))
            self.ids.prof_pere.text = MDApp.get_running_app().test_string(str(un_etudiant["proffession_pere"]))
            self.ids.nom_mere.text = MDApp.get_running_app().test_string(str(un_etudiant["nom_mere"]))
            self.ids.prof_mere.text = MDApp.get_running_app().test_string(str(un_etudiant["proffession_mere"]))
            self.ids.addresse_parent.text = MDApp.get_running_app().test_string(str(un_etudiant["adresse_parent"]))
            self.ids.select.active = bool(un_etudiant['select'])
            self.ids.mention_field.text = \
                MDApp.get_running_app().read_by_key(MDApp.get_running_app().ALL_MENTION, "uuid",
                                                    MDApp.get_running_app().MENTION)[0]["title"]
            self.selected_mention = MDApp.get_running_app().MENTION
            if str(un_etudiant["uuid_parcours"]) != "None" and str(un_etudiant["uuid_parcours"]) != "":
                self.ids.parcours_field.text = MDApp.get_running_app().read_by_key(
                    MDApp.get_running_app().ALL_PARCOURS, "uuid",
                    str(un_etudiant["uuid_parcours"]))[0]["abreviation"].upper()

            if not self.ids.select.active:
                self.ids.validation.active = False

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

    @mainthread
    def spinner_toggle(self):
        if not self.ids.spinner.active:
            self.ids.spinner.active = True
        else:
            self.ids.spinner.active = False

    def process_update_toggle(self):
        self.spinner_toggle()
        threading.Thread(target=(
            self.enreg_etudiant)).start()

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

    # def read_mention_by_title(self, data: list, titre: str):
    #     return list(filter(lambda mention: mention["title"].lower() == titre.lower(), data))

    def back_home(self):
        # self.reset_champs()
        MDApp.get_running_app().root.current = 'Selection'

    def menu_calback_niveau(self, text_item):
        self.ids.niveau_field.text = text_item
        self.menu_niveau.dismiss()

    def menu_calback_sexe(self, text_item):
        self.ids.sexe.text = text_item
        self.menu_sexe.dismiss()

    def menu_calback_serie(self, text_item):
        self.ids.serie_bacc.text = text_item
        self.menu_serie.dismiss()

    def menu_calback_nation(self, text_item):
        self.ids.nation.text = text_item
        self.menu_nation.dismiss()

    # def read_by_niveau(self, data: list, niveau: str):
    #     return list(filter(lambda etudiant: etudiant["niveau"].lower() == niveau.lower(), data))

    def transforme_data(self, all_data: list):
        data = []
        k: int = 1
        for un_et in all_data:
            etudiant = (k, ("human-female",
                            [39 / 256, 174 / 256, 96 / 256, 1], un_et["num_select"]),
                        f'{un_et["nom"]} {un_et["prenom"]}', un_et["select"])

            data.append(etudiant)
            k += 1
        data.append(("", "", "", ""))
        return data

    def auto_complete(self):
        self.ids.num_select.text = MDApp.get_running_app().create_secret(5)
        self.ids.nom.text = MDApp.get_running_app().create_secret(20)
        self.ids.prenom.text = MDApp.get_running_app().create_secret(5)
        self.ids.date_naiss.text = "1993-12-10"
        self.ids.lieu_naiss.text = MDApp.get_running_app().create_secret(12)
        self.ids.addresse.text = MDApp.get_running_app().create_secret(8)
        self.ids.num_cin.text = MDApp.get_running_app().create_secret(12)
        self.ids.date_cin.text = "2012-02-13"
        self.ids.lieu_cin.text = MDApp.get_running_app().create_secret(4)

    def get_all_parcours(self):
        parcours = MDApp.get_running_app().ALL_PARCOURS
        print("kjkgy", parcours)
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

    def enreg_etudiant(self):
        annee = MDApp.get_running_app().ANNEE
        if len(annee) != 0:
            host = MDApp.get_running_app().HOST
            token = MDApp.get_running_app().TOKEN

            num_select = self.ids.num_select.text
            nom = self.ids.nom.text
            prenom = self.ids.prenom.text
            sexe = self.ids.sexe.text
            date_naiss = self.ids.date_naiss.text
            lieu_naiss = self.ids.lieu_naiss.text
            adresse = self.ids.addresse.text
            num_cin = self.ids.num_cin.text
            date_cin = self.ids.date_cin.text
            lieu_cin = self.ids.lieu_cin.text
            nation = self.ids.nation.text
            montant = self.ids.montant.text
            num_quintance = self.ids.num_quintance.text
            date_quitance = self.ids.date_quintance.text
            profession = self.ids.prof_et.text
            anne_bacc = self.ids.annee_bacc.text
            serie_bacc = self.ids.serie_bacc.text
            centre_bacc = self.ids.centre_bacc.text
            num_bacc = self.ids.num_bacc.text
            situation = self.ids.situation.text
            phone = self.ids.phone.text
            nom_pere = self.ids.nom_pere.text
            prof_pere = self.ids.prof_pere.text
            nom_mere = self.ids.nom_mere.text
            prof_mere = self.ids.prof_mere.text
            adresse_parent = self.ids.addresse_parent.text

            branche = MDApp.get_running_app().read_by_key(MDApp.get_running_app().ALL_MENTION, "uuid",
                                                          self.selected_mention)[0]["branche"]
            niveau = self.ids.niveau_field.text
            uuid_mention = MDApp.get_running_app().MENTION
            if not self.ids.validation.active:
                url = f"http://{host}/api/v1/nouveau_etudiants/update_etudiant_by_num_select/"
                response = request_etudiants.update_select_etudiant(
                    url=url, annee=annee, token=token, num_select=num_select, nom=nom, prenom=prenom, sexe=sexe,
                    date_naiss=date_naiss, lieu_naiss=lieu_naiss, branche=branche, nation=nation, adresse=adresse,
                    num_cin=num_cin, date_cin=date_cin, lieu_cin=lieu_cin, uuid_mention=uuid_mention, niveau=niveau,
                    select=self.ids.select.active)
            else:
                uuid_parcours = MDApp.get_running_app().read_by_key(
                    MDApp.get_running_app().ALL_PARCOURS, "abreviation", self.ids.parcours_field.text)[0]["uuid"]
                url = f"http://{host}/api/v1/nouveau_etudiants/update_etudiant_by_num_select_admis/"
                response = request_etudiants.update_selected_etudiant(
                    url=url, annee=annee, token=token, num_select=num_select, nom=nom, prenom=prenom,
                    date_naiss=date_naiss, lieu_naiss=lieu_naiss, adresse=adresse, sexe=sexe, nation=nation,
                    num_cin=num_cin, date_cin=date_cin, lieu_cin=lieu_cin, montant=montant, etat="Passant",
                    num_quitance=num_quintance, date_quitance=date_quitance, situation=situation, telephone=phone,
                    bacc_num=num_bacc, bacc_centre=centre_bacc, bacc_anne=anne_bacc, bacc_serie=serie_bacc,
                    proffession=profession, nom_pere=nom_pere, proffession_pere=prof_pere, nom_mere=nom_mere,
                    proffession_mere=prof_mere, adresse_parent=adresse_parent, branche=branche,
                    uuid_mention=uuid_mention, uuid_parcours=uuid_parcours, niveau=niveau,
                    select=self.ids.select.active)

            if response:
                if response[1] == 200:
                    MDApp.get_running_app().ALL_ETUDIANT_SELECTIONNER = response[0]
                elif response[1] == 400:
                    toast(str(response[0]))
                else:
                    toast(str(response))
        else:
            toast("Choisir l'annee universitaire")
        self.spinner_toggle()

    def reset_champs(self):

        self.ids.num_select.text = MDApp.get_running_app().test_string()
        self.ids.nom.text = MDApp.get_running_app().test_string()
        self.ids.prenom.text = MDApp.get_running_app().test_string()
        self.ids.sexe.text = MDApp.get_running_app().test_string()
        self.ids.date_naiss.text = MDApp.get_running_app().test_string()
        self.ids.lieu_naiss.text = MDApp.get_running_app().test_string()
        self.ids.addresse.text = MDApp.get_running_app().test_string()
        self.ids.num_cin.text = MDApp.get_running_app().test_string()
        self.ids.date_cin.text = MDApp.get_running_app().test_string()
        self.ids.lieu_cin.text = MDApp.get_running_app().test_string()
        self.ids.nation.text = MDApp.get_running_app().test_string()

        self.ids.num_quintance.text = MDApp.get_running_app().test_string()
        self.ids.date_quintance.text = MDApp.get_running_app().test_string()
        self.ids.montant.text = MDApp.get_running_app().test_string()
        self.ids.prof_et.text = MDApp.get_running_app().test_string()
        self.ids.annee_bacc.text = MDApp.get_running_app().test_string()
        self.ids.niveau_field.text = MDApp.get_running_app().test_string()
        self.ids.mention_field.text = MDApp.get_running_app().test_string()
        self.ids.serie_bacc.text = MDApp.get_running_app().test_string()
        self.ids.centre_bacc.text = MDApp.get_running_app().test_string()
        self.ids.num_bacc.text = MDApp.get_running_app().test_string()
        self.ids.situation.text = MDApp.get_running_app().test_string()
        self.ids.phone.text = MDApp.get_running_app().test_string()
        self.ids.nom_pere.text = MDApp.get_running_app().test_string()
        self.ids.prof_pere.text = MDApp.get_running_app().test_string()
        self.ids.nom_mere.text = MDApp.get_running_app().test_string()
        self.ids.prof_mere.text = MDApp.get_running_app().test_string()
        self.ids.addresse_parent.text = MDApp.get_running_app().test_string()

    def on_cancel(self, instance, value):
        """Events called when the "CANCEL" dialog box button is clicked."""

    def on_save_date(self, instance, value, date_range):
        """
        """
        if self.button == "quintance":
            self.ids.date_quintance.text = str(value)
        elif self.button == "naiss":
            self.ids.date_naiss.text = str(value)
        elif self.button == "cin":
            self.ids.date_cin.text = str(value)

    def show_date_picker(self, button):
        self.button = button
        date_dialog = MDDatePicker(min_year=1980,
                                   max_year=2030,
                                   primary_color=get_color_from_hex("#72225b"),
                                   accent_color=get_color_from_hex("#5d1a4a"),
                                   selector_color=get_color_from_hex("#e93f39"),
                                   text_toolbar_color=get_color_from_hex("#cccccc"),
                                   text_color="#ffffff",
                                   text_current_color=get_color_from_hex("#e93f39"),
                                   input_field_background_color=(1, 1, 1, 0.2), )
        date_dialog.bind(on_save=self.on_save_date, on_cancel=self.on_cancel)
        date_dialog.open()
