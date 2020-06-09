import sys
import socket
import threading
import getopt
import os

#Kristofer Hughes
#Messenger with Files assignment

def clientorServ():
    print("Usage:")
    print(' Server: py messenger_with_files.py -l <listening port number>')
    print(' Client: py messenger_with_files.py -l <listening port number> -p <connect server port> [-s] [connect server address]')

def transferA(fsock, file_name):
    file = open(file_name, 'rb')
    readingFile = file.read(1024)
    while readingFile:
        fsock.send(readingFile)
        readingFile = file.read(1024)
    file.close()

def transferB(fsock, file_name):
    file = open(file_name, 'wb')
    readingFile = fsock.recv(1024)
    while readingFile:
        file.write(readingFile)
        file.flush()
        readingFile = fsock.recv(1024)
    file.close()

def incomingTransfer():
    while True:
        messRec = sock.recv(1024)
        if not messRec:
            sock.shutdown(socket.SHUT_WR)
            fsock.shutdown(socket.SHUT_WR)
            sock.close()
            fsock.close()
            os._exit(0)
        print(messRec.decode(), end='')

        file_name = messRec.decode().rstrip('\n')
        transferDesc = os.path.exists(file_name)
        if transferDesc:
            transferA(fsock, file_name)

if __name__ == '__main__':
    try:
        options, args = getopt.getopt(sys.argv[1:], 'l:p:s')
    except:
        clientorServ()
        sys.exit(1)
        
    checkOption = dict(options)

    if len(options) == 1:
        newSock = socket.socket()
        newSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        newSock.bind(('localhost', int(checkOption['-l'])))
        newSock.listen(5)
        sock,addr = newSock.accept()
        
        secondSock = socket.socket()
        secondSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        secondSock.bind(('localhost', int(checkOption['-l']) + 1))
        secondSock.listen(5)
        fsock,addr = secondSock.accept()

    elif len(options) > 1:
        checkPort = int(checkOption['-p'])
        server_address = checkOption['-s'] if '-s' in checkOption else 'localhost'

        sock = socket.socket()
        sock.connect((server_address, checkPort))

        fsock = socket.socket()
        fsock.connect((server_address, int(checkOption['-p']) + 1))
    else:
        clientorServ()
        sys.exit(1)

    threading.Thread(target = incomingTransfer).start()

    while True:
        print('Enter an option (\'m\', \'f\', \'x\'):\n (M)essage (send)\n (F)file (request)\n e(X)it')
        option_choice = input()

        if option_choice == 'm':
            print('Enter your message: ')
            optionMessage = sys.stdin.readline()
            sock.send(optionMessage.encode())
            
        elif option_choice == 'f':
            print('Which file do you want?')
            file_name = sys.stdin.readline()
            sock.send(file_name.encode())
            threading.Thread(target = transferB, args = (fsock, file_name.rstrip('\n'))).start()

        elif option_choice == 'x':
            print('closing your sockets... goodbye')
            sock.shutdown(socket.SHUT_WR)
            fsock.shutdown(socket.SHUT_WR)
            sock.close()
            fsock.close()
            os._exit(0)
        
