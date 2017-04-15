Getting started
===============

Tutorials
---------

As a start run the jupyter notebooks in tutorials section::

    source activate roboy
    pip install jupyter-notebook
    cd ~/Vision/tutorials
    jupyter notebook

There is four different tutorials:

- **Face_Detection** tutorial will show you how to run a face detection an an image or webcam input using the MTCNN neural network. Additionally also DLib face detector is used.

- **Facenet_Embeddings** tutorial shows how to calculate the 128D embeddings given a face using facenet. There exist 2 versions of this tutorial. One is using MTCNN for face detection, the other one using DLib. This tutoial provides the functionality to caluclate and save embeddings on a database of pictures, where all pictures are stored in a folder structure, with the folder name being the person in the picture.

- **Classifier_Training** uses embeddings calculated in the previous tutorial to train a classifier to distinguish between the classes in these embeddings. Currently only SVM and a binary Tree have been implemented.

- **Face_Recognition** tutorial shows how to run the classification on an image or webcam input. It demonstrates this using KNN and the classifiers trained in the previous tutorial. 


Real Time
---------

For running face detection in real time you can run the script::

    source activate roboy
    cd ~/Vision
    python src/vision_service/scripts/face_detection.python


This will show the currently detected images in an extra frame. Startig face recognition for a given face and to query whether a face is nearby are to be implemented as ROS services. Currently ROS is runnung with python 2.7 only. This is why in dirty_final_hack branch an alternative approach for Communication using File I/O was implemented. This should be replaced.