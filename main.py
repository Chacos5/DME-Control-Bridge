from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.dispatcher import Dispatcher
from serial import Serial

ser = Serial()
ser.baudrate = 38400
ser.port = "/dev/ttySC0"


ip = "0.0.0.0"
port = 1337


# Shorthand for server and dispatcher
dispatcher = Dispatcher()
server = BlockingOSCUDPServer((ip,port), dispatcher)



# Serial communication function, send messages to serial device
def sendSerial(message: str):
    # print(f"Message: {message}")
    ser.open()
    ser.write(message.encode("ascii"))
    ser.close()





# SPR (set parameter) functions

# Create command string and send to serial
def setParameter(index: int, value: int):
    commandStr = f"SPR 0 {index} {value}\n"
    sendSerial(commandStr)

# Callback function for osc, parse osc string, validate, then send to setVolume
def setParameterHandler(address, *args):
    if len(args) == 2:
        index = int(args[0])
        value = int(args[1])

        print(f"Command: {address} {index} {value}")
        setParameter(index, value)
    else:
        print(f"Incorrect OSC arguments passed! Required: 2 Passed: {len(args)}")



# SVOL (set volume) functions

# Create command string and send to serial
def setVolume(index: int, value: int):
    commandStr = f"SVL 0 {index} {value}\n"
    sendSerial(commandStr)

# Callback function for osc, parse osc string, validate, then send to setVolume
def setVolumeHandler(address, *args):
    if len(args) == 2:
        index = int(args[0])
        value = int(args[1])

        print(f"Command: {address} {index} {value}")
        setVolume(index, value)
    else:
        print(f"Incorrect OSC arguments passed! Required: 2 Passed: {len(args)}")



# WAV playback related functions

# Create command string and send to serial
def playWav(index: int):
    commandStr = f"PWF 0 {index}\n"
    sendSerial(commandStr)

# Callback function for osc, parse osc string, validate, then send to setVolume
def playWavHandler(address, *args):
    if len(args) == 1:
        index = int(args[0])

        print(f"Command: {address} {index}")
        playWav(index)
    else:
        print(f"Incorrect OSC arguments passed! Required: 1 Passed: {len(args)}")


# Create command string and send to serial
def stopWav():
    commandStr = f"SWF 0\n"
    sendSerial(commandStr)

# Callback function for osc, parse osc string, validate, then send to setVolume
def stopWavHandler(address, *args):
    if len(args) == 0:
        print(f"Command: {address}")
        stopWav()
    else:
        print(f"Incorrect OSC arguments passed! Required: 0 Passed: {len(args)}")




# Address mapping
dispatcher.map("/set/parameter", setParameterHandler)
dispatcher.map("/set/volume", setVolumeHandler)
dispatcher.map("/wav/play", playWavHandler)
dispatcher.map("/wav/stop", stopWavHandler)



print("OSC server started")
server.serve_forever()
