#! python3

"""
Automated testing
Assignment: Messenger with file transfers
Test 2 for Python code

1. Start the program with server command line args
2. Start the program with client command line args
3. Input data from standard input for the server and the client
4. Redirect standard output to files
5. Compare output files to input files
6. Compare transferred files to original files

14 points total
"""

import os, time, sys
from file_compare import FileCompare
from within_file import WithinFile
points= 0
compare= FileCompare()
withinFile= WithinFile()

shell_command= 'cd server; rm one-liners.txt'
os.system( shell_command )
shell_command= 'cd client; rm Ameca_splendens.jpg'
os.system( shell_command )

print( 'Executing single file transfers between server and client...' )

shell_command= 'cd server; py ../input-writer-cmds-messenger.py 2 0 4 server-file.txt 2>>errors.txt | py -u ../messenger_with_files.py -l 6001 >server-recvd.txt &'
os.system( shell_command )

time.sleep( 1 ) 

shell_command= 'cd client; py ../input-writer-cmds-messenger.py 0 0 6 client-file.txt 2>>errors.txt | py -u ../messenger_with_files.py -l 6002 -p 6001 >client-recvd.txt'
os.system( shell_command )

print( 'execution completed; grading...' )

differ= compare.binFiles( 'client/Ameca_splendens.jpg', 'server/Ameca_splendens.jpg' )
if differ is False: 
	points+= 2

differ= compare.binFiles( 'client/one-liners.txt', 'server/one-liners.txt' )
if differ is False: 
	points+= 2

if points == 0:
	print( 'Points: ' + str(points) + ' (file transfers failed)' );
	sys.exit()
	
shell_command= 'cd server; rm one-liners.txt'
os.system( shell_command )
shell_command= 'cd client; rm Ameca_splendens.jpg'
os.system( shell_command )

print( 'Executing multiple transfers between server and client...' )

shell_command= 'cd server; py ../input-writer-cmds-messenger.py 2 1 2 server-all.txt 2>>errors.txt | py -u ../messenger_with_files.py -l 6001 >server-recvd.txt &'
os.system( shell_command )

time.sleep( 1 ) 

shell_command= 'cd client; py ../input-writer-cmds-messenger.py 0 1 2 client-all.txt 2>>errors.txt | py -u ../messenger_with_files.py -l 6002 -p 6001 >client-recvd.txt'
os.system( shell_command )

time.sleep( 2 ) 

print( 'execution completed; grading...' )

differ= compare.binFiles( 'client/Ameca_splendens.jpg', 'server/Ameca_splendens.jpg' )
if differ is False: 
	points+= 1

differ= compare.binFiles( 'client/one-liners.txt', 'server/one-liners.txt' )
if differ is False: 
	points+= 1

found= withinFile.searchText( 'client/client-recvd-multiple-file-ref.txt', 'client/client-recvd.txt' )
if found:
	points+= 1

found= withinFile.searchText( 'server/server-recvd-multiple-file-ref.txt', 'server/server-recvd.txt' )
if found:
	points+= 1

print( 'Executing server and client with a single message...' )

shell_command= 'cd server; py ../input-writer-cmds-messenger.py 2 1 2 server-msg.txt 2>errors.txt | py -u ../messenger_with_files.py -l 6001 >server-recvd.txt &'
os.system( shell_command )

time.sleep( 1 ) 

shell_command= 'cd client; py ../input-writer-cmds-messenger.py 0 1 2 client-msg.txt 2>errors.txt | py -u ../messenger_with_files.py -l 6002 -p 6001 >client-recvd.txt'
os.system( shell_command )

time.sleep( 2 ) 

print( 'execution completed; grading...' )

found= withinFile.searchText( 'client/client-recvd-single-ref.txt', 'client/client-recvd.txt' )
if found:
	points+= 1
	
found= withinFile.searchText( 'server/server-recvd-single-ref.txt', 'server/server-recvd.txt' )
if found:
	points+= 1

print( 'Executing server and client with multiple messages...' )

shell_command= 'cd server; py ../input-writer-cmds-messenger.py 2 1 2 server-msgs.txt 2>>errors.txt | py -u ../messenger_with_files.py -l 6001 >server-recvd.txt &'
os.system( shell_command )

time.sleep( 1 ) 

shell_command= 'cd client; py ../input-writer-cmds-messenger.py 0 1 2 client-msgs.txt 2>>errors.txt | py -u ../messenger_with_files.py -l 6002 -p 6001 >client-recvd.txt'
os.system( shell_command )

time.sleep( 2 ) 

print( 'execution completed; grading...' )

found= withinFile.searchText( 'client/client-recvd-multiple-ref.txt', 'client/client-recvd.txt' )
if found:
	points+= 2

found= withinFile.searchText( 'server/server-recvd-multiple-ref.txt', 'server/server-recvd.txt' )
if found:
	points+= 2

print( 'Points: ' + str(points) );
