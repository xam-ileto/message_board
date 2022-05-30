import socket
import json

#Set variables for listening address and listening port
listening_address='172.16.0.20' #Put in the IP address of server CSNET01
listening_port=8009 #Put in the assigned port address 7

# Create a UDP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

# Bind the socket to the port
print ("starting up on %s port %d" %(listening_address, listening_port))
sock.bind((listening_address, listening_port)) 

userlist = [] # Store usernames

while True:
    #waiting for data to arrive, this is a blocking function
    print ('\nwaiting to receive message')
    data, address = sock.recvfrom(1024) 

    print ('received %s bytes from %s' % (len(data), address))
    print (data.decode("utf-8")) 
    
    json_obj = json.loads(data)
    cmd = json_obj('message').get('command')

    if data:
        # TODO if statements for return codes
        # For register commands
        if (cmd == "msg"):
            print ("message command")         
            username = json_obj('message').get('username')
            user_msg = json_obj('message').get('message')
            
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
                 json_data = {
                    "command": "ret_code",
                    "code_no": 401 # User not accepted
                }                    
            
        # For register commands
        elif (cmd == "register" or cmd == "deregister"): 
            print ("de/register command") 
            username = json_obj('message').get('username')
           
            if (cmd == "register"):
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
                    json_data = {
                        "command": "ret_code",
                        "code_no": 401 # User not accepted
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
                    json_data = {
                        "command": "ret_code",
                        "code_no": 401 # User not accepted
                    }         
        # Unknown Command
        else: 
            print ("unknown command") 
            json_data = {
                "command": "ret_code",
                "code_no": 301 # Command unknown
            }
        # TODO format return code as json
        response = json.dumps(json_data)
        
    #echo back received data from connecting client
        sent = sock.sendto(bytes(response,"utf-8"), address)
        print ('sent %s bytes back to %s' % (sent, address))
