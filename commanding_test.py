# CACTUS I - basic commanding TEST
# Periodically populates command_queue.txt with sample commands
# to be executed by the flight core


# MODES OF OPERATION (command line args):
#	default (no args or invalid args): user input
#		Accept commands directly from user, sends 5 at a time unless user
#		manually sends queue
#
#	-r : random commands
#		Generates 10 random commands every 10 seconds and sends them automatically

import random,time,sys

with open('valid_commands.txt') as fi:
	valid_commands = fi.readlines()
	valid_commands = [x.strip() for x in valid_commands]

#select mode based on command line arguments
if len(sys.argv)>1:
	if sys.argv[1]=='-r':
		mode = 'r'
	else:
		mode = 'c'
else:
	mode = 'c'
		
if mode=='r':
	while 1:
		# open command_queue\
		fi = open('command_queue.txt', "a")
		for i in range(0,10):
			# random number between 0 and valid.size to select command
			cmd_index = random.randint(0,len(valid_commands)-1)
			# random number between 0 and 1000 to select parameter
			param = random.randint(0,1000)
			# concatenate some special characters and shit to beginning and end of command
			command = "413#$%Gsff"+valid_commands[cmd_index]+" "+str(param)+"@$%sdfere4\n"
			# append the command to end of the file
			print command
			fi.write(command)
		# close file
		fi.close()	
		# pause for 10 seconds
		time.sleep(10)
elif mode=='c':
	while 1:
		quit=False
		#get input from user
		cmd=[]
		for i in range(0,5):
			cmd.append(raw_input("Enter Command "+str(i)+" (q=quit, e=excecute queue): "))
			if (cmd[i]=='q'):
				quit = True
				break
			elif (cmd[i]=='e'):
				del cmd[i]
				break
		if(quit):
			break
		#append input to file
		with open('command_queue.txt','a') as fi:
			for i in range(0,len(cmd)):
				fi.write(cmd[i]+"\n")
			print str(len(cmd))+" commands sent"