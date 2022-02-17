from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivymd.material_resources import dp
from kivymd.toast import toast
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.picker import MDDatePicker
from all_requests.request_etudiants import save_etudiant


class ReinscriptionAddScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu_mention = None
        self.menu_parcours = None
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=True,
        )

        self.selected_mention = ""
        self.selected_parcours = ""

    screenManager = ObjectProperty(None)

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

    def back_home(self):
        MDApp.get_running_app().root.current = 'Reinscription'

    def file_manager_open(self):
        self.file_manager.show('/')  # output manager to the screen
        self.manager_open = True

    def select_path(self, path):
        """It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        """

        print(path)
        try:
            self.ids.ellipse.source = f"{path}"
        except Exception as e:
            print(e)
            pass
        self.exit_manager()
        toast(path)

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

    def show_date_picker_cin(self):
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

    def enreg_etudiant(self):
        num_carte = self.ids.num_ce.text
        nom = self.ids.nom.text
        prenom = self.ids.prenom.text
        sexe = self.ids.sexe.text = \
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
        annee = MDApp.get_running_app().ANNEE
        uuid_mention = self.selected_mention
        uuid_parcours = self.selected_parcoursselected_parcours
        semestre_petit = ""
        semestre_grand = ""
        url_enreg: str = f'http://{host}/api/v1/ancien_etudiants/'
        response = save_etudiant(url_enreg, annee, token, 'POST', num_carte, nom, prenom, sexe, date_naiss, lieu_naiss,
                                 nation, adresse, num_cin, date_cin, lieu_cin, quintance, date_quintance, montant,
                                 etat, moyenne, uuid_mention, uuid_parcours, bacc_anne, semestre_petit, semestre_grand)
        if response:
            print(response)

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

    def read_mention_by_title(self, data: list, titre: str):
        return list(filter(lambda mention: mention["title"].lower() == titre.lower(), data))
