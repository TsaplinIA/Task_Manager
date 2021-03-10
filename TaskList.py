import Task
import threading
import Status
from datetime import datetime


class TaskList:
    def __init__(self):
        self.list = []
        self.lock = threading.Lock()  # to synchronize threads

    def addTask(self, name, time_start, time_end, description):
        self.lock.acquire(1)
        newTask = Task.Task({
            "task_name": name,
            "status": Status.Status.created,
            "start_time": time_start,
            "end_time": time_end,
            "description": description
        })
        self.list.append(newTask)
        self.lock.release()
        return "Task %s added" % newTask.name

    def deleteTask(self, id):
        self.lock.acquire(1)
        for task in self.list:
            if task.task_ID == id:
                #print("Task %s removed" % task.name)
                self.list.remove(task)
                self.lock.release()
                return True
        self.lock.release()
        return False

    def selectTask(self, id):
        self.lock.acquire(1)
        for task in self.list:
            if task.task_ID == id:
                #print("Task %s selected" % task.name)
                self.lock.release()
                return id
        #print("Task not Found")
        self.lock.release()
        return 0

    def chTime(self, time, isStart, id):
        self.lock.acquire(1)
        time_ = datetime.strptime(time, "%d/%m/%y %H:%M")
        for task in self.list:
            if task.task_ID == id:
                if isStart:
                    task.setStartTime(time_)
                    #print("Start Time changed")
                    self.lock.release()
                    return True
                else:
                    task.setEndTime(time_)
                    #print("End Time changed")
                    self.lock.release()
                    return True
        self.lock.release()
        #print("Task not found")
        return False

    def chDescription(self, description, id):
        self.lock.acquire(1)
        for task in self.list:
            if task.task_ID == id:
                task.setDescription(description)
                #print("Description changed")
                self.lock.release()
                return True
        #print("Task not found")
        self.lock.release()
        return False

    def chStatus(self, status, id):
        self.lock.acquire(1)
        for task in self.list:
            if task.task_ID == id:
                task.setStatus(status)
                #print("Status  changed")
                self.lock.release()
                return True
        #print("Task not found")
        self.lock.release()
        return False

    def printList(self):
        self.lock.acquire(1)
        res = ""
        for task in self.list:
            #print("IterFor")
            res += task.__str__() + "\n"
        self.lock.release()
        #print(res)
        return res

    def printTask(self, id):
        self.lock.acquire(1)
        isFound = False
        for task in self.list:
            if task.task_ID == id:
                isFound = True
                res = ""
                res += "ID: %d\n" % task.task_ID
                res += "Name: %s\n" % task.name
                res += "Status: %s\n" % task.status
                res += "Start_time %s\n" % str(task.start_time)
                res += "End_time %s\n" % str(task.end_time)
                res += "Description: %s\n" % task.description
                # print(task.getData())
        if not isFound:
            res = "Task not Found"
        self.lock.release()
        return res
