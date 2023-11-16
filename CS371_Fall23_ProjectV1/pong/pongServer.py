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
from threading import Lock

def handle_client(client_socket, player_id):
    paddle_side = ""
    if(player_id == 0):         # player_id = 0: left 
        paddle_side = "left"
        client_socket.send(paddle_side.encode('utf-8'))     # send the first client its paddle side
    else:
        paddle_side = "right"
        client_socket.send(paddle_side.encode('utf-8'))     # send the second client its paddle side
        # client_socket.send("go".encode('utf-8'))            # send a go message to first client
        # client_socket_1.send("go".encode('utf-8'))

    game_data = {
        "l_score": 0,
        "r_score": 0,
        "player_x": 0,
        "player_y": 0,
        "ball_x": 0,
        "ball_y": 0,
        "opponent_x": 0,
        "opponent_y": 0,
        "paddle_move": "",
        "paddle_side": "",
        "sync": 0
    }
    while True: 
        mutex = Lock()
        # receive the client data 
        buffer = client_socket.recv(1024)           # getting the game state from the client for the first time
        client_data = buffer.decode('utf-8')
        dict_data = {}
        dict_data = json.loads(client_data)
        if not dict_data:
            break
        mutex.acquire()
        try:
            if paddle_side == "left":
                player_1['ball_x'] = dict_data['ball_x']
                player_1['ball_y'] = dict_data['ball_y']
                player_1['player_x'] = dict_data['player_x']
                player_1['player_y'] = dict_data['player_y']
                player_1['opponent_x'] = dict_data['opponent_x']
                player_1['opponent_y'] = dict_data['opponent_y']
                player_1['l_score'] = dict_data['l_score']
                player_1['r_score'] = dict_data['r_score']
                player_1['paddle_move'] = dict_data['paddle_move']
                player_1['paddle_side'] = dict_data['paddle_side']
                player_1['sync'] = dict_data['sync']
            else:
                player_2['ball_x'] = dict_data['ball_x']
                player_2['ball_y'] = dict_data['ball_y']
                player_2['player_x'] = dict_data['player_x']
                player_2['player_y'] = dict_data['player_y']
                player_2['opponent_x'] = dict_data['opponent_x']
                player_2['opponent_y'] = dict_data['opponent_y']
                player_2['l_score'] = dict_data['l_score']
                player_2['r_score'] = dict_data['r_score']
                player_2['paddle_move'] = dict_data['paddle_move']
                player_2['paddle_side'] = dict_data['paddle_side']
                player_2['sync'] = dict_data['sync']
        finally:
            mutex.release()
        
        if(player_id == 0):         # left paddle
            if(dict_data['sync'] > player_2['sync']):   
                player_1['ball_x'] = dict_data['ball_x']
                player_1['ball_y'] = dict_data['ball_y']
                player_1['player_x'] = dict_data['player_x']
                player_1['player_y'] = dict_data['player_y']
                player_1['opponent_x'] = dict_data['opponent_x']
                player_1['opponent_y'] = dict_data['opponent_y']
                player_1['l_score'] = dict_data['l_score']
                player_1['r_score'] = dict_data['r_score']
                player_1['paddle_move'] = dict_data['paddle_move']
                player_1['paddle_side'] = dict_data['paddle_side']
                player_1['sync'] = dict_data['sync'] 
            else:
                # populate game_dat2'
                game_data['ball_x'] = player_2['ball_x'] 
                game_data['ball_y'] = player_2['ball_y'] 
                game_data['player_x'] = player_2['player_x']
                game_data['player_y'] = player_2['player_y']
                game_data['opponent_x'] = player_2['opponent_x']
                game_data['opponent_y'] = player_2['opponent_y']
                game_data['l_score'] = player_2['l_score']
                game_data['r_score'] = player_2['r_score']
                game_data['paddle_move'] = player_2['paddle_move']
                game_data['paddle_side'] = player_2['paddle_side']
                game_data['sync'] = player_2['sync']
        else:                       # right paddle
            if(dict_data['sync'] > player_2['sync']):
                # populate game data 
            else:
                # populate game data 

        # compare the sync values
        if(player_1['sync'] and player_2['sync']):
            if(player_1['sync'] > player_2['sync']):              # if left has a higher sync 
                client_socket.send(client_array[0].encode('utf-8'))     # send the client the game state with the higher sync value 
            else:                                           # if right has a higher sync
                client_socket.send(client_array[1].encode('utf-8'))       # send the client the game state with the higher sync value  

    client_socket.close()

# creating the server 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# binding it to an address
server.bind(("localhost", 12321))
server.listen(2)

# # store the sockets 
# socket_array = [None] * 2
# store client data 
client_array = [None] * 2
# overwrite the sync variables, not append them each time
sync_array = [None] * 2

# player 1 data 
player_1 = {
    "l_score": 0,
    "r_score": 0,
    "player_x": 0,
    "player_y": 0,
    "ball_x": 0,
    "ball_y": 0,
    "opponent_x": 0,
    "opponent_y": 0,
    "paddle_move": "",
    "paddle_side": "",
    "sync": 0
}

# player 2 data 
player_2 = {
    "l_score": 0,
    "r_score": 0,
    "player_x": 0,
    "player_y": 0,
    "ball_x": 0,
    "ball_y": 0,
    "opponent_x": 0,
    "opponent_y": 0,
    "paddle_move": "",
    "paddle_side": "",
    "sync": 0
}
# client handling
# do separate lines for each thread
player_id = 0
client_socket_1, client_address_1 = server.accept()
client_handler_1 = threading.Thread(target=handle_client, args=(client_socket_1, player_id))
player_id += 1

client_socket_2, client_address_2 = server.accept()
client_handler_2 = threading.Thread(target=handle_client, args=(client_socket_2, player_id))

client_handler_1.start()
client_handler_2.start()

client_handler_1.join()
client_handler_2.join()

# while player_id < 2:
#     client_socket, client_address = server.accept()
#     client_handler = threading.Thread(target=handle_client, args=(client_socket, player_id))
#     client_handler.start()
#     player_id += 1

# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games
