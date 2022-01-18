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
from kivy.uix.checkbox import CheckBox
from kivy.uix.switch import Switch
from kivy.uix.textinput import TextInput
from kivymd.uix.datatables import MDDataTable
from kivy.uix.recycleview import RecycleView
from kivy.metrics import dp
from kivy.storage.jsonstore import JsonStore
from todosync import addTask, sync_todoist
from functools import partial
import re


# Instatiate our todoist class
todos = getInfo.todoist()

class MainWindow(Screen):
    pass

class ProjectLabel(Label):
    pass

class ProjectSwitch(Switch):
    pass

class SettingsWindow(Screen):
    def updateKey(self, apiKey):
        keystore= JsonStore('keystore.json')
        keystore.put('todoistKey', api_key=apiKey)
        tasks = JsonStore('tasks.json')
        print(keystore.get('todoistKey')['api_key'])
        api_sync = sync_todoist(keystore.get('todoistKey')['api_key'])
        print(api_sync)


    def listProjects(self):
        projects = todos.getProjects()
        box = self.ids.list_projects_settings
        box.clear_widgets()
        grid = GridLayout(cols=2)

        for project, id in projects.items():
            print (project, id)
            label = Label(text=str(project))
            switch = Switch(id=int(id))
            grid.add_widget(label)
            grid.add_widget(switch)
        box.add_widget(grid)
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