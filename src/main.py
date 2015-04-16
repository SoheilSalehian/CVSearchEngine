import numpy as np
import cv2
import glob
from kMeansDomColor import KMeansDominantColorAlg

imagePath = "../images"
indexFile = "../outputIndex.txt"

def main():
    # Initialize k-means algorithm object
    myCD = KMeansDominantColorAlg(0);
    # Open index file to be written
    output = open(indexFile, "w")
    # Step through the image path jpeg files
    for path in glob.glob(imagePath + "/*.jpg"):
        print "Processing: " + path
        # Construct image ID for the image index file
        imageID = path[path.rfind("/") + 1:]
        # Generate the descriptor features 
        myCD.describe(path)

        # Append to the list of features for top K dominant colors
        features = [str(featureVector) for featureVector in myCD.dominantColors]
        print features
        # Write the index file with the descriptor values
        output.write("%s,%s\n" % (imageID, ",".join(features))) 
         
    # Close the fp of index file
    output.close()       
      
    
        
        
    
    
    
    





if __name__ == "__main__":
    main()