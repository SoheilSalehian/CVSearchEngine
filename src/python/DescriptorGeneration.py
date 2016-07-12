import numpy as np
import cv2


class ColorDescriptor:
    def __init__(self,bins):
        self.bins = bins
        
    def describe(self,image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        features = []
        hist = self.histogram(image)
        features.extend(hist)
        return features
              
    def histogram(self, image):
        hist = cv2.calcHist([image],[0],None,[256],[0,256])
        hist = cv2.normalize(hist).flatten()
        return hist
    




