## Test code of Scratch Remote Sensors Protocol or RSP in Python 3 / Scratch 1.4
（[Japanese is here. 日本語はこちら。](./README-ja.md)）

### You can talk to Scratch with messages or sensor-updates with [Talker code](talk_to_scratch.py):

 1. Input computer name (also called as hostname) or IP address of the computer to connect, which Scratch is running on. "localhost" will be set if you just hit the enter key then the code tries to connect to the same computer which the code itself is running on.
 - When the RSP connection has successfully established, you are in the message sending mode.
   - Input a message to talk to Scratch.
   - Scratch can receive the incoming message with [When I receive (message)] hat block.
 - Put an empty message to bring you into the sensor update mode.
   - Input sensor name and value. Scratch can receive the value with [(sensor name) sensor value] block.
 - Back to the message sending mode again.
 - Press ctrl-c to exit.

### You can listen to the message from Scratch with [Listener code](listen_to_scratch.py):

 1. Input computer name (also called as hostname) or IP address of the computer to connect, which Scratch is running on. "localhost" will be set if you just hit the enter key.
  - Scratch issues a sensor-update message via RSP **only when actual update of a variable happens**.
 - Scratch issues a broadcast message via RSP when [broadcast (message)] block fired a message.
 - Listener script prints messages from Scratch.
 - Hit ctrl-c to terminate the listener script.
 - Change HOST setting in the script if you want to listen to the Scratch on remote computer.
 - Press ctrl-c to exit.


## Quick start
1. Launch Scratch and open ```RSP_remote_sensors_protocol.sb```, click the green flag to start.
2. Open an LXTerminal window and enter ```python3 listen_to_scratch.py``` to start the listener code.
3. Open another LXTerminal window and enter ```python3 talk_to_scratch.py``` to start the talker code.
4   . In Scratch, use the green dragon to talk and the use scratch cat to listen to the Remote Sensors Protocol port.
5. Remember variables must be "For all sprites" AND sensor-update message occurs only when the value changed.
6. You can use Japanese for messages and sensor/variable names.


## How it works
### talk_to_scratch.py

Launch Scratch and right-click on the block "slider sensor value" in sensing blocks pallet to open the connection. You will see the dialog "Remote sensor connections enabled", then click OK.

```
$ python3 talk_to_scratch.py
```

In the Scratch script, use [When I receive (hello)] to listen to the message "hello".

Enter "hello" to the Python dialog to run the "hello" blocks in Scratch.

You can enter Japanese text, too. Try "こんにちは"

Scratch code RSP_remote_sensors_protocol.sb is to help you understand the mechanism.


### listen_to_scratch.py

It listens to the messages from Scratch running on localhost and prints in the terminal.

How to run the script and how to see the messages from Scratch:

```
Launch Scratch first then,

$ python3 listen_to_scratch.py

listening to Scratch to receive messages like these:
 - [broadcast (message)]
 - [set (global variable) to (VALUE)]
 - [change (global variable) by (delta)]

then print like these:

bytes received: 16 <message|broadcast "1234"|EOL>
bytes received: 17 <message|broadcast "hello"|EOL>
bytes received: 24 <message|sensor-update "G1" 1234 |EOL>
bytes received: 36 <message|sensor-update "G1" "1234c123456789" |EOL>
bytes received: 46 <message|sensor-update "G1" "1234c123456789c123456789" |EOL>
bytes received: 56 <message|sensor-update "G1" "1234c123456789c123456789c123456789" |EOL>
bytes received: 27 <message|broadcast "こんにちは"|EOL>
```

Sensor-update will be issuing only when the global variable actually updated to the different value. And it needs an [wait (0) secs] block between two updates, or they will be one combined message. In contrast, broadcast message is always happen if it was same as before.

## Basic of RSP
When remote sensors are enabled, Scratch listens for connections on TCP port 42001. Once a connection is established, messages are sent in both directions over the socket connection according to the protocol as below.

```
<size: 4 bytes><msg: size bytes>
00 00 00 11 b r o a d c a s t SP " h e l l o "
00 00 00 18 s e n s o r - u p d a t e SP " G 1 " SP 1 2 3 4 SP
SP: space character
```

# Sample codes to broadcast a message in Scratch-RSP by official

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
## Official sample codes
 - https://en.scratch-wiki.info/wiki/Communicating_to_Scratch_via_Python_with_a_GUI (Python 2)
 - https://en.scratch-wiki.info/wiki/Communicating_to_Scratch_via_Python (Python 3)

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
 - https://lab.yengawa.com/2015/12/11/scratch-remote-sensor-protocol-on-udp/

## Bezelie remote control
 - https://qiita.com/toyoda/items/bb6be6614750a8410fc9
 - http://bezelie.com/blog/?page_id=819
 - https://github.com/hine/pyscratch
 - https://github.com/hine/ScratchBezelie
 - http://hine.hatenablog.com/entry/2016/12/20/020133
