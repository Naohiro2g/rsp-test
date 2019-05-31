## Scratch遠隔センサープロトコル(Remote Sensors Protocol, RSP)のPython3 / Scratch 1.4によるテストコード
([English version is hear. 英語版はこちら。](./README.md))

### [Talkerコード](talk_to_scratch.py)で、メッセージやセンサーデータの更新をScratchに伝える（話す）ことができる：

 1. Scratch 1.4 が走っているコンピューターの名前（ホスト名とも呼ばれる）を接続先として入力する。エンターキーだけ押した場合は、"localhost"が設定され、このPythonコードが走っているコンピューター自身のScratchと接続を試みる。
 - RSP接続に成功すると、メッセージ入力モードになる。
    - メッセージを入力してScratchへ送る。日本語メッセージも大体は大丈夫。
    - Scratchは、やって来たメッセージをハット型の [(メッセージ)を受け取ったとき]ブロックで受け取る。
 - メッセージ入力モードでエンターキーだけを押すと、センサー更新モードに入る。
    - センサー名と値を入力してScratchへ送る。日本語名はラズパイだったら大体は大丈夫。Macはダメっぽい。
    - Scratch側では [(センサー名) センサーの値] で値を知ることができる。
 - 再び、メッセージ入力モードに戻る。終了するときは、ctrl-cを押す。
 - Scratchは、RSP経由で入ってきた情報をそのまま、RSPで送り出す。

### [Listenerコード](listen_to_scratch.py)で、Scratchからのメッセージや変数の更新情報を受け取る（聴く）ことができる：

 1. Scratch 1.4 が走っているコンピューターの名前（ホスト名とも呼ばれる）を入力する。エンターキーだけ押すとlocalhostが設定され、このPythonコードが走っているコンピューター自身のScratchと接続を試みる。
 - Scratchは、グローバル変数（全てのスプライト用）の値が **実際に変化した時** に、センサー値更新メッセージをRSPで送り出す。日本語名はラズパイだったら大体は大丈夫。Macはダメっぽい。
 - Scratchは、[(メッセージ)を送る]ブロックによってメッセージを送ると同時にRSPでも送り出す。
 - Listenerコードは、Scratchからの情報を表示する。
 - 終了するときは、ctrl-cを押す。

### マルチバイト文字について
 - UTF-8は、マルチバイト文字が2バイトから4バイトになる。古い規格だと6バイトまで。
 - 日本語はほとんどは3バイトで一部が4バイト。
 - 仮名漢字の日本語はほとんど3バイト。
 - Talkerは、メッセージのバイト数をカウントし、メッセージの先頭に付けて送出する。

### Mac版Scratch 1.4の場合
 - メッセージに日本語を使っても問題ない。
 - 変数名、変数値に日本語を使っても表示できる。
 - センサー名、センサー値に日本語を使うと、Scratch上でどちらもascii表示になり文字化けする。
 - メッセージの日本語は問題ないが、変数、センサー値に日本語を使うと動作が全体的に遅くなる。


### Scratchの挙動
 - RSPサーバーとして動いていて、複数のTalker/Listenerからクライアントとしての接続を受け付ける。
 - RSP経由でTalkerから入ってきた情報を受け取り、そのまま、RSP経由で送出している。つまり、Listenerでもあり、Talkerでもある。そのため、あるTalkerのメッセージは、全てのListenerが聴くことができる。
 - あるTalker/Listenerからの接続が確立された時、全てのグローバル変数の値をSensor-updateとして送出している。すべてのListenerが同じ情報を共有できることになる。
 - 実は、ScratchはRSPクライアントとして動かすこともできる。この場合、ホスト（サーバー）になったScratchに、他のScratchがクライアントとしてJoin（参加）することができる。「scratch mesh接続」でググってみよう！  ラズパイ同士だと簡単に実現できる。MacやWindowsだと、ちょっと面倒。

### 同じネットワーク内なら、コンピューターの間での通信が可能
 - 同じコンピューターでも良いが、同じネットワーク内の他のコンピューターとの間でも送信／受信ができる。
 - his-raspi.localなどの名前指定か、192.168.1.32などのIPアドレス指定ができる。
 - 名前による指定は、ラズパイなどのLinuxコンピューター、macOS(Unix)、iPhone / iPadだけで可能。AndroidやWindowsの場合は、IPアドレスで指定する。
 - iPhone / iPadアプリのPythonista 3（無料じゃないけど）を使えば、Scratchをリモコンできる。

## Quick start
1. Launch Scratch and open ```RSP_remote_sensors_protocol.sb```, click the green flag to start.
2. Open an LXTerminal window and enter ```python3 listen_to_scratch.py``` to start the listener code.
3. Open another LXTerminal window and enter ```python3 talk_to_scratch.py``` to start the talker code.
4. In Scratch, use the green dragon to talk and the use scratch cat to listen to the Remote Sensors Protocol port.
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

You can enter Japanse text, too. Try "こんにちは"

Scratch code RSP_remote_sensors_protocol.sb is to help you understand the mechanism.


### listen_to_scratch.py

It listens to the messages from Scratch running on localhost and prints in the terminal.

How to run the script and how to see the messages from Scratch:

```
Launch Scratch first then,

$ python3 listen_to_scratch.py

listening to Sctach to make:
 - [broadcast (message)]
 - [set (global variable) to (VALUE)]
 - [change (glovbal variable) by (delta)]

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
https://lab.yengawa.com/2015/12/11/scratch-remote-sensor-protocol-on-udp/
