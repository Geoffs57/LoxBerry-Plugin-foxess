#############################################################################
# Note this script is not used in the working plugin but comes in handy to
# test the Loxone Configuration of Virtual UDP Inputs with some static data
# 
# Can be used in conjunction with UDP Monitor in Loxone Config to check messages
# are being sent, received and interpreted correctly by the miniserver
# 
############################################################################# 
import socket
import json
from datetime import datetime

# Define the UDP IP address and port to send to
UDP_IP = "192.168.1.50"
UDP_PORT = 7000

# construct dictionary
now = datetime.now()
currentdate = now.strftime("%d-%m-%Y")
currenttime = now.strftime("%H:%M:%S")
# Create a dictionary to send
data = {
    'dat':currentdate,
    'tim':currenttime,
    'con':0.59,
    'gin':0,
    'gxp':2,
    'gen':4.29,
    'bat':0.09,
    'soc':98
    }

# Serialize the dictionary to a JSON string
message = json.dumps(data)

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    # Send the JSON string to the specified IP and port
    sock.sendto(message.encode(), (UDP_IP, UDP_PORT))
    print(f"Sent UDP packet to {UDP_IP}:{UDP_PORT}: {message}")
finally:
    # Close the socket
    sock.close()
