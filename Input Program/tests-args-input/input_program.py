#Kristofer Hughes
#args and input hw 1
#CSC376
#Professor Karen Heart

import sys #need for command args

print("Standard Input:") #When your program starts, it must output the heading, "Standard Input:"
comparing = sys.stdin.readline()

while comparing:
    print(comparing[:-1]) #need -1 to keep out last character
    comparing = sys.stdin.readline()
    
catchWords = []
catchWords.append("Command line arguments:") #Once all data has been read from standard input and output accordingly, your program will output the heading, "Command line arguments:"

for i in range(len(sys.argv)):
#option1 must be displayed first, if present, then option2, and finally option3
    if sys.argv[i] == '-o':
        catchWords.append("option 1: " + sys.argv[i + 1]) #option1 must be displayed first
        
for i in range(len(sys.argv)):
	if sys.argv[i] == '-t':
            catchWords.append("option 2: " + sys.argv[i + 1]) #then option2

for i in range(len(sys.argv)):
	if sys.argv[i] == '-h':
            catchWords.append("option 3") #finally option3

for i in catchWords:
    print(i)


