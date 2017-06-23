Solution Strategy
=================

Basic decisions for Vision Package:

- Seperation of different tasks into sub-modules (Face Detection, Object tracking, face recognition, mood recognition, age estimation, scene classification, ...)
- Highest priority on face detection and face pose estimation. Recognition of people as second priority. All other properties concerning people with lower priority and general object detection with least importance.
- Face detection using this approach: `Joint Face Detection and Alignment using MTCNNs <https://kpzhang93.github.io/MTCNN_face_detection_alignment/paper/spl.pdf>`_. Good real time performance, other modules to be built on top.
- Face embeddings using `FaceNet <https://arxiv.org/pdf/1503.03832.pdf>`_. These embeddings can be used for recognition.


Current implementation:

- **Face detection** running in realtime with function to query whether a face is nearby (to be called as ROS service).
- **Face recognition** implemented as extra thread (to be called as ROS service on a given face). Using Facenet for calculating embeddings for a given face and SVM for classification. SVM currently trained on pictures of LFW (labelled Faces in the Wild) dataset, using Roboy Team members as next step.
- **ROS services** currently not implemented in devel branch. Only workaround in dirty_final_hack branch.
- **Tracking objects/faces** running in realtime. This implementation is based on the MIL(Visual Tracking with Online Multiple Instance Learning). Also part of the Opencv_contrib module. 
 
Plan for coming semester with priorities in red (5 being highest priority):

.. _plan_for_semester:
.. figure:: images/Plan.*
  :alt: Semester Plan


Future plans on current implentation:
* Improve tracking by implementing the GOTURN algorithm. 



Architecture of the current System:

.. __systemArchitecture:
.. figure:: images/systemArchitecture.*
	:alt: System Architecture