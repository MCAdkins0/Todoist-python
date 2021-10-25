import sqlite3
from sqlite3 import Error

class db:
    def __init__(self, database):
        try:
            self.db = sqlite3.connect(database)
            print("Connected to Database")
            self.cursor = self.db.cursor()
        except Error:
            print(Error)

    def setUpDB(self):
        self.db.execute('''CREATE TABLE IF NOT EXISTS PROJECTS
            (PROJECTID INT PRIMARY KEY  NOT NULL,
            NAME        TEXT            NOT NULL,
            COLOR       TEXT,
            PARENTID    INT,
            FOREIGN KEY (PARENTID) REFERENCES PROJECTS(PROJECTID) 
            );''')
        self.db.execute('''CREATE TABLE IF NOT EXISTS TASKS
            (TASKID INT PRIMARY KEY  NOT NULL,
            NAME        TEXT            NOT NULL,
            PARENTID    INT,
            CHECKED       INT           NOT NULL,
            DATEADDED   TEXT            NOT NULL,
            DUEDATE     TEXT,
            DATECOMPLETED TEXT,
            LABELS      TEXT,
            SECTION     INT,
            RECURRING   INT,
            PROJECTID   INT             NOT NULL,
            FOREIGN KEY (PROJECTID) REFERENCES PROJECTS(PROJECTID),
            FOREIGN KEY (PARENTID) REFERENCES TASKS(TASKID)
            );''')

    def insertProject(self, project):
        #Inserts project details into the Projects table
        self.cursor.execute("SELECT EXISTS(SELECT 1 FROM PROJECTS WHERE PROJECTID=:id)", {'id':project['id']})
        exists = self.cursor.fetchone()[0]
        if exists: 
            self.cursor.execute("UPDATE PROJECTS SET NAME=:name, COLOR=:color, PARENTID=:parent WHERE PROJECTID=:id",{'id': project['id'], 'name': project['name'], 'parent': project['parent_id'], 'color': project['color']})
            result = ' updated'
        else:
            self.cursor.execute("INSERT INTO PROJECTS VALUES (:id,:name,:color,:parent)", {'id': project['id'], 'name':project['name'], 'parent': project['parent_id'], 'color': project['color']})
            result = ' added to database'
        self.db.commit()
        print('Project '+project['name']+result)
    
    def insertTask(self, task):
        #Inserts task details into the Tasks table
        self.cursor.execute("INSERT OR IGNORE INTO TASKS VALUES (:id,:name,:parent,:checked,:date_added,:due,:datecompleted,:labels,:section,:recurring,:projectid)", {'id': task['id'], 'name':task['name'], 'parent': task['parent_id'], 'color': task['color'], })
        self.db.commit()
        print('Project '+task['name']+' added to database')

    def  queryProject(self, value):
        self.cursor.execute("SELECT * FROM PROJECTS WHERE NAME=:value",{'value':value})
        result = self.cursor.fetchone()
        return result

    def queryAllProjects(self):
        self.cursor.execute("SELECT * FROM PROJECTS")
        result = self.cursor.fetchall()
        return result

    def queryTask(self, value):
        self.cursor.execute("SELECT * FROM TASKS WHERE NAME=:value",{'value':value})
        result = self.cursor.fetchone()
        return result

    def addTasktoDB(self, project, task):
        self.cursor.execute("INSERT OR IGNORE INTO TASKS VALUES (:id,:name,:parent,:color)", {'id': project['id'], 'name':project['name'], 'parent': project['parent_id'], 'color': project['color']})

    def closeConnection(self):
        self.db.close()
        print('Connection to Database closed')

testProject = {
    'id' : 1234567,
    'name' : 'Test Project',
    'color' : 45,
    'parent_id' : None
    }

"""testdb= db(':memory:')

testdb.setUpDB()
testdb.insertProject(testProject)
print(testdb.queryProject('Test Project'))
#testdb.cursor.execute("SELECT * FROM PROJECTS")
#print(testdb.cursor.fetchall())
testdb.closeConnection() """



