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

Currently there is no ROS Integration for Python 3. This is why a workaround was integrated to implement ROS service communication with ROS running under python 2.7 and the vision module on python 3.6.
Please refer to dirty_final_hack branch for details.
