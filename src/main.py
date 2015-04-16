import numpy as np
import colorsys
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
        features = [featureVector for featureVector in myCD.dominantColors]
        print features
        hsvFeatures = []
        # Conversion to hsv space 
        for f in features:
            # Normalize rgb values before passing to colorsys.rgb_to_hsv
            hsvFeatures.append(colorsys.rgb_to_hsv(f[0]/255.0, f[1]/255.0, f[2]/255.0))
        
        features = [hsvVector for hsvVector in hsvFeatures]   
        # Write the index file with the descriptor values
        output.write("%s,%s\n" % (imageID, ",".join(features))) 
         
    # Close the fp of index file
    output.close()       
      
    
        
        
    
    
    
    





if __name__ == "__main__":
    main()