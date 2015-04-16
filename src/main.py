import numpy as np
import cv2
import glob
from DescriptorGeneration import ColorDescriptor

imagePath = "../images"
indexFile = "../outputIndex.txt"

def main():
    # Initilize the color descriptor object
    myCD = ColorDescriptor((10,20,30))
    # Open index file to be written
    output = open(indexFile, "w")
    # Step through the image path jpeg files
    for path in glob.glob(imagePath + "/*.jpg"):
        print "Processing: " + path
        # Construct image ID for the image index file
        imageID = path[path.rfind("/") + 1:]
        # Read image
        image = cv2.imread(path)
        # Generate the descriptor features 
        features = myCD.describe(image)
        # Append to the list of features
        features = [str(f) for f in features]
        # Write the index file with the descriptor values
        output.write("%s,%s\n" % (imageID, ",".join(features)))   
    # Close the fp of index file
    output.close()       
      
    
        
        
    
    
    
    





if __name__ == "__main__":
    main()