import cv2
import numpy as np
from matplotlib import pyplot as plt

def compare(target, contender):

    



    dif = #math to assign algebra value to this variable

    return dif
    


#blue = 0
#green = 1
#red = 2

img = cv2.imread('test.jpg')
img2 = cv2.imread('test2.jpg')
  
# testing 2 bins. It's the value right after "None"
b = cv2.calcHist([img],[0],None,[2],[0,256]).tolist()
g = cv2.calcHist([img],[1],None,[2],[0,256]).tolist()
r = cv2.calcHist([img],[2],None,[2],[0,256]).tolist()

# print("blue", b)
# print("green", g)
# print("red", r)


#creating neat array package for each photo
imgRGB = []
imgRGB.extend([b, g, r])
print("RGB SUMMARY FOR IMG1: ", imgRGB)

print("-----")

b2 = cv2.calcHist([img2],[0],None,[2],[0,256]).tolist()
g2 = cv2.calcHist([img2],[1],None,[2],[0,256]).tolist()
r2 = cv2.calcHist([img2],[2],None,[2],[0,256]).tolist()

# print("blue", b2)
# print("green", g2)
# print("red", r2)

imgRGB2 = []
imgRGB2.extend([b2, g2, r2])
print("RGB SUMMARY FOR IMG2: ", imgRGB2)
