from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty,StringProperty
from kivymd.uix.list import MDList,OneLineListItem,TwoLineListItem
from kivymd.uix.button import MDFlatButton
#from kivy.uix.scrollview import ScrollView
#import json
from kivy.storage.jsonstore import JsonStore
from kivy.clock import Clock,mainthread
import sys
import os.path
import json

file = sys.argv[0]
foldername =os.path.dirname(file)

store = JsonStore("data/data.json")

print("ssdqsqsdqsd",foldername)

screen_helper = """
ScreenManager
    MainScreen: 
    AddScreen: 
    PerScreen: 
    TripDetail:
<AddScreen>:
    id: addScreen
    name: 'Add'
    MDLabel:
        text: 'add new'
        halign: 'center'
        pos_hint:{'center_x':0.5,'center_y':0.9}
    MDRectangleFlatButton:
        text: 'back'
        pos_hint:{'center_x':0.5,'center_y':0.1}
        on_press: root.manager.current = 'Main'
    MDTextField:
        id: addNewCal
        hint_text: "Enter cal name:"
        pos_hint: {'center_x': 0.5,'center_y':0.6}
        size_hint_x: None
        width:300
    MDRectangleFlatButton:
        text: 'save'
        pos_hint:{'center_x':0.5,'center_y':0.4}
        on_press: root.save()

<MainScreen>:
    name:  'Main'
    MDRectangleFlatButton:
        text: 'add new'
        pos_hint: {'center_x':0.5,'center_y':0.5}
        on_press: root.manager.current = 'Add'
    MDRectangleFlatButton:
        text: 'pervius cal'
        pos_hint: {'center_x':0.5,'center_y':0.2}
        on_press: root.manager.current = 'Per'

<PerScreen>:
    name: 'Per'
    ScrollView:
        size_hint_y:None
        height: 400
        MDList:
            id: tripList
    MDLabel:
        text: 'pervius cal'
        halign: 'center'
        pos_hint: {'center_x': 0.3,'center_y':0.9}
    MDRectangleFlatButton:
        text: 'back'
        pos_hint: {'center_x': 0.7,'center_y':0.9}
        on_press: root.showTrip()
<TripDetail>:
    name: 'TripDetail'

"""

class MainScreen(Screen):
    pass

class AddScreen(Screen):
    screenManager = ObjectProperty(None)
    def save(self):
        calName = self.ids.addNewCal.text
        trip = {"tripname":calName,"persons":[],"sumCost": "0","personCost":[]}
        with open("data/data.json","r") as f:
            data = json.load(f)
            data["trips"].append(trip)
        with open("data/data.json","w") as f:
            json.dump(data,f,indent = 2)
        print(calName)

    pass

class PerScreen(Screen):
    
    @mainthread

    def on_enter(self, *args):
        """Event fired when the screen is displayed: the entering animation is
        complete."""
        
        def on_enter(interval):
            with open("data/data.json","r") as f:
                data = json.load(f)
                trip = data["trips"]
            self.ids.tripList.clear_widgets()
                
            for i in range(len(trip)):
                self.ids.tripList.add_widget(MDFlatButton(text=trip[i]["tripname"],on_press = showTrip))
        def showTrip(self,*args):
            MDApp.get_running_app().root.current = 'TripDetail'

        Clock.schedule_once(on_enter)
    def showTrip(self,*args):
            MDApp.get_running_app().root.current = 'TripDetail'
    
            

class TripDetail(Screen):
    def build(self):
        screen = Screen()
        label = MDLabel("TEXT")
        screen.add_widget(label)
        return screen
        
    def showTrip(self,*args):
            MDApp.get_running_app().root.current = 'Per'

sm = ScreenManager()
sm.add_widget(AddScreen(name='Add'))
sm.add_widget(MainScreen(name='Main'))
sm.add_widget(PerScreen(name='Per'))
sm.add_widget(TripDetail(name='TripDetail'))


class DongApp(MDApp):
    def build(self):
        screen = Builder.load_string(screen_helper)
        return screen  
        
    def showTrip(self):
        self.sm.current = 'TripDetail'


DongApp().run()