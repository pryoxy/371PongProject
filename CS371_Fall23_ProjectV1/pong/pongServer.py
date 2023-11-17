# =================================================================================================
# Contributing Authors:	    Joshna Sravanthi Kurra, Tharanie Subramaniam
# Email Addresses:          jku230@uky.edu, tsu241@uky.edu
# Date:                     <The date the file was last edited>
# Purpose:                  Acts as the server for the pong game
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

import socket
import threading
import json
from threading import Lock

def handle_client(client_socket: socket.socket, player_id: int) -> None:
    # Author: Joshna Sravanthi Kurra, Tharanie Subramaniam
    # Purpose: Handling the clients, including assigning paddle side and synchronizing
    # Arguments:
    # client_socket: A socket object that gives the socket of current thread
    # player_id: An integer that indicates which paddle a client is
    # Pre: a thread is created
    # Post: data is sent back and forth between server and client

    # Assign paddle sides based on player_id
    paddle_side = ""
    if(player_id == 0):         
        paddle_side = "left"
        client_socket.send(paddle_side.encode('utf-8'))    
    else:
        paddle_side = "right"
        client_socket.send(paddle_side.encode('utf-8'))  

    # dictionary to store most up-to-date game data
    game_data = {
        "l_score": 0,
        "r_score": 0,
        "player_x": 0,
        "player_y": 0,
        "ball_x": 0,
        "ball_y": 0,
        "opponent_x": 0,
        "opponent_y": 0,
        "paddle_side": "",
        "sync": 0
    }
    
    # go into a loop of synchronization 
    while True: 
        mutex = Lock()
        # receive and decode the client data 
        buffer = client_socket.recv(1024)           
        client_data = buffer.decode('utf-8')
        dict_data = {}
        dict_data = json.loads(client_data)
        if not dict_data:
            break
        mutex.acquire()

        # populate each player's data
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
                player_2['paddle_side'] = dict_data['paddle_side']
                player_2['sync'] = dict_data['sync']
        finally:
            mutex.release()
        
        if(player_id == 0):        # compare sync values for thread 1
            if(dict_data['sync'] > player_2['sync']):       # if player_1 has a higher sync 
                game_data['ball_x'] = dict_data['ball_x']
                game_data['ball_y'] = dict_data['ball_y']
                game_data['player_x'] = dict_data['player_x']
                game_data['player_y'] = dict_data['player_y']
                game_data['opponent_x'] = player_2['player_x']
                game_data['opponent_y'] = player_2['player_y']
                game_data['l_score'] = dict_data['l_score']
                game_data['r_score'] = dict_data['r_score']
                game_data['paddle_side'] = dict_data['paddle_side']
                game_data['sync'] = dict_data['sync'] 
            else:                                           # if player_2 has a higher sync 
                # populate game_dat2'
                game_data['ball_x'] = player_2['ball_x'] 
                game_data['ball_y'] = player_2['ball_y'] 
                game_data['player_x'] = player_2['player_x']
                game_data['player_y'] = player_2['player_y']
                game_data['opponent_x'] = player_1['player_x']
                game_data['opponent_y'] = player_1['player_y']
                game_data['l_score'] = player_2['l_score']
                game_data['r_score'] = player_2['r_score']
                game_data['paddle_side'] = player_2['paddle_side']
                game_data['sync'] = player_2['sync']
        else:                       # compare sync values for thread 2
            if(dict_data['sync'] > player_1['sync']):       # if player_2 has a higher sync 
                game_data['ball_x'] = dict_data['ball_x']
                game_data['ball_y'] = dict_data['ball_y']
                game_data['player_x'] = dict_data['player_x']
                game_data['player_y'] = dict_data['player_y']
                game_data['opponent_x'] = player_1['player_x']
                game_data['opponent_y'] = player_1['player_y']
                game_data['l_score'] = dict_data['l_score']
                game_data['r_score'] = dict_data['r_score']
                game_data['paddle_side'] = dict_data['paddle_side']
                game_data['sync'] = dict_data['sync'] 
            else:                                           # if player_1 has a higher sync 
                # populate game_dat2'
                game_data['ball_x'] = player_1['ball_x'] 
                game_data['ball_y'] = player_1['ball_y'] 
                game_data['player_x'] = player_1['player_x']
                game_data['player_y'] = player_1['player_y']
                game_data['opponent_x'] = player_2['player_x']
                game_data['opponent_y'] = player_2['player_y']
                game_data['l_score'] = player_1['l_score']
                game_data['r_score'] = player_1['r_score']
                game_data['paddle_side'] = player_1['paddle_side']
                game_data['sync'] = player_1['sync']

        # encode and send updated data 
        data_to_send = json.dumps(game_data)
        client_socket.send(data_to_send.encode('utf-8'))

    client_socket.close()

# creating the server 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# binding it to an address
server.bind(("10.113.32.61", 12321))
server.listen(2)

# dictionary to store player_1 data
player_1 = {
    "l_score": 0,
    "r_score": 0,
    "player_x": 0,
    "player_y": 0,
    "ball_x": 0,
    "ball_y": 0,
    "opponent_x": 0,
    "opponent_y": 0,
    "paddle_side": "",
    "sync": 0
}

# dictionary to store player_2 data
player_2 = {
    "l_score": 0,
    "r_score": 0,
    "player_x": 0,
    "player_y": 0,
    "ball_x": 0,
    "ball_y": 0,
    "opponent_x": 0,
    "opponent_y": 0,
    "paddle_side": "",
    "sync": 0
}

# client handling: create threads
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