import requests
import pprint
import json
import uuid
import constants

url = "https://wttr.in/97219?format=j1"

response = requests.get(url)
response.raise_for_status()

responsejson = response.json()

""" def makecall(url, key):
    response = requests.get(
        url,
        headers{
            "Authorization": "Bearer "+key
        }
    ) """

class todoist:
    def __init__(self):
        self.apikey = constants.todoistKey
    def getProjects(self):
        self.projecturl = "https://api.todoist.com/rest/v1/projects"
        todoistCall = requests.get(
            self.projecturl, 
            headers={
                "Authorization": "Bearer "+self.apikey
            }).json()
        self.projects = {}
        for each in todoistCall:
            self.projects[each["name"]] = (each["id"])
        return self.projects
    
    def listProjects(self):
        self.projectNumber = 1
        self.projectlist = list(self.projects.keys())
        for key in self.projectlist:
            print(str(self.projectNumber)+" : "+key)
            self.projectNumber += 1

    def getTasks(self, project):
        self.taskurl = "https://api.todoist.com/rest/v1/tasks"
        todoistcall = requests.get(
            self.taskurl,
            params={
                "project_id": project
            },
            headers={
                "Authorization": "Bearer %s" % constants.todoistKey
            }).json()
        return todoistcall

    def tasksByProject(self):
        #choice = int(input("Please choose a project to get the tasks for: "))-1
        #self.projectid = projects[projectlist[choice]]
        self.tasks = self.getTasks(self.projectid)
        return self.tasks

"""Extract nested values from a JSON tree."""
def json_extract(obj, key):
    """Recursively fetch values from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values

print(json_extract(responsejson, "value"))
print(json_extract(responsejson, "temp_F"))

weatherInfo = {}
for k, v in responsejson.items():
    if k == "current_condition":
        for item in v:
            for v in item:
                if isinstance(v, dict):
                    for k, v in v.items():
                        print(k, v)
                elif isinstance(v, list):
                    for item in v:
                        print(v)
                weatherInfo["time"] = item['observation_time']
                weatherInfo["rain"] = float(item['precipInches'])
                weatherInfo["tempF"] = int(item['temp_F'])

print("Current Temperature is %d" % weatherInfo["tempF"])

    
