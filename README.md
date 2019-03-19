## Test code for Scratch Remote Sensors Protocol for Scratch 1.4

To broadcast the typed in message to Scratch.

 - Scratch cat can receive it with "When I receive 'message'".
 - Just click OK without message to terminate the script.

## How it works
### rsp-to_scratch.py

Start Scratch and right-click on the block "slider sensor value" in sensing blocks pallet to open the connection. You will see the dialog "Remote sensor connections enabled", then click OK.

```
$ python rsp-to_scratch.py
```

If the computer running scratch is remote in the LAN, enter the remote IP address. If it's the same computer, just hit [enter] or enter localhost then hit [enter].

In the Scratch script, use [When I receive (hello)] to listen to the message "hello".

Enter "hello" to the Python dialog to run the "hello" blocks in Scratch.


### rsp-from_scratch.py

It listens to the messages from Scratch running on localhost and prints in the terminal.

How to run the script and how to see the messages from Scratch:

```
Launch SCratch first.

$ python rsp-from_scratch.py

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

## Scratch Remote Sensor Protocol on UDP (YOKOBOND)
https://lab.yengawa.com/2015/12/11/scratch-remote-sensor-protocol-on-udp/

