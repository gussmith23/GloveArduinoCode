# Glove Listener
Listens for incoming serial bytes that indicate which motor(s) should vibrate to provide haptic feedback to the user.
 
 
### Packet Structure
Each packet is made up of 5 bytes, each of which is an 8 bit unsigned integer.


The format is as follows:
  [0xFF][motor][intensity][duration][checksum]


[0xFF] - Preamble byte, 255 in integer form, used to tell when a new packet is starting

[motor] - The motor to be toggled on, ranging from motor 0 to 3 (5 will turn on all motors)

[intensity] - The intensity of the motor that is being toggled on, ranging from 0 - 100%

[duration] - The duration to keep the motor on for, ranging from 0 - 100% of a second (10% is 100ms, 100% is 1sec)

[checksum] - Used to make sure the data was received properly. Never 255. The sender will truncate to 254 rather than send a 255.


If a new packet is received, it will overwrite the duration of the previous one, terminating it immediately.
