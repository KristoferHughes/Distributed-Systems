import socket
import sys
import os
import threading

#Kristofer Hughes
#Distributed Systems

servArray = []

def checkErr(file):
    print("Usage: " + file + " <port number>")
    sys.exit()

def messAge(first, second, name):
    try:
        messageCatch = first.recv(1024)
        while messageCatch:
            for itemS in servArray:
                if itemS != first: #DO NOT SEND THE MESSAGE BACK TO THE ORIGINATING CLIENT!
                    messageCompose = (name + ": ").encode() + messageCatch
                    itemS.send(messageCompose)
            messageCatch = first.recv(1024)

        print(str(second[0]) + ": " + str(second[1]), "Disconnected") #when user disconnects
        servArray.remove(first)
        first.close()
        sys.exit()

    except:
        first.close()
        sys.exit()

argc = len(sys.argv)

if argc != 2:
    checkErr(sys.argv[0])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', int(sys.argv[1])))
sock.listen(50)

try:
    while True:
        first, second = sock.accept()
        name = first.recv(1024).decode()
        name = name.rstrip()
        if name:
            finalThread = threading.Thread(target=messAge, args=(first,second,name))
            finalThread.start()
            servArray.append(first)
            print(name, "connected.")
        else:
            os._exit(0)

except:
    sock.close()
    os._exit(0)

sock.close()
os._exit(0)
