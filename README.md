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
2. Install Anaconda 
```shell
bash ~/Downloads/Anaconda3-4.3.0-Linux-x86_64.sh
```
3. Create Conda Environment 
```shell
conda create --name roboy python=3
```
4. Work on Environment: 
```shell
source activate roboy
```
5. Install OpenCV: 
```shell
conda install -c menpo opencv3=3.1.0
```
6. Install Tensorflow:
```shell
conda install -c conda-forge tensorflow=1.0.0
```
7. Install librealsense according to tutorial on https://github.com/IntelRealSense/librealsense/blob/master/doc/installation.md
8. Install pyrealsense: 
```shell
pip install pyrealsense
```
9. Install ROS outside the conda environment using Python 2.7 according to http://wiki.ros.org/kinetic/Installation/Ubuntu

## Getting Started
1. Download all required models using download_models.py in models directory.
2. Experiment with jupyter notebooks in tutorials section for different parts of project: face detection, alignment & face recognition

## Running with ROS

Currently there is no ROS Integration for Python 3 which is why we are using File I/O for communication. Files will be written into a directory which has to be empty before.

This directory is set using a environment variable containing the path:
```shell
export VISION_COMM_PATH='/yourpath/'
```

To build all service messages run
```shell
catkin_make
```
in the root folder of the project. Then do
```shell
source devel/setup.bash
```
To make the ROS interface available one has to start following two nodes:
```shell
rosrun vision_service face_detector.py 
rosrun vision_service recognizer.py
```
To run the actual Face detector run
```shell
./run_roboy_nuke
```

This will set all necessary environment variables on Roboy Nuke PC. You will have to edit the paths for your own machine.

The two services can then be called using following ROS commands:
```shell
rosservice call /recognize_face 0
rosservice call /rdetect_face
```

The recognize face gets the object_id as an argument. Currently this is not used and just the closest face is returned.
