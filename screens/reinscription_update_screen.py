from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivymd.material_resources import dp
from kivymd.uix.menu import MDDropdownMenu


class ReinscriptionUpdateScreen(Screen):
    # http://localhost/api/v1/ancien_etudiants/photo?name_file=4465.jpg
    screenManager = ObjectProperty(None)

    def __init__(self, **kw):
        super().__init__(kw)
        self.selected_parcours = None

    def on_enter(self):
        self.ids.s1_check.active = True
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
        num_carte = MDApp.get_running_app().NUM_CARTE
        self.host = MDApp.get_running_app().HOST
        if num_carte != "":
            un_etudiant = self.read_by_num_carte(MDApp.get_running_app().ALL_ETUDIANT, num_carte)[0]
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
            self.ids.mention_field.text = self.read_mention_by_uuid(MDApp.get_running_app().ALL_MENTION,
                                                                    MDApp.get_running_app().MENTION)[0]["title"]
            try:
                self.ids.ellipse.source = f'http://{self.host}/api/v1/ancien_etudiants/photo?name_file={str(un_etudiant["photo"])}'
            except Exception as e:
                print(e)
                pass

    def back_home(self):
        MDApp.get_running_app().root.current = 'Reinscription'

    def read_by_num_carte(self, data: list, num_carte: str):
        return list(filter(lambda etudiant: etudiant["num_carte"] == num_carte, data))

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
        self.selected_mention = self.read_mention_by_title(MDApp.get_running_app().ALL_MENTION, text_item)[0]['uuid']
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
        self.selected_parcours = self.read_parcours_by_title(MDApp.get_running_app().ALL_PARCOURS, text_item)[0]['uuid']
        self.ids.parcours_field.text = text_item
        self.menu_parcours.dismiss()

    def read_parcours_by_title(self, data: list, titre: str):
        return list(filter(lambda parcours: parcours["abreviation"].lower() == titre.lower(), data))

    def read_parcours_by_uuid(self, data: list, uuid: str):
        return list(filter(lambda parcours: parcours["uuid"] == uuid, data))

    def read_mention_by_title(self, data: list, titre: str):
        return list(filter(lambda mention: mention["title"].lower() == titre.lower(), data))

    def read_mention_by_uuid(self, data: list, uuid: str):
        return list(filter(lambda mention: mention["uuid"] == uuid, data))
