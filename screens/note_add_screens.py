from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivymd.uix.list import TwoLineListItem


class NoteAddScreen(Screen):
    screenManager = ObjectProperty(None)

    def on_enter(self, *args):
        for i in range(20):
            self.ids.container.add_widget(
                TwoLineListItem(
                    text=f"Numéro Carte: {i}",
                    secondary_text="Secondary text here fhiuhiquhfqnifqgfqnfqgfq f qfgqgfqgsfq fyqgsyfgqygf qyfgqsgf qf"
                                   "qsiqgf qfguqsgf qufsgu"
                )
            )


