from unittest import case
import numpy as np
import pyautogui
import time
import random
import datetime
import cv2
from nltk.corpus import words
# from nltk.corpus import brown
# freqs = nltk.FreqDist([w.lower() for w in brown.words()])
# word_list = sorted(words.words(), key=lambda x: freqs[x.lower()], reverse=True)
word_list = words.words()
arr = []
start_phrase = "marry"
for word in word_list:
  if len(word) == 5:
    arr.append(word.lower())
# 9972 words
word_set = set(arr)
print(len(word_set))
green_letters = ["", "", "", "", ""]
yellow_letters = [[], [], [], [], []]
wrong_letters = []
time.sleep(3)
guess_word = start_phrase
for index in range(0, 5):
  pyautogui.typewrite(guess_word)
  pyautogui.press("enter")
  time.sleep(3)
  image = pyautogui.screenshot(region=(745, 200, 430, 550))
  image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
  cv2.imwrite("game.png", image)
  cv2.imshow("image", image)

  image = cv2.imread("game.png")
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  gray = cv2.bilateralFilter(gray, 11, 17, 17)
  blur = cv2.blur(gray, (1,1))
  ret, thresh = cv2.threshold(blur, 50, 255, cv2.THRESH_BINARY)

  contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  output = cv2.drawContours(image, contours, -1, (0, 0, 255), 2)

  colors = []

  for contour in contours:
    y = contour[0][0][1] + 15
    x = contour[0][0][0] + 15
    (b, g, r) = output[y, x]
    # print(str(b) + " " + str(g) + " " + str(r))
    cv2.circle(output, (x, y), 2, (255, 0, 0), 2)
    text = ""
    if(b == 60 and g == 58 and r == 58):
      text = "gray"
    elif(b == 59 and g == 159 and r == 181):
      text = "yellow"  
    elif(b == 78 and g == 141 and r == 83):
      text = "green"
    elif(b == 19 and g == 18 and r == 18):
      text = "empty"
    cv2.putText(output, text, (x+10, y), cv2.FONT_HERSHEY_COMPLEX, 0.4, (255, 0, 0), 1, cv2.LINE_AA)
    if text != "empty":
      colors.insert(0, text)

  tmp = []
  for i in range(len(colors)-5, len(colors)):
    tmp.append(colors[i])
  colors = tmp.copy()

  for i in range(len(colors) - 5, len(colors)):
    if colors[i] == "empty":
      break
    elif colors[i] == "green":
      if green_letters[i] == "":
        green_letters[i] = guess_word[i]
      print(str(i) + " " + guess_word[i] + " is green", end="")
    elif colors[i] == "yellow":
      yellow_letters[i].append(guess_word[i])
      print(str(i), end=" ")
      for j in range(0, len(yellow_letters[i])):
        print(yellow_letters[i][j], end=" ")
      print("is yellow", end="")
    elif colors[i] == "gray":
      if guess_word[i] not in wrong_letters:
        wrong_letters.append(guess_word[i])
      print("Wrong letters:", end=" ")
      for j in range(0, len(wrong_letters)):
        print(wrong_letters[j], end = " ")
    print("")

  if "" not in green_letters:
    print("You Win")
    break

  green_letters[4] = "y"
  tmp = word_set.copy()
  for word in word_set:
    for i in range(0, len(green_letters)):
      if green_letters[i] != "":
        if word[i] != green_letters[i]:
          tmp.discard(word)
    for letter in wrong_letters:
      if letter in word:
        for i in range(0, len(word)):
          if green_letters[i] == "":
            tmp.discard(word)
          else:
            if green_letters[i] != word[i]:
              tmp.discard(word)
    for i in range(0, len(yellow_letters)):
      if not yellow_letters[i]:
        continue
      for j in range(0, len(yellow_letters[i])):
        if yellow_letters[i][j] in word:
          if word[i] == yellow_letters[i][j]:
            tmp.discard(word)
        else:
          tmp.discard(word)
  word_set = tmp.copy()
  for word in word_set:
    print(word)
  print(len(word_set))
  guess_word = list(word_set)[random.randint(0, len(word_set)-1)]
  print("word: " + guess_word)
  time.sleep(3)
  
cv2.imwrite("results/game"+str(datetime.date.today())+"-"+str(random.randint(100,999))+".png", output)
cv2.imshow("Thresh", thresh)
cv2.imshow("Output", output)
cv2.waitKey()
cv2.destroyAllWindows()

# TODO
# words with double letters (one green)
# better words
# sort words?