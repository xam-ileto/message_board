import socket
import json

#Set variables for server address and destination port
server_host='172.16.0.20' #IP address of the server CSNET01
dest_port=8009 #Input assigned port number for server 7
# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

try:
    # TODO ask input from user
    command = input("Input your command: ")
    
    username = input("Input your username: ")
    
    msg = input("Input your message (input anything if registering/deregistering): ")
    
    # TODO format as json
    # if register/deregister
    if (command != "msg"):
        json_data = {
            "command": command,
            "username": username
        }
    else:
        # if posting message
        json_data = {
            "command": command,
            "username": username,
            "message": msg
        }
    message = json.dumps(json_data)
    
    # Send data, string has to be sent as 'bytes' as string in Python is inUnicode format
    print('sending "%s"' % message)
    sent = sock.sendto(bytes(message,"utf-8"), (server_host,dest_port)) 
    
    # waiting for server to send data back, this is blocking function
    print ('waiting to receive')
    data, server = sock.recvfrom(1024)
    print ('received "%s"' % data.decode("utf-8")) 
    
    # TODO print server echo
finally:
    #close socket
    print ('closing socket')
sock.close()