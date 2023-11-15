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

def handle_client(client_socket, player_id):
    paddle_side = ""
    if(player_id == 0):
        paddle_side = "left"
    else:
        paddle_side = "right"

    # send client which side it is 
    client_socket.send(paddle_side.encode('utf-8'))

    while True: 
        # receive the client data 
        client_data = client_socket.recv(1024).decode('utf-8')
        str_data = client_data.split(",")
        if paddle_side == "left":
            client_array[0] = client_data
            sync_array[0] = str_data[0]
        else:
            client_array[1] = client_data
            sync_array[1] = str_data[0]

        # compare the sync values
        if((sync_array[0] != None) and (sync_array[1] != None)):
            if(sync_array[0] > sync_array[1]):              # if left has a higher sync 
                client_socket.send(client_array[0].encode('utf-8'))
            else:                                           # if right has a higher sync
                client_socket.send(client_array[1].encode('utf-8'))         

    client_socket.close()

# creating the server 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# binding it to an address
server.bind(("localhost", 12321))
server.listen(2)

# store client data 
client_array = [None] * 2
# overwrite the sync variables, not append them each time
sync_array = [None] * 2

# client handling
player_id = 0
while player_id < 2:
    client_socket, client_address = server.accept()
    client_handler = threading.Thread(target=handle_client, args=(client_socket, player_id))
    client_handler.start()
    player_id += 1

# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games
