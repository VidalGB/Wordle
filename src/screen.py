import pygame as Pg
from pygame.locals import *
import operator
from src.logic import *
from src.events import *
from main import *


# Game screen function
def screen(windows):
  logging.info('pintando pantalla')

# Window resize
  width, height, widthRest, heightRest = window(windows.get_width(), windows.get_height())

# Pos Buttons
  posCheck = (widthRest + pixel(65, 'w'), heightRest + pixel(81.5, 'h'))
  posCross = (widthRest + pixel(80, 'w'), heightRest + pixel(81.5, 'h'))

#   Box measurements
  boxWidth = pixel(proportion[lenWord][2], 'w')
  boxHeight = pixel(proportion[lenWord][3], 'h')
  spaceWidth = pixel(proportion[lenWord][0], 'w')
  spaceHeight = pixel(proportion[lenWord][1], 'h')
  rectWidth = pixel(proportion[lenWord][4], 'w')

#   Update font size and text input, buttons measurements
  font = Pg.font.Font('data/font/CascadiaMonoPL.ttf', int(boxHeight))
  textInput = Pg.Rect(widthRest + pixel(12, 'w'), heightRest + pixel(81.5, 'h'), rectWidth, boxHeight)
  checkButton = Pg.Rect(posCheck[0], posCheck[1], boxWidth, boxHeight)
  crossButton = Pg.Rect(posCross[0], posCross[1], boxWidth, boxHeight)
  lineIcon = {'checkButton':[(posCheck[0]+pixel(3,'w'),posCheck[1]+pixel(6,'h')),(posCheck[0]+pixel(5,'w'),posCheck[1]+pixel(9,'h')),(posCheck[0]+pixel(5,'w'),posCheck[1]+pixel(9,'h')),(posCheck[0]+pixel(9,'w'),posCheck[1]+pixel(2,'h'))],'crossButton':[(posCross[0]+pixel(3,'w'),posCross[1]+pixel(2,'h')),(posCross[0]+pixel(8,'w'),posCross[1]+pixel(9,'h')),(posCross[0]+pixel(3,'w'),posCross[1]+pixel(9,'h')),(posCross[0]+pixel(8,'w'),posCross[1]+pixel(2,'h'))]}

#   Game screen
  if gameScreen:
    logging.info('pantalla de juego')
#   Paint the Window and letters, boxes and text input
    windows.fill(colorBackground)
    for row in range(5):
      for column in range(lenWord):
        if row == Attempts:
          Pg.draw.rect(windows, colorActive, Pg.Rect(widthRest + spaceWidth*(column+1) + (spaceWidth + boxWidth)*column, heightRest + spaceHeight*(row+1) + (spaceHeight + boxHeight)*row, boxWidth, boxHeight))
        elif row > Attempts:
          Pg.draw.rect(windows, colors['gray'], Pg.Rect(widthRest + spaceWidth*(column+1) + (spaceWidth + boxWidth)*column, heightRest + spaceHeight*(row+1) + (spaceHeight + boxHeight)*row, boxWidth, boxHeight))
        else:
          listColor = rowColor[row]
          listLyrics = rowLyrics[row]
          Pg.draw.rect(windows, colors[listColor[column]], Pg.Rect(widthRest + spaceWidth*(column+1) + (spaceWidth + boxWidth)*column, heightRest + spaceHeight*(row+1) + (spaceHeight + boxHeight)*row, boxWidth, boxHeight))

#     lyrics
          fontText = font.render(listLyrics[column], True, colorFont)
          windows.blit(fontText, (pixel(2.4, 'w') + widthRest + spaceWidth*(column+1) + (spaceWidth + boxWidth)*column, (heightRest + spaceHeight*(row+1) + (spaceHeight + boxHeight)*row) - pixel(1, 'h'), boxWidth, boxHeight))

#   Draw text input, check button box and cross button box
    Pg.draw.rect(windows, colorInput, textInput)
    Pg.draw.rect(windows, colorCheck, checkButton)
    Pg.draw.rect(windows, colorCross, crossButton)

#   Draw icon line
    List = ['green', 'red']
    m = 0
    for icon in lineIcon:
      for n in range(0, operator.length_hint(lineIcon[icon]), 2):
        Pg.draw.line(windows, colors[List[m]], lineIcon[icon][n], lineIcon[icon][n+1], width = int(pixel(2, 'w')))
      m += 1

#   Paint the text of the input text
    userText = userText.upper()
    fontText = font.render(userText, True, colorFont)
    windows.blit(fontText, (textInput.x + pixel(1, 'w'), textInput.y - pixel(1, 'h')))

#   Create config icon
    posCircle = (widthRest + width - pixel(3.5, 'w'), heightRest + height - pixel(3.5, 'h'))
    Pg.draw.circle(windows, colorConfig, posCircle, (pixel(1.5, 'w') + pixel(1.5, 'h')))

#     load gear image
    gear = Pg.image.load('./data/image/gear.png')
    gear = Pg.transform.scale(gear, (pixel(4, 'w'), pixel(4, 'h')))
    windows.blit(gear, (posCircle[0] - pixel(2, 'w'), posCircle[1] - pixel(2, 'h')))

#   Create the icon check word and its counter
#     Draw text the counter
    font = Pg.font.Font('data/font/CascadiaMonoPL.ttf', int(pixel(5, 'h')))
    textHits = font.render(str(hits), True, colorFont)
    windows.blit(textHits, (widthRest + pixel(22.22, 'w'), heightRest + pixel(93.5, 'h')))

#     Load check image
    check = Pg.image.load('./data/image/check.png')
    check = Pg.transform.scale(check, (pixel(6, 'w'), pixel(6, 'h')))
    windows.blit(check, (widthRest + pixel(16.66, 'w'), heightRest + pixel(93.5, 'h')))

#   End screen
  if endScreen:
    logging.info('pantalla de fin')

#     Create the transparent surface
    background = Pg.Surface((windows.get_width(), windows.get_height()))
    background.set_alpha(200)
    background.fill(colorBackground)
    windows.blit(background, (0,0))

#   Paint text the end game
    font = Pg.font.Font('data/font/CascadiaMonoPLItalic.ttf', int(boxHeight))
    text = dicEndText[idiom]
    if win:
      fontText = font.render(text[1], True, colorFont)
      windows.blit(fontText, (widthRest + pixel(25, 'w'), heightRest + pixel(25, 'h')))
    else:
      fontText = font.render(text[0], True, colorFont)
      windows.blit(fontText, (widthRest + pixel(25, 'w'), heightRest + pixel(25, 'h')))

#    Create the icon check word and its counter
#     Draw text the counter
    font = Pg.font.Font('data/font/CascadiaMonoPL.ttf', int(pixel(5, 'h')))
    textHits = font.render(str(hits), True, colorFont)
    windows.blit(textHits, (widthRest + pixel(50, 'w'), heightRest + pixel(40, 'h')))

#     Load check image
    check = Pg.image.load('./data/image/check.png')
    check = Pg.transform.scale(check, (pixel(6, 'w'), pixel(6, 'h')))
    windows.blit(check, (widthRest + pixel(43.47826087, 'w'), heightRest + pixel(40, 'h')))

#   Create the icon star record and its counter
#     Draw text the counter
    font = Pg.font.Font('data/font/CascadiaMonoPL.ttf', int(pixel(5, 'h')))
    textRecord = font.render(str(record), True, colorFont)
    windows.blit(textRecord, (widthRest + pixel(50, 'w'), heightRest + pixel(46, 'h')))

#     Load star image
    star = Pg.image.load('./data/image/star.png')
    star = Pg.transform.scale(star, (pixel(6, 'w'), pixel(6, 'h')))
    windows.blit(star, (widthRest + pixel(43.47826087, 'w'), heightRest + pixel(46, 'h')))

#    Paint text to continue play
    if idiom == 'en':
      posWidthText = pixel(19, 'w')
    else:
      posWidthText = pixel(11.11, 'w')
      text = dicPlayText[idiom]
      font = Pg.font.Font('data/font/CascadiaMonoPLBold.ttf', int(pixel(3, 'h')))
    playText = font.render(text, True, colorFont)
    windows.blit(playText, (widthRest + posWidthText, heightRest + pixel(94, 'h')))

#   Configuration screen
  if configScreen:
    windows.fill(colorBackground)

#   Update window
  Pg.display.flip()


# Screen functions
#   Window resize function
def window(actualWidth, actualHeight):
  widthRest = 0
  heightRest = 0
  height = actualHeight
  width = actualWidth
  if actualHeight > actualWidth:
    height = actualWidth
    width = actualWidth
    heightRest = (actualHeight - actualWidth)/2
  elif actualWidth > actualHeight:
    height = actualHeight
    width = actualHeight
    widthRest = (actualWidth - actualHeight)/2
  return (width, height, widthRest, heightRest)

#   Function for calculate screen pixels by percentage
def pixel(por, obj):
  if obj == 'w':
    return por*width/100
  elif obj == 'h':
    return por*height/100