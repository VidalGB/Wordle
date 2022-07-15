import pygame as Pg
from pygame.locals import *
import math
from main import *
from src.screen import *
from src.logic import *


# Function for detect and work to events
def events():
  logging.info('detectando eventos')
  for event in Pg.event.get():

#   Exit events
    if event.type == Pg.QUIT:
      return True

#   Mouse events
    if event.type == Pg.MOUSEBUTTONDOWN:

#     click on the check button
      if not endScreen:
        if checkButton.collidepoint(event.pos):
          if len(userText) == int(read('length')):
            sendText = True
            pressCheck = True

#       Click on the cross button
        if crossButton.collidepoint(event.pos):
          userText = ''
          pressCross = True

#       Click on the text input
        if textInput.collidepoint(event.pos):
          focusText = True
        else:
          focusText = False

#       Click on the config button
        posWidthCircke = (event.pos[0] - posCircle[0])**2
        posHeightCircke = (event.pos[1] - posCircle[1])**2
        if math.sqrt(posWidthCircke + posHeightCircke) < 15:
          pressConfig = True
          configScreen = True
          gameScreen = False


#   Keyboard envents
    if event.type == Pg.KEYDOWN:
      if event.key == Pg.K_ESCAPE:
        return True
      elif event.key == Pg.K_SPACE:
        if endScreen == True:
          endScreen = False
          game = False
      elif event.key == Pg.K_RETURN:
        if endScreen == True:
          endScreen = False
          game = False
        elif len(userText) == int(read('length')):
          sendText = True
      elif event.key == Pg.K_BACKSPACE:
        userText = userText[:-1]
      else:
        for letre in dicLanguage[idiom]:
          if letre == event.unicode:
            if focusText == True and len(userText) +1 <= int(read('length')):
              userText += event.unicode
  return False