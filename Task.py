import threading
import Status
from datetime import datetime

class Task:
    def __init__(self, data):
        self.task_ID = id(self)
        self.name = str(data.get("task_name"))
        self.status = data.get("status")
        self.start_time = data.get("start_time")
        self.end_time = data.get("end_time")
        self.description = str(data.get("description"))
        self.lock = threading.Lock() # to synchronize threads

    def __str__(self):
        return  str(self.task_ID) + ": " + self.name

    def getData(self):
        return {
            "task_ID" : str(self.task_ID),
            "task_name" : str(self.name),
            "status" : str(self.status),
            "start_time" : str(self.start_time),
            "end_time" : str(self.end_time),
            "description" : str(self.description)
                }

    def setID(self, id):
        self.task_ID = id

    def setStatus(self, status):
        self.status = status

    def setDescription(self, text):
        self.description = text

    def setStartTime(self, time):
        self.start_time = time

    def setEndTime(self, time):
        self.end_time = time

    def setName(self, string):
        self.name = string
