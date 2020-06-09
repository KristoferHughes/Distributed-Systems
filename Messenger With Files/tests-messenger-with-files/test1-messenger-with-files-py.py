#! python3

'''
Automated testing
Assignment: Messenger with file transfers
Test 1 for Python code

Tests included:
Does the program start? If not, perhaps the name is wrong?
Is a file transferred immediately?
Does the program end when stdin ends?
Does the program transfer the file correctly?
'''

import os, sys, time, subprocess
from within_file import WithinFile
from file_compare import FileCompare
withinFile= WithinFile()
compare= FileCompare()
cur_dir=os.getcwd()

shell_command= 'rm client/Ameca_splendens.jpg'
os.system( shell_command )
shell_command= 'rm server/one-liners.txt'
os.system( shell_command )

program_name = 'messenger_with_files.py'
transfer_points= 0

#check whether the file is named correctly
try:
	file_stat= os.stat( program_name )
except FileNotFoundError:
	print( program_name + ' does not exist; the name of your program must match exactly' )
	sys.exit()
if file_stat.st_size == 0:
	print( 'Your program, ' + program_name + ', is an empty file' )
	sys.exit()

# Transfer file from server to client
#print( 'Transferring file from server to client...' )

# create blank input for the pipe to the server
args= ['py','-u','input-writer-cmds-messenger.py','7', '0', '0', 'server/blank.txt']
server_input_writer= subprocess.Popen( args, stdout=subprocess.PIPE)

# start the program as a server
args= ['py','-u', '../' + program_name, '-l', '6001' ]
server_output_text= open( 'server/server-recvd.txt', 'w' )
server_messenger= subprocess.Popen( args, stdin= server_input_writer.stdout, stdout=server_output_text, cwd= cur_dir + '/server')

time.sleep( 1 )

# create the input for the pipe to the client
args= ['py','-u','input-writer-cmds-messenger.py','1', '0', '6', 'client/client-file.txt']
client_input_writer= subprocess.Popen( args, stdout=subprocess.PIPE)

# start the program as a client
args= ['py','-u', '../' + program_name, '-l', '6002', '-p', '6001' ]
client_output_text= open( 'client/client-recvd.txt', 'w' )
client_messenger= subprocess.Popen( args, stdin= client_input_writer.stdout, stdout=client_output_text, cwd= cur_dir + '/client')

# check whether file was transferred immediately from server to client
time.sleep( 4 )
differ= compare.binFiles( 'client/Ameca_splendens.jpg', 'server/Ameca_splendens.jpg' )
if differ:
	print( 'The file Ameca_splendens.jpg was not transferred properly; your program must be revised. Pay close attention to detail.' )
	#server_messenger.kill()
	#client_messenger.kill()
	#sys.exit()
else:
	transfer_points= 1

# wait until the server input pipe closes; then, check whether the server process terminated
try:
	server_messenger.wait( 5 )
	if server_messenger.returncode != 0:
		print( 'server ' + program_name + ' returned: ' + str(server_messenger.returncode) + '; your program must be revised' )
		client_messenger.kill()
		sys.exit()
except subprocess.TimeoutExpired:
	print( 'server ' + program_name + ' has not exited within the expected timeframe; your program must be revised' )
	server_messenger.kill()
	client_messenger.kill()
	sys.exit()

# wait until the client input pipe closes; then, check whether the client process terminated
try:
	client_messenger.wait( 0 )
	if client_messenger.returncode != 0:
		print( 'client ' + program_name + ' returned: ' + str(client_messenger.returncode) + '; your program must be revised' )
		sys.exit()
except subprocess.TimeoutExpired:
	print( 'client ' + program_name + ' has not exited within the expected timeframe; your program must be revised' )
	client_messenger.kill()
	sys.exit()

# Transfer file from client to server
#print( 'Transferring file from client to server...' )

# create the input for the pipe to the server
args= ['py','-u','input-writer-cmds-messenger.py','1', '0', '6', 'server/server-file.txt']
server_input_writer= subprocess.Popen( args, stdout=subprocess.PIPE)

# start the program as a server
args= ['py','-u', '../' + program_name, '-l', '6001' ]
server_output_text= open( 'server/server-recvd.txt', 'w' )
server_messenger= subprocess.Popen( args, stdin= server_input_writer.stdout, stdout=server_output_text, cwd= cur_dir + '/server')

time.sleep( 1 )

# create blank input for the pipe to the client
args= ['py','-u','input-writer-cmds-messenger.py','7', '0', '0', 'client/blank.txt']
client_input_writer= subprocess.Popen( args, stdout=subprocess.PIPE)

# start the program as a client
args= ['py','-u', '../' + program_name, '-l', '6002', '-p', '6001' ]
client_output_text= open( 'client/client-recvd.txt', 'w' )
client_messenger= subprocess.Popen( args, stdin= client_input_writer.stdout, stdout=client_output_text, cwd= cur_dir + '/client')

# check whether file was transferred immediately from client to server
time.sleep( 4 )
differ= compare.binFiles( 'server/one-liners.txt', 'client/one-liners.txt' )
if differ:
	print( 'The file one-liners.txt was not transferred properly; your program must be revised. Pay close attention to detail.' )
	#server_messenger.kill()
	#client_messenger.kill()
	#sys.exit()
else:
	transfer_points+= 1

# wait until the client input pipe closes; then, check whether the client process terminated
try:
	client_messenger.wait( 4 )
	if client_messenger.returncode != 0:
		print( 'client ' + program_name + ' returned: ' + str(client_messenger.returncode) + '; your program must be revised' )
		server_messenger.kill()
		sys.exit()
except subprocess.TimeoutExpired:
	print( 'client ' + program_name + ' has not exited within the expected timeframe; your program must be revised' )
	client_messenger.kill()
	server_messenger.kill()
	sys.exit()

# wait until the server input pipe closes; then, check whether the server process terminated
try:
	server_messenger.wait( 0 )
	if server_messenger.returncode != 0:
		print( 'server ' + program_name + ' returned: ' + str(server_messenger.returncode) + '; your program must be revised' )
		sys.exit()
except subprocess.TimeoutExpired:
	print( 'server ' + program_name + ' has not exited within the expected timeframe; your program must be revised' )
	server_messenger.kill()
	sys.exit()

if transfer_points:
	print( 'test1 terminated properly' )
