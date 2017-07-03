Installation
=============

Running all sub modules in realtime requires Ubuntu 16.04 with Kernel version 4.4.x. For getting started a jupyter notebook installation using anaconda will be sufficient. Tutorials in form of jupyter notebooks are provided.

Anaconda
----------------

We recommend the use of Anaconda. This allows all python libraries to only be installed in a virtual environment which then won't have any influence on other programs you are running. We will create a virtual environment using python 3. 

- Download Anaconda from https://www.continuum.io/downloads#linux::

- Install Anaconda:: 

    bash ~/Downloads/Anaconda3-4.4.0-Linux-x86_64.sh

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

- For running the tutorials DLib and jupyter notebook will also be required::
    
    conda install -c menpo dlib
    pip install jupyter

- The Last step is to install ROS Kinetic. Since ROS currently is not running using Python3 we install outside the virtual environment and Python 2. The ROS installation tutorial can be found on: http://wiki.ros.org/kinetic/Installation/Ubuntu. 

.. todo:: Compile ROS with Python 3 to be able to use together with Tensorflow v1.x

Build
----------------

To build all ROS message and service files you can use catkin::

    cd ~/Vision
    catkin_make

To build doxygen documentation offline for viewing you can run::

    cd ~/Vision
    sphinx-build -b html ./docs ./build/docs


Please download the files 
    - SharedLibs
    - StaticLibs 
from https://drive.google.com/drive/folders/0B0cOyLVrawK5TFJhdGJvNE9wNzg

Compiling opencv from source
----------------

Note: This is required only if you want to work with multiple object/face tracking. This step is needed as this Multiple tracking is part of opencv_contrib module which needs to be compiled along with opencv, as it doesnt gets shipped with openv. 
The following instructions are for Mac.


First you will need:

1. Mac OSX 10.12
2. XCode
3. Command Line Tools (This is done from inside XCode)
4. CMake(http://www.cmake.org/download/)

Step 1:
Download openCV and unzip it somewhere on your computer. Create two new folders inside of the openCV directory, one called StaticLibs and the other SharedLibs.

Step 2a: Build the Static Libraries with Terminal.
To build the libraries in Terminal.

* Open CMake.
* Click Browse Source and navigate to your openCV folder.
* Click Browse Build and navigate to your StaticLib Folder.
* Click the configure button. You will be asked how you would like to generate the files. Choose Unix-Makefile from the Drop Down menu and Click OK. CMake will perform some tests and return a set of red boxes appear in the CMake Window.

You will need to uncheck and add to the following options.

* Uncheck BUILD_SHARED_LIBS
* Uncheck BUILD_TESTS
* Add an SDK path to CMAKE_OSX_SYSROOT, it will look something like this “/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.9.sdk”. (NOTE: make sure your version of SDK is used here)
* Add x86_64 to CMAKE_OSX_ARCHITECTURES, this tells it to compile against the current system
* Uncheck WITH_1394
* Uncheck WITH_FFMPEG

Click Configure again, then Click Generate.

When the application has finished generating, Open Terminal and type the following commands.
    - cd <path/to/your/opencv/staticlibs/folder/>
    - make (This will take awhile)
    - sudo make install

Enter your password.
This will install the static libraries on your computer.

Step 2c: Build the Shared Libraries with Terminal.

* Open CMake.
* Click Browse Source and navigate to your openCV folder.
* Click Browse Build and navigate to your SharedLib Folder.
* Click the configure button. You will be asked how you would like to generate the files. Choose Unix-Makefile from the Drop Down menu and Click OK. CMake will perform some tests and return a set of red boxes appear in the CMake Window.

You will need to uncheck and add to the following options.

* Check BUILD_SHARED_LIBS
* Uncheck BUILD_TESTS
* Add an SDK path to CMAKE_OSX_SYSROOT, it will look something like this “/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.9.sdk”.
* Add x86_64 to CMAKE_OSX_ARCHITECTURES, this tells it to compile against the current system
* Uncheck WITH_1394
* Uncheck WITH_FFMPEG
* Click Configure again, then Click Generate.

When the application has finished generating, Open Terminal.


    - cd <path/to/your/opencv/SharedLibs/folder/>
    - make (This will take awhile)
    - sudo make install


You should see the libraries build in the shared and static libraries folders. 

    - cd /Users/<Username>/<path-to-installation>/StaticLibs/lib/python3
    - ls -s cv2.cpython-36m-darwin.so cv2.so

The above step would help in creating a symbolic link so you can use it with python.

