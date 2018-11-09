# System imports
import sys
import os
import random

# Database import
import sqlite3

# Kivy related imports
from kivy.app import App
from kivy.config import Config
Config.set('graphics', 'width', '512')
Config.set('graphics', 'height', '512')
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.graphics import *
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, NoTransition
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.core.window import Window




def tile(src):
    new_tile = Image(source = src,size_hint_x=None,width=16,size_hint_y=None,height=16,allow_stretch=True)
    
    return new_tile

# Establish connection with local database (to come)
def database_connect():
    pass

class mainApp(App):
    def build(self):
        self._keyboard = Window.request_keyboard(self._keyboard_closed,self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        self.manager = ScreenManager()
        self.manager.transition = NoTransition()
        
        self.initView()
        return self.view

    def initView(self):
        self.view = GridLayout(cols=32,rows=32)
        for i in range(1024):
            self.view.add_widget(tile("atlas://map/grass"+str(random.randint(1,2))+"-" + str(random.randint(1,5))))


    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self.keyboard = None

    def _on_keyboard_down(self,keyboard,keycode,text,modifiers):
        if keycode[1] == 'w':
            pass
        elif keycode[1] == 'a':
            pass
        elif keycode[1] == 's':
            pass
        elif keycode[1] == 'd':
            pass
        elif keycode[1] == 'q':
            exit()
        return True

if __name__=="__main__":
    main = mainApp()
    main.run()
