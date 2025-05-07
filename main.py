from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.dispatcher import Dispatcher

ip = "0.0.0.0"
port = 1337


# Shorthand for server and dispatcher
dispatcher = Dispatcher()
server = BlockingOSCUDPServer((ip,port), dispatcher)



# Serial communication function, send messages to serial device
def sendSerial(message: str):
    print(f"Message: {message}")





# SPR (set parameter) functions
def setParameter(index: int, value: int):
    commandStr = f"SPR 0 {index} {value}\n"
    sendSerial(commandStr)

def setParameterHandler(address, *args):
    if len(args) == 2:
        setParameter(index = int(args[0]), value = int(args[1]))
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
        print(f"Command: {address} {args[0]} {args[1]}")
        setVolume(index = int(args[0]), value = int(args[1]))
    else:
        print(f"Incorrect OSC arguments passed! Required: 2 Passed: {len(args)}")




# Address mapping
dispatcher.map("/set/parameter", setParameterHandler)
dispatcher.map("/set/volume", setVolumeHandler)



print("OSC server started")
server.serve_forever()
