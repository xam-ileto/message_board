import socket
import json

listening_address='172.16.0.20' #IP address of the server CSNET01
listening_port=8009 #Assigned port number

# Create a UDP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

# Bind the socket to port
print ("starting up on %s port %d" %(listening_address, listening_port))
sock.bind((listening_address, listening_port)) 

userlist = [] # Store usernames
print("waiting to receive message")
    
while True:
    data, address = sock.recvfrom(1024) 

    json_obj = json.loads(data)     # object that gets the client data 
    command = json_obj["command"]   # gets client command
    username = json_obj["username"] # gets client username

    if data:
        # TODO delete
        print(json_obj)
        # For message commands
        if (command == "msg"):
            user_msg = json_obj["message"]       
            
            if (username == "" or user_msg == ""): # Inputs may be empty
                json_data = {
                    "command": "ret_code",
                    "code_no": 201 # Command parameters incomplete
                } 
            elif (userlist.count(username) == 0): # User does not exist
                 json_data = {
                    "command": "ret_code",
                    "code_no": 501 # User not registered
                }
            else: # Command Execute Success!

                print("from " + username + " : " + user_msg)
                
                json_data = {
                    "command": "ret_code",
                    "code_no": 401 # Command accepted
                }                    
            
        # For register and deregister commands
        elif (command == "register" or command == "deregister"):
            if (command == "register"):
                if (username == ""): # Input may be empty
                    json_data = {
                        "command": "ret_code",
                        "code_no": 201 # Command parameters incomplete
                    } 
                elif (userlist.count(username) == 1): # User already exists
                    json_data = {
                        "command": "ret_code",
                        "code_no": 502 # User account exists
                    }
                else: # Command Execute Success!
                    userlist.append(username)
                    
                    print("Users in message board: ", end="")
                    print(userlist)
                    
                    json_data = {
                        "command": "ret_code",
                        "code_no": 401 # Command accepted
                    }  
            else: # (cmd == "deregister")
                if (username == ""): # Input may be empty
                    json_data = {
                        "command": "ret_code",
                        "code_no": 201 # Command parameters incomplete
                    } 
                elif (userlist.count(username) == 0): # User does not exist
                    json_data = {
                        "command": "ret_code",
                        "code_no": 501 # User not registered
                    }
                else: # Command Execute Success!
                    userlist.remove(username)

                    print("User " + username + " exiting...")
                    print("Users in message board: ", end="")
                    print(userlist)
                    
                    json_data = {
                        "command": "ret_code",
                        "code_no": 401 # Command accepted
                    }         
        # Unknown Command
        else: 
            json_data = {
                "command": "ret_code",
                "code_no": 301 # Command unknown
            }

        response = json.dumps(json_data)
        
        #echo back received data from connecting client
        sent = sock.sendto(bytes(response,"utf-8"), address)
