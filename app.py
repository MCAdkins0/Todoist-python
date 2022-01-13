from asyncio.proactor_events import constants
import kivy
kivy.require('2.0.0')
import getInfo

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.bubble import Bubble, BubbleButton
from kivy.uix.switch import Switch
from kivy.uix.textinput import TextInput
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from todosync import addTask
from functools import partial
import re


# Instatiate our todoist class
todos = getInfo.todoist()
# Fetch Projects
projects = todos.getProjects()

class MainWindow(Screen):
    pass

class SettingsWindow(Screen):
    def updateKey(self, apiKey):
        with open('constants.py', 'r+') as constantsFile:
            contents = constantsFile.read()
            newcontents = re.sub('^todoistKey:.*$', apiKey, contents, flags = re.M)
            constantsFile.seek(0)
            constantsFile.truncate()
            constantsFile.write(contents)
        print("This currently doesn't work, please change the key manually in the constants.py file")
    def listProjects(self, projects):
        for project, id in projects.items():
            print (project, id)

class TaskListWindow(Screen):
    def listTasks(self, tasks):
        pass

class AddTaskWindow(Screen):
    def listProjects(self, projects):
        for project, id in projects.items():
            print (project, id)
    def project_spinner_clicked(self, value):
        self.ids.task_project.text = value


class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("todoapp.kv")

class TodoApp(App):

    def build(self):
        return kv

if __name__ == '__main__':
    TodoApp().run()