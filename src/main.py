import numpy as np
import colorsys
import glob
from kMeansDomColor import KMeansDominantColorAlg



imagePath = "../images/flickr/"
indexFile = "../outputIndex.csv"

def main():
    # Initialize k-means algorithm object
    myCD = KMeansDominantColorAlg(0);
    # Open index file to be written
    output = open(indexFile, "w")
    
    output.write("%s|%s|%s|%s|%s|%s|%s|%s|%s|%s\n" % ("imagename", "h1", "s1", "v1", \
                                                  "h2", "s2", "v2",\
                                                  "h3", "s3", "v3")) 
    # Step through the image path jpeg files
    for path in glob.glob(imagePath + "/*.jpg"):
        print "Processing: " + path
        # Construct image ID for the image index file
        imageID = path[path.rfind("/") + 1:]
        # Generate the descriptor features 
        myCD.describe(path)
        # Append to the list of features for top K dominant colors
        features = [featureVector for featureVector in myCD.dominantColors]
        hsvFeatures = []
        # Conversion to hsv space 
        for f in features:
            # Normalize rgb values before passing to colorsys.rgb_to_hsv
            hsvFeatures.append(colorsys.rgb_to_hsv(f[0]/255.0, f[1]/255.0, f[2]/255.0)) 
        
        features = []
        # denormalize hsv feature vector back
        for f in hsvFeatures:
            features.append(tuple([int(f[0]*360), int(f[1]*100), int(f[2]*100)]))
        
        finalFeatures = []
        for f in features:
            finalFeatures.append(str(f[0]))
            finalFeatures.append(str(f[1]))
            finalFeatures.append(str(f[2]))
        print finalFeatures
            
        # Write the index file with the descriptor values
        output.write("%s|%s\n" % (imageID, "|".join(finalFeatures))) 
         
    # Close the fp of index file
    output.close()       
      

        
        
    
    
    
    





if __name__ == "__main__":
    main()