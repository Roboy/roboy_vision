"""@package RecogniseFace
1. Module responsible for Face Recognition
2. This uses a model already trained on LWF, to extract facial features
3. Another model of members from Roboy are trained
4. We use a SVM classifier to classify the detected face to match with the model of trained faces
"""
from imutils import face_utils
import imutils
import dlib
import cv2
#import RosMsgUtil
import os
import re
import numpy as np
import time
import math
try:
    from setuptools import setup, find_packages
except AttributeError:
    from setuptools import setup, find_packages
import tensorflow as tf
from tensorflow.python.platform import gfile
import sys
from models.mtcnn.align_dlib import AlignDlib
from scipy import misc
import pickle
from sklearn.svm import SVC
import Ros_Publisher
IMAGE_SIZE = 160
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
    print('started recognition')
    if not vs:
        sys.exit()
        # Ros_Publisher.publishNewFacialFeatures(speaking, shape)
    while True:
        rects = RectsQueue.get()
        FaceVal = []
        if len(rects) >0:
            # print("MULTI FACEEEEEEEEEEEEEEEE")
            dataset = get_dataset("/Users/prashanth/code/roboy/Vision/src/images")
            for rect in rects:
                FaceVal.append((rect.left(),rect.top(),rect.right(),rect.bottom()))
                print(FaceVal)
            # print(":enght of Faceval",len(FaceVal))
            ok,frame = vs.read()
            if not ok:
                sys.exit();
            image = imutils.resize(frame, width=800)
            print("Range of FaceVal:",range(len(FaceVal)))
            facesEmbeddings = []
            # for i in range(len(FaceVal)):
            # print("i is:",i)
            aligned_face, lm = align_face_dlib(image, FaceVal[0], AlignDlib.OUTER_EYES_AND_NOSE)

            feed_dict = {
                image_batch: np.expand_dims(aligned_face, 0),
                phase_train_placeholder: False
            }
            rep = session.run(embeddings, feed_dict=feed_dict)[0]
            facesEmbeddings.append(rep)
            print("Face Embeddings are:", facesEmbeddings)

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

def get_image_paths_and_labels(dataset):
    image_paths_flat = []
    labels_flat = []
    for i in range(len(dataset)):
        image_paths_flat += dataset[i].image_paths
        labels_flat += [i] * len(dataset[i].image_paths)
    return image_paths_flat, labels_flat


class ImageClass():
    "Stores the paths to images for a given class"

    def __init__(self, name, image_paths):
        self.name = name
        self.image_paths = image_paths

    def __str__(self):
        return self.name + ', ' + str(len(self.image_paths)) + ' images'

    def __len__(self):
        return len(self.image_paths)

def get_image_paths(facedir):
    image_paths = []
    if os.path.isdir(facedir):
        images = os.listdir(facedir)
        image_paths = [os.path.join(facedir, img) for img in images]
    return image_paths


def get_dataset(paths, has_class_directories=True):
    dataset = []
    for path in paths.split(':'):
        path_exp = os.path.expanduser(path)
        classes = os.listdir(path_exp)
        classes.sort()
        nrof_classes = len(classes)
        for i in range(nrof_classes):
            class_name = classes[i]
            facedir = os.path.join(path_exp, class_name)
            image_paths = get_image_paths(facedir)
            dataset.append(ImageClass(class_name, image_paths))

    return dataset


def load_data(image_paths, do_random_crop, do_random_flip, image_size, do_prewhiten=True):
    nrof_samples = len(image_paths)
    images = np.zeros((nrof_samples, image_size, image_size, 3))
    for i in range(nrof_samples):
        img = misc.imread(image_paths[i])
        if img.ndim == 2:
            img = to_rgb(img)
        if do_prewhiten:
            img = prewhiten(img)
        img = crop(img, do_random_crop, image_size)
        img = flip(img, do_random_flip)
        print(i," : ",image_paths[i])
        images[i,:,:,:] = img
    return images

def processImage(img, do_random_crop, do_random_flip, image_size, do_prewhiten=True):
    if img.ndim == 2:
        img = to_rgb(img)
    if do_prewhiten:
        img = prewhiten(img)
    img = crop(img, do_random_crop, image_size)
    img = flip(img, do_random_flip)
    return img

def to_rgb(img):
    w, h = img.shape
    ret = np.empty((w, h, 3), dtype=np.uint8)
    ret[:, :, 0] = ret[:, :, 1] = ret[:, :, 2] = img
    return ret

def prewhiten(x):
    mean = np.mean(x)
    std = np.std(x)
    std_adj = np.maximum(std, 1.0/np.sqrt(x.size))
    y = np.multiply(np.subtract(x, mean), 1/std_adj)
    return y



def crop(image, random_crop, image_size):
    if image.shape[1] > image_size:
        sz1 = int(image.shape[1] // 2)
        sz2 = int(image_size // 2)
        if random_crop:
            diff = sz1 - sz2
            (h, v) = (np.random.randint(-diff, diff + 1), np.random.randint(-diff, diff + 1))
        else:
            (h, v) = (0, 0)
        image = image[(sz1 - sz2 + v):(sz1 + sz2 + v), (sz1 - sz2 + h):(sz1 + sz2 + h), :]
    return image


def flip(image, random_flip):
    if random_flip and np.random.choice([True, False]):
        image = np.fliplr(image)
    return image



def train(session):
    dataset = get_dataset("/Users/prashanth/code/roboy/Vision/src/images")
    paths, labels = get_image_paths_and_labels(dataset)

    print('Number of classes: %d' % len(dataset))
    print('Number of images: %d' % len(paths))

    # Load the model
    print('Loading feature extraction model')
    model_dir = '../models/facenet/20170512-110547.pb'
    load_model(model_dir,"","")

    # Get input and output tensors
    images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
    embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
    phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
    embedding_size = embeddings.get_shape()[1]

    # Run forward pass to calculate embeddings
    print('Calculating features for images')
    batch_size = 1000
    nrof_images = len(paths)
    nrof_batches_per_epoch = int(math.ceil(1.0 * nrof_images / batch_size))
    emb_array = np.zeros((nrof_images, embedding_size))
    for i in range(nrof_batches_per_epoch):
        start_index = i * batch_size
        end_index = min((i + 1) * batch_size, nrof_images)
        paths_batch = paths[start_index:end_index]
        images = load_data(paths_batch, False, True, EXPECT_SIZE)
        feed_dict = {images_placeholder: images, phase_train_placeholder: False}
        emb_array[start_index:end_index, :] = session.run(embeddings, feed_dict=feed_dict)


    classifier_filename_exp = os.path.expanduser("TrainedModel_1.pkl")




#TESTING CLASSIFIER
    print('Testing classifier')
    with open(classifier_filename_exp, 'rb') as infile:
        (model, class_names) = pickle.load(infile)

    print('Loaded classifier model from file "%s"' % classifier_filename_exp)

    predictions = model.predict_proba(emb_array)
    best_class_indices = np.argmax(predictions, axis=1)
    best_class_probabilities = predictions[np.arange(len(best_class_indices)), best_class_indices]

    for i in range(len(best_class_indices)):
        print('%4d  %s: %.3f' % (i, class_names[best_class_indices[i]], best_class_probabilities[i]))

    accuracy = np.mean(np.equal(best_class_indices, labels))
    print('Accuracy: %.3f' % accuracy)
