import random
import socket
import time
from _thread import *
import threading
from datetime import datetime
import json
import requests
import sys

urlUpdate = "https://hmg9l717g9.execute-api.us-east-2.amazonaws.com/default/updatePlayers"
urlGetAll = "https://97i3wr7bo1.execute-api.us-east-2.amazonaws.com/default/getPlayers"
queryparams = {'player-id' : 'player'}, {'rating' : 'r'}

f = open('multiplayerfile', 'w')

numGames = input("How many games do you want to play?")
sys.stdout = f
#if get match request run local 3 player coop game

for x in range(0, int(numGames)):
    
    print('Game:' + str(x))

    response = requests.get(urlGetAll)

    responseBody = json.loads(response.content)
#this gets all the player info
    items = responseBody['Items']
# get 3 random players
    temp1 = random.randrange(0, 10)
    temp2 = random.randrange(0, 10)
    temp3 = random.randrange(0, 10)

    players = [temp1, temp2, temp3]
# print out what players we're using
    print(items[temp1]['player-id'] + ' ' + items[temp1]['rating'])
    print(items[temp2]['player-id'] + ' ' + items[temp2]['rating'])
    print(items[temp3]['player-id'] + ' ' + items[temp3]['rating'])

    averageRating = (float(items[temp1]['rating']) + float(items[temp2]['rating']) + float(items[temp3]['rating'])) / 3
    print('The average rating is ' + str(averageRating))

#game loop picking 0-2 where 0 is always the winner
    winner = random.randrange(0, 2)
    print('The winner is ' + items[players[winner]]['player-id'])
#player 1 is the winner!
    newRatingWinner = float(items[players[winner]]['rating']) + (1 - float(items[players[winner]]['rating']) / averageRating) * 100
    newRatingLoser1 = float(items[players[(winner + 1) % 3]]['rating']) + (0 - float(items[players[(winner + 1) % 3]]['rating']) / averageRating) * 10
    newRatingLoser2 = float(items[players[(winner + 2) % 3]]['rating']) + (0 - float(items[players[(winner + 2) % 3]]['rating']) / averageRating) * 10

    print(items[players[winner]]['player-id'] + ' ' + str(newRatingWinner))
    print(items[players[(winner + 1) % 3]]['player-id'] + ' ' + str(newRatingLoser1))
    print(items[players[(winner + 2) % 3]]['player-id'] + ' ' + str(newRatingLoser2))

# updating winner
#queryparams = {'player-id' : items[players[winner]]['player-id'], 'rating' : str(newRatingWinner)}
    newRequest = urlUpdate + '?player-id='+items[players[winner]]['player-id']+'&rating='+str(newRatingWinner)
    response = requests.put(newRequest)
    responseBody = json.loads(response.content)
    #print(responseBody)
# updating loser 1
#queryparams = {'player-id' : items[players[(winner + 1) % 3]]['player-id'], 'rating' : str(newRatingLoser1)}
    newRequest = urlUpdate + '?player-id='+items[players[(winner + 1) % 3]]['player-id']+'&rating='+str(newRatingLoser1)
    response = requests.put(newRequest)
#print(response)
# updating loser 2
#queryparams = {'player-id' : items[players[(winner + 2) % 3]]['player-id'], 'rating' : str(newRatingLoser1)}
    newRequest = urlUpdate + '?player-id='+items[players[(winner + 2) % 3]]['player-id']+'&rating='+str(newRatingLoser2)
    response = requests.put(newRequest)
#print(response)

#close file
f.close()

# grab random player from ec2
# if enough players run game loop x times
# players roll 1-6, highest wins
# send your player data to server for update
# algo is the 3 players ratings averaged,
# 1 if win - player rating / average rating * 100 added to player rating
# 0 if loss - player rating / average rating * 10 added to player rating