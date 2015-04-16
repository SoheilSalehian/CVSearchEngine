from collections import namedtuple
from math import sqrt
import random
from PIL import Image


Point = namedtuple('Point', ('coords', 'n', 'ct'))
Cluster = namedtuple('Cluster', ('points', 'center', 'n'))
# Lambda to generate RGB color code
rtoh = lambda rgb: '#%s' % ''.join(('%02x' % p for p in rgb))

## @class This class implements a K-means based algorithm to find the top K dominant colors in the image
#  @param imageFile Takes as input the path to the image file    
class KMeansDominantColorAlg:
    def __init__(self, dominantColors):
        self.dominantColors = dominantColors
    
    ## @func This function outputs the features based on dominant color
    #  @param imageFile Takes as input the path to the image file    
    def describe(self,imageFile):
        image = Image.open(imageFile)
        features = []
        domColor = self.getDomColors(image)
        features.extend(domColor)
        # Set the object dominant colors
        self.dominantColors = features
        
   
    def getDomColors(self, image, dim=5):
        # Generate the datapoints
        points = self.getPoints(image)
        # Find the k clusters
        clusters = self.kmeans(points, dim, 1)
        #
        rgbs = [map(int, c.center.coords) for c in clusters]
        return map(rtoh, rgbs)
    
    def getPoints(self, image, dim=3):
        points = []
        # ROI of the image to extract the data from
        width, height = image.size
        # Generate the data points from the colors in the whole image
        for count, color in image.getcolors(width*height):
            # of color and number of occurances 
            points.append(Point(color,dim,count))
        return points
    
    def kmeans(self,points, k, minDiff):
        # Pick a set of random clusters based on data samples
        clusters = [Cluster([p], p, p.n) for p in random.sample(points, k)]
        # Main loop to find the k clusters based on data points
        while 1:
            plists = [[] for i in range(k)]
            
            for p in points:
                smallestDist = float('Inf')
                # Iterate over each cluster k
                for i in range(k):
                    # Get the eculidian distance from the data point to the cluster center 
                    distance = self.euclidean(p, clusters[i].center)
                    # If our distance is smaller
                    if distance < smallestDist:
                        # Start minimizing smallest distance
                        smallestDist = distance
                        # Keep track of the cluster id
                        idx = i
                # Cluster to point mapping   
                plists[idx].append(p)
            # Reset difference between cluster centers
            diff = 0 
            # Iterate over each cluster again 
            for i in range(k):
                old = clusters[i]
                # Calculate the center of the cluster
                center = self.calculateCenter(plists[i], old.n)
                # Set as new cluster 
                new = Cluster(plists[i], center, old.n)
                clusters[i] = new
                # Find the maximum difference between centers are not are about the same
                diff = max(diff, self.euclidean( old.center, new.center))
            # If the center difference has become smaller than a threshold, clusters are finalized   
            if diff < minDiff:
                break
        # Return the found clusters for further calcs
        return clusters
    
    ## @func Function calculates the L2 distance from points to centers of clusters and intra-clusters.
    #  @param p1 first point.
    #  @param p2 second point.
    def euclidean(self, p1, p2):
        return sqrt(sum([
        (p1.coords[i] - p2.coords[i]) ** 2 for i in range(p1.n)
    ]))
        
    ## @func Function calculates the center of between points knowing dimensions
    #  @param points data points
    #  @param p2 dimensiality of the data points
    def calculateCenter(self, points, n):
        vals = [0.0 for i in range(n)]
        pLength = 0
        for p in points:
            # Start with the center of the point
            pLength += p.ct
            for i in range(n):
                vals[i] += (p.coords[i] * p.ct)
        return Point([(v/pLength) for v in vals], n, 1)
        

if __name__ == "__main__":
    desc = KMeansDominantColorAlg(0)
    features = desc.describe("../images/image2.jpg")
    print desc.dominantColors 
        
    