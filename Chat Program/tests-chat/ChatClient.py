import socket
import sys
import os
import threading

#Kristofer Hughes
#Distributed Systems

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', int(sys.argv[1])))
except:
    os._exit(0)

def sendClient():
    try:
        newMess = sys.stdin.readline().rstrip()
        while newMess:
            sock.send(newMess.encode())
            newMess = sys.stdin.readline().rstrip()          
    except:
        sock.close()
        os._exit(0)

def receiveClient():
    try:
        newMess = sock.recv(1024)
        while newMess:
            if not newMess:
                break
            print(newMess.decode())
            newMess = sock.recv(1024)

    except:
        sock.close()
        os._exit(0)

checkUser = sys.stdin.readline().rstrip() #create name
sock.send(checkUser.encode()) #first message sent by the client must be the name of the user

try:
    sendThread = threading.Thread(target=sendClient) #create send thread
    recThread = threading.Thread(target=receiveClient) #create receive thread
    sendThread.start()
    recThread.start()
    sendThread.join()

except:
    sock.close()
    os._exit(0)

if (not (sendThread.is_alive() and recThread.is_alive())):
    sock.close()
    os._exit(0)
