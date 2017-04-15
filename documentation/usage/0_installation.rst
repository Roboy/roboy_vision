Installation
=============

Running all sub modules in realtime requires Ubuntu 16.04 with Kernel version 4.4.x. For getting started a jupyter notebook installation using anaconda will be sufficient. Tutorials in form of jupyter notebooks are provided.

Anaconda
----------------

We recommend the use of Anaconda. This allows all python libraries to only be installed in a virtual environment which then won't have any influence on other programs you are running. We will create a virtual environment using python 3. 

- Download Anaconda from https://www.continuum.io/downloads#linux::

    bash ~/Downloads/Anaconda3-4.3.0-Linux-x86_64.sh

- Install Anaconda:: 

    bash ~/Downloads/Anaconda3-4.3.0-Linux-x86_64.sh

- Create a Conda Environment with the name "roboy" and python 3::

    conda create --name roboy python=3

- To work on the created environment it has to be activated::

    source activate roboy

- When you want to leave the environmant you have to use::

    source deactivate

Dependencies
----------------

Now you should be working in your virtual environment. We then will install all requirements. We are working with python 3, because of tensorflow requirements.

- First clone the Vision repository and install the necessary python dependencies::

    cd ~/
    git clone https://github.com/Roboy/Vision
    pip install -r Vision/requirements.txt

- Install OpenCV::

    conda install -c menpo opencv3=3.1.0

- Install Tensorflow::

    conda install -c conda-forge tensorflow=1.0.0

- Install librealsense according to tutorial on https://github.com/IntelRealSense/librealsense/blob/master/doc/installation.md (this currently requires a Linux Kernel of maximum 4.4.x)

- Install pyrealsense::

    pip install pyrealsense

- Install ROS Kinetic according to tutorial on http://wiki.ros.org/kinetic/Installation/Ubuntu. ROS is currently running outside the conda environment using python 2.

Build
----------------

To build all ROS message and service files you can use catkin::

    cd ~/Vision
    catkin_make

To build doxygen documentation run::

    cd ~/Vision
    sphinx-build -b html ./documentation ./build/documentation

