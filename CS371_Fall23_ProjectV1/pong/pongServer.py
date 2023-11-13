# =================================================================================================
# Contributing Authors:	    Joshna Sravanthi Kurra, Tharanie Subramaniam
# Email Addresses:          jku230@uky.edu, tsu241@uky.edu
# Date:                     <The date the file was last edited>
# Purpose:                  Acts as the server
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

import socket
import threading
counter = 0; 
def handle_client(client_socket, client_address):
    if(counter == 1):
         paddle_side = "left"
    else:
        paddle_side = "right"

    counter += 1;
    
    paddle.send 



# creating the server 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# binding it to an address
server.bind(("localhost", 12321))
server.listen(2)

# wait for a connection
client_socket, client_address = server.accept()
data = client_socket.recv(1024)
print(f"Received: {data.decode('utf-8')} from {client_address}")

# # store the client game states

# # client handlers

client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
client_handler.start()

# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games


