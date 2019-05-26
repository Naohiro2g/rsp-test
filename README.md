## Test code of Scratch Remote Sensors Protocol in Python2 and Scratch 1.4

You can talk to Scratch with the message you entered:

 - Scratch cat can receive the incoming broadcast message with "When I receive 'message'".
 - Just click OK without message on the input dialog of talker script to terminate.

You can listen to the message from Scratch:

 - Scratch issues a sensor-update message via socket when *actual* update of a variable happens.
 - Scratch issues a broadcast message via socket when [broadcast (message)] block fired a message.
 - Listner script prints messages from Scratch with byte count.
 - Hit ctrl-c to terminate the listner script.
 - Change HOST setting in the script if you want to listen to the Scratch on remote computer.

## How it works
### talk_to_scratch.py

Launch Scratch and right-click on the block "slider sensor value" in sensing blocks pallet to open the connection. You will see the dialog "Remote sensor connections enabled", then click OK.

```
$ python talk_to_scratch.py
```

If the computer running scratch is remote in the LAN, enter the remote IP address. If it's the same computer, just hit [enter] or enter localhost then hit [enter].

In the Scratch script, use [When I receive (hello)] to listen to the message "hello".

Enter "hello" to the Python dialog to run the "hello" blocks in Scratch.


### listen_to_scratch.py

It listens to the messages from Scratch running on localhost and prints in the terminal.

How to run the script and how to see the messages from Scratch:

```
Launch Scratch first.

$ python listen_to_scratch.py

 - [broadcast (message)]
 - [set (global variable) to (VALUE)]
 - [change (glovbal variable) by (delta)]

byte count: 16   broadcast "1234"
byte count: 17   broadcast "hello"
byte count: 24   sensor-update "G1" 1234 
byte count: 36   sensor-update "G1" "1234c123456789" 
byte count: 46   sensor-update "G1" "1234c123456789c123456789" 
byte count: 56   sensor-update "G1" "1234c123456789c123456789c123456789" 
```

Sensor-update will be issuing only when the global variable actually updated to the different value. And it needs an [wait (0) secs] block between two updates. In contrast, broadcast message is always happen if it was same as before.

## Basic of RSP
When remote sensors are enabled, Scratch listens for connections on TCP port 42001. Once a connection is established, messages are sent in both directions over the socket connection according to the protocol as below.

```
<size: 4 bytes><msg: size bytes>
00 00 00 11 b r o a d c a s t SP " h e l l o "
00 00 00 18 s e n s o r - u p d a t e SP " G 1 " SP 1 2 3 4 SP
SP: space character
```

# Sample codes to broadcast a message in Scratch-RSP by offical

## In Python 2

 - https://en.scratch-wiki.info/wiki/Communicating_to_Scratch_via_Python_with_a_GUI

```
def sendScratchCommand(cmd):
    n = len(cmd)
    a = array('c')
    a.append(chr((n >> 24) & 0xFF))
    a.append(chr((n >> 16) & 0xFF))
    a.append(chr((n >>  8) & 0xFF))
    a.append(chr(n & 0xFF))
    scratchSock.send(a.tostring() + cmd)    
```

## In Python 3

 - https://en.scratch-wiki.info/wiki/Communicating_to_Scratch_via_Python

In Python 3, you can make it much simpler using int.to_bytes() method like below:

```
def sendCMD(cmd):
    sock.send(len(cmd).to_bytes(4, 'big'))
    sock.send(bytes(cmd, 'UTF-8'))
```

### int to byte in Python 2 and Python 3

 - https://www.delftstack.com/howto/python/how-to-convert-int-to-bytes-in-python-2-and-python-3/

You can use struct.pack() method for both Python 2 and Python 3. Yay!

```
import struct

print(len(cmd).to_bytes(4, 'big'))
print(struct.pack(">I",len(cmd)))
```

But be careful, sock.send() method had changed...
```
In Python 2:
    a = struct.pack(">I",len(cmd))
    scratchSock.send(a.tostring())
    scratchSock.send(cmd)           // to send str as bytes

In Pythin 3:
    sock.send(struct.pack(">I",len(cmd)))   
    sock.send(bytes(cmd, 'UTF-8'))  // to send bytes
```    


# Remote Sensors Protocol Documents

## Official wiki
 - https://en.scratch-wiki.info/wiki/Remote_Sensor_Connections
 - http://wiki.scratch.mit.edu/wiki/Remote_Sensors_Protocol

## blog.champierre.com (Junya Ishihara)

1. https://blog.champierre.com/1047
2. https://blog.champierre.com/1048
3. https://blog.champierre.com/1049
4. https://blog.champierre.com/1050
5. https://blog.champierre.com/1051

## node module (YOKOBOND)
scratch-rsp
 - https://www.npmjs.com/package/scratch-rsp
 - https://github.com/yokobond/node-scratch-rsp

## Scratch Remote Sensor Protocol via UDP (YOKOBOND)
https://lab.yengawa.com/2015/12/11/scratch-remote-sensor-protocol-on-udp/

