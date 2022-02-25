from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivymd.material_resources import dp
from kivymd.toast import toast
from kivymd.uix.menu import MDDropdownMenu
from all_requests.request_etudiants import update_etudiant


class ReinscriptionUpdateScreen(Screen):
    # http://localhost/api/v1/ancien_etudiants/photo?name_file=4465.jpg
    screenManager = ObjectProperty(None)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.host = None
        self.selected_mention = None
        self.photo = None
        self.selected_parcours = None
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
        self.list_semestre = ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10"]
        self.selected_semestre = []

    def on_enter(self):

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
                self.ids.ellipse.source = f'http://{self.host}/api/v1/ancien_etudiants/photo?name_file={str(un_etudiant["photo"])}'
            except Exception as e:
                print(e)
                pass

    def back_home(self):
        self.reset_champs()
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
        self.selected_parcours = \
            MDApp.get_running_app().read_by_key(MDApp.get_running_app().ALL_PARCOURS, "abreviation", text_item)[0][
                'uuid']
        self.ids.parcours_field.text = text_item
        self.menu_parcours.dismiss()

    # def read_parcours_by_title(self, data: list, titre: str):
    #     return list(filter(lambda parcours: parcours["abreviation"].lower() == titre.lower(), data))

    # def read_parcours_by_uuid(self, data: list, uuid: str):
    #     return list(filter(lambda parcours: parcours["uuid"] == uuid, data))

    # def read_mention_by_title(self, data: list, titre: str):
    #     return list(filter(lambda mention: mention["title"].lower() == titre.lower(), data))

    # def read_mention_by_uuid(self, data: list, uuid: str):
    #     return list(filter(lambda mention: mention["uuid"] == uuid, data))

    def enreg_etudiant(self):
        self.selected_semestre = self.get_semestre()
        annee = MDApp.get_running_app().ANNEE
        if len(annee) != 0:
            if len(self.selected_semestre) != 0:
                num_carte = self.ids.num_ce.text
                photo = self.photo
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
                url_enreg: str = f'http://{host}/api/v1/ancien_etudiants/update_etudiant/'
                response = update_etudiant(url_enreg, annee, token, num_carte, nom, prenom, sexe, date_naiss,
                                           lieu_naiss,
                                           nation, adresse, num_cin, date_cin, lieu_cin, quintance, date_quintance,
                                           montant,
                                           photo, etat, moyenne, uuid_mention, uuid_parcours, bacc_anne, semestre_petit,
                                           semestre_grand)
                if response:
                    self.reset_champs()
                    MDApp.get_running_app().ALL_ETUDIANT = response
                    MDApp.get_running_app().root.current = 'Reinscription'
            else:
                toast("Sélectioner d'abord le(s) semestre(s)")
        else:
            toast("Sélectioner d'abord l'année universitaires")

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
        self.check_box = self.license + self.master_one + self.master_two
        for check in self.check_box:
            check.active = False

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
        self.check_box = self.license + self.master_one + self.master_two
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
