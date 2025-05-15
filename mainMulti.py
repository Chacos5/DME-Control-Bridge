from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.dispatcher import Dispatcher
from serial import Serial
import yaml

config = yaml.safe_load(open("config.yaml","r"))

devices = []


# Serial setup
ser = Serial()
ser.baudrate = config["communication"]["serial"]["baudRate"]


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


# Convert each device in the config file to a dictionary in the devices array, index of each device is based on its "id" setting 
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
def sendSerial(message: str, serialPort: str):
    if debugMode:
        print(f"Message: {message} ID: {message[1]}")
    if serialEnabled:
        ser.port = serialPort
        ser.open()
        ser.write(message.encode("ascii"))
        ser.close()



# SPR (set parameter) functions

# Create command string and send to serial
def setParameter(address: str, *args):
    print("run")
    reqArgs = 2
    id = int(address[1])
    if len(args) == reqArgs:
        index = args[0]
        value = args[1]
        commandStr = f"SPR 0 {index} {value} \n"

        if devices[id]["mode"] == "serial":
            sendSerial(commandStr, devices[id]["serialPort"])
    else:
        print(f"Incorrect args provided! Required: {reqArgs} Provided: {len(args)}")

    print(address[1])
    



# RSPR (set parameter relative) functions
def setParameterRel(index: int, value: int):
    commandStr = f"RSPR 0 {index} {value}\n"
    sendSerial(commandStr)








# SVOL (set volume) functions

# Create command string and send to serial
def setVolume(address: str, *args):
    print(address[1])
    commandStr = f"SVL 0"


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

for id,device in enumerate(devices):
    id = id 
    name = device["name"]

    if debugMode:
        print(f"ID: {id}")
        print(f"Device def: {device}")
    dispatcher.map(f"/{id}/set/parameter", setParameter)
    dispatcher.map(f"/{id}/set/parameter/relative", setParameterRel)
    
    dispatcher.map(f"/{id}/set/volume", setVolume)
    dispatcher.map(f"/{id}/set/volume/relative", setVolume)

    dispatcher.map(f"/{id}/wav/play", playWav)
    dispatcher.map(f"/{id}/wav/stop", stopWav)



print("OSC server starting")
print(dispatcher)
server.serve_forever()