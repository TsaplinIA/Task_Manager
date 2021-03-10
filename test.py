from enum import Enum, auto
import Task
import TaskList
from datetime import datetime
import Status


st = Status.Status.created
st2 = Status.Status(0)
print(st2.name)
db = TaskList.TaskList()
db.addTask("hi", datetime.today(), datetime.today(), "123")
db.addTask("hello", datetime.today(), datetime.today(), "123")
db.addTask("hi2", datetime.today(), datetime.today(), "123")
db.printList()
id = int(input())
db.deleteTask(id)
db.printList()
print("OK")
