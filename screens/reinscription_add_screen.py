from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty,StringProperty

class ReinscriptionAddScreen(Screen):
    screenManager = ObjectProperty(None)
    def on_enter(self):
        self.ids.s1_check.active = True
    def back_home(self):
        MDApp.get_running_app().root.current = 'Reinscription'

    def select_semestre(self):
        s1: str = self.ids.s1.text
        s1_check: str = self.ids.s1_check

        s2: str = self.ids.s2.text
        s2_check: str = self.ids.s2_check

        s3: str = self.ids.s3.text
        s3_check: str = self.ids.s3_check

        s4: str = self.ids.s4.text
        s4_check: str = self.ids.s4_check

        s5: str = self.ids.s5.text
        s5_check: str = self.ids.s5_check

        s6: str = self.ids.s6.text
        s6_check: str = self.ids.s6_check

        s7: str = self.ids.s7.text
        s7_check: str = self.ids.s7_check

        s8: str = self.ids.s8.text
        s8_check: str = self.ids.s8_check

        s9: str = self.ids.s1.text
        s9_check: str = self.ids.s9_check

        s10: str = self.ids.s10.text
        s10_check: str = self.ids.s10_check

        license_ :list = [s1_check,s2_check,s3_check,s4_check,s5_check,s6_check,]
        master_one :list = [s7_check,s8_check]
        master_two :list = [s9_check,s10_check]
        list_active :list = []
        list_niveau : list = [license_, master_one,master_two]

        for index, niveau in enumerate(list_niveau):
            for sems in niveau:
                if sems.disabled:
                    for index_, niveau_ in enumerate(list_niveau):
                        if index_ != index:
                            for sems_ in niveau_:
                                sems_.disabled = True
                else:
                    for index_, niveau_ in enumerate(list_niveau):
                        if index_ != index:
                            for sems_ in niveau_:
                                sems_.disabled = False




