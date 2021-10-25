import tkinter as tk
from tkinter.constants import ANCHOR, BOTH, BOTTOM, END, TOP, LEFT, RIGHT
import todosync
import db
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
from functools import partial

# Set up tkinter window
window = tk.Tk()
window.geometry('800x600')
window.title("Todoist Task Manager")
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

# Get Projects and Display them
projectsLabel = tk.Label(topFrame, text="Projects List", font=(font, 20))
projectsLabel.grid(row=0, column=0)
projectrow = 0
projectLabels = {}

#taskList for right side of screen
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

collectedTasks = {}

# Fetch tasks based on project
def fetchTasks():
    #collectedTasks = [p['content'] for p in todosync.projectObjects['items']]
    collectedTasks.clear()
    tasksTitle = tk.Label(topFrame, text="Task List", font=(font, 20))
    tasksTitle.grid(row=0, column=3)
    for project in todosync.projectObjects:
        enabled = project.projectCheckVal.get()
        if enabled:
            taskList.insert(END, project.projectName)
            lastItem = taskList.size()-1
            taskList.itemconfig(lastItem, {'bg': project.color})
            tasks = project.taskInfo['items']
            projectTaskCounts = len(tasks) 
            for task in tasks:
                collectedTasks[task['content']] = task['id']
                taskList.insert(END, task['content'])

def taskDetail():
    content = taskList.get(ANCHOR)
    id = collectedTasks[content]
    taskDetails = todosync.api.items.get(id)
    try:
        content = taskDetails['item']['content']
        description = taskDetails['item']['description']
        due = taskDetails['item']['due']['string']
    except TypeError as e:
        print(e)
    message = "Task Information\nTask: "+content+"\nDescription: "+description+"\nDue: "+due
    taskMessage = messagebox.Message(title=content, message=message)


for each in todosync.projectObjects:
    each.tkInit(projectFrame)
    each.projectCheck.grid(row=projectrow, column=1)
    #label = tk.Label(projectFrame, text=project[1], font=(font, 14))
    #checkboxVal = tk.StringVar()
    #checkbox = tk.Checkbutton(projectFrame, text=project[1], variable=checkboxVal, onvalue=project[1], offvalue="None", command=isChecked).grid(row=projectrow, column=1)
    #label.grid(row=projectrow, column=0)
    #projectLabels[id] = checkboxVal
    projectrow += 1


def clearTasks():
    #for widget in taskFrame.winfo_children():
    #    widget.destroy()      
    taskList.delete(0,END)          

# Buttons for app
getTaskButton = tk.Button(projectFrame, text="Get Tasks", command=fetchTasks)
getTaskButton.grid(row=projectrow, column=0)
#projectrow += 1
clearTasksButton = tk.Button(projectFrame, text="Clear Tasks", command=clearTasks)
clearTasksButton.grid(row=projectrow, column=1)
taskDetailButton = tk.Button(projectFrame, text="Get Task Detail", command=taskDetail)
taskDetailButton.grid(row=projectrow, column=2)
#getTaskButton.pack(side=BOTTOM)



window.mainloop()