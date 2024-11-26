import numpy as np
import pyautogui
import imutils
import cv2
from shape_detector import ShapeDetector
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

image = pyautogui.screenshot(region=(750, 220, 430, 530))
image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
cv2.imwrite("game.png", image)
cv2.imshow("image", image)
cv2.waitKey()

image = cv2.imread("game.png")
resized = imutils.resize(image, width=400)
ratio = image.shape[0] / float(resized.shape[0])
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 11, 17, 17)
norm_img = np.zeros((gray.shape[0], gray.shape[1]))
normal = cv2.normalize(gray, norm_img, 0, 255, cv2.NORM_MINMAX)
blur = cv2.blur(normal, (1,1))
ret, thresh = cv2.threshold(blur, 160, 255, cv2.THRESH_BINARY_INV)
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
sd = ShapeDetector()

cv2.imshow("gray", gray)
cv2.imshow("thresh", thresh)

height, width = thresh.shape[:2]
res = cv2.resize(thresh,(2*width, 2*height), interpolation = cv2.INTER_CUBIC)
kernel = np.ones((5,5),np.uint8)
res = cv2.morphologyEx(res, cv2.MORPH_CLOSE, kernel)
res = cv2.medianBlur(res, 5)

custom_config = r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ --psm 6'
print(pytesseract.image_to_string(res, config=custom_config))

cv2.imshow("blur",res)
cv2.waitKey(0)