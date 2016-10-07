import configparser
import string
import threading
import serial
import time

# Get current configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Check which port to use and open serial connection
s = 0
if (config['Serial'].getboolean('useDevGlove')):
	s = serial.Serial(port=config['Serial']['devPort'], baudrate=9600)
else:
	s = serial.Serial(port=config['Serial']['livePort'], baudrate=9600)


# Say how the data should be formatted
print("The format for the data is \"motor,intensity,duration\"."
	  "\nThe ranges are 0-5,0-100,0-100.\n")

# Read incoming serial data
def readSerial(e):
	# Run forever
	while True:
		# Pause for 10ms then wait until the write is done
		time.sleep(0.1)
		e.wait()
		
		# Get any incoming bytes
		bytesToRead = s.inWaiting()
		byte = s.read(bytesToRead)
		s.flush()
    	
		# Convert the bytes into a string
		string = byte.decode("utf-8") 
		# Display the incoming data
		print(string, end='')

# Write serial data to the port
def writeSerial(e):
	# Run forever
	while True:
		passed = False
		
		# Split user input into a list based on ',' delimiter
		data = input()
		data = data.split(',')
		# Convert the strings to ints in the list
		data = [int(i) for i in data]
		
		# Make sure we only have three values
		if (len(data) == 3):
			# Make sure they are all numbers within their ranges
			if ((data[0] >= 0 and data[0] <= 3) or data[0] == 5): 
				if (data[1] >= 0 and data[1] <= 100):
					if (data[2] >= 0 and data[2] <= 100):
						# Add the preamble and checksum
						data.insert(0, 255)
						data.append(0)
						
						# Pause the read thread
						e.clear()
						
						# Write the data to the serial port as bytes
						s.write(bytes(data))
						s.flush()
						print("\033[92m" + str(data) + "\033[0m")
						
						# Wait 0.5 seconds then start the read thread
						time.sleep(0.5)

						e.set()
						
						passed = True
		
		# Display a message if everything didn't pass
		if(not(passed)):
			print("The data was not formatted properly.")
	
# Create two processes so we can asynchronously read and write serial data 	
if __name__ == '__main__':
	event = threading.Event()
	
	read = threading.Thread(name='read', target=readSerial, args=(event,))
	write = threading.Thread(name='write', target=writeSerial, args=(event,))
	event.set()
	
	read.start()
	write.start()