import threading
import socket
from datetime import datetime
import Status
import time


class TMThread(threading.Thread):
    def __init__(self, sock, TList):
        threading.Thread.__init__(self)
        self.sock = sock
        # self.sock.settimeout(1.5)
        self.list = TList
        # self.list.addTask("hi", datetime.today(), datetime.today(), "123")  # for Tests
        # self.list.addTask("hello", datetime.today(), datetime.today(), "Privet")#for Tests
        # self.list.addTask("hi2", datetime.today(), datetime.today(), "456")#for Tests
        self.stop_event = threading.Event()

    def sendMessage(self, msg):
        try:
            self.sock.send(msg.encode('utf-8'))
        except socket.error:
            self.stop_event.set()

    def receiveMessage(self):
        try:
            return str(self.sock.recv(40).decode('utf-8'))
        except socket.error:
            print("Disconnected")
            exit(0)

    def run(self):
        selectedTask = 0
        while True:
            time.sleep(1)
            if self.stop_event.is_set(): break
            # print("NewWhile")
            if selectedTask == 0:
                # print("send0")
                self.sendMessage("0")
            else:
                # print("send1")
                self.sendMessage("1")

            try:
                parts = str(self.sock.recv(40).decode('utf-8')).split()
                if len(parts) == 0:  # client is dead
                    self.stop_event.set()
                    continue
            except socket.timeout:
                continue

            if parts[0] == "exit":
                break

            # print("1) printTaskList")
            # print("2) info <id>")
            # print("3) select <id>")
            # print("4) addNewTask")
            # print("5) delete <id>")
            if selectedTask == 0:
                if parts[0] == "printTaskList":
                    res = self.list.printList()
                    self.sendMessage(res)
                if parts[0] == "info":
                    res = self.list.printTask(int(parts[1]))
                    self.sendMessage(res)
                if parts[0] == "select":
                    res = self.list.selectTask(int(parts[1]))
                    if res == 0:
                        self.sendMessage("Task not found")
                    else:
                        self.sendMessage("Task selected")
                        selectedTask = res
                if parts[0] == "delete":
                    res = self.list.deleteTask(int(parts[1]))
                    if res:
                        self.sendMessage("Task deleted")
                    else:
                        self.sendMessage("Task not found")
                if parts[0] == "addNewTask":
                    name = self.receiveMessage()

                    isOk = False
                    start_time = datetime.today()
                    while not isOk:
                        try:
                            tmp_time = datetime.strptime(self.receiveMessage(), "%d/%m/%y %H:%M")
                            self.sendMessage("True")
                            start_time = tmp_time
                            isOk = True
                        except ValueError:
                            self.sendMessage("False")

                    isOk = False
                    end_time = datetime.today()
                    while not isOk:
                        try:
                            tmp_time = datetime.strptime(self.receiveMessage(), "%d/%m/%y %H:%M")
                            self.sendMessage("True")
                            end_time = tmp_time
                            isOk = True
                        except ValueError:
                            self.sendMessage("False")

                    # start_time = datetime.strptime(self.receiveMessage(), "%d/%m/%y %H:%M")
                    # end_time = datetime.strptime(self.receiveMessage(), "%d/%m/%y %H:%M")
                    description = self.receiveMessage()
                    res = self.list.addTask(name, start_time, end_time, description)
                    self.sendMessage(res)
            else:
                # print("1) changeDescription")
                # print("2) changeStatus")
                # print("3) changeStartTime")
                # print("4) changeEndTime")
                # 5unselected
                if parts[0] == "changeDescription":
                    des = self.receiveMessage()
                    res = self.list.chDescription(des, selectedTask)
                    if res:
                        self.sendMessage("Description changed")
                    else:
                        self.sendMessage("Task not found")
                if parts[0] == "changeStatus":
                    status = int(self.receiveMessage())
                    st_ = Status.Status(status)
                    res = self.list.chStatus(st_, selectedTask)
                    if res:
                        self.sendMessage("Status changed")
                    else:
                        self.sendMessage("Task not found")
                if parts[0] == "changeStartTime":
                    date = self.receiveMessage()
                    res = self.list.chTime(date, True, selectedTask)
                    if res:
                        self.sendMessage("Start Time changed")
                    else:
                        self.sendMessage("Task not found")
                if parts[0] == "changeEndTime":
                    date = self.receiveMessage()
                    res = self.list.chTime(date, False, selectedTask)
                    if res:
                        self.sendMessage("End Time changed")
                    else:
                        self.sendMessage("Task not found")
                if parts[0] == "unselect":
                    selectedTask = 0

        self.sock.close()
