# System imports
import sys
import os
import random


# Database import
import sqlite3

# Kivy related imports
from kivy.app import App
from kivy.config import Config
Config.set('graphics', 'width', '250')
Config.set('graphics', 'height', '125')
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
from kivy.uix.widget import Widget

os.environ['KIVY_AUDIO']='sdl2'
from kivy.core.audio import SoundLoader

track1 = SoundLoader.load(filename='music/stonefortress.ogg')
if track1:
    track1.volume = .1
    
melee1 = SoundLoader.load(filename='sounds/melee1.wav')
if melee1:
    melee1.volume = .17
    
melee2 = SoundLoader.load(filename='sounds/melee2.wav')
if melee2:
    melee2.volume = .17
    
melee3 = SoundLoader.load(filename='sounds/melee3.wav')
if melee3:
    melee3.volume = .17

grass_step_l = SoundLoader.load(filename='sounds/sfx_step_grass_l.ogg')
if grass_step_l:
    grass_step_l.volume = .2
    
grass_step_r = SoundLoader.load(filename='sounds/sfx_step_grass_r.ogg')
if grass_step_r:
    grass_step_r.volume = .2

def tile(src):
    new_tile = Image(source = src,size_hint_x=None,width=32,size_hint_y=None,height=32,allow_stretch=True)
    
    return new_tile

# Establish connection with local database (to come)
def database_connect():
    pass

class player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.visible = False
        self.direction = None
        self.moving = False
        self.animationName = ''
        self.lastAnimation = ''
        self.numberFrames = 0
        self.lastFrames = 0
        self.foot = 'left'
        
    def summon(self,x,y):
        self.avatar = Image(source = 'atlas://sprites/Adventurer/fall-left-1',size_hint_x = None, width=32,size_hint_y = None,height=32,pos = (x,y))
        self.visible = True
        return self.avatar
        
    def clock_begin(self):
        Clock.schedule_interval(self.update, 1.0/60.0)
        
    def animate(self,animationName,numberFrames):
        self.time = 0.0
        self.rate = 0.1
        self.frame = 1
        self.lastFrames = self.numberFrames
        self.numberFrames = numberFrames
        self.lastAnimation = self.animationName
        self.animationName = animationName
    def move(self):
        if (self.avatar.pos[0] <= -22 and self.direction == 'left') or (self.avatar.pos[0] >= 240 and self.direction == 'right'):
            return
        if self.direction == 'left':
            self.avatar.pos[0] -= 1.5
        else:
            self.avatar.pos[0] += 1.5
        if self.foot == 'left' and grass_step_l:
            self.foot = 'right'
            grass_step_l.play()
        elif self.foot == 'right' and grass_step_r:
            self.foot = 'left'
            grass_step_r.play()
        
    def update(self, dt):
        if 'walk' in self.animationName:
            self.move()
        if 'jump' in self.animationName and 'walk' in self.lastAnimation:
            self.move()
        self.time += dt
        if (self.time > self.rate):
            self.time -= self.rate
            self.avatar.source = "atlas://sprites/Adventurer/"+self.animationName+'-'+ str(self.frame)
            self.frame = self.frame + 1
            if (self.frame == self.numberFrames):
                if 'jump' in self.animationName or 'slash' in self.animationName or 'stab' in self.animationName:
                    if 'slash' in self.lastAnimation or 'stab' in self.lastAnimation:
                        self.animate('idle-'+self.direction,13)
                    else:
                        self.animationName = self.lastAnimation
                        self.numberFrames = self.lastFrames
                self.frame = 1

class mainApp(App):
    def build(self):
        self.field = FloatLayout()
        self._keyboard = Window.request_keyboard(self._keyboard_closed,self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        self.manager = ScreenManager()
        self.manager.transition = NoTransition()
        
        self.initView()
        
        self.ev.clock_begin()
        
        if track1:
            track1.play()
        
        return self.field

    def initView(self):
        self.view = Image(source = "back/Transparent/full_background.png")

        self.field.add_widget(self.view)
        self.ev = player()
        self.ev.animate("idle-left",13)
        self.ev.direction = 'left'
        self.field.add_widget(self.ev.summon(100,13))



    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self.keyboard = None

    def _on_keyboard_down(self,keyboard,keycode,text,modifiers):
        if keycode[1] == 'w':
            self.ev.animate('jump-'+self.ev.direction,6)
        elif keycode[1] == 'a':
            self.ev.animate("walk-left",8)
            self.ev.direction = 'left'
            self.ev.moving = True
        elif keycode[1] == 's':
            if self.ev.direction == 'left':
                self.ev.animate("idle-left",13)
            else:
                self.ev.animate("idle-right",13)
            self.ev.moving = False
        elif keycode[1] == 'd':
            self.ev.animate("walk-right",8)
            self.ev.direction = 'right'
            self.ev.moving = True
        elif keycode[1] == 'r':
            self.ev.animate("up-slash-"+self.ev.direction,10)
            if melee3:
                melee3.play()
        elif keycode[1] == 'f':
            self.ev.animate("stab-"+self.ev.direction,10)
            if melee2:
                melee2.play()
        elif keycode[1] == 'c':
            self.ev.animate("down-slash-"+self.ev.direction,10)
            if melee1:
                melee1.play()
        elif keycode[1] == 'p':
            exit()
        return True

if __name__=="__main__":
    main = mainApp()
    main.run()
