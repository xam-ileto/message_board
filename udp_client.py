import socket
import json

server_host='172.16.0.20' #IP address of the server CSNET01
dest_port=8009 #Assigned port number
# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

try:
    command = input("Input your command: ")
    
    username = input("Input your username: ")
    
    msg = input("Input your message (input anything if registering/deregistering): ")
    
    # format input as json
    
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
            "message": msg # contains additional message
        }
    message = json.dumps(json_data)
    
    # send data to server
    sent = sock.sendto(bytes(message,"utf-8"), (server_host,dest_port)) 
    
    # receive server response
    print ('waiting to receive')
    data, server = sock.recvfrom(1024)
    
    # print server response
    json_obj = json.loads(data)
    print(json_obj)
finally:
    #close socket
    print ('closing socket')
sock.close()