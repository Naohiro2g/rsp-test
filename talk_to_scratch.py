# Python 3 version  Talker
# Sends messages and sensor-updates in Scratch Remote Sensors Protocol
# use control-c to quit

from array import array
import socket
import time, sys
import struct, unicodedata

#HOST = 'localhost'   # his-raspi.local or 192.168.1.22
#                     # to connect to another computer on the same network
PORT = 42001          # Scratch Remote Sensors Protocol port


print("\nScratch Remote Sensors Protocol  talker")
HOST = input("What is the name of computer which Scratch is running on?\n \
(hint: his-raspi.local or 192.168.22.13)\n host name?  (hit enter to make it localhost):")
if not HOST : HOST = 'localhost'

print("\nConnecting to {}...".format(HOST))
scratchSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
scratchSock.connect((HOST, PORT))
print("==== Connected to Scratch at {}!".format(HOST))

def sendScratchCommand(cmd):
    scratchSock.send(struct.pack(">I",lenCount(cmd)))
    print(struct.pack(">I",lenCount(cmd)))
    scratchSock.send(bytes(cmd, 'UTF-8'))
    print(bytes(cmd, 'UTF-8'))

def lenCount(text):
    count = 0
    for c in text:
        if unicodedata.east_asian_width(c) in 'FWA':
            count += 3
        else:
            count += 1
    return count

def sensorUpdater():
    print("\n<<Sensor-update mode>>")
    sensorName = input("Sensor Name: ")
    sensorValue = input("Value: ")
    return (sensorName + '" ' + sensorValue)


print('    Please try "hello" or "こんにちは" as the test message.')
print('    Put an empty message to go into sensor-update mode.')
print('    In the sensor-update mode, try "G1" as name and "1234" as value.')

try:
    while True:
        print('\n<<Message mode>> Input a message to talk to Scratch')
        msg = input("Message: ")
        if not msg:
            msg = sensorUpdater()
            sendScratchCommand('sensor-update "' + msg + ' ')
            #print('sensor-update "' + msg + ' ')
        else:
            sendScratchCommand('broadcast "' + msg + '"')
            #print('broadcast "' + msg + '"')

except KeyboardInterrupt:
    print("\n\n\n  closing socket...")
    scratchSock.close()
    print("               bye...")
    sys.exit(0)
