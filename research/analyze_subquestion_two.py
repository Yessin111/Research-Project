import urllib.request
import cv2
import numpy as np
from pytesseract import pytesseract
import PIL

obj_detect = ObjectDetection()
obj_detect.setModelTypeAsYOLOv3()

pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

with urllib.request.urlopen("https://m.media-amazon.com/images/I/81nycUl7i+L.jpg") as input_image:
    arr = np.asarray(bytearray(input_image.read()), dtype=np.uint8)
    image = cv2.imdecode(arr, -1)
    # grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

    # cv2.imshow('image', ret)
    # cv2.waitKey(0)

    text = pytesseract.image_to_string(ret)
    print(text)
