# Python 3 Version
# Receives and prints message sent in Scratch Remote Sensors Protocol
# use control-c to quit

from array import array
import socket
import time
import codecs
import sys

HOST = 'localhost'
PORT = 42001

print("connecting...")
scratchSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
scratchSock.connect((HOST, PORT))
print("Connected to Scratch! waiting for data...")

# print incoming data forever, ctrl-c to break and quit
# First four bytes is size of message in byte string format.
# 00 00 00 11 broadcast "hello"
# 00 00 00 18 sensor-update "G1" 1234
data = scratchSock.recv(1024)  # ignore the first garbage
while True:
    data = scratchSock.recv(1024)
    if not data: break
    count = int(codecs.encode(data[0:4], 'hex'), 16)
    print ('bytes received: ' + str(count) + ' ', end="")
    print('<message|' + data[4:].decode('utf-8') + '|EOL>')
    time.sleep(0.05)


print("closing socket...")
scratchSock.close()
print("bye...")
sys.exit()
