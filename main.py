from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.dispatcher import Dispatcher
from serial import Serial
import yaml

config = yaml.safe_load(open("config.yaml","r"))


# Serial setup
ser = Serial()
ser.baudrate = config["communication"]["serial"]["baudRate"]
ser.port = config["communication"]["serial"]["port"]

# Debug mode will print out prepared serial messages, serial enabled will disable/enable serial output
debugMode = config["debugMode"]
serialEnabled = config["serialEnabled"]
if debugMode:
    print(ser)


# OSC network setup
oscIp = config["communication"]["osc"]["listenIp"]
oscPort = config["communication"]["osc"]["listenPort"]


# Shorthand for server and dispatcher
dispatcher = Dispatcher()
server = BlockingOSCUDPServer((oscIp,oscPort), dispatcher)



# Serial communication function, send messages to serial device
def sendSerial(message: str):
    if debugMode:
        print(f"Message: {message}")
    if serialEnabled:
        ser.open()
        ser.write(message.encode("ascii"))
        ser.close()



# SPR (set parameter) functions

# Create command string and send to serial
def setParameter(index: int, value: int):
    commandStr = f"SPR 0 {index} {value}\n"
    sendSerial(commandStr)

# Callback function for osc
def setParameterHandler(address, *args):
    if len(args) == 2:
        index = int(args[0])
        value = int(args[1])

        print(f"Command: {address} {index} {value}")
        setParameter(index, value)
    else:
        print(f"Incorrect OSC arguments passed! Required: 2 Passed: {len(args)}")


# RSPR (set parameter relative) functions
def setParameterRel(index: int, value: int):
    commandStr = f"RSPR 0 {index} {value}\n"
    sendSerial(commandStr)

def setParameterRelHandler(address, *args):
    if len(args) == 2:
        index = int(args[0])
        value = int(args[1])

        print(f"Command: {address} {index} {value}")
        setParameterRel(index, value)
    else:
        print(f"Incorrect OSC arguments passed! Required: 2 Passed: {len(args)}")







# SVOL (set volume) functions

# Create command string and send to serial
def setVolume(index: int, value: int):
    commandStr = f"SVL 0 {index} {value}\n"
    sendSerial(commandStr)

# Callback function for osc
def setVolumeHandler(address, *args):
    if len(args) == 2:
        index = int(args[0])
        value = int(args[1])

        print(f"Command: {address} {index} {value}")
        setVolume(index, value)
    else:
        print(f"Incorrect OSC arguments passed! Required: 2 Passed: {len(args)}")


# RSVL (set volume relative) functions
def setVolumeRel(index: int, value: int):
    commandStr = f"RSVL 0 {index} {value}\n"
    sendSerial(commandStr)

def setVolumeRelHandler(address, *args):
    if len(args) == 2:
        index = int(args[0])
        value = int(args[1])

        print(f"Command: {address} {index} {value}")
        setVolumeRel(index, value)
    else:
        print(f"Incorrect OSC arguments passed! Required: 2 Passed: {len(args)}")



# WAV playback related functions

# Create command string and send to serial
def playWav(index: int):
    commandStr = f"PWF 0 {index}\n"
    sendSerial(commandStr)

# Callback function for osc
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

# Callback function for osc
def stopWavHandler(address, *args):
    if len(args) == 0:
        print(f"Command: {address}")
        stopWav()
    else:
        print(f"Incorrect OSC arguments passed! Required: 0 Passed: {len(args)}")



# Address mapping

dispatcher.map("/set/parameter", setParameterHandler)
dispatcher.map("/set/parameter/relative", setParameterRelHandler)

dispatcher.map("/set/volume", setVolumeHandler)
dispatcher.map("/set/volume/relative", setVolumeRelHandler)

dispatcher.map("/wav/play", playWavHandler)
dispatcher.map("/wav/stop", stopWavHandler)




print("OSC server starting")
server.serve_forever()