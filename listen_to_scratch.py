# Python 3 Version  Listener
# Receives and prints messages sent in Scratch Remote Sensors Protocol
# use control-c to quit

from array import array
import socket
import time, sys
import codecs

#HOST = 'localhost'
PORT = 42001           # Scratch Remote Sensors Protocol port

print("\nScratch Remote Sensors Protocol  listener")
HOST = input("What is the name of computer which Scratch is running on?\n \
(hint: his-raspi.local or 192.168.22.13)\n host name? (hit enter to make it localhost) :")
if not HOST : HOST = 'localhost'

print("\nConnecting to {}...".format(HOST))
scratchSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
scratchSock.connect((HOST, PORT))
print("==== Connected to Scratch at {}! I'm listening...".format(HOST))

# print incoming data forever, ctrl-c to break and quit
# First four bytes is size of message in byte string format.
# 00 00 00 11 broadcast "hello"
# 00 00 00 18 sensor-update "G1" 1234
data = scratchSock.recv(1024)  # ignore the first garbage

try:
   while True:
       data = scratchSock.recv(1024)
       if not data: break
       count = int(codecs.encode(data[0:4], 'hex'), 16)
       print ('bytes received: ' + str(count) + ' ', end="")
       print('<message|' + data[4:].decode('utf-8') + '|EOL>')
       time.sleep(0.05)

except KeyboardInterrupt:
   print("\n\n\n  closing socket...")
   scratchSock.close()
   print("               bye...")
   sys.exit(0)

