Welcome to Vision repository documentation!
===========================================================

This project's goal is to provide Roboy with extensive vision capabilities. This means to recognize, localize and classify objects in its environment as well as to provide data for localization to be processed by other modules. The input will be a ZED camera device, the output should be high-level data about Roboy's environment provided using ROS messages and services.

The most import task in Vision for human interaction is to detect and recognize faces, which is why this was considered the highest priority of this project. The current main tasks of this project are:

- Identification of Roboy Team Members
- Pose estimation of a detected face and Roboy Motor Control
- Tracking of detected objects
- Person Talking detection
- Mood Recognition
- Gender Recognition
- Remebering faces online
- Age classification
- Scene and object classification


.. _background_prerequisits:

Relevant Background Information and Pre-Requisits
--------------------------------------------------

Our approach to tackle the given tasks in Vision is to use machine learning methods. Therefore a basic understanding of machine learning, specifically also deep Neural Networks and Convolutional Neural Networks will be necessary.

The following links are to be seen as suggestions for getting started on machine learning:

- Crash Course on Deep Learning in the form of Youtube tutorials: `DeepLearning.tv <https://www.youtube.com/channel/UC9OeZkIwhzfv-_Cb7fCikLQ/videos/>`_
- Closer Look at the implementation of Neural Networks: `The Foundations of deep learning <https://www.youtube.com/watch?v=zij_FTbJHsk&list=PLrAXtmErZgOfMuxkACrYnD2fTgbzk2THW>`_
- An introduction to Convolutional Neural Networks (CNNs): `Deep learning in Computer vision <https://www.youtube.com/watch?v=u6aEYuemt0M&index=2&list=PLrAXtmErZgOfMuxkACrYnD2fTgbzk2THW>`_
- The machine learning framework used for implementation:    `Tensorflow <https://www.tensorflow.org/>`_
- Stanford's CNNs for Computer Vision course:  `CS231n <https://www.youtube.com/watch?v=vT1JzLTH4G4&list=PL3FW7Lu3i5JvHM8ljYj-zLfQRF3EO8sYv/>`_
- Furthermore a basic understanding of simple machine learning approaches like Regression, Tree Learning, K-Nearest-Neighbours (KNN), Support Vector Machines (SVMs), Gaussian Models, Eigenfaces, etc. will be helpful.


The papers currently used for implementation should be understood:

- `Joint Face Detection and Alignment using Multi-task Cascaded Convolutional Networks <https://kpzhang93.github.io/MTCNN_face_detection_alignment/paper/spl.pdf>`_
- `FaceNet: A Unified Embedding for Face Recognition and Clustering <https://arxiv.org/pdf/1503.03832.pdf>`_
- `DLIB: Facial landmarks and face recognition <http://www.pyimagesearch.com/2017/04/03/facial-landmarks-dlib-opencv-python/>`_
- You Only Look Once: Unified, Real-Time Object Detection `YOLO <https://pjreddie.com/media/files/papers/yolo.pdf>`_


Furthermore there are plans to extend the implementation using this paper:

- `An All-In-One Convolutional Neural Network for Face Analysis <https://arxiv.org/pdf/1611.00851v1.pdf>`_


Contents
---------------------

.. _usage:
.. toctree::
  :maxdepth: 1
  :glob:
  :caption: Usage and Installation
  
  usage/*

.. _development:
.. toctree::
  :maxdepth: 1
  :glob:
  :caption: Development

  development/*

.. toctree::
   :maxdepth: 1

   about-arc42



