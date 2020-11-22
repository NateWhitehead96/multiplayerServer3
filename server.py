import random
import socket
import time
from _thread import *
import threading
from datetime import datetime
import json
import requests

clients_lock = threading.Lock()
connected = 0
# first one to update all players, 2nd one to get all players
urlUpdate = "https://hmg9l717g9.execute-api.us-east-2.amazonaws.com/default/updatePlayers"
urlGetAll = "https://tmxw2nq9z8.execute-api.us-east-2.amazonaws.com/default/GetAllPlayers"
queryparams = {'player-id' : 'player'}, {'rating' : 'r'}

response = requests.get(urlGetAll)

message = json.load(response)

matchID = 0

clients = {}

def connectionLoop(sock):
   while True:
      data, addr = sock.recvfrom(1024)
      data = str(data)
      if addr in clients:
         if 'heartbeat' in data:
            clients[addr] = {}
            clients[addr]['lastBeat'] = datetime.now()
      else:
         if 'connect' in data:
            clients[addr] = {}
            clients[addr]['lastBeat'] = datetime.now()
            clients[addr]['color'] = 0
            clients[addr]['position'] = {"X": 0, "Y": 0, "Z": 0}
            message = {"cmd": 0,"player":{"id":str(addr)}}
            m = json.dumps(message)
            for c in clients:
               sock.sendto(bytes(m,'utf8'), (c[0],c[1]))
         if 'hearbeat' in data:
            clients[addr] = {}
            clients[addr]['lastBeat'] = datetime.now()
            clients[addr]['color'] = 0
            clients[addr]['position'] = {"X": 0, "Y": 0, "Z": 0}
            message = {"cmd": 0,"player":{"id":str(addr)}}
            m = json.dumps(message)
            for c in clients:
               sock.sendto(bytes(m,'utf8'), (c[0],c[1]))

def cleanClients():
   while True:
      for c in list(clients.keys()):
         if (datetime.now() - clients[c]['lastBeat']).total_seconds() > 5:
            print('Dropped Client: ', c)
            clients_lock.acquire()
            del clients[c]
            clients_lock.release()
      time.sleep(1)

def gameLoop(sock):
   while True:
      GameState = {"cmd": 1, "players": []}
      clients_lock.acquire()
      print (clients)
      for c in clients:
         player = {}
         clients[c]['color'] = {"R": random.random(), "G": random.random(), "B": random.random()}
         clients[c]['position']
         player['id'] = str(c)
         player['color'] = clients[c]['color']
         player['position'] = clients[c]['position']
         GameState['players'].append(player)
      s=json.dumps(GameState)
      print(s)
      for c in clients:
         sock.sendto(bytes(s,'utf8'), (c[0],c[1]))
      clients_lock.release()
      time.sleep(1/60.0)

def main():
   port = 12345
   s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   s.bind(('', port))
   start_new_thread(gameLoop, (s,))
   start_new_thread(connectionLoop, (s,))
   start_new_thread(cleanClients,())
   while True:
      time.sleep(1)

if __name__ == '__main__':
   main()
