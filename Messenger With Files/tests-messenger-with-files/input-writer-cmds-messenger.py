# open a file
# read all the lines
# output each command and its data to standard input
# pace the timing of output

import sys
import time

argc= len( sys.argv )
if argc != 5 :
	print( 'Usage: py ' + sys.argv[0] + ' <initial delay> <pace> <wait to exit> <input file>' )
	sys.exit()
		
initial_delay= int(sys.argv[1])
pace= int(sys.argv[2])
wait_to_exit= int(sys.argv[3])
input_file= open( sys.argv[4] )
lines= input_file.readlines()
input_file.close()
number_of_lines= len(lines)

# delay before outputting any data?
if initial_delay:
	time.sleep( initial_delay )
	
i= 0
while i < number_of_lines:
	try:
		command= lines[i]
		if command[0] == 'f': # print the command and the next line
			print( command, end= '' )
			print( lines[i+1], end= '' )
			i+= 2
		elif command[0] == 'm': # print the command and the next line
			print( command, end= '' )
			print( lines[i+1], end= '' )
			i+= 2
		else: # 'x' encountered; exit the loop
			break
		sys.stdout.flush()
	except BrokenPipeError: # process receiving input ended
		sys.exit()
	if pace:
		time.sleep( pace )	
		
if wait_to_exit:
	time.sleep( wait_to_exit )
try:
	print( 'x' )
	sys.stdout.flush()
except BrokenPipeError: # process receiving input ended
	pass
sys.stderr.close() # eliminate message at end
