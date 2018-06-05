#!/usr/bin/env python

# Requirements:
# pip install tk
# pip install pillow
from Tkinter import *
from PIL import Image
from PIL import ImageTk
import cv2, threading, os, time
from threading import Thread
from os import listdir
from os.path import isfile, join

import dlib
#import imutils
from imutils import face_utils, rotate_bound
import math

import rospy
from roboy_communication_cognition.srv import ApplyFilter


def handleRequest(req):
    print ("Chosen filter: "+req.name)
    
    if req.name == "roboy":
        put_sprite(0)     
    if req.name == "mustache":
        put_sprite(1)
    if req.name == "sunglasses":
        put_sprite(2)
    if req.name == "hat":
        put_sprite(3)
    if req.name == "flies":
        put_sprite(4)
    if req.name == "crown":
        put_sprite(5)
    return True

def snapchat_server():
	rospy.init_node('snapchat_server')
	server = rospy.Service('/roboy/cognition/apply_filter', ApplyFilter, handleRequest)
	print("Ready for Snapchat")
	#rospy.spin()

### Function to set wich sprite must be drawn
def put_sprite(num):
    global SPRITES
    SPRITES[num] = (1 - SPRITES[num]) #not actual value

# Draws sprite over a image
# It uses the alpha chanel to see which pixels need to be reeplaced
# Input: image, sprite: numpy arrays
# output: resulting merged image
def draw_sprite(frame, sprite, x_offset, y_offset):
    (h,w) = (sprite.shape[0], sprite.shape[1])
    (imgH,imgW) = (frame.shape[0], frame.shape[1])

    if y_offset+h >= imgH: #if sprite gets out of image in the bottom
        sprite = sprite[0:imgH-y_offset,:,:]

    if x_offset+w >= imgW: #if sprite gets out of image to the right
        sprite = sprite[:,0:imgW-x_offset,:]

    if x_offset < 0: #if sprite gets out of image to the left
        sprite = sprite[:,abs(x_offset)::,:]
        w = sprite.shape[1]
        x_offset = 0

    #for each RGB chanel
    for c in range(3):
            #chanel 4 is alpha: 255 is not transpartne, 0 is transparent background
            frame[y_offset:y_offset+h, x_offset:x_offset+w, c] =  \
            sprite[:,:,c] * (sprite[:,:,3]/255.0) +  frame[y_offset:y_offset+h, x_offset:x_offset+w, c] * (1.0 - sprite[:,:,3]/255.0)
    return frame

#Adjust the given sprite to the head's width and position
#in case of the sprite not fitting the screen in the top, the sprite should be trimed
def adjust_sprite2head(sprite, head_width, head_ypos, ontop = True):
    (h_sprite,w_sprite) = (sprite.shape[0], sprite.shape[1])
    factor = 1.0*head_width/w_sprite
    sprite = cv2.resize(sprite, (0,0), fx=factor, fy=factor) # adjust to have the same width as head
    (h_sprite,w_sprite) = (sprite.shape[0], sprite.shape[1])

    y_orig =  head_ypos-h_sprite if ontop else head_ypos # adjust the position of sprite to end where the head begins
    if (y_orig < 0): #check if the head is not to close to the top of the image and the sprite would not fit in the screen
            sprite = sprite[abs(y_orig)::,:,:] #in that case, we cut the sprite
            y_orig = 0 #the sprite then begins at the top of the image
    return (sprite, y_orig)

# Applies sprite to image detected face's coordinates and adjust it to head
def apply_sprite(image, path2sprite,w,x,y, angle, ontop = True):
    sprite = cv2.imread(path2sprite,-1)
    #print sprite.shape
    sprite = rotate_bound(sprite, angle)
    (sprite, y_final) = adjust_sprite2head(sprite, w, y, ontop)
    image = draw_sprite(image,sprite,x, y_final)

# Applies rainbow sprite to image detected face's coordinates and adjust it to head
def apply_sprite_rainbow(image, path2sprite,w,x,y, angle, ontop = True):
    sprite = cv2.imread(path2sprite,-1)
    #print sprite.shape
    sprite = rotate_bound(sprite, angle)
    #print(angle)
    if not (-5 <= angle <= 5):
    	(sprite, y_final) = adjust_sprite2head(sprite, w+abs(angle*1.5), y, ontop)
    else:
    	(sprite, y_final) = adjust_sprite2head(sprite, w, y, ontop)
    image = draw_sprite(image,sprite,x, y_final)


#points are tuples in the form (x,y)
# returns angle between points in degrees
def calculate_inclination(point1, point2):
    x1,x2,y1,y2 = point1[0], point2[0], point1[1], point2[1]
    incl = 180/math.pi*math.atan((float(y2-y1))/(x2-x1))
    return incl


def calculate_boundbox(list_coordinates):
    x = min(list_coordinates[:,0])
    y = min(list_coordinates[:,1])
    w = max(list_coordinates[:,0]) - x
    h = max(list_coordinates[:,1]) - y
    return (x,y,w,h)

def get_face_boundbox(points, face_part):
    if face_part == 1:
        (x,y,w,h) = calculate_boundbox(points[17:22]) #left eyebrow
    elif face_part == 2:
        (x,y,w,h) = calculate_boundbox(points[22:27]) #right eyebrow
    elif face_part == 3:
        (x,y,w,h) = calculate_boundbox(points[36:42]) #left eye
    elif face_part == 4:
        (x,y,w,h) = calculate_boundbox(points[42:48]) #right eye
    elif face_part == 5:
        (x,y,w,h) = calculate_boundbox(points[29:36]) #nose
       # print ('x,y,w,h',x,y,w,h)
    elif face_part == 6:
        (x,y,w,h) = calculate_boundbox(points[48:68]) #mouth
    return (x,y,w,h)


#Principal Loop where openCV (magic) ocurs
def cvloop(run_event):
    global panelA
    global SPRITES

    spr = "../sprites/"
    dir_ = spr+"flyes/"
    flies = [f for f in listdir(dir_) if isfile(join(dir_, f))] #image of flies to make the "animation"
    i = 0
    video_capture = cv2.VideoCapture(0) #read from webcam
    (x,y,w,h) = (0,0,10,10) #whatever initial values

    #Filters path
    detector = dlib.get_frontal_face_detector()


    #Facial landmarks
    print("[INFO] loading Roboy Snapchat Filter ...")
    model = "../filters/shape_predictor_68_face_landmarks.dat"
    predictor = dlib.shape_predictor(model) # link to model: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2


    while run_event.is_set(): #while the thread is active we loop
        ret, image = video_capture.read()
        #image = imutils.resize(image, width=3000)
        image = image[0:376, 0:500]
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = detector(gray, 0)

        for face in faces: #if there are faces
            (x,y,w,h) = (face.left(), face.top(), face.width(), face.height())
            # *** Facial Landmarks detection
            shape = predictor(gray, face)
            shape = face_utils.shape_to_np(shape)
            incl = calculate_inclination(shape[17], shape[26]) #inclination based on eyebrows

            # condition to see if mouth is open
            is_mouth_open = (shape[66][1] -shape[62][1]) >= 10 #y coordiantes of landmark points of lips

            
            #mustache condition
            if (SPRITES[1] and not SPRITES[0]):
                (x1,y1,w1,h1) = get_face_boundbox(shape, 6)
                apply_sprite(image, spr+"mustache.png",w1+10,x1-5,y1+5, incl)
            
            #pixelated sunglasses condition
            if (SPRITES[2] and not SPRITES[0]):
                (x3,y3,_,h3) = get_face_boundbox(shape, 1)
                apply_sprite(image, spr+"pixelated_sunglasses.png",w,x,y3, incl, ontop = False)

             #crown condition
            if (SPRITES[5] and not SPRITES[0]):
                apply_sprite(image, spr+"crown.png",w+30,x-20,y, incl)

            #hat condition
            if (SPRITES[3] and not SPRITES[0] and not SPRITES[5]):
                apply_sprite(image, spr+"hat.png",w+30,x-20,y, incl)
            
            
            
            #roboy + mustache + sunglasses + crown + rainbow condition
            elif (SPRITES[0] and SPRITES[1] and SPRITES[2] and SPRITES[5] and is_mouth_open):
                apply_sprite_rainbow(image, spr+"roboy_sunglasses_mustache_crown_rainbow.png",w+35,x-15,y-85, incl, ontop = False)
            
            #roboy + mustache + sunglasses + crown condition
            elif (SPRITES[0] and SPRITES[1] and SPRITES[2] and SPRITES[5]):
                apply_sprite(image, spr+"roboy_sunglasses_mustache_crown.png",w+35,x-18,y-85, incl, ontop = False)

            
            #roboy + mustache + sunglasses + hat + rainbow condition
            elif (SPRITES[0] and SPRITES[1] and SPRITES[2] and SPRITES[3] and is_mouth_open):
                apply_sprite_rainbow(image, spr+"roboy_sunglasses_mustache_hat_rainbow.png",w+40,x-17,y-65, incl, ontop = False)
            
            #roboy + mustache + sunglasses + hat condition
            elif (SPRITES[0] and SPRITES[1] and SPRITES[2] and SPRITES[3]):
                apply_sprite(image, spr+"roboy_sunglasses_mustache_hat.png",w+38,x-20,y-70, incl, ontop = False)

            
            #roboy + mustache + sunglasses + rainbow condition
            elif (SPRITES[0] and SPRITES[1] and SPRITES[2] and is_mouth_open):
                apply_sprite_rainbow(image, spr+"roboy_sunglasses_mustache_rainbow.png",w+35,x-15,y-45, incl, ontop = False)

            #roboy + mustache + sunglasses condition
            elif (SPRITES[0] and SPRITES[1] and SPRITES[2]):
                apply_sprite(image, spr+"roboy_sunglasses_mustache.png",w+40,x-20,y-50, incl, ontop = False)

           
            #roboy + mustache + crown + rainbow condition
            elif (SPRITES[0] and SPRITES[1] and SPRITES[5] and is_mouth_open):
                apply_sprite_rainbow(image, spr+"roboy_mustache_crown_rainbow.png",w+35,x-15,y-85, incl, ontop = False)

            #roboy + mustache + crown condition
            elif (SPRITES[0] and SPRITES[1] and SPRITES[5]):
                apply_sprite(image, spr+"roboy_mustache_crown.png",w+35,x-18,y-85, incl, ontop = False)

           
            #roboy + mustache + hat + rainbow condition
            elif (SPRITES[0] and SPRITES[1] and SPRITES[3] and is_mouth_open):
                apply_sprite_rainbow(image, spr+"roboy_mustache_hat_rainbow.png",w+40,x-17,y-65, incl, ontop = False)

            #roboy + mustache + hat condition
            elif (SPRITES[0] and SPRITES[1] and SPRITES[3]):
                apply_sprite(image, spr+"roboy_mustache_hat.png",w+38,x-20,y-70, incl, ontop = False)

            
            #roboy + sunglasses + crown + rainbow condition
            elif (SPRITES[0] and SPRITES[2] and SPRITES[5] and is_mouth_open):
                apply_sprite_rainbow(image, spr+"roboy_sunglasses_crown_rainbow.png",w+35,x-15,y-85, incl, ontop = False)

            #roboy + sunglasses + crown condition
            elif (SPRITES[0] and SPRITES[2] and SPRITES[5]):
                apply_sprite(image, spr+"roboy_sunglasses_crown.png",w+35,x-18,y-85, incl, ontop = False)

            
            #roboy + sunglasses + hat + rainbow condition
            elif (SPRITES[0] and SPRITES[2] and SPRITES[3] and is_mouth_open):
                apply_sprite_rainbow(image, spr+"roboy_sunglasses_hat_rainbow.png",w+40,x-17,y-65, incl, ontop = False)

            #roboy + sunglasses + hat condition
            elif (SPRITES[0] and SPRITES[2] and SPRITES[3]):
                apply_sprite(image, spr+"roboy_sunglasses_hat.png",w+38,x-20,y-70, incl, ontop = False)

            
             #roboy + mustache + rainbow condition
            elif (SPRITES[1] and SPRITES[0] and is_mouth_open):
                apply_sprite_rainbow(image, spr+"roboy_mustache_rainbow.png",w+35,x-15,y-45, incl, ontop = False)

            #roboy + mustache condition
            elif (SPRITES[1] and SPRITES[0]):
                apply_sprite(image, spr+"roboy_mustache.png",w+40,x-20,y-50, incl, ontop = False)

            
            #roboy + sunglasses + rainbow condition
            elif (SPRITES[0] and SPRITES[2] and is_mouth_open):
                apply_sprite_rainbow(image, spr+"roboy_sunglasses_rainbow.png",w+35,x-15,y-45, incl, ontop = False)
            
            #roboy + sunglasses condition
            elif (SPRITES[0] and SPRITES[2]):
                apply_sprite(image, spr+"roboy_sunglasses.png",w+40,x-20,y-50, incl, ontop = False)
            
            
            #roboy + hat + rainbow condition
            elif (SPRITES[0] and SPRITES[3] and is_mouth_open):
                apply_sprite_rainbow(image, spr+"roboy_hat_rainbow.png",w+40,x-17,y-65, incl, ontop = False)
            
            #roboy + hat condition
            elif (SPRITES[0] and SPRITES[3]):
                apply_sprite(image, spr+"roboy_hat.png",w+38,x-20,y-70, incl, ontop = False)
            
            
            #roboy + crown + rainbow condition
            elif (SPRITES[0] and SPRITES[5] and is_mouth_open):
                apply_sprite_rainbow(image, spr+"roboy_crown_rainbow.png",w+35,x-15,y-85, incl, ontop = False)
            
            #roboy + crown condition
            elif (SPRITES[0] and SPRITES[5]):
                apply_sprite(image, spr+"roboy_crown.png",w+35,x-18,y-85, incl, ontop = False)
            
            
            #roboy + rainbow condition
            elif (SPRITES[0] and is_mouth_open):
                apply_sprite_rainbow(image, spr+"roboy_rainbow.png",w+35,x-15,y-45, incl, ontop = False)

            #roboy condition
            elif SPRITES[0]:
                apply_sprite(image, spr+"roboy.png",w+40,x-20,y-50, incl, ontop = False)

            
            else:
                if (is_mouth_open and not SPRITES[0]):
                    (x0,y0,w0,h0) = get_face_boundbox(shape, 6) #bound box of mouth
                    apply_sprite(image, spr+"rainbow.png",w0,x0,y0, incl, ontop = False)


            #flies condition
            if (SPRITES[4]):
                #to make the "animation" we read each time a different image of that folder
                # the images are placed in the correct order to give the animation impresion
                apply_sprite(image, dir_+flies[i],w,x,y, incl)
                i+=1
                i = 0 if i >= len(flies) else i #when done with all images of that folder, begin again
		       	
     
        # OpenCV represents image as BGR; PIL but RGB, we need to change the chanel order
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # conerts to PIL format
        image = Image.fromarray(image)
        # Converts to a TK format to visualize it in the GUI
        image = ImageTk.PhotoImage(image)
        # Actualize the image in the panel to show it
        panelA.configure(image=image)
        panelA.image = image

    video_capture.release()

# Initialize GUI object
root = Tk()
root.title("ROBOY SNAPCHAT FILTERS")
this_dir = os.path.dirname(os.path.realpath(__file__))

# Adds a custom logo
imgicon = PhotoImage(file=os.path.join(this_dir, '../sprites/roboy_sunglasses_mustache_crown.png'))
root.tk.call('wm', 'iconphoto', root._w, imgicon)

# Create the panel where webcam image will be shown
panelA = Label(root)
panelA.pack( padx=10, pady=10)

# Variable to control which sprite you want to visualize
SPRITES = [0,0,0,0,0,0] #roboy, mustache, sunglasses, flies, crown -> 1 is visible, 0 is not visible

# Creates a thread where the magic ocurs
run_event = threading.Event()
run_event.set()
action = Thread(target=cvloop, args=(run_event,))
action.setDaemon(True)
action.start()

snapchat_server()

# Function to close all properly, aka threads and GUI
def terminate():
        global root, run_event, action
        print "Closing thread opencv..."
        run_event.clear()
        time.sleep(1)
        root.destroy()
        print "All closed!"

# When the GUI is closed it actives the terminate function
root.protocol("WM_DELETE_WINDOW", terminate)
root.mainloop() #creates loop of GUI
