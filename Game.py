import pygame
import sys
import csv
import os
from os import path
from abc import ABC, abstractmethod
from copy import deepcopy
pygame.init()
pygame.mouse.set_cursor(pygame.cursors.arrow)

WIDTH = 400
HEIGHT = 300
SCALE = 2
GW, GH = WIDTH*SCALE/1.7, HEIGHT*SCALE/1.7
screen = pygame.display.set_mode((WIDTH*SCALE, HEIGHT*SCALE))
display = pygame.Surface((WIDTH, HEIGHT))
pygame.display.set_caption('PROOP')
clock = pygame.time.Clock()
gmap = []

running = True
tileSize = 16
clicking = False
click = False
removing = False

tileMap = []
clientNumber = 0

def t2l(text, divider):
  List = []
  current = ''
  for char in text:
    if char != divider:
      current += char
    else:
      List.append(current)
      current = ''
  return List

def loadImage(path, ca=False):
  img = pygame.image.load(path).convert()
  if ca: img.convert_alpha()
  img.set_colorkey((0, 0, 0))
  return img

AllImage = None
if path.exists("folder/Texture.png"):
  AllImage = loadImage('folder/Texture.png')
else:
  AllImage = loadImage('data/SimpleTexture.png')
def getTI(x, y):
  return AllImage.subsurface(x*16, y*16, 16, 16)
PlayerImage = None
if path.exists("folder/Player.png"):
  PlayerImage = loadImage('folder/Player.png')
  if PlayerImage.get_width() != 16 and PlayerImage.get_height() != 16:
    print("=]Player image size must be 8x8 pixels!")
    sys.exit()
else:
  PlayerImage = loadImage('data/Player.png')
SelectImage = loadImage('data/Select.png')
SelectImage.set_alpha(100)
FontImage = loadImage('data/Font.png')

Grass0Image = getTI(0, 0)
Grass1Image = getTI(1, 0)
Grass2Image = getTI(0, 1)
Grass3Image = getTI(2, 1)
Grass4Image = getTI(1, 2)
Grass5Image = getTI(4, 0)
Grass6Image = getTI(4, 1)
Soil0Image = getTI(1, 1)
BlockImage = getTI(5, 0)
SignImage = getTI(5, 1)
TestBlockImage = getTI(6, 0)

trueScroll = [0, 0]

canM = True
canP = True

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
    self.speed = 1

  def update(self):
    keys = pygame.key.get_pressed()
    if canM:
      if self.right:
        self.velX = self.speed
        self.dir = 'R'
      elif self.left:
        self.velX = -self.speed
        self.dir = 'L'
      else:
        self.velX = 0
      self.velY += 1
      if self.up:
        self.velY = -self.speed
        self.dir = 'U'
      elif self.down:
        self.velY = self.speed
        self.dir = 'D'
      else:
        self.velY = 0

    self.rect.x += self.velX
    self.rect.y += self.velY

  def draw(self):
    self.surface.blit(self.image, (self.rect.x - scroll[0], self.rect.y - scroll[1]))
    #pygame.draw.rect(self.surface, (255, 255, 255), self.rect)

def GenerateFont(FontImage,FontSpacingMain,TileSize,TileSizeY,color):
    FontSpacing = deepcopy(FontSpacingMain)
    FontOrder = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9','.',':',',','(',')','-','+']
    FontImage = pygame.image.load(FontImage).convert()
    NewSurf = pygame.Surface((FontImage.get_width(),FontImage.get_height())).convert()
    NewSurf.fill(color)
    FontImage.set_colorkey((255,255,255))
    NewSurf.blit(FontImage,(0,0))
    FontImage = NewSurf.copy()
    FontImage.set_colorkey((0, 0, 0))
    num = 0
    for char in FontOrder:
        FontImage.set_clip(pygame.Rect(((TileSize)*num),0,TileSize,TileSizeY))
        CharacterImage = FontImage.subsurface(FontImage.get_clip())
        FontSpacing[char].append(CharacterImage)
        num += 1
    FontSpacing['Height'] = TileSizeY
    return FontSpacing

def ShowText(Text,X,Y,Spacing,WidthLimit,Font,surface,overflow='normal'):
    Text = Text.upper()
    Text += ' '
    OriginalX = X
    OriginalY = Y
    CurrentWord = ''
    if overflow == 'normal':
        for char in Text:
            if char not in [' ','\n']:
                try:
                    Image = Font[str(char)][1]
                    CurrentWord += str(char)
                except KeyError:
                    pass
            else:
                WordTotal = 0
                for char2 in CurrentWord:
                    WordTotal += Font[char2][0]
                    WordTotal += Spacing
                if WordTotal+X-OriginalX > WidthLimit:
                    X = OriginalX
                    Y += Font['Height']
                for char2 in CurrentWord:
                    Image = Font[str(char2)][1]
                    surface.blit(Image,(X,Y))
                    X += Font[char2][0]
                    X += Spacing
                if char == ' ':
                    X += Font['A'][0]
                    X += Spacing
                else:
                    X = OriginalX
                    Y += Font['Height']
                CurrentWord = ''
            if X-OriginalX > WidthLimit:
                X = OriginalX
                Y += Font['Height']
        return X,Y
    if overflow == 'cut all':
        for char in Text:
            if char not in [' ','\n']:
                try:
                    Image = Font[str(char)][1]
                    surface.blit(Image,(X,Y))
                    X += Font[str(char)][0]
                    X += Spacing
                except KeyError:
                    pass
            else:
                if char == ' ':
                    X += Font['A'][0]
                    X += Spacing
                if char == '\n':
                    X = OriginalX
                    Y += Font['Height']
                CurrentWord = ''
            if X-OriginalX > WidthLimit:
                X = OriginalX
                Y += Font['Height']
        return X,Y

font_dat = {'A':[8],'B':[8],'C':[8],'D':[8],'E':[8],'F':[8],'G':[8],'H':[8],'I':[8],'J':[8],'K':[8],'L':[8],'M':[8],'N':[8],'O':[8],'P':[8],'Q':[8],'R':[8],'S':[8],'T':[8],'U':[8],'V':[8],'W':[8],'X':[8],'Y':[8],'Z':[8],
          '0':[8],'1':[8],'2':[8],'3':[8],'4':[8],'5':[8],'6':[8],'7':[8],'8':[8],'9':[8],
          '.':[8],':':[8],',':[8],'(':[8],')':[8],'-':[8],'+':[8]}

font_dat = {'A':[7],'B':[7],'C':[7],'D':[7],'E':[7],'F':[7],'G':[7],'H':[7],'I':[7],'J':[7],'K':[7],'L':[7],'M':[7],'N':[7],'O':[7],'P':[7],'Q':[7],'R':[7],'S':[7],'T':[7],'U':[7],'V':[7],'W':[7],'X':[7],'Y':[7],'Z':[7],
          '0':[7],'1':[7],'2':[7],'3':[7],'4':[7],'5':[7],'6':[7],'7':[7],'8':[7],'9':[7],
          '.':[7],':':[7],',':[7],'(':[7],')':[7],'-':[7],'+':[7]}

myFont = GenerateFont('data/Font.png', deepcopy(font_dat), 8, 8, (255, 255, 255))

# ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9','.',':',',','(',')','-','+']

def dist(text, x, y):
  ShowText(text, x, y, 1, 500, myFont, display, overflow='normal')

class Block(ABC):
  def __init__(self, surface, x, y):
    self.surface = surface
    self.x = x
    self.y = y
    self.w = 16
    self.h = 16
    self.name = ''
    self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
    self.solid = False

  @abstractmethod
  def update(self):
    pass

  @abstractmethod
  def draw(self):
    pass

class SimpleBlock(Block):
  def __init__(self, surface, x, y):
    super().__init__(surface, x, y)
    self.image = BlockImage
    self.solid = True
    self.name = 'block'

  def update(self):
    pass

  def draw(self):
    self.surface.blit(self.image, (self.rect.x-scroll[0], self.rect.y-scroll[1]))

class Sign(Block):
  def __init__(self, surface, x, y):
    super().__init__(surface, x, y)
    self.image = SignImage
    self.solid = False
    self.name = 'sign'

  def update(self):
    pass

  def draw(self):
    self.surface.blit(self.image, (self.rect.x-scroll[0], self.rect.y-scroll[1]))

class TestBlock(Block):
  def __init__(self, surface, x, y):
    super().__init__(surface, x, y)
    self.image = TestBlockImage
    self.solid = True
    self.name = 'test'

  def update(self):
    pass

  def draw(self):
    self.surface.blit(self.image, (self.rect.x-scroll[0], self.rect.y-scroll[1]))

def save():
  ntm = tileMap.copy()
  tileMap.clear()
  for i in ntm:
    tileMap.append(i)
  with open('map.txt', 'w') as map:
    map.truncate(0)
    map.seek(0)
    for tile in tileMap:
      map.write(tile.name + ',' + str(hex(tile.x)) + ',' + str(hex(tile.y)) + ';')

def loadMap(m):
  file = open(m, 'r')
  fm = file.read()
  file.close()
  tls = t2l(fm, ';')
  ntls = []
  for i in tls:
    etls = i.split(',')
    while tls.count(i) > 1:
      tls.remove(i)
    for j in etls:
      if etls[0] == 'block':
        ntls.append(SimpleBlock(display, int(etls[1], 0), int(etls[2], 0)))
      elif etls[0] == 'sign':
        ntls.append(Sign(display, int(etls[1], 0), int(etls[2], 0)))
      elif etls[0] == 'testBlock':
        ntls.append(TestBlock(display, int(etls[1], 0), int(etls[2], 0)))
  return ntls

if os.path.exists('map.txt'):
  tileMap = loadMap('map.txt')
else:
  tileMap = []

def readcsv(filename):
  map = []
  with open(os.path.join(filename)) as data:
    data = csv.reader(data, delimiter=',')
    for row in data:
      map.append(list(row))
  return map

def renderMap():
  tileRect = []
  gmap = readcsv('data/TestMap.csv')
  x, y = 0, 0
  for row in gmap:
    x = 0
    for tile in row:
      if tile == '0':
        display.blit(Grass0Image, (x * tileSize - scroll[0], y * tileSize - scroll[1]))
      if tile == '1':
        display.blit(Grass1Image, (x * tileSize - scroll[0], y * tileSize - scroll[1]))
      if tile == '4':
        display.blit(Grass5Image, (x * tileSize - scroll[0], y * tileSize - scroll[1]))
      if tile == '20':
        display.blit(Grass2Image, (x * tileSize - scroll[0], y * tileSize - scroll[1]))
      if tile == '21':
        display.blit(Soil0Image, (x * tileSize - scroll[0], y * tileSize - scroll[1]))
      if tile == '22':
        display.blit(Grass3Image, (x * tileSize - scroll[0], y * tileSize - scroll[1]))
      if tile == '24':
        display.blit(Grass6Image, (x * tileSize - scroll[0], y * tileSize - scroll[1]))
      if tile == '41':
        display.blit(Grass4Image, (x * tileSize - scroll[0], y * tileSize - scroll[1]))

      if tile != '-1':
        tileRect.append(pygame.Rect(x * tileSize - scroll[0], y * tileSize - scroll[1], tileSize, tileSize))
      x += 1
    y += 1

tiles = ['block', 'sign', 'testBlock']
currentTile = tiles[0]

player = Player(display, 20, 20)

while running:
  display.fill((0, 0, 0))

  trueScroll[0] += (player.rect.x - trueScroll[0] - WIDTH/2-8)
  if trueScroll[0] < 0: trueScroll[0] = 0
  elif trueScroll[0] > 368: trueScroll[0] = 368
  trueScroll[1] += (player.rect.y - trueScroll[1] - HEIGHT/2-8)
  if trueScroll[1] < 0: trueScroll[1] = 0
  elif trueScroll[1] > 368: trueScroll[1] = 368
  scroll = trueScroll.copy()
  scroll[0] = int(scroll[0])
  scroll[1] = int(scroll[1])

  if player.rect.left <= 0: player.rect.left = 0
  if player.rect.right >= 768: player.rect.right = 768

  if player.rect.top <= 0: player.rect.top = 0
  if player.rect.bottom >= 768: player.rect.bottom = 768

  renderMap()

  for tile in tileMap:
    tile.update()
    tile.draw()
    if tile.rect.colliderect(player.rect):
      if tile.solid:
        if player.rect.right == tile.rect.left+1 and player.velX > 0:
          player.rect.right = tile.rect.left
        elif player.rect.left == tile.rect.right-1 and player.velX < 0:
          player.rect.left = tile.rect.right

        if player.rect.bottom == tile.rect.top+1 and player.velY > 0:
          player.rect.bottom = tile.rect.top
        elif player.rect.top == tile.rect.bottom-1 and player.velY < 0:
          player.rect.top = tile.rect.bottom

  MX, MY = pygame.mouse.get_pos()
  MX = int(MX/2)
  MY = int(MY/2)
  MouseR = pygame.Rect(MX-scroll[0],MY-scroll[1],2,2)
  MX = int(round((scroll[0]+MX-8)/tileSize,0))
  MY = int(round((scroll[1]+MY-8)/tileSize,0))
  display.blit(SelectImage, (MX*16-scroll[0], MY*16-scroll[1]))
  if canP:
    if clicking:
      if currentTile == tiles[0]:
        tileMap.append(SimpleBlock(display, MX*16, MY*16))
      elif currentTile == tiles[1]:
        tileMap.append(Sign(display, MX*16, MY*16))
      elif currentTile == tiles[2]:
        tileMap.append(TestBlock(display, MX*16, MY*16))
    if removing:
      for tm in tileMap:
        if MX*16 == tm.x and MY*16 == tm.y:
          tileMap.remove(tm)

  click = False
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      save()
      running = False
      pygame.quit()
      sys.exit()
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        save()
        running = False
        pygame.quit()
        sys.exit()
      if event.key == pygame.K_d:
        player.right = True
      if event.key == pygame.K_a:
        player.left = True
      if event.key == pygame.K_w:
        player.up = True
      if event.key == pygame.K_s:
        player.down = True

      if event.key == pygame.K_1:
        currentTile = tiles[0]
      elif event.key == pygame.K_2:
        currentTile = tiles[1]
      elif event.key == pygame.K_3:
        currentTile = tiles[2]
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_d:
        player.right = False
      if event.key == pygame.K_a:
        player.left = False
      if event.key == pygame.K_w:
        player.up = False
      if event.key == pygame.K_s:
        player.down = False
    if event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 1:
        clicking = True
        click = True
      if event.button == 3:
        removing = True
    if event.type == pygame.MOUSEBUTTONUP:
      if event.button == 1:
        clicking = False
      if event.button == 3:
        removing = False

    if player.x < 0: player.x = 0
    if player.x+player.w > 48*16: player.x = 48*16

    if player.y < 0: player.y = 0
    if player.y+player.h > 48*16: player.y = 48*16

  player.update()
  player.draw()

  dist('Version\nTest 1', 32, 32)

  surf = pygame.transform.scale(display, (WIDTH*SCALE, HEIGHT*SCALE))
  screen.blit(surf, (0, 0))
  pygame.display.update()
  clock.tick(60)
