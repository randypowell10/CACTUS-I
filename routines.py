# Routines module for CACTUS
import time, os

#Checks if any commands have been received
def checkRX():
	if os.stat('command_queue.txt').st_size >0:
		with open('command_queue.txt') as fi:
			commands = fi.readlines()
			commands = [x.strip() for x in commands] 
		return {'true': 1,'queue': commands}
	else:
                return {'true': 0}

#Logs bad commands
def log_bad_command(command, current_timestamp):
	f = open("bad_command_log.txt", "a+")
	f.write("%s\t%s\n" % (command, time.ctime(current_timestamp)))
	
#Empties command queue
def empty_queue():
	f = open("command_queue.txt","w")
	f.close()
	
def junk(par):
	return