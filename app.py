import kivy
kivy.require('2.0.0')
import getInfo

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.bubble import Bubble, BubbleButton
from kivy.uix.switch import Switch
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from PIL import Image, ImageTk
from tkinter import Toplevel, ttk

from todosync import addTask

from functools import partial


class MainWindow(Screen):
    pass

class SettingsWindow(Screen):
    pass

class TaskListWindow(Screen):
    pass

class AddTaskWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("todoapp.kv")

class TodoApp(App):

    def build(self):
        return kv

if __name__ == '__main__':
    TodoApp().run()