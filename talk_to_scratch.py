# Sends data to Scratch;
# default host is localhost, put an empty message to quit
from array import array
import socket
import time
import sys

from Tkinter import Tk
from tkSimpleDialog import askstring
root = Tk()
root.withdraw()

PORT = 42001
HOST = askstring('Scratch Connector', 'IP:')
if not HOST: HOST = 'localhost'

print("connecting...")
scratchSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
scratchSock.connect((HOST, PORT))
print("connected")

def sendScratchCommand(cmd):
    n = len(cmd)
    a = array('c')
    a.append(chr((n >> 24) & 0xFF))
    a.append(chr((n >> 16) & 0xFF))
    a.append(chr((n >>  8) & 0xFF))
    a.append(chr(n & 0xFF))
    scratchSock.send(a.tostring() + cmd)

while True:
    msg = askstring('Scratch Connector', 'Send Broadcast:')
    if not msg: break
    sendScratchCommand('broadcast "' + msg + '"')

print("closing socket...")
scratchSock.close()
print("done")
sys.exit()
