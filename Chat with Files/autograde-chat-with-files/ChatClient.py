import sys
import os
import threading
import socket
import struct
import getopt

def usage(script_name):
    print('Argument(s) specified incorrectly.')
    print('Usage: python3 ' + script_name + ' -l <listen port> [-s] [connect server address]\
                -p <connect server port>')

argv = sys.argv
argc = len(sys.argv)
if argc < 2 or argc > 7 :
    usage(sys.argv[0])
    sys.exit(1)

def checkPort(argv, argc):
    checkingNum = ''
    port = ''
    host = 'localhost'
    serverStatus = True

    options, args = getopt.getopt(argv[1:], "l:s:p:")

    for (opt, val) in options:
        if opt == '-l':
            checkingNum = val
            try:
                int(checkingNum)
            except ValueError:
                print("Client: The listening port is not valid.")
                usage(argv[0])

        if opt == '-s':
            host = val
            serverStatus = False
            if host == '':
                print("Client: The host is not valid.")
                usage(argv[0])

        if opt == '-p':
            port = val
            serverStatus = False
            try:
                int(port)
            except ValueError:
                print("The server port is not valid.")
                usage(argv[0])

    if checkingNum == '':
        usage(argv[0])
    if not serverStatus:
        if host == '' or port == '':
            usage(argv[0])

    return [serverStatus, checkingNum, host, port]

class Messenger:

    def __init__(self, port):
        self.lisSock = None
        self.hostServer = None
        self.portofServer = None
        self.msgSock   = None
        self.threadArray = []
        self.port = port


    def startListener(self, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('localhost', int(port)))
            sock.listen(5)
        except:
            self.closeProgram()
        return sock

    def initalizeConnect(self, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, int(port)))
        return sock

    def acceptConnect(self):
        sock, addr = self.lisSock.accept()
        print("Client: Connection accepted, addr: " + str(addr))
        return (sock, addr)

    def startMessage( self ):
        startingMsg = threading.Thread(target=self.retrieveMessages)
        startingMsg.start()
        self.threadArray.append(startingMsg)
        file_server = threading.Thread(target=self.openServer)
        file_server.start()
        self.threadArray.append(file_server)
        self.clientInterface()

    def retrieveMessages(self):
        message = self.msgSock.recv(4096)
        while message:
            print(message.decode(), end='')
            message = self.msgSock.recv(4096)
        self.closeProgram()

    def clientInterface(self):
        print("Enter your name:")
        line = sys.stdin.readline()
        self.moveMesage(line)
        while True:
            print("Enter an option ('m', 'f', 'x'):")
            print("  (M)essage (send)")
            print("  (F)ile (request)")
            print(" e(X)it")
            optionChoice = sys.stdin.readline().rstrip('\n')
            if optionChoice == 'x':
                break
            elif optionChoice == 'm':
                print("Enter your message:")
                line = sys.stdin.readline()
                line = 'm:' + line
                self.moveMesage(line)
            elif optionChoice == 'f':
                print("Who owns the file?")
                owner = sys.stdin.readline().rstrip('\n')
                print("Which file do you want?")
                file_name = sys.stdin.readline().rstrip('\n')
                request = 'f:' + owner + ':' + file_name
                self.moveMesage(request)
        self.closeProgram()

    def moveMesage( self, text ):
        self.msgSock.send( text.encode() )

    def grabFile( self, request, file_name ):
        grabStatus = threading.Thread( target=self.initiateFile, args=(request, file_name) )
        self.threadArray.append(grabStatus)
        grabStatus.start()

    def initiateFile( self, port, file_name ):
        try:
            fileSocket = self.initalizeConnect( 'localhost', port )
            if fileSocket:
                print("fileSocket opened")
            fileSocket.send( file_name.encode() )
            totalFizeSize = fileSocket.recv( 4 )
            if totalFizeSize:
                file_size= struct.unpack( '!L', totalFizeSize[:4] )[0]
                if file_size:
                    Messenger.acceptFile( fileSocket, file_name )
                else:
                    print( 'File does not exist or is empty' )
            else:
                print( 'File does not exist or is empty' )
        except:
            print("Could not open connection to file server.")
        finally:
            if fileSocket:
                fileSocket.close()

    def acceptFile(sock, filename):
        file= open( filename, 'wb' )
        while True:
            file_bytes= sock.recv(1024)
            if file_bytes:
                file.write(file_bytes)
            else:
                break
        file.close()

    def openServer(self):
        print("Opening file server...")
        while True:
            sock, addr = self.acceptConnect()
            file_server = threading.Thread( target=self.checkRequest, args=(sock,) )
            file_server.start()
            self.threadArray.append(file_server)

    def checkRequest(self, sock):
        msgRequested= sock.recv(1024)
        msgDecode = msgRequested.decode()
        msgSplit = msgDecode.split(':',1)
        if len(msgSplit) > 1:
            port = msgSplit[0]
            file_name = msgSplit[1]
            self.initiateFile( port, file_name )
        else:
            file_name = msgSplit[0]
            Messenger.fileMoveRequest( sock, file_name )

    def fileMoveRequest(sock, file_name):
        print("Received file name: {}".format(file_name))
        try:
            file_stat= os.stat(file_name)
            if file_stat.st_size:
                print("Found file {}".format(file_name))
                file= open( file_name, 'rb' )
                Messenger.finishFile( sock, file_stat.st_size, file )
            else:
                print("File not found: {}".format(file_name))
                Messenger.emptyFile(sock)
        except OSError:
            Messenger.emptyFile(sock)
        finally:
            sock.close()

    def finishFile(sock, file_size, file):
        print( 'File size is ' + str(file_size) )
        totalFizeSize= struct.pack( '!L', file_size )
        sock.send( totalFizeSize )
        while True:
            file_bytes= file.read( 1024 )
            if file_bytes:
                sock.send( file_bytes )
            else:
                break
        file.close()

    def emptyFile(sock):
        zero_bytes= struct.pack( '!L', 0 )
        sock.send( zero_bytes )

    def closeProgram(self):
        self.msgSock.close()
        self.lisSock.close()
        os._exit(0)

class Server(Messenger):
    def __init__(self, checkingNum):
        super().__init__(checkingNum)
        self.lisSock = self.startListener(self.port)
        self.msgSock, addr = self.acceptConnect()
        self.hostServer = addr[0]
        messengerPort = self.msgSock.recv( 4 ).decode()
        print("Client: Client sent back listen port " + messengerPort + ".")
        try:
            int(messengerPort)
        except ValueError:
            print("Client: Client's port number is not valid.")
            sys.exit(1)
        self.portofServer = messengerPort


class Client( Messenger ):
    def __init__( self, checkingNum, host, port ):
        super().__init__( checkingNum )
        self.hostServer = host
        self.portofServer = port
        self.msgSock = self.initalizeConnect( self.hostServer, self.portofServer )
        if self.msgSock is None:
            print("Could not open socket.")
            sys.exit(1)
        print("Connection accepted.  Sending listen port " + checkingNum + ".")
        self.msgSock.send( checkingNum.encode() )
        self.lisSock = self.startListener( checkingNum )


def main():
    finalCheck = checkPort(argv, len(argv))
    if finalCheck[0]:
        m = Server(finalCheck[1])
    else:
        m = Client(finalCheck[1], finalCheck[2], finalCheck[3])

    m.startMessage()

main()
