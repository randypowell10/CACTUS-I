# Cactus-I Flight Software Master Control Program
# v1.1
# Author: Randy Powell
# Organization: Capitol Technology University

import commands, routines, time, os, re
# Initialize stuff

#   comm turn-on commands via Mark/Alec
#   make sure Comm is in 'receive' mode  run RX.py script
####YOU CANNOT RUN A SCRIPT MULTIPLE TIMES USING IMPORT####
	
	#import RX
	
#   any TrapSat camera initialization 
#   if any power inits, here
#   if any sensors board inits, here


mode_sleep = 0  # 0 = off, 1 = loop periodically pauses itself
sleeptime = 0   # duration of how long it sleeps



last_camera_timestamp = 0
camera_cadence = 600 # take a pic every 10 minutes

last_sensors_timestamp = 0
sensors_cadence = 120 # take an HK reading every 2 seconds

#Create array of valid commands
with open('valid_commands.txt') as fi:
	valid_commands = fi.readlines()
	valid_commands = [x.strip() for x in valid_commands]

# program eternally loops-- have a cron job monitor in case of crashes
while 1:
	# get current time
	current_timestamp = time.time()

	# CHECK FOR INCOMING COMMANDS
	# first check if a transmission is incoming, probably file-based (check if external poller wrote a 'commands_queue.txt' file)
	incoming = routines.checkRX()  # some sort of routine that looks to see if any un-executed commands have been received
	if incoming['true']:
		FINAL_SHUTDOWN_COUNT=0
		BURN_COUNT=0
		for command in incoming['queue']:
			print command
			bad_command_flag=1
			# code to read what the transmitter received,
			# check if it's a valid command or mnemonic,
			# then carry out its function
			###command = commands.lookup_mnemonic(command)  # decrypts, checksums, authenticate that it's a valid command
		
			#loop through valid commands and check against current command in queue
			for valid in valid_commands:
				if valid in command:
					bad_command_flag=0
					print valid
					#Check for numeric parameter
					match = re.search(valid + r" \d+",command)
					if match:
						param = int(match.group().split()[1])
					else:
						param = 0
					command = valid
					
					if command == 'FAA_SHUTDOWN_FOREVER':
						FINAL_SHUTDOWN_COUNT += 1
						if FINAL_SHUTDOWN_COUNT==3:
							commands.FAA_SHUTDOWN_FOREVER(param)
					elif command == 'START_WIRE_BURN':
						BURN_COUNT += 1
						if BURN_COUNT == 2:
							commands.START_WIRE_BURN(param)
					else:
						BURN_COUNT=0
						FINAL_SHUTDOWN_COUNT = 0
						try:
							result = getattr(commands,command)(param)
						except:
							routines.log_bad_command(command,current_timestamp)
					break
				
			if bad_command_flag==1:
				# was a bad command, log that somewhere (for later debugging)
				routines.log_bad_command(command, current_timestamp)
			
			
		routines.empty_queue()
		
		
	# REGULAR TIMED TASKS
	# now, check if we need to do any data-gathering tasks

	if current_timestamp >= last_camera_timestamp + camera_cadence:
		#os.system("Take_Image.py") #Fires off the trapsat camera to take an image. ## FIGURE OUT BETTER WAY TO DO THIS
		
		
		last_camera_timestamp = current_timestamp # and mark it as done
		print 'image taken', current_timestamp
	if current_timestamp >= last_sensors_timestamp + sensors_cadence:
		# fire off the sensor/HK data-gathering scripts
		#import HK_gather
		
		last_sensors_timestamp = current_timestamp # and mark it as done
		print 'sensor data gathered', current_timestamp

	# PRE-SCHEDULED TASKS
	# maybe other 'if' time checking loops?
	
	

	# optional sleep? if it saves power
	if mode_sleep:
		time.sleep(sleeptime)
		
	
	
print ("If you see this, something went wrong and broke our infinite loop")

