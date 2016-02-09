# Receives and prints data sent by Scratch; use control-C to quit
from array import array
import socket
import time

HOST = 'localhost'
PORT = 42001

print("connecting...")
scratchSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
scratchSock.connect((HOST, PORT))
print("connected! waiting for data...")


# print incoming data forever

while True:
	time.sleep(0.01)
	data = scratchSock.recv(1024)
	if not data: break
	print(data)

print("closing socket...")
scratchSock.close()
print("done")
sys.exit()
