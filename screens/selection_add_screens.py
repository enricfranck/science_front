from kivy.metrics import dp
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivymd.toast import toast
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.picker import MDDatePicker

from all_requests import request_etudiants


class SelectionAddScreen(Screen):
    screenManager = ObjectProperty(None)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.menu_sexe = None
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
            MDApp.get_running_app().get_list_parcours()
        self.ids.mention_field.text = text_item
        self.menu_mention.dismiss()

    # def read_mention_by_title(self, data: list, titre: str):
    #     return list(filter(lambda mention: mention["title"].lower() == titre.lower(), data))

    def back_home(self):
        # self.reset_champs()
        MDApp.get_running_app().root.current = 'Selection'

    def menu_calback_niveau(self, text_item):
        self.ids.niveau_field.text = text_item
        self.menue_niveau.dismiss()

    def menu_calback_sexe(self, text_item):
        self.ids.sexe.text = text_item
        self.menu_sexe.dismiss()

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
        self.ids.sexe.text = "MASCULIN"
        self.ids.date_naiss.text = "1993-12-10"
        self.ids.lieu_naiss.text = MDApp.get_running_app().create_secret(12)
        self.ids.addresse.text = MDApp.get_running_app().create_secret(8)
        self.ids.num_cin.text = MDApp.get_running_app().create_secret(12)
        self.ids.date_cin.text = "2012-02-13"
        self.ids.lieu_cin.text = MDApp.get_running_app().create_secret(4)
        self.ids.nation.text = "Malagasy"

    def enreg_etudiant(self):
        num_select = self.ids.num_select.text
        abreviation = MDApp.get_running_app().read_by_key(MDApp.get_running_app().ALL_MENTION, "uuid",
                                                          self.selected_mention)[0]["abreviation"]
        annee = MDApp.get_running_app().ANNEE
        test_num = MDApp.get_running_app().read_by_key(
            MDApp.get_running_app().ALL_ETUDIANT_SELECTIONNER, "num_select", f"S{abreviation.upper()}{num_select}")
        if len(test_num) == 0:
            if len(annee) != 0:
                host = MDApp.get_running_app().HOST
                token = MDApp.get_running_app().TOKEN
                url = f"http://{host}/api/v1/nouveau_etudiants/"
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
                niveau = self.ids.niveau_field.text
                uuid_mention = MDApp.get_running_app().MENTION
                branche = MDApp.get_running_app().read_by_key(MDApp.get_running_app().ALL_MENTION, "uuid",
                                                              self.selected_mention)[0]["branche"]

                response = request_etudiants.save_etudiant_select(url=url, annee=annee, token=token,
                                                                  num_select=num_select,
                                                                  nom=nom, prenom=prenom, sexe=sexe,
                                                                  date_naiss=date_naiss,
                                                                  lieu_naiss=lieu_naiss, branche=branche, nation=nation,
                                                                  adresse=adresse, num_cin=num_cin, date_cin=date_cin,
                                                                  lieu_cin=lieu_cin, uuid_mention=uuid_mention,
                                                                  niveau=niveau
                                                                  )
                if response:
                    MDApp.get_running_app().ALL_ETUDIANT_SELECTIONNER = response
            else:
                toast("Choisir l'annee universitaire")
        else:
            toast("Numéro de dossier déjà inscrit")

    def on_cancel(self, instance, value):
        """Events called when the "CANCEL" dialog box button is clicked."""

    def on_save_cin(self, instance, value, date_range):
        """
        """
        self.ids.date_cin.text = str(value)

    def show_date_picker_cin(self, ):
        date_dialog = MDDatePicker(min_year=1980, max_year=2030)
        date_dialog.bind(on_save=self.on_save_cin, on_cancel=self.on_cancel)
        date_dialog.open()

    def on_save_naiss(self, instance, value, date_range):
        """
        """
        self.ids.date_naiss.text = str(value)

    def show_date_picker_naiss(self):
        date_dialog = MDDatePicker(min_year=1980, max_year=2030)
        date_dialog.bind(on_save=self.on_save_naiss, on_cancel=self.on_cancel)
        date_dialog.open()

    def on_save_quint(self, instance, value, date_range):
        """
        """
        self.ids.date_quintance.text = str(value)

    def show_date_picker_quint(self):
        date_dialog = MDDatePicker(min_year=1980, max_year=2030)
        date_dialog.bind(on_save=self.on_save_quint, on_cancel=self.on_cancel)
        date_dialog.open()
