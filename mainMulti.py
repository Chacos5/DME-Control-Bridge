from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.dispatcher import Dispatcher
from serial import Serial
import yaml

config = yaml.safe_load(open("config.yaml","r"))

devices = []


# Serial setup
ser = Serial()
ser.baudrate = config["communication"]["serial"]["baudRate"]
ser.port = config["communication"]["serial"]["port"]

# Debug mode will print out prepared serial messages, serial enabled will disable/enable serial output
debugMode = config["debugMode"]
serialEnabled = config["serialEnabled"]
networkEnabled = False
if debugMode:
    print(f"\n{ser}\n")


# OSC network setup
oscIp = config["communication"]["osc"]["listenIp"]
oscPort = config["communication"]["osc"]["listenPort"]


# Shorthand for server and dispatcher
dispatcher = Dispatcher()
server = BlockingOSCUDPServer((oscIp,oscPort), dispatcher)


for device in config["dmeDevices"]:
    try:
        if device["mode"] == "serial":
            devices.insert(device["id"],{"name": device["name"], "mode": "serial", "serialPort": device["serialPort"]})
        elif device["mode"] == "network":
            devices.insert(device["id"],{"name": device["name"], "mode": "network", "ip": device["ip"], "netPort": device["netPort"]})
        else:
            print("Error, device mode is not set, skipping!")
    except Exception as error:
        print(f"Invalid config item! Item:\n{device}\n")


# Serial communication function, send messages to serial device
def sendMessage(message: str, mode: str):

    if debugMode:
        print(f"Message: {message} Mode: {mode}")
    if serialEnabled and mode == "serial":
        ser.open()
        ser.write(message.encode("ascii"))
        ser.close()
    elif networkEnabled and mode == "network":
        print("Network stuff! :)")



# SPR (set parameter) functions

# Create command string and send to serial
def setParameter(address: str, *args):

    commandStr = f"SPR 0\n"



# RSPR (set parameter relative) functions
def setParameterRel(index: int, value: int):
    commandStr = f"RSPR 0 {index} {value}\n"
    sendSerial(commandStr)








# SVOL (set volume) functions

# Create command string and send to serial
def setVolume(index: int, value: int):
    commandStr = f"SVL 0 {index} {value}\n"
    sendSerial(commandStr)


# RSVL (set volume relative) functions
def setVolumeRel(index: int, value: int):
    commandStr = f"RSVL 0 {index} {value}\n"
    sendSerial(commandStr)


# WAV playback related functions

# Create command string and send to serial
def playWav(index: int):
    commandStr = f"PWF 0 {index}\n"
    sendSerial(commandStr)



# Create command string and send to serial
def stopWav():
    commandStr = f"SWF 0\n"
    sendSerial(commandStr)


# Address mapping

# dispatcher.map("/set/parameter", setParameterHandler)
# dispatcher.map("/set/parameter/relative", setParameterRelHandler)

# dispatcher.map("/set/volume", setVolumeHandler)
# dispatcher.map("/set/volume/relative", setVolumeRelHandler)

# dispatcher.map("/wav/play", playWavHandler)
# dispatcher.map("/wav/stop", stopWavHandler)

for device in devices:
    id = device["id"]
    name = device["name"]

    dispatcher.map(f"/{id}/set/parameter", setParameter())




print("OSC server starting")
server.serve_forever()