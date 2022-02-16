from kivy.app import App
from kivy.lang import Builder

kv = '''
BoxLayout:
    orientation: 'vertical'
    FloatLayout:
        canvas:
            Color:
                rgb: 1, 1, 1
            Ellipse:
                pos: 280, 200
                size: 200 , 200 
                source: 'image.jpg'
                angle_start: 0
                angle_end: 360

'''


class App(App):
    def build(self):
        return Builder.load_string(kv)


App().run()
