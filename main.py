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


# logging basic config
logging.basicConfig(level = logging.DEBUG, filename = path('./data/app.log'), filemode = 'w', format = '%(name)s-%(levelname)s: %(message)s')


#Game class, contains three main functions (logic, events, screen) and the functions of the objects
class Game(object):

  def __init__(self):

# Set the Gobal variables
    logging.info('estableciendo variables de inicio')
    self.userText = ''
    self.Attempts = 0
    self.hits = 0
    self.idiom = read('idiom')
    self.record = int(read('record'))
    self.rowColor = {}
    self.rowLyrics = {}
    self.colors = ast.literal_eval(read('colors'))
    self.colorActive = self.colors['lightBlue']
    self.colorPassive = self.colors['gray']
    self.colorInput = self.colorPassive
    self.colorCheck = self.colorPassive
    self.colorCross = self.colorPassive
    self.colorConfig = self.colors['white']
    self.focusText = False
    self.sendText = False
    self.pressCheck = False
    self.pressCheck = False
    self.pressCross = False
    self.pressConfig = False
    self.win = False
    self.newRecord = False
    self.endScreen = False
    self.configScreen = False
    self.gameScreen = True
    self.game = False
    self.font = Pg.font.Font(path('data/font/CascadiaMonoPL.ttf'), 60)
    self.proportion = ast.literal_eval(read('proportion'))
    self.dicLanguage = ast.literal_eval(read('language'))
    self.dicPlayText = ast.literal_eval(read('playText'))
    self.dicEndText = ast.literal_eval(read('endText'))
    self.dicNewRecord = ast.literal_eval(read('recordText'))
    self.lenWord = int(read('length'))

    logging.info('estableciondo color de la app')
# Seletc the color app
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

#     click on the check button
        if not self.endScreen:
          if self.checkButton.collidepoint(event.pos):
            if len(self.userText) == int(read('length')):
              self.sendText = True
              self.pressCheck = True

#       Click on the cross button
          if self.crossButton.collidepoint(event.pos):
            self.userText = ''
            self.pressCross = True

#       Click on the text input
          if self.textInput.collidepoint(event.pos):
            self.focusText = True
          else:
            self.focusText = False

#       Click on the config button
          posWidthCircke = (event.pos[0] - self.posCircle[0])**2
          posHeightCircke = (event.pos[1] - self.posCircle[1])**2
          if math.sqrt(posWidthCircke + posHeightCircke) < 15:
            self.pressConfig = True
            self.configScreen = True
            self.gameScreen = False


#   Keyboard envents
      if event.type == Pg.KEYDOWN:
        if event.key == Pg.K_ESCAPE:
          return True
        elif event.key == Pg.K_SPACE:
          if self.endScreen == True:
            self.endScreen = False
            self.game = False
            self.Sound('./data/sound/keyboardKey.wav')
        elif event.key == Pg.K_RETURN:
          if self.endScreen == True:
            self.endScreen = False
            self.game = False
            self.Sound('./data/sound/keyboardEnter.wav')
          elif len(self.userText) == int(read('length')):
            self.sendText = True
            self.Sound('./data/sound/keyboardEnter.wav')
        elif event.key == Pg.K_BACKSPACE:
          self.userText = self.userText[:-1]
          self.Sound('./data/sound/keyboardKey.wav')
        else:
          for letre in self.dicLanguage[self.idiom]:
            if letre == event.unicode:
              if self.focusText == True and len(self.userText) +1 <= int(read('length')):
                self.userText += event.unicode
                self.Sound('./data/sound/keyboardKey.wav')
    return False


# Game logic function
  def logic(self):
    logging.info('calculando logica')

#   New game
    if not self.game:
      self.game = True
      self.newRecord = False
      self.win = False
      self.userText = ''
      self.randomWord()
      self.rowColor = {}
      self.rowLyrics = {}
      self.Attempts = 0
      self.flagCheckWord = True

#   Control word
    self.corretWord = []
    if self.sendText == True:
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
#     Color the boxes
      lyrics = []
      for item in self.corretWord:
        if '2' in item:
          lyrics.append('green')
        elif '1' in item:
          lyrics.append('yellow')
        else:
          lyrics.append('red')
        self.rowColor[self.Attempts] = lyrics

#     Lyrics the boxes
        letters = []
        for item in self.corretWord:
          List = item.split(':')
          letters.append(List[0])
          self.rowLyrics[self.Attempts] = letters
      self.Attempts += 1

#   Win check
      letters = 0
      for item in self.corretWord:
        if '2' in item:
          letters += 1
      if letters == len(self.corretWord):
        self.win = True

#   End screen
    if self.Attempts == 5 or self.win == True:
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

#   Focus on the text input
    if self.focusText:
      self.colorInput = self.colorActive
    else:
      self.colorInput = self.colorPassive


# Game screen function
  def screen(self, windows):
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
    lineIcon = {'checkButton':[(posCheck[0]+self.pixel(3,'w'),posCheck[1]+self.pixel(6,'h')),(posCheck[0]+self.pixel(5,'w'),posCheck[1]+self.pixel(9,'h')),(posCheck[0]+self.pixel(5,'w'),posCheck[1]+self.pixel(9,'h')),(posCheck[0]+self.pixel(9,'w'),posCheck[1]+self.pixel(2,'h'))],'crossButton':[(posCross[0]+self.pixel(3,'w'),posCross[1]+self.pixel(2,'h')),(posCross[0]+self.pixel(8,'w'),posCross[1]+self.pixel(9,'h')),(posCross[0]+self.pixel(3,'w'),posCross[1]+self.pixel(9,'h')),(posCross[0]+self.pixel(8,'w'),posCross[1]+self.pixel(2,'h'))]}

#   Game screen
    if self.gameScreen:
      logging.info('pantalla de juego')
#   Paint the Window and letters, boxes and text input
      windows.fill(self.colorBackground)
      for row in range(5):
        for column in range(self.lenWord):
          if row == self.Attempts:
            Pg.draw.rect(windows, self.colorActive, Pg.Rect(widthRest + spaceWidth*(column+1) + (spaceWidth + boxWidth)*column, heightRest + spaceHeight*(row+1) + (spaceHeight + boxHeight)*row, boxWidth, boxHeight))
          elif row > self.Attempts:
            Pg.draw.rect(windows, self.colors['gray'], Pg.Rect(widthRest + spaceWidth*(column+1) + (spaceWidth + boxWidth)*column, heightRest + spaceHeight*(row+1) + (spaceHeight + boxHeight)*row, boxWidth, boxHeight))
          else:
            listColor = self.rowColor[row]
            listLyrics = self.rowLyrics[row]
            Pg.draw.rect(windows, self.colors[listColor[column]], Pg.Rect(widthRest + spaceWidth*(column+1) + (spaceWidth + boxWidth)*column, heightRest + spaceHeight*(row+1) + (spaceHeight + boxHeight)*row, boxWidth, boxHeight))

#     lyrics
            fontText = self.font.render(listLyrics[column], True, self.colorFont)
            windows.blit(fontText, (self.pixel(2.4, 'w') + widthRest + spaceWidth*(column+1) + (spaceWidth + boxWidth)*column, (heightRest + spaceHeight*(row+1) + (spaceHeight + boxHeight)*row) - self.pixel(1, 'h'), boxWidth, boxHeight))

#   Draw text input, check button box and cross button box
      Pg.draw.rect(windows, self.colorInput, self.textInput)
      Pg.draw.rect(windows, self.colorCheck, self.checkButton)
      Pg.draw.rect(windows, self.colorCross, self.crossButton)

#   Draw icon line
      List = ['green', 'red']
      m = 0
      for icon in lineIcon:
        for n in range(0, operator.length_hint(lineIcon[icon]), 2):
          Pg.draw.line(windows, self.colors[List[m]], lineIcon[icon][n], lineIcon[icon][n+1], width = int(self.pixel(2, 'w')))
        m += 1

#   Paint the text of the input text
      self.userText = self.userText.upper()
      fontText = self.font.render(self.userText, True, self.colorFont)
      windows.blit(fontText, (self.textInput.x + self.pixel(1, 'w'), self.textInput.y - self.pixel(1, 'h')))

#   Create config icon
      self.posCircle = (widthRest + self.width - self.pixel(3.5, 'w'), heightRest + self.height - self.pixel(3.5, 'h'))
      Pg.draw.circle(windows, self.colorConfig, self.posCircle, (self.pixel(1.5, 'w') + self.pixel(1.5, 'h')))

#     load gear image
      gear = Pg.image.load('./data/image/gear.png')
      gear = Pg.transform.scale(gear, (self.pixel(4, 'w'), self.pixel(4, 'h')))
      windows.blit(gear, (self.posCircle[0] - self.pixel(2, 'w'), self.posCircle[1] - self.pixel(2, 'h')))

#   Create the icon check word and its counter
#     Draw text the counter
      self.font = Pg.font.Font(path('data/font/CascadiaMonoPL.ttf'), int(self.pixel(5, 'h')))
      textHits = self.font.render(str(self.hits), True, self.colorFont)
      windows.blit(textHits, (widthRest + self.pixel(22.22, 'w'), heightRest + self.pixel(93.5, 'h')))

#     Load check image
      check = Pg.image.load('./data/image/check.png')
      check = Pg.transform.scale(check, (self.pixel(6, 'w'), self.pixel(6, 'h')))
      windows.blit(check, (widthRest + self.pixel(16.66, 'w'), heightRest + self.pixel(93.5, 'h')))

#   End screen
    if self.endScreen:
      logging.info('pantalla de fin')

#     Create the transparent surface
      self.background = Pg.Surface((windows.get_width(), windows.get_height()))
      self.background.set_alpha(200)
      self.background.fill(self.colorBackground)
      windows.blit(self.background, (0,0))

#     Paint text the end game
      self.font = Pg.font.Font(path('data/font/CascadiaMonoPLItalic.ttf'), int(boxHeight))
      text = self.dicEndText[self.idiom]
      if self.win:
        fontText = self.font.render(text[1], True, self.colorFont)
        windows.blit(fontText, (widthRest + self.pixel(25, 'w'), heightRest + self.pixel(25, 'h')))
      else:
        fontText = self.font.render(text[0], True, self.colorFont)
        windows.blit(fontText, (widthRest + self.pixel(25, 'w'), heightRest + self.pixel(25, 'h')))

#     Create the icon check word and its counter
#       Draw text the counter
      self.font = Pg.font.Font(path('data/font/CascadiaMonoPL.ttf'), int(self.pixel(5, 'h')))
      textHits = self.font.render(str(self.hits), True, self.colorFont)
      windows.blit(textHits, (widthRest + self.pixel(50, 'w'), heightRest + self.pixel(40, 'h')))

#       Load check image
      check = Pg.image.load('./data/image/check.png')
      check = Pg.transform.scale(check, (self.pixel(6, 'w'), self.pixel(6, 'h')))
      windows.blit(check, (widthRest + self.pixel(43.47826087, 'w'), heightRest + self.pixel(40, 'h')))

#     Create the icon star record and its counter
#       Draw text the counter
      self.font = Pg.font.Font(path('data/font/CascadiaMonoPL.ttf'), int(self.pixel(5, 'h')))
      textRecord = self.font.render(str(self.record), True, self.colorFont)
      windows.blit(textRecord, (widthRest + self.pixel(50, 'w'), heightRest + self.pixel(46, 'h')))

#       Draw text the New Record
      if self.newRecord:
        text = self.dicNewRecord[self.idiom]
        textNewRecord = self.font.render(text, True, self.colorFont)
        windows.blit(textNewRecord, (widthRest + self.pixel(53, 'w'), heightRest + self.pixel(46, 'h')))

#       Load star image
      star = Pg.image.load('./data/image/star.png')
      star = Pg.transform.scale(star, (self.pixel(6, 'w'), self.pixel(6, 'h')))
      windows.blit(star, (widthRest + self.pixel(43.47826087, 'w'), heightRest + self.pixel(46, 'h')))

#     Paint text to continue play
      if self.idiom == 'en':
        posWidthText = self.pixel(19, 'w')
      else:
        posWidthText = self.pixel(11.11, 'w')
      text = self.dicPlayText[self.idiom]
      self.font = Pg.font.Font(path('data/font/CascadiaMonoPLBold.ttf'), int(self.pixel(3, 'h')))
      playText = self.font.render(text, True, self.colorFont)
      windows.blit(playText, (widthRest + posWidthText, heightRest + self.pixel(94, 'h')))

#   Configuration screen
    if self.configScreen:
      windows.fill(self.colorBackground)

#   Update window
    Pg.display.flip()


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


# Function for get random word
  def randomWord(self):
    self.game = True
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


# Sound Function
  def Sound(self, sound):
    soundPlay = Pg.mixer.Sound(path(sound))
    Pg.mixer.Sound.play(soundPlay)


#Main function
def main():

#   Starting pygame
  logging.info('iniciando pygame')
  Pg.init()

#   Select icon for the app
  logo = Pg.image.load(path('./data/image/logo.png'))
  Pg.display.set_icon(logo)

#    Window measurements, title selec and mouse config
  windows = Pg.display.set_mode((int(read('width')), int(read('height'))), Pg.RESIZABLE)
  Pg.display.set_caption("Wordle")
  Pg.mouse.set_visible(True)
  clock = Pg.time.Clock()
  gameOver = False
  game = Game()
  logging.info('entrando al bucle principal')
#   Game loop
  while not gameOver:
    gameOver = game.events()
    game.logic()
    game.screen(windows)
    clock.tick(60)
  logging.warning('saliendo bucle principal')
  Pg.quit()
  sys.exit()


#Check script main
if __name__ == "__main__":
  logging.warning('iniciando funcioan principal')
  main()