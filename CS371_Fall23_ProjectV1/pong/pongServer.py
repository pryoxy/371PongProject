# =================================================================================================
# Contributing Authors:	    Joshna Sravanthi Kurra, Tharanie Subramaniam
# Email Addresses:          jku230@uky.edu, tsu241@uky.edu
# Date:                     <The date the file was last edited>
# Purpose:                  Acts as the server
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

import socket
import threading
import json

def handle_client(client_socket, counter):
    paddle_side = ""
    if(counter == 0):
        paddle_side = "left"
    else:
        paddle_side = "right"

    # send client which side it is 
    client_socket.send(paddle_side.encode('utf-8'))

    # receive the client data 
    client_data = client_socket.recv(1024)
    client_array.append(client_data)

    # decode the client data 
    dict_data = json.loads(client_data.decode('utf-8'))
    sync_array.append(dict_data['sync'])

    # compare the sync values
    if(sync_array[0] > sync_array[1]):              # if left has a higher sync 
        client_socket.send(client_array[0])
    else:                                           # if right has a higher sync
        client_socket.send(client_array[1])         

    client_socket.close()

# creating the server 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# binding it to an address
server.bind(("localhost", 12321))
server.listen(2)

# store client data 
client_array = []
sync_array = []

# client handling
counter = 0
while counter < 2:
    client_socket, client_address = server.accept()
    client_handler = threading.Thread(target=handle_client, args=(client_socket, counter))
    client_handler.start()
    counter += 1

# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games
