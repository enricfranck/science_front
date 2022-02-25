# from kivymd.app import MDApp
# from kivy.uix.screenmanager import Screen, ScreenManager
# from kivymd.uix.datatables import MDDataTable
# from kivy.metrics import dp
# from kivy.uix.anchorlayout import AnchorLayout
# from kivy.lang.builder import Builder
import json
import urllib.parse

# KV = """
# ScreenManager:
#     DemoPage:

#     ClientsTable:


# <DemoPage>:
#     MDRaisedButton:
#         text: " Next "
#         size_hint: 0.5, 0.06
#         pos_hint: {"center_x": 0.5, "center_y": 0.4}
#         on_release: 
#             root.manager.current = 'Clientstable'


# <ClientsTable>:
#     name: 'Clientstable'
#     BoxLayout:
#         orientation:'vertical'
#         MDToolbar:
#             title: 'Réinscription'
#             left_action_items:[["keyboard-backspace",lambda x: root.back_main()]]
#             elevation:5
#         Widget:
#  """


# class ClientsTable(Screen):
#     def load_table(self):
#         layout = AnchorLayout()
#         self.data_tables = MDDataTable(
#             pos_hint={'center_y': 0.5, 'center_x': 0.5},
#             size_hint=(0.9, 0.6),
#             use_pagination=True,
#             check=True,
#             column_data=[
#                 ("No.", dp(30)),
#                 ("Head 1", dp(30)),
#                 ("Head 2", dp(30)),
#                 ("Head 3", dp(30)),
#                 ("Head 4", dp(30)), ],
#             row_data=[
#                 (f"{i + 1}", "C", "C++", "JAVA", "Python")
#                 for i in range(42)], )
#         self.add_widget(self.data_tables)
#         return layout

#     def on_enter(self):
#         self.load_table()


# class DemoPage(Screen):
#     pass


# sm = ScreenManager()

# sm.add_widget(DemoPage(name='demopage'))
# sm.add_widget(ClientsTable(name='Clientstable'))


# class MainWindow(MDApp):
#     def build(self):
#         screen = Builder.load_string(KV)
#         return screen
from kivy.network.urlrequest import UrlRequest


def success(req, result):
    print('success')


def fail(req, result):
    print(req, result)


def error(req, result):
    print(req, result)


def progress(req, result, chunk):
    print('loading')


def find_key(lettre: str, key: str):
    value = lettre.lower()
    key_value = key.lower()
    return value.find(key_value)


def read_mention_by_title(data: list, titre: str):
    return list(
        filter(lambda mention: find_key(mention["name"], titre) != -1 or find_key(mention["adresse"], titre) != -1,
               data))


def create_face_carte(url: str, token: str, payload):
    headers = {'accept': 'application/json',
               'Content-Type': 'application/json',
               'Authorization': f'Bearer {token}'
               }
    payload_ = json.dumps(payload)
    print(payload_)
    # req = UrlRequest(url, on_success=success, on_failure=fail, on_error=error, on_progress=progress,
    #                  req_headers=headers, file_path="/home/enric/Documents/test.pdf", verify=False, method="GET")
    req = UrlRequest(url, on_success=success, on_failure=fail, on_error=error, on_progress=progress,
                     req_headers=headers, req_body=payload, verify=False, method="POST")
    req.wait()
    return req.result


if __name__ == "__main__":
    # MainWindow().run()
    # data = [{"name": "franck", "age": 26, "adresse": "paris"},
    #         {"name": "françois", "age": 27, "adresse": "france"},
    #         {"name": "frame", "age": 15, "adresse": "parisho"}
    #         ]
    # value = read_mention_by_title(data, "PA")
    # url = 'http://localhost/api/v1/liste/list_inscrit/?schemas=anne_2020_2021&semestre=S8&uuid_parcours=d7b9b12a-9d26-4fa7-8c18-cc5f8a3f01b8&uuid_mention=993e2bd1-8608-4885-aed9-3436d1736373'
    # url_= "http://localhost/api/v1/liste/list_inscrit/?schema=anne_2020_2021&uuid_mention=993e2bd1-8608-4885-aed9-3436d1736373&uuid_parcours=d7b9b12a-9d26-4fa7-8c18-cc5f8a3f01b8&semestre=S8"
    # token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NDUyODM1ODIsInV1aWQiOiJkM2FkMmQ5OC1hYjM3LTQyMjQtYjU2OS1mNGM1NGRlZjVlMDkifQ.wvpt1ViX2EZI8jKzsNcLMRkLZdgOTQ9d3ZOZc4k3gMQ "

    url = "http://localhost/api/v1/nouveau_etudiants/?schema=anne_2020_2021'"
    payload = {"num_select": "3", "nom": "zf2Bk9XUUBhQYCjjWFxL", "prenom": "iGjrj", "date_naiss": "1993-12-10",
     "lieu_naiss": "piGOiStUyzyD", "adresse": "zHpcIuGJ", "num_cin": "ZuivPshSHeKM", "date_cin": "2012-02-13",
     "lieu_cin": "3xoO", "uuid_mention": "993e2bd1-8608-4885-aed9-3436d1736373", "niveau": "L1",
     "branche": "mathematiques", "select": False, "nation": "Malagasy", "sexe": "MASCULIN",
     "uuid": "993e2bd1-8608-4885-aed9-3436d1736373"}

    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NDU1MzExNTQsInV1aWQiOiJmYWJmNTM5Ni1mMWJiLTRjOTQtOGQxNC1kZGM2MDI5ZmQ5ZmMifQ.8zNTp0-75hwXSu1q1mFMFqY21NoLUuttY9NlaQhbLmo"

    print(type(create_face_carte(url, token, payload)))
