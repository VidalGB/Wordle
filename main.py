#Python v3.9.2 more information and dependencies, read requirements.txt
#Syntax camelCase


#Imports
import os

# Hide welcome print in pygame
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as Pg
from pygame.locals import *
from src.screen import *
from src.logic import *
from src.events import *
import sys
import csv
import ast
import logging


#Logging basic config
logging.basicConfig(level = logging.DEBUG, filename = './data/app.log', filemode = 'w', format = '%(name)s-%(levelname)s: %(message)s')

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
  paht = path('data/data.csv')
  with open (paht, 'r', encoding="utf-8") as file:
    content = csv.reader(file, delimiter = ';')
    for line in content:
      if line[0] == obj:
        return line[1]
  file.close()

def write(obj, writer):
  save = []
  n = 0
  paht = path('data/data.csv')
  with open (paht, 'r', encoding="utf-8") as file:
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
  paht = path('data/data.csv')
  with open (paht, 'w', newline = '') as file:
    write = csv.writer(file, delimiter = ';')
    write.writerows(save)
    write.writerow([obj, writer])
  file.close()

#Main function
def main():

  def __init__():

  # Set the Gobal variables
    logging.info('estableciendo variables de inicio')
    global userText
    userText = ''
    global Attempts
    Attempts = 0
    global hits
    hits = 0
    global idiom
    idiom = read('idiom')
    global record
    record = int(read('record'))
    global rowColor
    rowColor = {}
    global rowLyrics
    rowLyrics = {}
    global colors
    colors = ast.literal_eval(read('colors'))
    global colorActive
    colorActive = colors['lightBlue']
    global colorPassive
    colorPassive = colors['gray']
    global colorInput
    colorInput = colorPassive
    global colorCheck
    colorCheck = colorPassive
    global colorCross
    colorCross = colorPassive
    global colorConfig
    colorConfig = colors['white']
    global focusText
    focusText = False
    global sendText
    sendText = False
    global pressCheck
    pressCheck = False
    global pressCross
    pressCross = False
    global pressConfig
    pressConfig = False
    global win 
    win = False
    global endScreen
    endScreen = False
    global configScreen
    configScreen = False
    global gameScreen
    gameScreen = True
    global game
    game = False
    global font
    font = Pg.font.Font('data/font/CascadiaMonoPL.ttf', 60)
    global proportion
    proportion = ast.literal_eval(read('proportion'))
    global dicLanguage
    dicLanguage = ast.literal_eval(read('language'))
    global dicPlayText
    dicPlayText = ast.literal_eval(read('playText'))
    global dicEndText
    dicEndText = ast.literal_eval(read('endText'))
    global lenWord
    lenWord = int(read('length'))

    logging.info('estableciondo color de la app')
  # Seletc the color app
    if read('color') == 'white':
      colorBackground = colors['white']
      colorFont = colors['black']
      colorActive = colors['lightBlue']
    elif read('color') == 'black':
      colorBackground = colors['black']
      colorFont = colors['white']
      colorActive = colors['blue']
    print('init')

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
  logging.info('entrando al bucle principal')
#   Game loop
  while not gameOver:
    gameOver = events()
    logic()
    screen(windows)
    clock.tick(90)
  logging.warning('saliendo bucle principal')
  Pg.quit()
  sys.exit()


#Check script main
if __name__ == "__main__":
  logging.warning('iniciando funcioan principal')
  main()