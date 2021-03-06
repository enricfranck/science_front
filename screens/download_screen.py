import os
import urllib
import threading
from kivy.clock import mainthread

from kivy.core.window import Window
from kivy.network.urlrequest import UrlRequest
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager


class DownloadScreen(Screen):
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

    @mainthread
    def spinner_toggle(self):
        if not self.ids.download.disabled:
            self.ids.download.disabled = True
        else:
            self.ids.download.disabled = False

    def process_download_toogle(self):
        self.spinner_toggle()
        threading.Thread(target=(
            self.download_file)).start()

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
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True

    def on_enter(self, *args):
        print(MDApp.get_running_app().URL_DOWNLOAD)
        self.ids.toolbar.title = MDApp.get_running_app().TITRE_FILE
        self.ids.progress_bar.value = 0

    def back_home(self):
        MDApp.get_running_app().root.current = MDApp.get_running_app().PARENT

    def update_progress(self, req, current_size, total_size):
        self.ids.progress_bar.value = current_size / total_size

    def download_file(self):
        url = MDApp.get_running_app().URL_DOWNLOAD
        token = MDApp.get_running_app().TOKEN
        path = f"{self.ids.path.text}/{MDApp.get_running_app().NAME_DOWNLOAD}"
        headers = {'accept': 'application/json',
                   'Authorization': f'Bearer {token}'
                   }
        req = UrlRequest(url, on_success=self.success, on_failure=self.fail,
                         on_error=self.error, on_progress=self.update_progress,
                         chunk_size=1024, req_headers=headers, file_path=path,
                         verify=False, method="GET", timeout=38000)
        req.wait()
        self.spinner_toggle()
        return req.result

    def success(self, req, result):
        self.ids.path.text = ""
        self.ids.download.disabled = False
        MDApp.get_running_app().PARAMS = ""
        self.back_home()
        print('success')

    def fail(self, req, result):
        self.spinner_toggle()
        print("fail_", req.resp_status, result)

    def error(self, req, result):
        self.spinner_toggle()
        print("error_", req.resp_status, result)
