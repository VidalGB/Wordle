#Python v3.9.2 more information and dependencies, read requirements.txt
#Syntax camelCase


#Imports
import os

# Hide welcome print in pygame
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as Pg
from pygame.locals import *
import random
import operator
import math
import sys
import csv
import ast
import logging


#Path search
def path(relativePath):
  logging.info(f'buscando la ruta de {relativePath}')
  try:
    bacePath = sys._MEIPASS
  except Exception:
    bacePath = os.path.abspath(".")
  return os.path.join(bacePath, relativePath)


#Read and write files functions
def read(obj):
  logging.info(f'leyendo el archivo "datos.csv", linea: {obj}')
  with open (path('data/data.csv'), 'r', encoding="utf-8") as file:
    content = csv.reader(file, delimiter = ';')
    for line in content:
      if line[0] == obj:
        return line[1]
  file.close()

def write(obj, writer):
  save = []
  n = 0
  with open (path('data/data.csv'), 'r', encoding="utf-8") as file:
    content = csv.reader(file, delimiter = ';')
    for line in content:
      if line[0] == obj:
        del line[1]
        del line[0]
      save.append(line)
    for element in save:
      if element == []:
        del save[n]
      n += 1
  logging.info(f'escribiendo el archivo "datos.csv", linea: {obj}, dato: {writer}')
  with open (path('data/data.csv'), 'w', newline = '') as file:
    write = csv.writer(file, delimiter = ';')
    write.writerows(save)
    write.writerow([obj, writer])
  file.close()


#Logging basic config
logging.basicConfig(level = logging.DEBUG, filename = path('./data/app.log'), filemode = 'w', format = '%(name)s-%(levelname)s: %(message)s')


#Game class, contains three main functions (logic, events, screen) and the functions of the objects
class Game():

  def __init__(self):
    logging.info('estableciendo variables de inicio')

# Set the Gobal variables
    self.userText = ''
    self.rowColor = {}
    self.rowLyrics = {}
    self.attempts = self.hits = 0

    self.idiom = read('idiom')
    self.lenWord = int(read('length'))
    self.record = int(read('record'))

    self.proportion = ast.literal_eval(read('proportion'))
    self.dicLanguage = ast.literal_eval(read('language'))
    self.dicPlayText = ast.literal_eval(read('playText'))
    self.dicEndText = ast.literal_eval(read('endText'))
    self.dicNewRecord = ast.literal_eval(read('recordText'))
    self.listConfigText = ast.literal_eval(read('configText'))
    self.colors = ast.literal_eval(read('colors'))

    self.colorActive = self.colors['lightBlue']
    self.colorPassive = self.colors['gray']
    self.colorInput = self.colorCheck = self.colorCross = self.colorPassive
    self.colorConfig = self.colors['white']

    self.focusText = self.sendText = self.pressCheck = self.pressCross = self.pressConfig = self.win = self.newRecord = self.endScreen = self.configScreen = self.play = False
    self.gameScreen = True
    self.font = Pg.font.Font(path('data/font/CascadiaMonoPL.ttf'), 60)

    logging.info('estableciondo color de la app')

#   Seletc the color app
    if read('color') == 'white':
      self.colorBackground = self.colors['white']
      self.colorFont = self.colors['black']
      self.colorActive = self.colors['lightBlue']
    elif read('color') == 'black':
      self.colorBackground = self.colors['black']
      self.colorFont = self.colors['white']
      self.colorActive = self.colors['blue']


# Function for detect and work to events
  def events(self):
    logging.info('detectando eventos')
    for event in Pg.event.get():

#   Exit events
      if event.type == Pg.QUIT:
        return True

#   Mouse events
      if event.type == Pg.MOUSEBUTTONDOWN:
        self.mouseEvents(event)

#   Keyboard envents
      if event.type == Pg.KEYDOWN:
        if event.key == Pg.K_ESCAPE:
          return True
        self.keyboardEvents(event)
    return False


# Game logic function
  def logic(self):
    logging.info('calculando logica')

#   New game
    if not self.play:
      self.play = self.flagCheckWord = True
      self.newRecord = self.win = False
      self.userText = ''
      self.attempts = 0
      self.rowColor = {}
      self.rowLyrics = {}
      self.randomWord()

#   Control word
    self.corretWord = []
    if self.sendText == True:
      self.controlWord()
      self.colorBoxes()
      self.checkWin()

#   End screen
    if self.attempts == 5 or self.win == True:
      self.endScreen = True
      if not self.win:
        if self.flagCheckWord:
          self.Sound('./data/sound/gameOver.wav')
          if self.hits > 0:
            self.hits = 0
          self.flagCheckWord = False

#   Win
    if self.win:
      if self.flagCheckWord:
        self.Sound('./data/sound/win.wav')
        self.hits += 1
        if self.hits > self.record:
          self.record = self.hits
          write('record', self.record)
          self.newRecord = True
          self.Sound('./data/sound/record.wav')
        self.flagCheckWord = False

#   Press button
    self.pressButton()


# Game screen function
  def screen(self, windows, clock):
    logging.info('pintando pantalla')

#   Window resize
    self.width, self.height, widthRest, heightRest = self.window(windows.get_width(), windows.get_height())

#   Pos Buttons
    posCheck = (widthRest + self.pixel(65, 'w'), heightRest + self.pixel(81.5, 'h'))
    posCross = (widthRest + self.pixel(80, 'w'), heightRest + self.pixel(81.5, 'h'))

#   Box measurements
    boxWidth = self.pixel(self.proportion[self.lenWord][2], 'w')
    boxHeight = self.pixel(self.proportion[self.lenWord][3], 'h')
    spaceWidth = self.pixel(self.proportion[self.lenWord][0], 'w')
    spaceHeight = self.pixel(self.proportion[self.lenWord][1], 'h')
    rectWidth = self.pixel(self.proportion[self.lenWord][4], 'w')

#   Update font size and text input, buttons measurements
    self.font = Pg.font.Font(path('data/font/CascadiaMonoPL.ttf'), int(boxHeight))

    self.textInput = Pg.Rect(widthRest + self.pixel(12, 'w'), heightRest + self.pixel(81.5, 'h'), rectWidth, boxHeight)

    self.checkButton = Pg.Rect(posCheck[0], posCheck[1], boxWidth, boxHeight)
    self.crossButton = Pg.Rect(posCross[0], posCross[1], boxWidth, boxHeight)

    lineIcon = {'checkButton':[(posCheck[0]+self.pixel(3,'w'),posCheck[1]+self.pixel(6,'h')),(posCheck[0]+self.pixel(5,'w'),posCheck[1]+self.pixel(9,'h')),(posCheck[0]+self.pixel(5,'w'),posCheck[1]+self.pixel(9,'h')),(posCheck[0]+self.pixel(9,'w'),posCheck[1]+self.pixel(2,'h'))],'crossButton':[(posCross[0]+self.pixel(3,'w'),posCross[1]+self.pixel(2,'h')),(posCross[0]+self.pixel(8,'w'),posCross[1]+self.pixel(9,'h')),(posCross[0]+self.pixel(3,'w'),posCross[1]+self.pixel(9,'h')),(posCross[0]+self.pixel(8,'w'),posCross[1]+self.pixel(2,'h'))]} # csv file

#   Game screen
    if self.gameScreen:
      logging.info('pantalla de juego')
      self.paintGameScreen(windows, widthRest = widthRest, heightRest = heightRest, posCheck = posCheck, posCross = posCross, boxWidth = boxWidth, boxHeight = boxHeight, spaceWidth = spaceWidth, spaceHeight = spaceHeight, rectWidth = rectWidth, lineIcon = lineIcon)
      self.paintIconGameScreen(windows, widthRest = widthRest, heightRest = heightRest)

#   End screen
    if self.endScreen:
      logging.info('pantalla de fin')
      self.paintEndScreen(windows, widthRest = widthRest, heightRest = heightRest, boxHeight = boxHeight)
      self.paintIconEndScreen(windows, widthRest = widthRest, heightRest = heightRest)

#   Configuration screen
    if self.configScreen:
      self.paintConfigScreen(windows, widthRest = widthRest, heightRest = heightRest)
      self.drawTextConfigScreen(windows, widthRest = widthRest, heightRest = heightRest)

    intFps = str(int(clock.get_fps()))
    fps = self.font.render(intFps, True, self.colorFont)
    windows.blit(fps, (0,0))

#   Update window
    Pg.display.flip()


# Events functions
#   Mouse events
  def mouseEvents(self, event):

#     Click on the check button
    if not self.endScreen:
      if self.checkButton.collidepoint(event.pos):
        if len(self.userText) == int(read('length')):
          self.sendText = True
          self.pressCheck = True

#     Click on the cross button
    if not self.endScreen:
      if self.crossButton.collidepoint(event.pos):
        self.userText = ''
        self.pressCross = True

#     Click on the text input
    if not self.endScreen:
      if self.textInput.collidepoint(event.pos):
        self.focusText = True
      else:
        self.focusText = False

#     Click on the config button
    if not self.endScreen:
      posWidthCircke = (event.pos[0] - self.posCircle[0])**2
      posHeightCircke = (event.pos[1] - self.posCircle[1])**2
      if math.sqrt(posWidthCircke + posHeightCircke) < 15:
        self.pressConfig = True
        self.configScreen = True
        self.gameScreen = False

#   Keyboard envents
  def keyboardEvents(self, event):

#     Key space
    if event.key == Pg.K_SPACE:
      if self.endScreen == True:
        self.endScreen = False
        self.play = False
        self.Sound('./data/sound/keyboardKey.wav')

#     Key enter
    elif event.key == Pg.K_RETURN:
      if self.endScreen == True:
        self.endScreen = False
        self.play = False
        self.Sound('./data/sound/keyboardEnter.wav')
      elif len(self.userText) == int(read('length')):
        self.sendText = True
        self.Sound('./data/sound/keyboardEnter.wav')

#     Key backspace
    elif event.key == Pg.K_BACKSPACE:
      self.userText = self.userText[:-1]
      self.Sound('./data/sound/keyboardKey.wav')

#     Key vocabulary
    else:
      for letre in self.dicLanguage[self.idiom]:
        if letre == event.unicode:
          if self.focusText == True and len(self.userText) +1 <= int(read('length')):
            self.userText += event.unicode
            self.Sound('./data/sound/keyboardKey.wav')


# Logic functions
#   Control word
  def controlWord(self):
    self.sendText = False
    self.userWord = list(self.userText)
    posUserWord = 0
    for lyrics in self.userWord:
      true = 0
      if lyrics in self.ranWord:
        true = 1
        posRanWord = 0
        for letters in self.ranWord:
          if lyrics == letters:
            if posRanWord == posUserWord:
              true = 2
          posRanWord += 1
      letters = lyrics + ':' + str(true)
      self.corretWord.append(letters)
      posUserWord += 1
    self.userText = ''

#   Boxes color and lyrics
  def colorBoxes(self):

#     Color the boxes
    lyrics = []
    for item in self.corretWord:
      if '2' in item:
        lyrics.append('green')
      elif '1' in item:
        lyrics.append('yellow')
      else:
        lyrics.append('red')
      self.rowColor[self.attempts] = lyrics

#     Lyrics the boxes
      letters = []
      for item in self.corretWord:
        List = item.split(':')
        letters.append(List[0])
        self.rowLyrics[self.attempts] = letters
    self.attempts += 1

#   Win check
  def checkWin(self):
    letters = 0
    for item in self.corretWord:
      if '2' in item:
        letters += 1
    if letters == len(self.corretWord):
      self.win = True

#   Press button
  def pressButton(self):

#     Check button
    if not self.pressCheck:
      self.colorCheck = self.colorPassive
    else:
      self.colorCheck = self.colorActive
      self.pressCheck = False

#     Cross button
    if not self.pressCross:
      self.colorCross = self.colorPassive
    else:
      self.colorCross = self.colorActive
      self.pressCross = False

#     Config button
    if not self.pressConfig:
      self.colorConfig = self.colors['white']
    else:
      self.colorConfig = self.colorActive
      self.pressConfig = False

#     Focus on the text input
    if self.focusText:
      self.colorInput = self.colorActive
    else:
      self.colorInput = self.colorPassive

#   Function for get random word
  def randomWord(self):
    self.play = True
    with open (path(f"./data/words/{read('length')}words-{read('idiom')}.txt"), 'r', encoding = "utf-8") as file:
      lines = file.readlines()
      line = ''.join(lines)
      word = line.split('\n')
      max = len(word) - 1

      while True:
        n = random.randint(0, max)
        self.ranWord = word[n]
        logging.debug(f'Numero aleatorio {n}, palabra aleatoria {self.ranWord}')
        wordList = ast.literal_eval(read('wordList'))
        if self.ranWord not in wordList:
          del wordList[0]
          wordList.append(self.ranWord)
          write('wordList', wordList)
          break

      self.ranWord = self.ranWord.upper()
      self.ranWord = list(self.ranWord)
      logging.info(f'Palabra a adivinar "{self.ranWord}"')
      print(self.ranWord)
      file.close()


# Screen functions
#   Window resize function
  def window(self, actualWidth, actualHeight):
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
  def pixel(self, por, obj):
    if obj == 'w':
      return por*self.width/100
    elif obj == 'h':
      return por*self.height/100

#   Piant and draw the element on the game screen
  def paintGameScreen(self, windows, **karg):

#     Paint the Window and letters, boxes and text input
    windows.fill(self.colorBackground)
    for row in range(5):
      for column in range(self.lenWord):
        if row == self.attempts:
          Pg.draw.rect(windows, self.colorActive, Pg.Rect(karg['widthRest'] + karg['spaceWidth']*(column+1) + (karg['spaceWidth'] + karg['boxWidth'])*column, karg['heightRest'] + karg['spaceHeight']*(row+1) + (karg['spaceHeight'] + karg['boxHeight'])*row, karg['boxWidth'], karg['boxHeight']))
        elif row > self.attempts:
          Pg.draw.rect(windows, self.colors['gray'], Pg.Rect(karg['widthRest'] + karg['spaceWidth']*(column+1) + (karg['spaceWidth'] + karg['boxWidth'])*column, karg['heightRest'] + karg['spaceHeight']*(row+1) + (karg['spaceHeight'] + karg['boxHeight'])*row, karg['boxWidth'], karg['boxHeight']))
        else:
          listColor = self.rowColor[row]
          listLyrics = self.rowLyrics[row]
          Pg.draw.rect(windows, self.colors[listColor[column]], Pg.Rect(karg['widthRest'] + karg['spaceWidth']*(column+1) + (karg['spaceWidth'] + karg['boxWidth'])*column, karg['heightRest'] + karg['spaceHeight']*(row+1) + (karg['spaceHeight'] + karg['boxHeight'])*row, karg['boxWidth'], karg['boxHeight']))

#       lyrics
          fontText = self.font.render(listLyrics[column], True, self.colorFont)
          windows.blit(fontText, (self.pixel(2.4, 'w') + karg['widthRest'] + karg['spaceWidth']*(column+1) + (karg['spaceWidth'] + karg['boxWidth'])*column, (karg['heightRest'] + karg['spaceHeight']*(row+1) + (karg['spaceHeight'] + karg['boxHeight'])*row) - self.pixel(1, 'h'), karg['boxWidth'], karg['boxHeight']))

#     Draw text input, check button box and cross button box
    Pg.draw.rect(windows, self.colorInput, self.textInput)
    Pg.draw.rect(windows, self.colorCheck, self.checkButton)
    Pg.draw.rect(windows, self.colorCross, self.crossButton)

#     Draw icon line (check and cross)
    List = ['green', 'red']
    nun = 0
    for icon in karg['lineIcon']:
      for n in range(0, operator.length_hint(karg['lineIcon'][icon]), 2):
        Pg.draw.line(windows, self.colors[List[nun]], karg['lineIcon'][icon][n], karg['lineIcon'][icon][n+1], width = int(self.pixel(2, 'w')))
      nun += 1

#     Paint the text of the input text
    self.userText = self.userText.upper()
    fontText = self.font.render(self.userText, True, self.colorFont)
    windows.blit(fontText, (self.textInput.x + self.pixel(1, 'w'), self.textInput.y - self.pixel(1, 'h')))

#   Piant and draw the Icon on the game screen
  def paintIconGameScreen(self, windows, **karg):

#     Create config icon
    self.posCircle = (karg['widthRest'] + self.width - self.pixel(3.5, 'w'), karg['heightRest'] + self.height - self.pixel(3.5, 'h'))
    Pg.draw.circle(windows, self.colorConfig, self.posCircle, (self.pixel(1.5, 'w') + self.pixel(1.5, 'h')))

#       load gear image
    gear = Pg.image.load('./data/image/gear.png')
    gear = Pg.transform.scale(gear, (self.pixel(4, 'w'), self.pixel(4, 'h')))
    windows.blit(gear, (self.posCircle[0] - self.pixel(2, 'w'), self.posCircle[1] - self.pixel(2, 'h')))

#     Create the icon check word and its counter
#       Draw text the counter
    self.font = Pg.font.Font(path('data/font/CascadiaMonoPL.ttf'), int(self.pixel(5, 'h')))
    textHits = self.font.render(str(self.hits), True, self.colorFont)
    windows.blit(textHits, (karg['widthRest'] + self.pixel(22.22, 'w'), karg['heightRest'] + self.pixel(93.5, 'h')))

#       Load check image
    check = Pg.image.load('./data/image/check.png')
    check = Pg.transform.scale(check, (self.pixel(6, 'w'), self.pixel(6, 'h')))
    windows.blit(check, (karg['widthRest'] + self.pixel(16.66, 'w'), karg['heightRest'] + self.pixel(93.5, 'h')))

#   Piant and draw the element on the end screen
  def paintEndScreen(self, windows, **karg):

#     Create the transparent surface
    self.background = Pg.Surface((windows.get_width(), windows.get_height()))
    self.background.set_alpha(200)
    self.background.fill(self.colorBackground)
    windows.blit(self.background, (0,0))

#     Paint text the end game
    self.font = Pg.font.Font(path('data/font/CascadiaMonoPLItalic.ttf'), int(karg['boxHeight']))
    text = self.dicEndText[self.idiom]
    if self.win:
      fontText = self.font.render(text[1], True, self.colorFont)
      windows.blit(fontText, (karg['widthRest'] + self.pixel(25, 'w'), karg['heightRest'] + self.pixel(25, 'h')))
    else:
      fontText = self.font.render(text[0], True, self.colorFont)
      windows.blit(fontText, (karg['widthRest'] + self.pixel(25, 'w'), karg['heightRest'] + self.pixel(25, 'h')))

#     Paint text to continue play
    if self.idiom == 'en':
      posWidthText = self.pixel(19, 'w')
    else:
      posWidthText = self.pixel(11.11, 'w')
    text = self.dicPlayText[self.idiom]
    self.font = Pg.font.Font(path('data/font/CascadiaMonoPLBold.ttf'), int(self.pixel(3, 'h')))
    playText = self.font.render(text, True, self.colorFont)
    windows.blit(playText, (karg['widthRest'] + posWidthText, karg['heightRest'] + self.pixel(94, 'h')))

#   Piant and draw the Icon on the end screen
  def paintIconEndScreen(self, windows, **karg):

#     Create the icon check word and its counter
#       Draw text the counter
    self.font = Pg.font.Font(path('data/font/CascadiaMonoPL.ttf'), int(self.pixel(5, 'h')))
    textHits = self.font.render(str(self.hits), True, self.colorFont)
    windows.blit(textHits, (karg['widthRest'] + self.pixel(50, 'w'), karg['heightRest'] + self.pixel(40, 'h')))

#       Load check image
    check = Pg.image.load('./data/image/check.png')
    check = Pg.transform.scale(check, (self.pixel(6, 'w'), self.pixel(6, 'h')))
    windows.blit(check, (karg['widthRest'] + self.pixel(43.47826087, 'w'), karg['heightRest'] + self.pixel(40, 'h')))

#     Create the icon star record and its counter
#       Draw text the counter
    self.font = Pg.font.Font(path('data/font/CascadiaMonoPL.ttf'), int(self.pixel(5, 'h')))
    textRecord = self.font.render(str(self.record), True, self.colorFont)
    windows.blit(textRecord, (karg['widthRest'] + self.pixel(50, 'w'), karg['heightRest'] + self.pixel(46, 'h')))

#       Draw text the New Record
    if self.newRecord:
      text = self.dicNewRecord[self.idiom]
      textNewRecord = self.font.render(text, True, self.colorFont)
      windows.blit(textNewRecord, (karg['widthRest'] + self.pixel(53, 'w'), karg['heightRest'] + self.pixel(46, 'h')))

#       Load star image
    star = Pg.image.load('./data/image/star.png')
    star = Pg.transform.scale(star, (self.pixel(6, 'w'), self.pixel(6, 'h')))
    windows.blit(star, (karg['widthRest'] + self.pixel(43.47826087, 'w'), karg['heightRest'] + self.pixel(46, 'h')))

#   Piant and draw the element on the configuration screen
  def paintConfigScreen(self, windows, **karg):
    spaceWidth = self.pixel(1, 'w')
    spaceHeight = self.pixel(2, 'h')

    windows.fill(self.colorBackground)

  def drawTextConfigScreen(self, windows, **karg):
    self.font = Pg.font.Font(path('data/font/CascadiaMonoPLBold.ttf'), int(self.pixel(5, 'h')))

#   Theme text
    textTheme = self.font.render(self.listConfigText[0][self.idiom], True, self.colorFont)
    windows.blit(textTheme, (karg['widthRest'] + self.pixel(15, 'w'), karg['heightRest'] + self.pixel(12, 'h')))

#   Sound text
    textSound = self.font.render(self.listConfigText[2][self.idiom], True, self.colorFont)
    windows.blit(textSound, (karg['widthRest'] + self.pixel(58, 'w'), karg['heightRest'] + self.pixel(12, 'h')))

#   dificulty text
    dificulText = self.font.render(self.listConfigText[4][self.idiom], True, self.colorFont)
    windows.blit(dificulText, (karg['widthRest'] + self.pixel(15, 'w'), karg['heightRest'] + self.pixel(45, 'h')))

#   idiom text
    idiomText = self.font.render(self.listConfigText[6][self.idiom], True, self.colorFont)
    windows.blit(idiomText, (karg['widthRest'] + self.pixel(58, 'w'), karg['heightRest'] + self.pixel(45, 'h')))

    self.font = Pg.font.Font(path('data/font/CascadiaMonoPL.ttf'), int(self.pixel(5, 'h')))

#   Texts Theme
#   Theme light text
    thmeLight = self.font.render(self.listConfigText[1][self.idiom][0], True, self.colorFont)
    windows.blit(thmeLight, (karg['widthRest'] + self.pixel(17, 'w'), karg['heightRest'] + self.pixel(22, 'h')))

#   Theme dark text
    themeDark = self.font.render(self.listConfigText[1][self.idiom][1], True, self.colorFont)
    windows.blit(themeDark, (karg['widthRest'] + self.pixel(17, 'w'), karg['heightRest'] + self.pixel(28, 'h')))

#   Sound text
    soundText = self.font.render(self.listConfigText[3][self.idiom], True, self.colorFont)
    windows.blit(soundText, (karg['widthRest'] + self.pixel(60, 'w'), karg['heightRest'] + self.pixel(22, 'h')))

#   Texts dificulty
#   Easy dificulty text
    easyDificulText = self.font.render(self.listConfigText[5][self.idiom][0], True, self.colorFont)
    windows.blit(easyDificulText, (karg['widthRest'] + self.pixel(17, 'w'), karg['heightRest'] + self.pixel(61, 'h')))

#   Normal dificulty text
    normalDificulText = self.font.render(self.listConfigText[5][self.idiom][1], True, self.colorFont)
    windows.blit(normalDificulText, (karg['widthRest'] + self.pixel(17, 'w'), karg['heightRest'] + self.pixel(67, 'h')))

#   Hard dificulty text
    hardDificulText = self.font.render(self.listConfigText[5][self.idiom][2], True, self.colorFont)
    windows.blit(hardDificulText, (karg['widthRest'] + self.pixel(17, 'w'), karg['heightRest'] + self.pixel(73, 'h')))

#   Extreme dificulty text
    extremeDificulText = self.font.render(self.listConfigText[5][self.idiom][3], True, self.colorFont)
    windows.blit(extremeDificulText, (karg['widthRest'] + self.pixel(17, 'w'), karg['heightRest'] + self.pixel(79, 'h')))

    self.font = Pg.font.Font(path('data/font/CascadiaMonoPL.ttf'), int(self.pixel(3, 'h')))

#   Texts idiom
#   Spanish text
    spanishText = self.font.render(self.listConfigText[7][self.idiom][0], True, self.colorFont)
    windows.blit(spanishText, (karg['widthRest'] + self.pixel(60, 'w'), karg['heightRest'] + self.pixel(61, 'h')))

#   English text
    englishText = self.font.render(self.listConfigText[7][self.idiom][1], True, self.colorFont)
    windows.blit(englishText, (karg['widthRest'] + self.pixel(60, 'w'), karg['heightRest'] + self.pixel(67, 'h')))

#   Portuguese text
    portugueseText = self.font.render(self.listConfigText[7][self.idiom][2], True, self.colorFont)
    windows.blit(portugueseText, (karg['widthRest'] + self.pixel(60, 'w'), karg['heightRest'] + self.pixel(73, 'h')))

#Sound Function
  def Sound(self, sound):
    soundPlay = Pg.mixer.Sound(path(sound))
    print(Pg.mixer.Sound.get_volume(soundPlay))
    Pg.mixer.Sound.play(soundPlay)


#Main function
def main():

# Starting pygame
  logging.info('iniciando pygame')
  Pg.init()

# Select icon for the app
  logo = Pg.image.load(path('./data/image/logo.png'))
  Pg.display.set_icon(logo)

# Window measurements, title selec and mouse config
  windows = Pg.display.set_mode((int(read('width')), int(read('height'))), Pg.RESIZABLE)
  Pg.display.set_caption("Wordle")
  Pg.mouse.set_visible(True)
  clock = Pg.time.Clock()
  gameOver = False
  game = Game()
  logging.info('entrando al bucle principal')
# Game loop
  while not gameOver:
    gameOver = game.events()
    game.logic()
    game.screen(windows, clock)
    clock.tick(60)
  logging.warning('saliendo bucle principal')
  Pg.quit()
  sys.exit()


#Check script main
if __name__ == "__main__":
  logging.warning('iniciando funcioan principal')
  main()