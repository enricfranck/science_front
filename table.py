from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.lang.builder import Builder

KV = """
ScreenManager:
    DemoPage:
    
    ClientsTable:


<DemoPage>:
    MDRaisedButton:
        text: " Next "
        size_hint: 0.5, 0.06
        pos_hint: {"center_x": 0.5, "center_y": 0.4}
        on_release: 
            root.manager.current = 'Clientstable'
            
            
<ClientsTable>:
    name: 'Clientstable'
    BoxLayout:
        orientation:'vertical'
        MDToolbar:
            title: 'Réinscription'
            left_action_items:[["keyboard-backspace",lambda x: root.back_main()]]
            elevation:5
        Widget:
 """


class ClientsTable(Screen):
    def load_table(self):
        layout = AnchorLayout()
        self.data_tables = MDDataTable(
            pos_hint={'center_y': 0.5, 'center_x': 0.5},
            size_hint=(0.9, 0.6),
            use_pagination=True,
            check=True,
            column_data=[
                ("No.", dp(30)),
                ("Head 1", dp(30)),
                ("Head 2", dp(30)),
                ("Head 3", dp(30)),
                ("Head 4", dp(30)), ],
            row_data=[
                (f"{i + 1}", "C", "C++", "JAVA", "Python")
                for i in range(42)], )
        self.add_widget(self.data_tables)
        return layout

    def on_enter(self):
        self.load_table()


class DemoPage(Screen):
    pass


sm = ScreenManager()

sm.add_widget(DemoPage(name='demopage'))
sm.add_widget(ClientsTable(name='Clientstable'))


class MainWindow(MDApp):
    def build(self):
        screen = Builder.load_string(KV)
        return screen


if __name__ == "__main__":
    MainWindow().run()