import signal
import TaskList
import socket
import TMThread


# actions before ending (on sigint)
def sigint_handler(sig, frame):
    for thread in threads:
        thread.stop_event.set()
        thread.join()
    server.close()
    exit(0)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 8081))
server.listen(5)

TList = TaskList.TaskList()

signal.signal(signal.SIGINT, sigint_handler)
print("Ctrl-C to exit")

threads = []
while True:
    sock, _ = server.accept()
    threads.append(TMThread.TMThread(sock, TList))
    threads[-1].start()  # start new thread for new client