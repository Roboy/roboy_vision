Solution Strategy
=================

Basic decisions for Vision Package:

- Seperation of different tasks into sub-modules (Face Detection, Object tracking, face recognition, mood recognition, age estimation, scene classification, ...)
- Face detection using this approach: `Joint Face Detection and Alignment using MTCNNs <https://kpzhang93.github.io/MTCNN_face_detection_alignment/paper/spl.pdf>`_. Good real time performance, other modules to be built on top.
- Face embeddings using `FaceNet <https://arxiv.org/pdf/1503.03832.pdf>`_. These embeddings can be used for recognition.

 
Plan for coming semester with priorities in red (5 being highest priority):

.. _plan_for_semester:
.. figure:: images/Plan.*
  :alt: Semester Plan
