import socket
import json

# server_host='172.16.0.20' #IP address of the server CSNET01
dest_port=8009 #Assigned port number
# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

# function to print outputs in client console
def print_output(command, ret_code):
    if (ret_code == 201):
        print("Task failed. Parameters incomplete.")
    elif (ret_code == 301): 
        print("Task failed. Command unknown.")
    elif (ret_code == 401): # if task was successful
        if (command == "register"):
            print("Registered successfully.")
        elif command == "deregister":
            print("Disconnecting.")
        else: # command == msg
            print("Message sent successfully.")
    elif (ret_code == 501):
        print("Task failed. User is not registered.")
    else: # (ret_code == 502): user already exists
        print("User account already exists in this chat room!")
        print("Unsuccessful registration. Exiting...")
    

try:
    server_host = input("Enter IP address of message board server: ")
    
    username = input("Enter preferred username: ")
    
    # REGISTER USER
    json_initial1 = {
            "command": "register",
            "username": username
        }
    
    json_sent1 = json.dumps(json_initial1)
    
    # send data to server
    sent = sock.sendto(bytes(json_sent1,"utf-8"), (server_host,dest_port))
    
    # receive server response
    data, server = sock.recvfrom(1024)
    json_returned1 = json.loads(data)
    ret_code = json_returned1["code_no"]
    
    # TODO delete
    print(json_returned1)
    print_output(json_initial1["command"], json_returned1["code_no"])
    
    # repeat while unregistered
    while (ret_code != 401):
        username = input("Enter preferred username: ")
    
        # register again
        json_initial1 = {
                "command": "register",
                "username": username
            }
        
        json_sent1 = json.dumps(json_initial1)
        
        # send data to server
        sent = sock.sendto(bytes(json_sent1,"utf-8"), (server_host,dest_port))
        
        # receive server response
        data, server = sock.recvfrom(1024)
        json_returned1 = json.loads(data)
        ret_code = json_returned1["ret_code"]
        
        print_output(json_initial1["command"], json_returned1["code_no"])
    
    
    # SEND MSG/ DEREGISTER USER
    msg = input("Enter message: ")
    
    while(msg != "bye"): # keep posting messages
        json_initial2 = {
            "command": "msg",
            "username": username,
            "message": msg # contains additional message
        }
        
        json_sent2 = json.dumps(json_initial2)
    
        # send data to server
        sent = sock.sendto(bytes(json_sent2,"utf-8"), (server_host,dest_port))
        
        data, server = sock.recvfrom(1024)
        json_returned2 = json.loads(data)
    
        # TODO delete
        print(json_returned2)
        print_output(json_initial2["command"], json_returned2["code_no"])
        
        msg = input("Enter message: ")
    
    # DEREGISTER
    json_initial3 = {
            "command": "deregister",
            "username": username,
        }
        
    json_sent3 = json.dumps(json_initial3)
    
    # send data to server
    sent = sock.sendto(bytes(json_sent3,"utf-8"), (server_host,dest_port))
    
    data, server = sock.recvfrom(1024)
    json_returned3 = json.loads(data)
    
    # TODO delete
    print(json_returned3)
    print_output(json_initial3["command"], json_returned3["code_no"])
        
finally:
    #close socket
    print ('closing socket')
sock.close()