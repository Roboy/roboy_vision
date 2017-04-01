# Roboy Vision
Repository to Roboy Vision Team

## Dependencies
- Python 3.5
- Tensorflow 1.x
- ROS Kinetic
- OpenCV 3.x
- librealsense 1.12.1 (Linux required Kernel max. 4.4!)
- pyrealsense 1.4
- libraries: numpy, matplotlib, dlib, re, signal, sklearn, scipy

## Installation
We recommend using Anaconda.
1. Download Anaconda from: https://www.continuum.io/downloads#linux
2. Install: bash ~/Downloads/Anaconda3-4.3.0-Linux-x86_64.sh
3. Create Environment: conda create --name roboy python=3
4. Work on Environment: source activate roboy
5. Install OpenCV: conda install -c menpo opencv3=3.1.0
6. Install Tensorflow: conda install -c conda-forge tensorflow=1.0.0
7. Install librealsense according to tutorial on https://github.com/IntelRealSense/librealsense/blob/master/doc/installation.md
8. Install pyrealsense: pip install pyrealsense
9. Install ROS according to http://wiki.ros.org/kinetic/Installation/Ubuntu

## Getting Started
1. Download all required models using download_models.py in models directory.
2. Experiment with jupyter notebooks in tutorials section for different parts of project: face detection, alignment & face recognition
