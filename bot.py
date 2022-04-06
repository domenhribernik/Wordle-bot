import numpy as np
import pyautogui
import imutils
import cv2

# image = pyautogui.screenshot(region=(750, 220, 430, 530))
# image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
# cv2.imwrite("game.png", image)
# cv2.imshow("image", image)
# cv2.waitKey()

image = cv2.imread("game.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 11, 17, 17)
blur = cv2.blur(gray, (1,1))
ret, thresh = cv2.threshold(blur, 50, 255, cv2.THRESH_BINARY)

contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
output = cv2.drawContours(image, contours, -1, (0, 0, 255), 3)

colors = []

for contour in contours:
  y = contour[0][0][1] + 15
  x = contour[0][0][0] + 15
  (b, g, r) = output[y, x]
  cv2.circle(output, (x, y), 2, (255, 0, 0), 2)
  text = ""
  if(b == 60 and g == 58 and r == 58):
    text = "gray"
  elif(b == 59 and g == 159 and r == 181):
    text = "yellow"  
  elif(b == 78 and g == 141 and r == 83):
    text = "green"
  cv2.putText(output, text, (x+10, y), cv2.FONT_HERSHEY_COMPLEX, 0.4, (255, 0, 0), 1, cv2.LINE_AA)
  colors.insert(0, text)
  
for i in range(0, len(colors)):
  print(colors[i], end=" ")
  if (i+1) % 5 == 0:
    print("")

cv2.imshow("Thresh", thresh)
cv2.imshow("Output", output)
cv2.waitKey(0)