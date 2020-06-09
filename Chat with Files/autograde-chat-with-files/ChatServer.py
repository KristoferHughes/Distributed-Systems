import threading
import sys
import os
import socket

def usage(script_name):
    print('Usage: python3 ' + script_name + ' <port number>')

argv = sys.argv
argc = len(sys.argv)
if argc != 2:
    usage(sys.argv[0])
    os.exit(1)

def checkforPort(argv):
    port = ''
    localNum = 'localhost'

    try:
        port = argv[1]
        int(port)
    except (IndexError, ValueError):
        print("Port number does not exist or is not valid")
        sys.exit()

    return (port, localNum)

class Server:
    ClientArray = {}
    TitlesArray = {}
    ListenerServ = None
    ConnectFailed = -1
    ServerMessage = 0
    newSocket = 0
    ClientTitle = 1
    ServerFile = 1
    ClientPort = 2

    def __init__(self, port):
        self.port = port
        self.startListener(self.port)

    def startListener(self, port):
        self.ListenerServ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ListenerServ.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ListenerServ.bind( ('localhost', int(port)) )
        self.ListenerServ.listen(5)

    def incrementClient(self):
        IncrementIng = 0
        try:
            while True:
                sock, addr = self.ListenerServ.accept()
                print("Server: Connection accepted, addr: " + str(addr) + " client number " + str(IncrementIng))        
                instance = threading.Thread(target=self.retrieveMessages, args=(sock, IncrementIng))
                instance.start()
                
                IncrementIng += 1
        finally:
            self.ListenerServ.close()

    def retrieveMessages(self, sock, id):
        StartFileTrans = sock.recv(4).decode()
        print("Server: Client " + str(id) + " sent back listen port " + StartFileTrans + ".")
        try:
            int(StartFileTrans)
        except ValueError:
            print("Server: Port number is not valid.")
            sock.close()
        self.ClientArray[id] = [sock, '', '']
        self.ClientArray[id][self.ClientPort] = StartFileTrans

        print("Server: Thread opened @client " + str(id))
        name  = sock.recv(4096)
        ins = name.decode().split('\n', 1)
        nameofClient = ins[0]
        self.ClientArray[id][self.ClientTitle] = nameofClient
    
        self.TitlesArray[nameofClient] = id
        print('Server: Client@client ' + str(id) + ' entered their name as ' + nameofClient)
        if len(ins) > 1 and ins[1] != '':
            print("Server: ins1: " + str(ins))
            ProcessFileReq = ins[1].encode()
        else:
            ProcessFileReq = sock.recv(4096)
        while ProcessFileReq:
            message = ProcessFileReq.decode()
            messages = message.split(':', 1)
            code = Server.checkRequest(messages[0])
            if code == Server.ConnectFailed:
                continue
            if code == Server.ServerMessage:
                print("Server: " + self.ClientArray[id][self.ClientTitle] + ': ' + messages[1], end='')
                self.showMessage(id, messages[1])
            if code == Server.ServerFile:
                rq = messages[1].split(':', 1)
                owner = rq[0]
                file_name = rq[1]
                print('Server: ' + self.ClientArray[id][self.ClientTitle] \
                    + ' requests to get file ' + file_name + ' from ' + owner )
                instance = threading.Thread(target=self.initiateFileChange, args=(sock, id, owner, file_name))
                instance.start()
            ProcessFileReq = sock.recv(4096)
        sock.close()
        self.ClientArray.pop(id)
        print('Server: ' +  nameofClient + ' disconnected and the socket was successfully closed.')
        
    def checkRequest(code):
        if code == 'm':
            return Server.ServerMessage
        if code == 'f':
            return Server.ServerFile
        else:
            return Server.ConnectFailed

    def initiateFileChange(self, sock, origNum, owner, file_name): #strongly encouraged to create a separate socket connection for transferring files
        destinationPortNum = self.ClientArray[origNum][self.ClientPort]
        fileNumber = self.TitlesArray[owner]
        port = self.ClientArray[fileNumber][self.ClientPort]
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('localhost', int(destinationPortNum)))
            msg = str(port) + ':' + file_name
            sock.send (msg.encode())
            sock.close()
        except:
            print('Server: could not send port + filename')


    def showMessage(self, clientNumber, message):
        transferredMessage = self.ClientArray[clientNumber][self.ClientTitle] + ': ' + message
        for c in self.ClientArray:
            if c != clientNumber:
                sock = self.ClientArray[c][self.newSocket]
                initateMessSend = threading.Thread(target=self.sendMessage, args=(sock, c, clientNumber, transferredMessage))
                initateMessSend.start()

    def sendMessage(self, sock, firstPort, secondPort, message):
        try:
            sock.send(message.encode())
        except:
            receivingClient = self.ClientArray[firstPort][ClientTitle]
            sendingClient = self.ClientArray[secondPort][ClientTitle]
            print('Server: Sending message to ' + receivingClient + ' from ' + sendingClient + ' failed.')


def main():
    port, localNum = checkforPort(argv)
    s = Server(port)
    s.incrementClient()

main()
