from imutils import face_utils
import imutils
import dlib
import cv2
#import RosMsgUtil
import os
import re
import numpy as np
import time
try:
    from setuptools import setup, find_packages
except AttributeError:
    from setuptools import setup, find_packages
import tensorflow as tf
from tensorflow.python.platform import gfile
import sys
from models.mtcnn.align_dlib import AlignDlib

def recogniseFace(RectsQueue):
    start = time.time()
    print("Started Recognition: Wait for 40")
    model_dir = '../models/facenet/20170512-110547.pb'
#    meta_file, ckpt_file = get_model_filenames(os.path.expanduser(model_dir))
    session = load_model(model_dir, "","")
    graph = tf.get_default_graph()
    image_batch = graph.get_tensor_by_name("input:0")
    phase_train_placeholder = graph.get_tensor_by_name("phase_train:0")
    embeddings = graph.get_tensor_by_name("embeddings:0")
    print('done.')
    print("Time taken:",time.time()-start," Seconds")
    vs = cv2.VideoCapture(0)
    facesEmbeddings = []
    if not vs:
        sys.exit()
    while True:
        rects = RectsQueue.get()
        FaceVal = []
        if len(rects) >1:
            # print("MULTI FACEEEEEEEEEEEEEEEE")
            for rect in rects:
                FaceVal.append((rect.left(),rect.top(),rect.right(),rect.bottom()))
                print(FaceVal)
            # print(":enght of Faceval",len(FaceVal))
            ok,frame = vs.read()
            if not ok:
                sys.exit();
            image = imutils.resize(frame, width=800)
#            try:
#                print(FaceVal[0],"Lenght of FaceVal is: ",len(FaceVall))
#            except Exception as e:
#                continue
            print("Range of FaceVal:",range(len(FaceVal)))
            facesEmbeddings = []
            for i in range(len(FaceVal)):
                # print("i is:",i)
                aligned_face, lm = align_face_dlib(image, FaceVal[i], AlignDlib.INNER_EYES_AND_BOTTOM_LIP)
                
                feed_dict = {
                   image_batch: np.expand_dims(aligned_face, 0),
                   phase_train_placeholder: False
                }

                rep = session.run(embeddings, feed_dict=feed_dict)[0]
                facesEmbeddings.append(rep)
            #    print("Face Embeddings are:",facesEmbeddings)
            if len(facesEmbeddings) >1:
                d = facesEmbeddings[-1] - facesEmbeddings[-2]
                diffVal = np.linalg.norm(d, axis=0)
                # print(diffVal," Diffvalue")
                if diffVal > 0.7:
                    print("Two different Faces found")
                    print("  + Squared l2 distance between representations:\
                     \ ",np.linalg.norm(d,axis=0))
                #dist = np.linalg.norm(facesEmbeddings[-1] - facesEmbeddings[-2])
            #print(dist)
        #print ("Vector: ",rep)
    # # get class probabilities using SVM classifier
    # probabilities = classifier.predict_proba(rep.reshape(1, -1))

    # # Calculate most likely class
    # out = np.argmax(probabilities[0])

    # # Retrieve class name
    # names = np.load('models/own_embeddings/own_names.npy')
    # face_name = names[out]

    # print('classification: ' + face_name + ' probability: ' +
    #       probabilities[0][out])


EXPECT_SIZE = 160
def align_face_dlib(image, face_box, landmarkIndices=AlignDlib.OUTER_EYES_AND_NOSE):
    align = AlignDlib('../models/dlib/shape_predictor_68_face_landmarks.dat')
    assert isinstance(face_box, tuple)
    face_rect = dlib.rectangle(*face_box)
    landmarks = align.findLandmarks(image, face_rect)
    alignedFace = align.align(EXPECT_SIZE, image, face_rect, 
                              landmarks=landmarks,
                              landmarkIndices=landmarkIndices)
    return alignedFace, landmarks

## Function to load a tensorflow model
#
#  TODO: To be moved into other module
#  @param model_dir model directory
#  @param model_meta meta file
#  @param model_content checpoint file
#  @return Returns a tensorflow session
def load_model(model_dir, model_meta, model_content):
    model_dir_exp = os.path.expanduser(model_dir)
    if (os.path.isfile(model_dir_exp)):
        print('Model filename: %s' % model_dir_exp)
        with gfile.FastGFile(model_dir_exp,'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            tf.import_graph_def(graph_def, name='')
    session = tf.InteractiveSession()
    #saver = tf.train.import_meta_graph(os.path.join(model_dir_exp, model_meta))
    #saver.restore(tf.get_default_session(),
    #              os.path.join(model_dir_exp, model_content))
    #tf.get_default_graph().as_graph_def()
    return session


## Helper Function to load a tensorlow model
#
#  TODO: To be moved into other module
#  The function finds the meta_file and checkpoint within a given path
#  @param model_dir Path where the model is stored
#  @return Returns meta_file and checkpoint
def get_model_filenames(model_dir):
    files = os.listdir(model_dir)
    meta_files = [s for s in files if s.endswith('.meta')]
    if len(meta_files) == 0:
        raise ValueError(
            'No meta file found in the model directory (%s)' % model_dir)
    elif len(meta_files) > 1:
        raise ValueError(
            'There should not be more than one meta file in the model directory (%s)'
            % model_dir)
    meta_file = meta_files[0]
    meta_files = [s for s in files if '.ckpt' in s]
    max_step = -1
    for f in files:
        step_str = re.match(r'(^model-[\w\- ]+.ckpt-(\d+))', f)
        if step_str is not None and len(step_str.groups()) >= 2:
            step = int(step_str.groups()[1])
            if step > max_step:
                max_step = step
                ckpt_file = step_str.groups()[0]
    return meta_file, ckpt_file
