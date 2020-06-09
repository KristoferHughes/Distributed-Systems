# open a file
# read each line
# output the line to standard input
# pace the timing of output
# NOTE: DO NOT CATCH THE BROKEN PIPE EXCEPTION; DISPLAY FOR USER. This
#  exception will occur only if the input program inappropriately
#  terminates stdin before the input-writer program closes.

import sys
import time

argc= len( sys.argv )
if argc != 4 :
	print( 'Usage: py ' + sys.argv[0] + ' <initial delay> <pace> <input file>' )
	sys.exit()
		
initial_delay= int(sys.argv[1])
pace= int(sys.argv[2])
input_file= open( sys.argv[3] )
if initial_delay:
	time.sleep( initial_delay )
for line in input_file:
	print( line, end= '' )
	sys.stdout.flush()
	if pace:
		time.sleep( pace )
if pace:
	time.sleep( pace )
