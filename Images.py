import pygame

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
  if PlayerImage.get_width() != 8 and PlayerImage.get_height() != 8:
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