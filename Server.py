import socket
from _thread import *
import pickle

server = "192.168.43.36"
port = 5555

class Player:
  def __init__(self, surface, x, y):
    self.surface = surface
    self.x = x
    self.y = y
    self.w = 16
    self.h = 16
    self.velX = 0
    self.velY = 0
    self.right, self.left, self.up, self.down = False, False, False, False
    self.image = PlayerImage
    self.rect = pygame.Rect(self.x, self.x, self.w, self.h)
    self.dir = 'D'

  def update(self):
    keys = pygame.key.get_pressed()
    if canM:
      if self.right:
        self.velX = 1
        self.dir = 'R'
      elif self.left:
        self.velX = -1
        self.dir = 'L'
      else:
        self.velX = 0
      self.velY += 1
      if self.up:
        self.dir = 'U'
        self.velY = -1
      elif self.down:
        self.velY = 1
        self.dir = 'D'
      else:
        self.velY = 0

    self.rect.x += self.velX
    self.rect.y += self.velY

  def draw(self):
    self.surface.blit(self.image, (self.rect.x - scroll[0], self.rect.y - scroll[1]))
    #pygame.draw.rect(self.surface, (255, 255, 255), self.rect)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
  s.bind((server, port))
except socket.error as e:
  str(e)

s.listen(2)
print("Waiting for a connection, Server started")

players = []

def threadedClient(conn, player):
  conn.send(pickle.dumps(players[player]))
  reply = ""
  while True:
    try:
      data = pickle.loads(conn.recv(2048))
      players[player] = data

      if not data:
        print("Disconnected")
        break
      else:
        if player == 1:
          reply = players[0]
        else:
          reply = players[1]
        print("Received: ", data)
        print("Sending : ", reply)

      conn.sendall(pickle.dumps(reply))
    except:
      break
  print("Lose connection")
  conn.close()

currentPlayer = 0

while True:
  conn, addr = s.accept()
  print("Connected to:", addr)

  start_new_thread(threadedClient, (conn, currentPlayer))
  players.append(Player(display, 0, 0))
  currentPlayer += 1
