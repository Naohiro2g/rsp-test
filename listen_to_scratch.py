# Python 3 Version  Listener
# Receives and prints messages sent in Scratch Remote Sensors Protocol
# use control-c to quit

import socket
import time
import sys
import codecs


# HOST = 'localhost'
PORT = 42001           # Scratch Remote Sensors Protocol port

print("\nScratch Remote Sensors Protocol  listener")
print("What is the name of computer which Scratch is running on?")
print("(hint: his-raspi.local or 192.168.22.13)")
HOST = input("host name?  (hit enter to make it localhost):")
if not HOST:
    HOST = 'localhost'

print("\nConnecting to {}...".format(HOST))
scratchSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
scratchSock.connect((HOST, PORT))
print("==== Connected to Scratch at {}! I'm listening...".format(HOST))

# print incoming data forever, ctrl-c to break and quit
# First four bytes is size of message in byte string format.
# 00 00 00 11 broadcast "hello"|
# 00 00 00 18 sensor-update "G1" 1234 |

try:
    while True:
        data = scratchSock.recv(1024)
        if not data: break
        i = 0
        while bool(data[i:i+4]):    # while byte count is exist
            count = int(codecs.encode(data[i:i+4], 'hex'), 16)
            print ('bytes received: ' + str(count) + ' ', end="")
            i += 4      # skip byte count
            print('<message|' + data[i:i+count].decode('utf-8') + '|EOL>')
            i += count  # head to the next message
        time.sleep(0.05)

except KeyboardInterrupt:
    print("\n\n\n  closing socket...")
    scratchSock.close()
    print("               bye...")
    sys.exit(0)
