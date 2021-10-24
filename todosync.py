from todoist.api import TodoistAPI
import constants
import json
import db
import tkinter as tk
from datetime import datetime

api = TodoistAPI(constants.todoistKey)
api.sync()

todoistDB = db.db(constants.database)
todoistDB.setUpDB()

todoistColors = {
    30 : '#b8256f',
    31 : '#db4035',
    32 : '#ff9933',
    33 : '#fad000',
    34 : '#afb83b',
    35 : '#7ecc49',
    36 : '#299438',
    37 : '#6accbc',
    38 : '#158fad',
    39 : '#14aaf5',
    40 : '#96c3eb',
    41 : '#4073ff',
    42 : '#884dff',
    43 : '#af38eb',
    44 : '#eb96eb',
    45 : '#e05194',
    46 : '#ff8d85',
    47 : '#808080',
    48 : '#b8b8b8',
    49 : '#ccac93'
}

class Project:
    def __init__(self, project):
        self.projectName = project['name']
        self.projectID = project['id']
        self.colorNum = project['color']
        self.color = todoistColors[self.colorNum]
        self.parentProject = project['parent_id']

    def projectInfo(self):
        self.projectDetails = {
            'id':self.projectID,
            'name':self.projectName,
            'color':self.color,
            'parent':self.parentProject
        }
        return (self.projectDetails)

    def projectToDB(self):
        details = self.projectInfo()
        todoistDB.insertProject(details)

    def tkInit(self, frame):
        self.projectCheckval = tk.BooleanVar()
        self.projectCheck = tk.Checkbutton(frame, text=self.name, variable=self.checkVal, onvalue=True, offvalue=False, command=appsyncapi.isChecked)

class Task(Project):
    def __init__(self, project, task):
        super().__init__(project)
        self.taskID = task['id']
        self.taskName = task['content']
        self.taskParent = task['parent_id']
        self.dateAdded = task['date_added']
        self.checked = task['checked']
        self.due = task['due']
        self.dateCompleted = task['date_completed']
        self.labels = task['labels']
        self.section = task['section_id']
        self.isRecurring = task['due']['is_recurring']

    def taskInfo(self):
        self.taskDetails = {
            'id':self.taskID,
            'projectid':None,
            'name':self.taskName,
            'parent':self.taskParent,
            'added':self.dateAdded,
            'checked':self.checked,
            'due':self.due,
            'datecompleted':self.dateCompleted,
            'labels':self.labels,
            'section':self.section,
            'recurring':self.isRecurring
        }
        return (self.taskDetails)

projectObjects = list()

def addProjects():
    projects = api.state['projects']
    wanted_keys = ['id','name','color','parent_id']
    for p in projects:
        project = {}
        for key in wanted_keys:
            project[key] = p[key]
        newProject = Project(project)
        newProject.projectToDB()
        projectObjects.append(newProject)
    

def createTask(taskInfo):
    """keylist = ['taskName','description', 'project_id', 'due', 'priority', 'parentid', 'section_id', 'labels']
    for each in keylist:
        task[each] = None"""
    task = {}
    for key in taskInfo:
        task

def addTask(taskName, projectName, **kwargs):
    project = (todoistDB.queryProject(projectName))
    projectid = project[0]
    addedTask = api.items.add(taskName, projectid, kwargs)
    api.commit()
    return addedTask

def getTasksByProject(projectName):
    project = (todoistDB.queryProject(projectName))
    projectid = project[0]
    projectInfo = api.projects.get_data(projectid)
    return projectInfo

addProjects()
print(projectObjects[0])

p = projectObjects[0]
task = {
    'id':'',
    'name':"Test adding a task",
    'parent':'',
    'added':datetime.now(),
    'checked':0,
    'due':'',
    'datecompleted':'',
    'labels':'',
    'section':'',
    'recurring': ''
}
test_task = Task(p,task)

