import sys 
sys.path.append('..')

import cv2

## Realsense libraries
import pyrealsense as pyrs
	
if __name__ == '__main__':

    ## start pyrealsense service
	pyrs.start()

	#Image Size (define size of image)
	x_pixel = 640
	y_pixel = 480

	# resize for faster processing
	resize_factor = 0.5

	#init realsense device
	dev = pyrs.Device()

	while True:  
	    
	    # Get Frame from Realsense
	    dev.wait_for_frame()
	    c = dev.colour	    
	    c = cv2.cvtColor(c, cv2.COLOR_RGB2BGR)
	    d = dev.depth*  dev.depth_scale * 1000
	    #print(c.shape)

	    cv2.imshow("detection result", c)
	    cv2.waitKey(10)