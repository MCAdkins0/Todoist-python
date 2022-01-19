import kivy
kivy.require('2.0.0')
import getInfo

from tinydb import TinyDB, Query
from kivy.app import App
from kivymd.app import MDApp
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
from todosync import sync_todoist
from functools import partial
import re


# Instatiate our todoist class
todos = getInfo.todoist()

todoDB = TinyDB('todoist.json')
projectTable = todoDB.table('projects')
taskTable = todoDB.table('tasks')

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
        print(keystore.get('todoistKey')['api_key'])
        api_sync = sync_todoist(keystore.get('todoistKey')['api_key'])
        get_projects = api_sync.state['projects']
        print(get_projects)

    def hitCB(self, pname, cbObject, cbValue):
        print(pname + " checkbox was pushed, updating DB")
        Projects = Query()
        projectTable.update({'fetch':cbValue}, Projects.ProjectName.search(pname))
        


    def listProjects(self):
        projects = todos.getProjects()
        box = self.ids.list_projects_settings
        box.clear_widgets()
        grid = GridLayout(cols=2)

        for project, id in projects.items():
            label = Label()
            cb = CheckBox()
            label.text = str(project)
            cb.bind(active=partial(self.hitCB, project))
            #project_to_db = {'ProjectName':project, 'projectID':int(id), 'fetch':bool(cb.active)}
            #checkFetch = Query()
            is_existing_project = Query()
            projectTable.upsert({'ProjectName':project, 'projectID':int(id), 'fetch':bool(cb.active)},\
                 is_existing_project.projectID == id)
            grid.add_widget(label)
            grid.add_widget(cb)
        box.add_widget(grid)
class TaskListWindow(Screen):
    def fetchTasks(self):
        projectQuery = Query()
        selectedProjects = projectTable.search(projectQuery.fetch == True)
        for project in selectedProjects:
            tasks = todos.getTasks(project['projectID'])
            for task in tasks:
                pquery = Query()
                is_existing_task = Query()
                project = projectTable.get(pquery.projectID == task['project_id'])
                pname = project['ProjectName']
                taskTable.upsert({'task':task['content'], 'taskID':task['id'], 'projectName':pname,\
                     'description':task['description'], 'priority':task['priority']}, is_existing_task.taskID == task['id'])
    
    def listTasks(self):
        self.fetchTasks()
        grid = self.ids.taskGrid
        taskQuery = Query()
        taskList = taskTable.all()
        taskData = []
        for task in taskList:
            taskData.append((task['projectName'],task['priority'], task['task'], task['description']))
        self.dt = MDDataTable(
            #use_pagination=True, 
            column_data=[
                ("Project", dp(30)),
                ("Priority", dp(30)),
                ("Task Name", dp(30)),
                ("Description", dp(30)),
            ],
            row_data= taskData
        )
        self.add_widget(self.dt)
        #self.ids.taskbox.data = taskList

class AddTaskWindow(Screen):
    def listProjects(self, projects):
        for project, id in projects.items():
            print (project, id)
    def project_spinner_clicked(self, value):
        self.ids.task_project.text = value


class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("todoapp.kv")

class TodoApp(MDApp):

    keystore = JsonStore('keystore.json')

    try:
        sync = sync_todoist(keystore.get('todoistKey')['api_key'])
        print('Synced with Todoist')
    except Exception as e:
        print("That didn't work, maybe try setting/updating your api key")
        print(e)
        
    def build(self):
        return kv

if __name__ == '__main__':
    TodoApp().run()