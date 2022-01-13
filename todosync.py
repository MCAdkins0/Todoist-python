from todoist.api import TodoistAPI
import constants
import json
import db
import tkinter as tk
from datetime import datetime

font = "Ubuntu Mono"

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
            'color':self.colorNum,
            'parent_id':self.parentProject
        }
        return (self.projectDetails)

    def projectToDB(self):
        details = self.projectInfo()
        todoistDB.insertProject(details)

    def getTasksByProject(self):
        self.taskInfo = api.projects.get_data(self.projectID)
        return self.taskInfo
        

    def isChecked(self):
        self.checkState = self.projectCheckVal.get()
        print(self.checkState)
        if self.checkState != 'None':
            self.getTasksByProject()
            pass
        else:
            pass

    def tkInit(self, frame):
        self.projectCheckVal = tk.BooleanVar()
        self.projectCheck = tk.Checkbutton(frame, text=self.projectName, variable=self.projectCheckVal, onvalue=True, offvalue=False, command=self.isChecked)

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
    
    def tasksToFrame(self, frame):
            taskList = tk.Listbox(frame,
            font=(font, 14),
            width=580,
            height=540,
            bg="SystemButtonFace",
            bd=0,
            fg="#464646",
            highlightthickness=0,
            selectbackground="#a6a6a6",
            activestyle="none"
            )
            taskScrollbar = tk.Scrollbar(frame)
            taskList.insert(END, apiFetchedTasks['project']['name'])
            lastItem = taskList.size()-1
            projectColor = todoistColors[apiFetchedTasks['project']['color']]
            taskList.itemconfig(lastItem, {'bg': projectColor})

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



addProjects()

p = projectObjects[0].projectDetails
task = {
    'id':'',
    'content':"Test adding a task",
    'parent_id':'',
    'date_added':datetime.now(),
    'checked':0,
    'due':{'is_recurring':False},
    'date_completed':'',
    'labels':'',
    'section_id':''
}
#test_task = Task(p,task)
#print(test_task.taskInfo())
