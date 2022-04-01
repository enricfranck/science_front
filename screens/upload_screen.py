import os
import urllib

from kivy.core.window import Window
from kivy.network.urlrequest import UrlRequest
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager


class UploadScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.select_path_ = ""
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            # preview=True,
        )

    def file_manager_open(self):
        self.file_manager.show('/')  # output manager to the screen
        self.manager_open = True

    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''

        self.exit_manager()
        if os.path.isdir(path):
            self.ids.path.text = path
        else:
            self.ids.path.text = str(path).rsplit('/', 1)[0]

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

    def on_enter(self, *args):
        self.ids.toolbar.title = MDApp.get_running_app().TITRE_FILE
        self.ids.progress_bar.value = 0

    def back_home(self):
        MDApp.get_running_app().root.current = MDApp.get_running_app().PARENT

    def update_progress(self, req, current_size, total_size):
        self.ids.progress_bar.value = current_size / total_size

    def upload_file(self):
        url = MDApp.get_running_app().URL_UPLOAD
        params = MDApp.get_running_app().PARAMS
        token = MDApp.get_running_app().TOKEN
        path = f"{self.ids.path.text}"
        headers = {'accept': 'application/json',
                   'Authorization': f'Bearer {token}'
                   }
        url = f"{url}?{params}"
        req = requests.post(url=url, headers=headers, files={"uploaded_file": open(f'{path}', 'rb')})
        self.ids.path.text = ""
        self.back_home()
        return req.json()
