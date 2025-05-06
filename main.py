from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.dispatcher import Dispatcher

ip = "0.0.0.0"
port = 1337


# Shorthand for server and dispatcher
dispatcher = Dispatcher()
server = BlockingOSCUDPServer((ip,port), dispatcher)

def test(address, *args):
    value = args[0]
    # value = value * 1023
    print(f"Address: {address} \n Value: {value}")

dispatcher.map("/set/parameter", test)
dispatcher.map("/set/volume", test)
dispatcher.map("/set/parameter/relative", test)
dispatcher.map("/set/volume/relative", test)

server.serve_forever()


