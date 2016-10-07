import configparser
import serial
import time

# [0xFF][orientation][intensity][duration][checksum - never 255. sender will truncate to 254 rather than send a 255]

# Get current configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Check which port to use and open serial connection
s = 0
if (config['Serial'].getboolean('useDevGlove')):
	s = serial.Serial(port=config['Serial']['devPort'], baudrate=9600)
else:
	s = serial.Serial(port=config['Serial']['livePort'], baudrate=9600)
	
# Run through each motor twice
print("Running each motor individually...")
time.sleep(1)
for i in range(0, 8):
	motor = i // 2
	s.write(bytes([ 255, motor, 90, 100, 0 ]))
	print("Motor", motor)
	time.sleep(1.5)


# Test all of them
print("Running every motor...")
s.write(bytes([ 255, 5, 90, 100, 0 ]))
time.sleep(1)
s.write(bytes([ 255, 5, 90, 100, 0 ]))
time.sleep(1)
s.write(bytes([ 255, 5, 90, 100, 0 ]))
time.sleep(1)
s.write(bytes([ 255, 5, 90, 100, 0 ]))
time.sleep(3)

# Test different durations
print("Running every motor at different durations...")
print("20%")
s.write(bytes([ 255, 5, 90, 20, 0 ]))
time.sleep(2)
print("50%")
s.write(bytes([ 255, 5, 90, 50, 0 ]))
time.sleep(2)
print("75%")
s.write(bytes([ 255, 5, 90, 75, 0 ]))
time.sleep(2)
print("100%")
s.write(bytes([ 255, 5, 90, 100, 0 ]))
time.sleep(3)

# Test different intensities
print("Running every motor at different intensities...")
print("100%")
s.write(bytes([ 255, 5, 100, 100, 0 ]))
time.sleep(2)
print("90%")
s.write(bytes([ 255, 5, 90, 100, 0 ]))
time.sleep(2)
print("75%")
s.write(bytes([ 255, 5, 75, 100, 0 ]))
time.sleep(2)
print("50%")
s.write(bytes([ 255, 5, 50, 100, 0 ]))
time.sleep(2)
print("25%")
s.write(bytes([ 255, 5, 25, 100, 0 ]))
print("Run complete.")
