# Python 3 version  Talker
# Sends messages and sensor-updates in Scratch Remote Sensors Protocol
# use control-c to quit

import socket
import sys
import struct

# HOST = 'localhost'  # make it as his-raspi.local or 192.168.1.22
#                     # to connect to another computer on the same network
PORT = 42001          # Scratch Remote Sensors Protocol port


print("\nScratch Remote Sensors Protocol  talker")
print("What is the name of computer which Scratch is running on?")
print("(hint: his-raspi.local or 192.168.22.13)")
HOST = input("host name?  (hit enter to make it localhost):")
if not HOST:
    HOST = 'localhost'
print("\nConnecting to {}...".format(HOST))
scratchSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
scratchSock.connect((HOST, PORT))
print("==== Connected to Scratch at {}!".format(HOST))


def sendScratchCommand(cmd):
    scratchSock.send(struct.pack(">I", len(cmd.encode('UTF-8'))))
    print(struct.pack(">I", len(cmd.encode('UTF-8'))))
    scratchSock.send(bytes(cmd, 'UTF-8'))
    print(bytes(cmd, 'UTF-8'))


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
            # print('sensor-update "' + msg + ' ')
        else:
            sendScratchCommand('broadcast "' + msg + '"')
            # print('broadcast "' + msg + '"')

except KeyboardInterrupt:
    print("\n\n\n  closing socket...")
    scratchSock.close()
    print("               bye...")
    sys.exit(0)
