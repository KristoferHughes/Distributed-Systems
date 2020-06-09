#! python3

'''
Automated testing
Assignment: Messenger
Test 1 for Java code

Tests included:
Does the program start? If not, perhaps the name is wrong?
Is message transferred immediately?
Does the program end when stdin ends?
Does the program write the correct output?
'''

import os, sys, time, subprocess
from within_file import WithinFile
from file_compare import FileCompare
withinFile= WithinFile()
compare= FileCompare()

shell_command= 'rm server-recvd.txt'
os.system( shell_command )
shell_command= 'rm client-recvd.txt'
os.system( shell_command )

program_name = 'Messenger'

#check whether the file is named correctly
try:
	file_stat= os.stat( program_name + '.class' )
except FileNotFoundError:
	print( program_name + '.class does not exist; the name of your program must match exactly' )
	sys.exit()
if file_stat.st_size == 0:
	print( 'Your program, ' + program_name + '.class, is an empty file' )
	sys.exit()

# create blank input for the pipe to the server
args= ['py','-u','input-writer.py','5', '0', 'blank.txt']
server_input_writer= subprocess.Popen( args, stdout=subprocess.PIPE)

# start the program as a server
args= ['java', program_name, '-l', '6001' ]
server_output_text= open( 'server-recvd.txt', 'w' )
server_messenger= subprocess.Popen( args, stdin= server_input_writer.stdout, stdout=server_output_text)

# create the input for the pipe to the client
args= ['py','-u','input-writer.py','0', '1', 'client-msgs.txt']
client_input_writer= subprocess.Popen( args, stdout=subprocess.PIPE)

# start the program as a client
args= ['java', program_name, '6001' ]
client_output_text= open( 'client-recvd.txt', 'w' )
client_messenger= subprocess.Popen( args, stdin= client_input_writer.stdout, stdout=client_output_text)

# check whether messages were transferred immediately from client to server
time.sleep( 4 )
found= withinFile.searchText( 'client-msgs.txt', 'server-recvd.txt' )
if not found:
	print( 'messages from client to server must be transferred immediately; your program must be revised' )
	server_messenger.kill()
	client_messenger.kill()
	sys.exit()

# wait until the server input pipe closes; then, check whether the server process terminated
try:
	server_messenger.wait( 2 )
	if server_messenger.returncode != 0:
		print( 'server ' + program_name + ' returned: ' + str(server_messenger.returncode) + '; your program must be revised' )
		client_messenger.kill()
		sys.exit()
except subprocess.TimeoutExpired:
	print( 'non-sending server ' + program_name + ' has not exited within the expected timeframe; your program must be revised' )
	server_messenger.kill()
	client_messenger.kill()
	sys.exit()

# wait until the client input pipe closes; then, check whether the client process terminated
try:
	client_messenger.wait( 2 ) #CHANGED FROM 0 TO 2
	if client_messenger.returncode != 0:
		print( 'client ' + program_name + ' returned: ' + str(client_messenger.returncode) + '; your program must be revised' )
		sys.exit()
except subprocess.TimeoutExpired:
	print( 'client sending messages, ' + program_name + ', has not exited within the expected timeframe; your program must be revised' )
	client_messenger.kill()
	sys.exit()

# check output
differ= compare.textFiles( 'client-msgs.txt', 'server-recvd.txt', True )
if differ:
	print( 'Server did not receive messages sent by client as expected; your program must be revised. Pay close attention to detail.' )
	sys.exit()

# create the input for the pipe to the server
args= ['py','-u','input-writer.py','1', '1', 'server-msgs.txt']
server_input_writer= subprocess.Popen( args, stdout=subprocess.PIPE)

# start the program as a server
args= ['java', program_name, '-l', '6001' ]
server_output_text= open( 'server-recvd.txt', 'w' )
server_messenger= subprocess.Popen( args, stdin= server_input_writer.stdout, stdout=server_output_text)

# create blank input for the pipe to the client
args= ['py','-u','input-writer.py','5', '0', 'blank.txt']
client_input_writer= subprocess.Popen( args, stdout=subprocess.PIPE)

# start the program as a client
args= ['java', program_name, '6001' ]
client_output_text= open( 'client-recvd.txt', 'w' )
client_messenger= subprocess.Popen( args, stdin= client_input_writer.stdout, stdout=client_output_text)

# check whether messages were transferred immediately from server to client
time.sleep( 4 )
found= withinFile.searchText( 'server-msgs.txt', 'client-recvd.txt' )
if not found:
	print( 'messages from server to client must be transferred immediately; your program must be revised' )
	server_messenger.kill()
	client_messenger.kill()
	sys.exit()

# wait until the client input pipe closes; then, check whether the client process terminated
try:
	client_messenger.wait( 2 )
	if client_messenger.returncode != 0:
		print( 'client ' + program_name + ' returned: ' + str(client_messenger.returncode) + '; your program must be revised' )
		sys.exit()
except subprocess.TimeoutExpired:
	print( 'non-sending client ' + program_name + ' has not exited within the expected timeframe; your program must be revised' )
	client_messenger.kill()
	server_messenger.kill()
	sys.exit()

# wait until the server input pipe closes; then, check whether the server process terminated
try:
	server_messenger.wait( 2 ) #CHANGED FROM 0 TO 2
	if server_messenger.returncode != 0:
		print( 'server ' + program_name + ' returned: ' + str(server_messenger.returncode) + '; your program must be revised' )
		client_messenger.kill()
		sys.exit()
except subprocess.TimeoutExpired:
	print( 'server sending messages, ' + program_name + ', has not exited within the expected timeframe; your program must be revised' )
	server_messenger.kill()
	sys.exit()

# check output
differ= compare.textFiles( 'server-msgs.txt', 'client-recvd.txt', True )
if differ:
	print( 'client did not receive messages sent by server as expected; your program must be revised. Pay close attention to detail.' )
	sys.exit()

print( 'test1 terminated properly' )

