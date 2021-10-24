import tkinter as tk
from tkinter.constants import BOTH, BOTTOM, END, TOP, LEFT, RIGHT
import todosync
import db
from PIL import Image, ImageTk
from tkinter import ttk
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

# Display Todoist Logo
logo = ImageTk.PhotoImage(Image.open('todoistlogo.png').resize((50,50)))
logo_label = tk.Label(topFrame, image=logo)
logo_label.image = logo
logo_label.grid(row=0, column=1)

def isChecked():
    checkState = checkboxVal.get()
    print(checkState)
    if checkState != 'None':
        #fetchTasks(checkState)
        pass
    else:
        pass




# Get Projects and Display them
projectsLabel = tk.Label(topFrame, text="Projects List", font=(font, 20))
projectsLabel.grid(row=0, column=0)
projectrow = 0
projectLabels = {}

projects = todosync.todoistDB.queryAllProjects()

taskList = tk.Listbox(taskFrame,
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
taskList.pack(side=LEFT, fill=BOTH)
taskScrollbar = tk.Scrollbar(taskFrame)
taskScrollbar.pack(side=RIGHT, fill=BOTH)

# Fetch tasks based on project
def fetchTasks(project):
    apiFetchedTasks = todosync.getTasksByProject(project)
    fields = ["content","description"]
    row = 0
    tasksTitle = tk.Label(topFrame, text="Task List", font=(font, 20))
    tasksTitle.grid(row=0, column=3)
    taskList.insert(END, apiFetchedTasks['project']['name'])
    lastItem = taskList.size()-1
    projectColor = todosync.todoistColors[apiFetchedTasks['project']['color']]
    taskList.itemconfig(lastItem, {'bg': projectColor})
    for item in apiFetchedTasks["items"]:
        taskList.insert(END, item['content'])


for project in projects:
    #label = tk.Label(projectFrame, text=project[1], font=(font, 14))
    checkboxVal = tk.StringVar()
    checkbox = tk.Checkbutton(projectFrame, text=project[1], variable=checkboxVal, onvalue=project[1], offvalue="None", command=isChecked).grid(row=projectrow, column=1)
    #label.grid(row=projectrow, column=0)
    #projectLabels[id] = checkboxVal
    projectrow += 1


def clearTasks():
    for widget in taskFrame.winfo_children():
        widget.destroy()                

# Buttons for app
getTaskButton = tk.Button(projectFrame, text="Get Tasks", command=fetchTasks)
getTaskButton.grid(row=projectrow, column=0)
#projectrow += 1
clearTasksButton = tk.Button(projectFrame, text="Clear Tasks", command=clearTasks)
clearTasksButton.grid(row=projectrow, column=1)
#getTaskButton.pack(side=BOTTOM)



window.mainloop()