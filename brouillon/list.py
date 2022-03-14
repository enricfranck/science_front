from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem, ThreeLineListItem

KV = '''
ScrollView:
    MDList:
        id: container
'''


class Test(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        for i in range(20):
            self.root.ids.container.add_widget(
                ThreeLineListItem(
                    text=f"Single-line item {i}",
                    secondary_text="This is a multi-line label where you can",
                    tertiary_text="fit more text than usual"
                )
            )


Test().run()
