# Python 3 version
# Sends messages to Scratch

from array import array
import socket
import time
import sys
import struct
import unicodedata

PORT = 42001         # Scratch Remote Sensors Protocol port
HOST = 'localhost'   # his-raspi.local or 192.168.1.22
                     # to connect to another computer on the same network

print("\n", "Connecting...")
scratchSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
scratchSock.connect((HOST, PORT))
print("Connected to Scratch!")

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
    print("Sensor name?  Try 'G1'")
    variableName = input()
    print("Value?   Try '1234'  You can check it by [(G1) sensor value] block.")
    variableValue = input()
    return (variableName + '" ' + variableValue)


print('\n', 'Scratch Remote Sensors Protocol talker started...\n')
print('    Please try "hello" or "こんにちは" as the test message.')
print('    Put an empty message to go into sensor-update mode.')

while True:
    print('\n', 'Input a message to broadcast in Scratch-RSP: ')
    msg = input()
    if not msg:
        msg = sensorUpdater()
        sendScratchCommand('sensor-update "' + msg + ' ')
        #print('sensor-update "' + msg + ' ')
    else:
        sendScratchCommand('broadcast "' + msg + '"')
        #print('broadcast "' + msg + '"')

print("closing socket...")
scratchSock.close()
print("\n", "bye...")
sys.exit()
