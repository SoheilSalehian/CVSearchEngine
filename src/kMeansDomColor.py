from collections import namedtuple
from math import sqrt
import random
from PIL import Image

Point = namedtuple('Point', ('coords', 'n', 'ct'))
Cluster = namedtuple('Cluster', ('points', 'center', 'n'))
rtoh = lambda rgb: '#%s' % ''.join(('%02x' % p for p in rgb))

class KMeansDominantColorAlg:
    def __init__(self, dominantColors):
        self.dominantColors = dominantColors
        
    def describe(self,imageFile):
        image = Image.open(imageFile)
        features = []
        domColor = self.getDomColors(image)
        features.extend(domColor)
        self.dominantColors = features
        
   
    def getDomColors(self, image, dim=3):
        points = self.getPoints(image)
        clusters = self.kmeans(points, dim, 1)
        rgbs = [map(int, c.center.coords) for c in clusters]
        return map(rtoh, rgbs)
    
    def getPoints(self, image, dim=3):
        points = []
        width, height = image.size
        for count, color in image.getcolors(width*height):
            points.append(Point(color,dim,count))
        return points
    
    def kmeans(self,points, k, minDiff):
        clusters = [Cluster([p], p, p.n) for p in random.sample(points, k)]
        
        while 1:
            plists = [[] for i in range(k)]
            
            for p in points:
                smallestDist = float('Inf')
                for i in range(k):
                    distance = self.euclidean(p, clusters[i].center)
                    if distance < smallestDist:
                        smallestDist = distance
                        idx = i
                    
                plists[idx].append(p)
            
            diff = 0 
            for i in range(k):
                old = clusters[i]
                center = self.calculateCenter(plists[i], old.n)
                new = Cluster(plists[i], center, old.n)
                clusters[i] = new
                diff = max(diff, self.euclidean( old.center, new.center))
                
            if diff < minDiff:
                break
        return clusters
        
    def euclidean(self, p1, p2):
        return sqrt(sum([
        (p1.coords[i] - p2.coords[i]) ** 2 for i in range(p1.n)
    ]))
        
    
    def calculateCenter(self, points, n):
        vals = [0.0 for i in range(n)]
        pLength = 0
        for p in points:
            pLength += p.ct
            for i in range(n):
                vals[i] += (p.coords[i] * p.ct)
        return Point([(v/pLength) for v in vals], n, 1)
        

if __name__ == "__main__":
    desc = KMeansDominantColorAlg(0)
    features = desc.describe("../images/image2.jpg")
    print desc.dominantColors 
        
    