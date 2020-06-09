#! python3

'''
Automated testing
Assignment: Args and Input
Test 1 for Java code

Tests included:
Does the program start? If not, perhaps the name is wrong?
Is output written immediately?
Does the program end when stdin ends?
Does the program write the correct output?
'''

import os, sys, time, subprocess
from within_file import WithinFile
from file_compare import FileCompare
withinFile= WithinFile()
compare= FileCompare()

shell_command= 'rm output.txt'
os.system( shell_command )

program_name = 'InputProgram'

#check whether the file is named correctly
try:
	file_stat= os.stat( program_name + '.class' )
except FileNotFoundError:
	print( program_name + '.class does not exist; the name of your program must match exactly' )
	sys.exit()
if file_stat.st_size == 0:
	print( 'Your program, ' + program_name + '.class, is an empty file' )
	sys.exit()

# create the input for the pipe
args= ['py','-u','input-writer.py','2', '1', 'input1.txt']
input_writer= subprocess.Popen( args, stdout=subprocess.PIPE)

# start the program
args= ['java', program_name]
output_text= open( 'output.txt', 'w' )
input_program= subprocess.Popen( args, stdin= input_writer.stdout, stdout=output_text)

# check whether output was written immediately
time.sleep( 3 )
found= withinFile.searchText( 'input1.txt', 'output.txt' )
if not found:
	print( 'output must be written immediately; your program must be revised' )
	sys.exit()

# wait until the input pipe closes; then, check whether the process terminated
try:
	input_program.wait( 2 )
	if input_program.returncode != 0:
		print( program_name + ' returned: ' + str(input_program.returncode) + '; your program must be revised' )
		sys.exit()
except subprocess.TimeoutExpired:
	print( program_name + ' has not exited within the expected timeframe; your program must be revised' )
	input_program.kill() # terminate process
	sys.exit()

# check output
differ= compare.textFiles( 'output.txt', 'ref1.txt', True )
if differ:
	print( 'Output of your program does not match expected output; your program must be revised. Pay close attention to detail, including the case (upper/lower) of text.' )
	sys.exit()

print( 'test1 terminated properly' )
