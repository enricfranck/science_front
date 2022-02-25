from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty


class PublicAddScreen(Screen):
    screenManager = ObjectProperty(None)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.titre = None
        self.email = None
        self.password = None
        self.nom = None
        self.prenom = None
        self.role = None
        self.mention = None

    def login(self):
        email = self.ids.email.text
        password = self.ids.password.text
        print(email, password)

    def back_home(self):
        MDApp.get_running_app().root.current = 'Public'

    def on_enter(self, *args):
        self.titre = MDApp.get_running_app().PUBLIC_TITRE
        self.ids.email.hint_text = self.titre
        self.email = self.ids.email
        self.password = self.ids.password
        self.nom = self.ids.nom
        self.prenom = self.ids.prenom
        self.mention = self.ids.mention
        self.role = self.ids.role

        if self.titre == "Email":
            self.role.opacity = 1
            self.role.disabled = False
            self.password.opacity = 1
            self.password.disabled = False
            self.nom.opacity = 1
            self.nom.disabled = False
            self.prenom.opacity = 1
            self.prenom.disabled = False
            self.mention.opacity = 1
            self.mention.disabled = False

            self.nom.hint_text = "Nom"
            self.password.hint_text = "Password"
            self.prenom.hint_text = "Prénom"

            self.ids.save_users.opacity = 1
            self.ids.save_mention.opacity = 0
            self.ids.save_parcours.opacity = 0
            self.ids.save_role.opacity = 0
            self.ids.save_annee.opacity = 0
            self.ids.save_droit.opacity = 0

        elif self.titre == "Titre mention":
            self.role.opacity = 0
            self.role.disabled = True
            self.password.opacity = 1
            self.password.disabled = False
            self.nom.opacity = 1
            self.nom.disabled = False
            self.prenom.opacity = 1
            self.prenom.disabled = False
            self.mention.opacity = 0
            self.mention.disabled = True

            self.nom.hint_text = "Dérniere CE"
            self.password.hint_text = "Abréviation"
            self.prenom.hint_text = "Branche"

            self.ids.save_users.opacity = 0
            self.ids.save_mention.opacity = 1
            self.ids.save_parcours.opacity = 0
            self.ids.save_role.opacity = 0
            self.ids.save_annee.opacity = 0
            self.ids.save_droit.opacity = 0

        elif self.titre == "Titre parcours":
            self.role.opacity = 0
            self.role.disabled = True
            self.password.opacity = 1
            self.password.disabled = False
            self.nom.opacity = 1
            self.nom.disabled = False
            self.prenom.opacity = 0
            self.prenom.disabled = True
            self.mention.opacity = 1
            self.mention.disabled = False

            self.nom.hint_text = "Semestre"
            self.password.hint_text = "Abréviation"

            self.ids.save_users.opacity = 0
            self.ids.save_mention.opacity = 0
            self.ids.save_parcours.opacity = 1
            self.ids.save_role.opacity = 0
            self.ids.save_annee.opacity = 0
            self.ids.save_droit.opacity = 0

        elif self.titre == "Titre role":
            self.role.opacity = 0
            self.role.disabled = True
            self.password.opacity = 0
            self.password.disabled = True
            self.nom.opacity = 0
            self.nom.disabled = True
            self.prenom.opacity = 0
            self.prenom.disabled = True
            self.mention.opacity = 0
            self.mention.disabled = True

            self.ids.save_users.opacity = 0
            self.ids.save_mention.opacity = 0
            self.ids.save_parcours.opacity = 0
            self.ids.save_role.opacity = 1
            self.ids.save_annee.opacity = 0
            self.ids.save_droit.opacity = 0

        elif self.titre == "Titre année":
            self.role.opacity = 0
            self.role.disabled = True
            self.password.opacity = 1
            self.password.disabled = False
            self.nom.opacity = 0
            self.nom.disabled = True
            self.prenom.opacity = 0
            self.prenom.disabled = True
            self.mention.opacity = 0
            self.mention.disabled = True

            self.password.hint_text = "Moyenne"

            self.ids.save_users.opacity = 0
            self.ids.save_mention.opacity = 0
            self.ids.save_parcours.opacity = 0
            self.ids.save_role.opacity = 0
            self.ids.save_annee.opacity = 1
            self.ids.save_droit.opacity = 0

        elif self.titre == "Montant":
            self.role.opacity = 0
            self.role.disabled = True
            self.password.opacity = 1
            self.password.disabled = False
            self.nom.opacity = 1
            self.nom.disabled = False
            self.prenom.opacity = 0
            self.prenom.disabled = True
            self.mention.opacity = 1
            self.mention.disabled = False

            self.password.hint_text = "Niveau"
            self.nom.hint_text = "Année"

            self.ids.save_users.opacity = 0
            self.ids.save_mention.opacity = 0
            self.ids.save_parcours.opacity = 0
            self.ids.save_role.opacity = 0
            self.ids.save_annee.opacity = 0
            self.ids.save_droit.opacity = 1

    def save_users(self):
        pass

    def save_mention(self):
        host = MDApp.get_running_app().HOST
        token = MDApp.get_running_app().TOKEN
        url = f"http://{host}/api/v1/mentions/"

        pass

    def save_parcours(self):
        pass

    def save_role(self):
        pass

    def save_droit(self):
        pass

    def save_annee(self):
        pass
