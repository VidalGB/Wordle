import random
import logging
import ast
from src.screen import *
from src.events import *
from main import *


# Function for get random word
def randomWord():
  game = True
  paht = path(f"./data/words/{read('length')}words-{read('idiom')}.txt")
  with open (paht, 'r', encoding = "utf-8") as file:
    lines = file.readlines()
    line = ''.join(lines)
    word = line.split('\n')
    max = len(word) - 1
    while True:
      n = random.randint(0, max)
      ranWord = word[n]
      logging.debug(f'Numero aleatorio {n}, palabra aleatoria {ranWord}')
      wordList = ast.literal_eval(read('wordList'))
      if ranWord not in wordList:
        del wordList[0]
        wordList.append(ranWord)
        write('wordList', wordList)
        break
    ranWord = ranWord.upper()
    ranWord = list(ranWord)
    logging.info(f'Palabra a adivinar "{ranWord}"')
    print(ranWord)
    file.close()


#Game logic function
def logic():
  logging.info('calculando logica')

#   New game
  if not game:
    game = True
    win = False
    userText = ''
    randomWord()
    rowColor = {}
    rowLyrics = {}
    Attempts = 0
    flackCheckWord = True

#   Control word
  corretWord = []
  if sendText == True:
    sendText = False
    userWord = list(userText)
    posUserWord = 0
    for lyrics in userWord:
      true = 0
      if lyrics in ranWord:
        true = 1
        posRanWord = 0
        for letters in ranWord:
          if lyrics == letters:
            if posRanWord == posUserWord:
              true = 2
          posRanWord += 1
      letters = lyrics + ':' + str(true)
      corretWord.append(letters)
      posUserWord += 1
    userText = ''

#   Boxes color and lyrics
#     Color the boxes
    lyrics = []
    for item in corretWord:
      if '2' in item:
        lyrics.append('green')
      elif '1' in item:
        lyrics.append('yellow')
      else:
        lyrics.append('red')
      rowColor[Attempts] = lyrics

#     Lyrics the boxes
      letters = []
      for item in corretWord:
        List = item.split(':')
        letters.append(List[0])
        rowLyrics[Attempts] = letters
    Attempts += 1

#   Win check
    letters = 0
    for item in corretWord:
      if '2' in item:
        letters += 1
    if letters == len(corretWord):
      win = True

#   End screen
  if Attempts == 5 or win == True:
    endScreen = True
    if not win:
      if flackCheckWord:
        if hits > 0:
          hits = 0
        flackCheckWord = False
#   Win
  if win:
    if flackCheckWord:
      hits += 1
      if hits > record:
        record = hits
        write('record', record)
      flackCheckWord = False


#   Press button
#     Check button
  if not pressCheck:
    colorCheck = colorPassive
  else:
    colorCheck = colorActive
    pressCheck = False

#     Cross button
  if not pressCross:
    colorCross = colorPassive
  else:
    colorCross = colorActive
    pressCross = False

#     Config button
  if not pressConfig:
    colorConfig = colors['white']
  else:
    colorConfig = colorActive
    pressConfig = False

#   Focus on the text input
  if focusText:
    colorInput = colorActive
  else:
    colorInput = colorPassive