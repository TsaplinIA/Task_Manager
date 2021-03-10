import signal
import socket
import re
import time

def sendMessage(msg):
    try:
        client.send(msg.encode('utf-8'))
    except socket.error:
        print("Server disconnected")
        exit(0)


def receiveMessage():
    try:
        return str(client.recv(1024).decode('utf-8'))
    except socket.error:
        print("Server disconnected")
        exit(0)


# actions before ending (on sigint)
def sigint_handler(sig, frame):
    client.send("exit".encode('utf-8'))
    client.close()
    exit(0)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.settimeout(1.5)
try:
    client.connect(("127.0.0.1", 8081))
except socket.error:
    print("Server is unavailable")
    exit(0)

signal.signal(signal.SIGINT, sigint_handler)
print("Ctrl-C to exit")

isCorrect = True
while True:
    #print("NewIterClient")
    if isCorrect:
        state = str(client.recv(1).decode('utf-8'))
        isCorrect = False
    time.sleep(0.5)
    if state == "0":
        print("1) printTaskList")
        print("2) info <id>")
        print("3) select <id>")
        print("4) addNewTask")
        print("5) delete <id>")
        line = input(">>> ")
        if re.fullmatch("addNewTask", line):
            sendMessage(line)
            line = input(">Name:")
            sendMessage(line)

            isOk = False
            while not isOk:
                line = input(">Format: %d/%m/%y %H:%M\n>Time Start:")
                sendMessage(line)
                if receiveMessage() == "True":
                    isOk = True
                else:
                    print("incorrect input, Try again")

            isOk = False
            while not isOk:
                line = input(">Format: %d/%m/%y %H:%M\n>Time End:")
                sendMessage(line)
                if receiveMessage() == "True":
                    isOk = True
                else:
                    print("incorrect input, Try again")

            #line = input(">Format: %d/%m/%y %H:%M\n>Time End:")
            #sendMessage(line)
            line = input(">Description:")
            sendMessage(line)
            print(receiveMessage())
            isCorrect = True

        if re.fullmatch("select [0-9]+|delete [0-9]+|info [0-9]+", line):
            sendMessage(line)
            res = receiveMessage()
            print(res)
            isCorrect = True

        if re.fullmatch("printTaskList", line):
            sendMessage(line)
            res = receiveMessage()
            print("TaskList:")
            print(res)
            print("---------")
            isCorrect = True

        if not isCorrect:
            print("Incorrect input")

    if state == "1":
        print("1) changeDescription")
        print("2) changeStatus")
        print("3) changeStartTime")
        print("4) changeEndTime")
        print("5) unselect")
        line = input(">>> ")
        isCorrect = False
        if re.fullmatch("changeDescription", line):
            sendMessage(line)
            line = input(">Text:")
            sendMessage(line)
            print(receiveMessage())
            isCorrect = True

        if re.fullmatch("changeStatus", line):
            sendMessage(line)
            print("1 = created")
            print("2 = inProcess")
            print("3 = cancelled")
            print("4 = done")
            print("5 = timeIsOver")
            isOk = False
            # line = ""
            while not isOk:
                line = input(">Status:")
                if re.fullmatch("[1-5]", line):
                    isOk = True
                else:
                    print("Incorrect status, try again")
            sendMessage(line)
            print(receiveMessage())
            isCorrect = True

        if re.fullmatch("changeStartTime", line):
            sendMessage(line)
            line = input(">Format: %d/%m/%y %H:%M\n>Time:")
            sendMessage(line)
            print(receiveMessage())
            isCorrect = True

        if re.fullmatch("changeEndTime", line):
            sendMessage(line)
            line = input(">Format: %d/%m/%y %H:%M\n>Time:")
            sendMessage(line)
            print(receiveMessage())
            isCorrect = True

        if re.fullmatch("unselect", line):
            sendMessage(line)
            isCorrect = True

        if not isCorrect:
            print("Incorrect input")
