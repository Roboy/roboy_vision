# Roboy Vision
Repository to Roboy Vision Team

Documentation can be found here:

[![Documentation Status](https://readthedocs.org/projects/roboyvision/badge/?version=devel)](http://roboyvision.readthedocs.io/en/latest/?badge=devel)


## Dependencies
- Python 3.5
- Tensorflow 1.x
- ROS Kinetic
- OpenCV 3.x
- librealsense 1.12.1 (Linux required Kernel max. 4.4!)
- pyrealsense 1.4
- libraries: numpy, matplotlib, dlib, re, signal, sklearn, scipy


## Getting Started

1. Download all required models using download_models.py in models directory.
2. Experiment with jupyter notebooks in tutorials section for different parts of project: face detection, alignment & face recognition

## Running with ROS

Currently there is no ROS Integration for Python 3. This is why a workaround was integrated to implement ROS service communication with ROS running under python 2.7 and the vision module on python 3.6.
Please refer to dirty_final_hack branch for details.
