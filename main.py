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
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics import *
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, NoTransition
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock




def tile(src):
    new_tile = Image(source = src,size_hint_x=None,width=16,size_hint_y=None,height=16,allow_stretch=True)
    
    return new_tile

# Establish connection with local database (to come)
def database_connect():
    pass

class player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.visible = False
        
    def summon(self,x,y):
        self.avatar = Image(source = 'atlas://Adventurer/fall-left-1',size_hint_x = None, width=32,size_hint_y = None,height=32,pos = (x,y))
        return self.avatar
        
    def animate(self,animationName,numberFrames):
        self.time = 0.0
        self.rate = 0.1
        self.frame = 1
        self.numberFrames = numberFrames
        self.animationName = animationName
        Clock.schedule_interval(self.update, 1.0/60.0)
        
    def update(self, dt):
        self.time += dt
        if (self.time > self.rate):
            self.time -= self.rate
            self.avatar.source = "atlas://Adventurer/"+self.animationName+'-'+ str(self.frame)
            self.frame = self.frame + 1
            if (self.frame == self.numberFrames):
                self.frame = 1

class mainApp(App):
    def build(self):
        self.field = FloatLayout()
        self._keyboard = Window.request_keyboard(self._keyboard_closed,self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        self.manager = ScreenManager()
        self.manager.transition = NoTransition()
        
        self.initView()
        
        self.ev.animate("walk-right",8)
        
        return self.field

    def initView(self):
        self.view = GridLayout(cols=32,rows=32)
        for i in range(1024):
            self.view.add_widget(tile("atlas://map/grass"+str(random.randint(1,2))+"-" + str(random.randint(1,5))))

        self.field.add_widget(self.view)
        self.ev = player()
        self.field.add_widget(self.ev.summon(100,100))



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
