from kivy.app import App
from kivy.uix.camera import Camera
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.core.window import Window

# set window size
Window.size = (500, 550)


class cameraApp(App):
    def build(self):
        global cam
        # create camera instance
        cam = Camera()
        # ceate button
        btn = Button(text="Capture Image")
        btn.size_hint = (.1, .1)
        btn.font_size = 35
        btn.background_color = 'blue'
        btn.bind(on_press=self.capture_image)
        # create grid layout
        layout = GridLayout(rows=2, cols=1)
        # add widgets in layout
        layout.add_widget(cam)
        layout.add_widget(btn)
        return layout

    def capture_image(self, *args):
        global cam
        # save captured image
        cam.export_to_png('image.png')
        # print message after capturing the image
        print('Image captured and saved in current working directory')


if __name__ == '__main__':
    # run app
    cameraApp().run()