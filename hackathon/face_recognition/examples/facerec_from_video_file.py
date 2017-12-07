import face_recognition
import os

import dlib
import cv2
from ctypes import *
import random
import numpy as np
import beer_list
import ttsClient


# Initialize some variables
labels = []
known_faces = []
face_locations = []
face_encodings = []
face_names = []
objectDetails = {}
peopleDetails = {}


def get_image_paths(facedir):
    image_paths = []
    if os.path.isdir(facedir):
        images = os.listdir(facedir)
        image_paths = [os.path.join(facedir, img) for img in images]
    return image_paths


# Get the embeddings, read the pictures and store the embeddings.
def Initialize():
    image_paths = get_image_paths("/home/roboy/Vision/hackathon/face_recognition/examples/Test_images/")
    for path in image_paths:
        name = os.path.basename(os.path.splitext(path)[0])
        labels.append(name)
        person_image = face_recognition.load_image_file(path)
        person_face_encoding = face_recognition.face_encodings(person_image)[0]
        known_faces.append(person_face_encoding)
        print name


def recognisePeople():
    global peopleDetails
    peopleDetails = {}
    objectDetails = {}
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("../../../models/dlib/shape_predictor_68_face_landmarks.dat")
    detect_net = load_net("../../../darknet/cfg/yolo.cfg", "../../../darknet/yolo.weights", 0)
    detect_meta = load_meta("../../../darknet/cfg/coco.data")
    peopleDetails = {}
    # input_movie = cv2.VideoCapture("_test.mp4")
    input_movie = cv2.VideoCapture(1)
    frame_number = 0
    length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))

    # Create an output movie file (make sure resolution/frame rate matches input video!)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output_movie = cv2.VideoWriter('output.avi', fourcc, 29.97, (640, 360))

    while frame_number < 10:
        # Grab a single frame of video
        ret, frame = input_movie.read()
        if ret:
            # frame = cv2.resize(frame, (0,0), fx=0.2, fy=0.2)
            frame = frame[0:376, 0:500]
        frame_number += 1

        # Quit when the input video file ends
        if not ret:
            break

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        personName = ""

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # See if the face is a match for the known face(s)
            match = face_recognition.compare_faces(known_faces, face_encoding)

            name = "Unknown"
            try:
                name = str(labels[match.index(True)])
            except:
                name = "Unknown"

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            if name != "Unknown":
                peopleDetails[name] = face_locations

        # Write the resulting image to the output video file
        # print("Writing frame {} / {}".format(frame_number, length))
        output_movie.write(frame)
        detectObjects(frame, detect_net, detect_meta)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 0)
        cv2.imshow("Video", frame)
        cv2.waitKey(1)
    # input_movie.release()
    # cv2.destroyAllWindows()
    return peopleDetails


def sample(probs):
    s = sum(probs)
    probs = [a / s for a in probs]
    r = random.uniform(0, 1)
    for i in range(len(probs)):
        r = r - probs[i]
        if r <= 0:
            return i
    return len(probs) - 1


def c_array(ctype, values):
    return (ctype * len(values))(*values)


class BOX(Structure):
    _fields_ = [("x", c_float),
                ("y", c_float),
                ("w", c_float),
                ("h", c_float)]


class IMAGE(Structure):
    _fields_ = [("w", c_int),
                ("h", c_int),
                ("c", c_int),
                ("data", POINTER(c_float))]


class METADATA(Structure):
    _fields_ = [("classes", c_int),
                ("names", POINTER(c_char_p))]


lib = CDLL("../../../darknet/libdarknet.so", RTLD_GLOBAL)
lib.network_width.argtypes = [c_void_p]
lib.network_width.restype = c_int
lib.network_height.argtypes = [c_void_p]
lib.network_height.restype = c_int

predict = lib.network_predict_p
predict.argtypes = [c_void_p, POINTER(c_float)]
predict.restype = POINTER(c_float)

make_boxes = lib.make_boxes
make_boxes.argtypes = [c_void_p]
make_boxes.restype = POINTER(BOX)

free_ptrs = lib.free_ptrs
free_ptrs.argtypes = [POINTER(c_void_p), c_int]

num_boxes = lib.num_boxes
num_boxes.argtypes = [c_void_p]
num_boxes.restype = c_int

make_probs = lib.make_probs
make_probs.argtypes = [c_void_p]
make_probs.restype = POINTER(POINTER(c_float))

detect = lib.network_predict_p
detect.argtypes = [c_void_p, IMAGE, c_float, c_float, c_float, POINTER(BOX), POINTER(POINTER(c_float))]

reset_rnn = lib.reset_rnn
reset_rnn.argtypes = [c_void_p]

load_net = lib.load_network_p
load_net.argtypes = [c_char_p, c_char_p, c_int]
load_net.restype = c_void_p

free_image = lib.free_image
free_image.argtypes = [IMAGE]

letterbox_image = lib.letterbox_image
letterbox_image.argtypes = [IMAGE, c_int, c_int]
letterbox_image.restype = IMAGE

load_meta = lib.get_metadata
lib.get_metadata.argtypes = [c_char_p]
lib.get_metadata.restype = METADATA

load_image = lib.load_image_color
load_image.argtypes = [c_char_p, c_int, c_int]
load_image.restype = IMAGE

predict_image = lib.network_predict_image
predict_image.argtypes = [c_void_p, IMAGE]
predict_image.restype = POINTER(c_float)

network_detect = lib.network_detect
network_detect.argtypes = [c_void_p, IMAGE, c_float, c_float, c_float, POINTER(BOX), POINTER(POINTER(c_float))]


def detect(net, meta, image, thresh=.5, hier_thresh=.5, nms=.45):
    # check if image is an OpenCV frame

    if isinstance(image, np.ndarray):
        # GET C,H,W, and DATA values
        img = image.transpose(2, 0, 1)
        c, h, w = img.shape[0], img.shape[1], img.shape[2]
        nump_data = img.ravel() / 255.0
        nump_data = np.ascontiguousarray(nump_data, dtype=np.float32)

        # make c_type pointer to numpy array
        ptr_data = nump_data.ctypes.data_as(POINTER(c_float))

        # make IMAGE data type
        im = IMAGE(w=w, h=h, c=c, data=ptr_data)

    else:
        im = load_image(image, 0, 0)

    boxes = make_boxes(net)
    probs = make_probs(net)
    num = num_boxes(net)
    network_detect(net, im, thresh, hier_thresh, nms, boxes, probs)
    res = []
    for j in range(num):
        for i in range(meta.classes):
            if probs[j][i] > 0:
                res.append((meta.names[i], probs[j][i], (boxes[j].x, boxes[j].y, boxes[j].w, boxes[j].h)))
    res = sorted(res, key=lambda x: -x[1])
    # free_image(im)
    # free_ptrs(cast(probs, POINTER(c_void_p)), num)

    return res


def draw_results(res, img):
    for element in res:
        box = element[2]
        xmin = int(box[0] - box[2] / 2. + 1)
        xmax = int(box[0] + box[2] / 2. + 1)
        ymin = int(box[1] - box[3] / 2. + 1)
        ymax = int(box[1] + box[3] / 2. + 1)
        rand_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color=rand_color, thickness=3, )
        cv2.putText(img, str(element[0]) + " " + '%.2f' % element[1],
                    (xmin, ymin),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, rand_color, thickness=3)
    return img


DONE = 0


def detectObjects(frame, detect_net, detect_meta):
    # ret, frame = CameraFrame.read()
    # RUN OBJECT DETECTION ON FRAME
    frame = frame[0:376, 0:500]
    if detect_net:
        results = detect(detect_net, detect_meta, frame, thresh=0.5)
        img = draw_results(results, frame)
        print results
        global objectDetails
        for result in results:
            objectDetails[result[0]] = result[2]
        print objectDetails


def Converse():
    bottle = objectDetails.get("bottle","")
    person = objectDetails.get("person","")
    cup = objectDetails.get("cup","")
    chair = objectDetails.get("chair", "")
    if bottle:
        ttsClient.ts_client("I see a bottle")
        bottlexmin = int(bottle[0] - bottle[2] / 2. + 1)
        bottlexmax = int(bottle[0] + bottle[2] / 2. + 1)
        bottleymin = int(bottle[1] - bottle[3] / 2. + 1)
        bottleymax = int(bottle[1] + bottle[3] / 2. + 1)

    if person:
        ttsClient.ts_client("Oh Great. I see a person here")
        personxmin = int(person[0] - person[2] / 2. + 1)
        personxmax = int(person[0] + person[2] / 2. + 1)
        personymin = int(person[1] - person[3] / 2. + 1)
        personymax = int(person[1] + person[3] / 2. + 1)

    if cup:
        ttsClient.ts_client("I see a Cup")
        cupxmin = int(cup[0] - cup[2] / 2. + 1)
        cupxmax = int(cup[0] + cup[2] / 2. + 1)
        cupymin = int(cup[1] - cup[3] / 2. + 1)
        cupymax = int(cup[1] + cup[3] / 2. + 1)

    print bottle, person, cup
#    (top, right, bottom, left) =
    name =  peopleDetails.iterkeys().next()  if any(peopleDetails) else "Stranger"
    if(bottle and person and bottlexmin > personxmin and bottlexmax < personxmax and bottleymax < personymax and bottleymin > personymin):
        print beer_list.generateDialogue(name,True,False)
        ttsClient.ts_client(beer_list.generateDialogue(name,True,False))
    elif (cup and person and cupxmin > personxmin and cupxmax < personxmax and cupymax < personymax and cupymin > personymin):
        print beer_list.generateDialogue(name, False, True)
        ttsClient.ts_client(beer_list.generateDialogue(name, False, True))

    if chair and person and bottle:
        ttsClient.ts_client("Ah "+name+" I see a chair next you. Please down and enjoy your beer")

    elif chair and person and cup:
        ttsClient.ts_client("Ah "+name+" I see a chair next you. Please down and enjoy your Coffee")

    elif chair and person:
        ttsClient.ts_client("Ah "+name+" I see a chair next you. Please sit. Enjoy your time")



if __name__ == "__main__":
    peopleList = {}
    Initialize()
    while True:
        print "Roboy as a bartender!"
        print "1. Find the people in the frame \n 2. Count the number of people \n 3. Talk a dialogue"
        userInput = raw_input("Choice:")
        if userInput == "1":
            peopleList = recognisePeople()
            print peopleList
        elif userInput == "2":
            Initialize()  # Reinitializing the people known.
        elif userInput == "3":
            Converse()


            # elif userInput == 2:

"""Todo: 
1. To find the bottle and see if its inside the person's frame
2. To send ROS messages for the dialogue. 
3. After the dialogue continue back with the detection"""
