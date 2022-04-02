import numpy as np
import pyautogui
import imutils
import cv2
from shapedetector import ShapeDetector
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

# image = pyautogui.screenshot(region=(750, 220, 430, 530))
# image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
# cv2.imwrite("game.png", image)
# cv2.imshow("image", image)
# cv2.waitKey()

image = cv2.imread("game.png")
resized = imutils.resize(image, width=400)
ratio = image.shape[0] / float(resized.shape[0])
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
norm_img = np.zeros((gray.shape[0], gray.shape[1]))
normal = cv2.normalize(gray, norm_img, 0, 255, cv2.NORM_MINMAX)
blur = cv2.blur(normal, (2,2))
ret, thresh = cv2.threshold(blur, 165, 255, cv2.THRESH_BINARY_INV)
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
sd = ShapeDetector()

cv2.imshow("gray", gray)
cv2.imshow("thresh", thresh)

for c in cnts:
	# compute the center of the contour, then detect the name of the
	# shape using only the contour
	M = cv2.moments(c)
	cX = int((M["m10"] / M["m00"]) * ratio)
	cY = int((M["m01"] / M["m00"]) * ratio)
	shape = sd.detect(c)
	# multiply the contour (x, y)-coordinates by the resize ratio,
	# then draw the contours and the name of the shape on the image
	c = c.astype("float")
	c *= ratio
	c = c.astype("int")
	cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
	cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
		0.5, (255, 255, 255), 1)
	# show the output image
cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

height, width = thresh.shape[:2]
res = cv2.resize(thresh,(2*width, 2*height), interpolation = cv2.INTER_CUBIC)
kernel = np.ones((5,5), np.uint8)
res = cv2.erode(res, kernel)
res = cv2.blur(res, (3,3))

custom_config = r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ --psm 6'
print(pytesseract.image_to_string(res, config=custom_config))

cv2.imshow("blur",res)
cv2.waitKey(0)