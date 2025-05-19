from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.dispatcher import Dispatcher
from serial import Serial
import yaml

config = yaml.safe_load(open("config.yaml","r"))

devices = {}


# Serial setup
ser = Serial()
ser.baudrate = config["communication"]["serial"]["baudRate"]


# Debug mode will print out prepared serial messages, serial enabled will disable/enable serial output
debugMode = config["debugMode"]
serialEnabled = config["serialEnabled"]

if debugMode:
    print(f"\n{ser}\n")


# OSC network setup
oscIp = config["communication"]["osc"]["listenIp"]
oscPort = config["communication"]["osc"]["listenPort"]


# Shorthand for server and dispatcher
dispatcher = Dispatcher()
server = BlockingOSCUDPServer((oscIp,oscPort), dispatcher)


# Convert each device in the config file to a dictionary in the devices array, index of each device is based on its "id" setting 
for item in config["dmeDevices"]:
    try:
        if (item["mode"] == "serial"):
            devices[item["id"]] = {"mode": "serial", "serialPort": item["serialPort"]}
        elif (item["mode"] == "network"):
            devices[item["id"]] = {"mode": "network", "ip": item["ip"], "port": item["port"]}
        else:
            print("Error, device mode is not set, skipping!")
    except:
        print(f"Invalid config item!")
print(devices)

# Serial communication function, send messages to serial device
def sendSerial(message: str, serialPort: str):
    if debugMode:
        print(f"Message: {message} Port: {serialPort}")
    if serialEnabled:
        ser.port = serialPort
        ser.open()
        ser.write(message.encode("ascii"))
        ser.close()



# SPR function
def setParameter(address: str, *args):
    reqParameters = 2 # Number of paramters expected
    
    if len(args) == reqParameters:

        id = int(address[1]) # Get device id from address str
        device = devices[id] # Get device dict from devices based on ID

        index = args[0]
        value = args[1]

        mode = device["mode"]

        if mode == "serial":
            port = device["serialPort"]
            command = f"SPR 0 {index} {value}\n"
            sendSerial(command, port)
        elif mode == "network":
            print("Network logic")
    elif debugMode:
        print(f"Invalid number of paramters provided. Needed: {reqParameters} Provided: {len(args)}")



def setParameterRel(address: str, *args):
    reqParameters = 2 # Number of paramters expected
    
    if len(args) == reqParameters:

        id = int(address[1]) # Get device id from address str
        device = devices[id] # Get device dict from devices based on ID

        index = args[0]
        value = args[1]

        mode = device["mode"]

        if mode == "serial":
            port = device["serialPort"]
            command = f"RSPR 0 {index} {value}\n"
            sendSerial(command, port)
        elif mode == "network":
            print("Network logic")
    elif debugMode:
        print(f"Invalid number of paramters provided. Needed: {reqParameters} Provided: {len(args)}")




def setVolume(address: str, *args):
    reqParameters = 2 # Number of paramters expected
    
    if len(args) == reqParameters:

        id = int(address[1]) # Get device id from address str
        device = devices[id] # Get device dict from devices based on ID

        index = args[0]
        value = args[1]

        mode = device["mode"]

        if mode == "serial":
            port = device["serialPort"]
            command = f"SVL 0 {index} {value}\n"
            sendSerial(command, port)
        elif mode == "network":
            print("Network logic")
    elif debugMode:
        print(f"Invalid number of paramters provided. Needed: {reqParameters} Provided: {len(args)}")


def setVolumeRel(address: str, *args):
    reqParameters = 2 # Number of paramters expected
    
    if len(args) == reqParameters:

        id = int(address[1]) # Get device id from address str
        device = devices[id] # Get device dict from devices based on ID

        index = args[0]
        value = args[1]

        mode = device["mode"]

        if mode == "serial":
            port = device["serialPort"]
            command = f"RSVL 0 {index} {value}\n"
            sendSerial(command, port)
        elif mode == "network":
            print("Network logic")
    elif debugMode:
        print(f"Invalid number of paramters provided. Needed: {reqParameters} Provided: {len(args)}")



def playWav(address: str, *args):
    reqParameters = 1 # Number of paramters expected
    
    if len(args) == reqParameters:

        id = int(address[1]) # Get device id from address str
        device = devices[id] # Get device dict from devices based on ID

        index = args[0]

        mode = device["mode"]

        if mode == "serial":
            port = device["serialPort"]
            command = f"PWF 0 {index}\n"
            sendSerial(command, port)
        elif mode == "network":
            print("Network logic")
    elif debugMode:
        print(f"Invalid number of paramters provided. Needed: {reqParameters} Provided: {len(args)}")


def stopWav(address: str, *args):
    reqParameters = 0 # Number of paramters expected
    
    if len(args) == reqParameters:

        id = int(address[1]) # Get device id from address str
        device = devices[id] # Get device dict from devices based on ID

        mode = device["mode"]

        if mode == "serial":
            port = device["serialPort"]
            command = f"SWF 0\n"
            sendSerial(command, port)
        elif mode == "network":
            print("Network logic")
    elif debugMode:
        print(f"Invalid number of paramters provided. Needed: {reqParameters} Provided: {len(args)}")

print("\n")
for item in devices:
    id = item

    print(f"Mapping device with id {id}")

    dispatcher.map(f"/{id}/set/parameter", setParameter)
    dispatcher.map(f"/{id}/set/parameter/relative", setParameterRel)

    dispatcher.map(f"/{id}/set/volume", setVolume)
    dispatcher.map(f"/{id}/set/volume/relative", setVolumeRel)

    dispatcher.map(f"/{id}/wav/play", playWav)
    dispatcher.map(f"/{id}/wav/stop", stopWav)
    


print("OSC server starting")
server.serve_forever()