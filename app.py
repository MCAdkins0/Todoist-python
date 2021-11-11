import tkinter as tk
from tkinter.constants import BOTTOM, TOP, LEFT, RIGHT
import getInfo
from PIL import Image, ImageTk
from tkinter import Toplevel, ttk

from todosync import addTask

from functools import partial

# Set up tkinter window
window = tk.Tk()
window.geometry('800x600')
topFrame = ttk.Frame(window, borderwidth=3, width=800, height=60)
topFrame.pack(side=TOP)
#topFrame.grid(row=0, column=0)
projectFrame = ttk.Frame(window, borderwidth=3, width=200, height=540)
projectFrame.pack(side=LEFT, anchor="n")
#projectFrame.grid(row=1, column=0)
taskFrame = ttk.Frame(window, borderwidth=3, width=600, height=540)
taskFrame.pack(side=RIGHT)
#taskFrame.grid(row=1, column=1)
#canvas = tk.Canvas(window, width=800, height=400)
#canvas.grid(columnspan=5)
font = "Ubuntu Mono"

# Instatiate our todoist class
todos = getInfo.todoist()

# Display Todoist Logo
logo = ImageTk.PhotoImage(Image.open('todoistlogo.png').resize((50,50)))
logo_label = tk.Label(topFrame, image=logo)
logo_label.image = logo
logo_label.grid(row=0, column=1)


# Get Projects and Display them
projects = todos.getProjects()
projectsLabel = tk.Label(topFrame, text="Projects List", font=(font, 20))
projectsLabel.grid(row=0, column=0)
projectrow = 0
projectLabels = {}
for project, id in projects.items():
    label = tk.Label(projectFrame, text=project, font=(font, 14))
    checkboxVal = tk.IntVar()
    checkbox = tk.Checkbutton(projectFrame, variable=checkboxVal)
    #label.pack(side=LEFT)
    #checkbox.pack(side=RIGHT)
    label.grid(row=projectrow, column=0)
    checkbox.grid(row=projectrow, column=1)
    projectLabels[id] = checkboxVal
    projectrow += 1

# Fetch tasks based on selected projects
def fetchTasks():
    fields = ["content","description"]
    row = 0
    tasksTitle = tk.Label(topFrame, text="Task List", font=(font, 20))
    tasksTitle.grid(row=0, column=3)
    for id, check  in projectLabels.items():
        value = check.get()
        if value:
            projectid = id
            tasks = todos.getTasks(projectid)
            for task in tasks:
                taskLabel = ""
                for search_key in fields:
                    if search_key in task.keys():
                        print(task[search_key], str(row))
                        taskLabel = taskLabel + " " +str(task[search_key])
                label=tk.Label(taskFrame, text=taskLabel, font=(font, 14), wraplength=550, justify="left")
                #label.grid(row = row, column=3)
                label.pack(anchor="w")
                row+=1

def clearTasks():
    for widget in taskFrame.winfo_children():
        widget.destroy()

def addNewTask():
    addTaskWindow = Toplevel(window)
    addTaskWindow.title("Add New Task")
    addTaskWindow.geometry("400x400")
    addedTask = tk.StringVar
    notDoneLabel = tk.Label(addTaskWindow, text="This doesn't yet do anything")
    newTaskLabel = tk.Label(addTaskWindow, text="Task")
    newTask = tk.Entry(addTaskWindow)
    setProjectLabel= tk.Label(addTaskWindow, text="Project")
    setProject = tk.Entry(addTaskWindow)
    taskReturnLabel = tk.Label(addTaskWindow, textvariable=addedTask)
    notDoneLabel.grid(columnspan=2, row=0)
    newTaskLabel.grid(column=0, row=1)
    newTask.grid(column=1, row=1)
    setProjectLabel.grid(column=0, row=2)
    setProject.grid(column=1, row=2)
    task = newTask.get()
    project = setProject.get()
    addTaskButton = tk.Button(addTaskWindow, text="Add Task", command=partial(addTask, task, project))
    addTaskButton.grid(column=0, row=3)
    taskReturnLabel.grid(columnspan=2, row=4)


mainMenuBar = tk.Menu(window)
menu = tk.Menu(mainMenuBar)
menu.add_command(label="New Task", underline=1, command=addNewTask)
menu.add_command(label="Exit", underline=1, command=window.destroy)
mainMenuBar.add_cascade(label="File", menu=menu)
helpMenu = tk.Menu(mainMenuBar)
helpMenu.add_command(label="Help")
mainMenuBar.add_cascade(label="Help", menu=helpMenu)
window.config(menu=mainMenuBar)

# Buttons for app
getTaskButton = tk.Button(projectFrame, text="Get Tasks", command=fetchTasks)
getTaskButton.grid(row=projectrow, column=0)
#projectrow += 1
clearTasksButton = tk.Button(projectFrame, text="Clear Tasks", command=clearTasks)
clearTasksButton.grid(row=projectrow, column=1)
#getTaskButton.pack(side=BOTTOM)



window.mainloop()