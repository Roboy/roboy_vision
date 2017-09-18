Installation
=============

Running all sub modules in realtime requires Ubuntu 16.04 with Kernel version 4.4.x. For getting started a jupyter notebook installation using anaconda will be sufficient. Tutorials in form of jupyter notebooks are provided.

Anaconda
----------------

We recommend the use of Anaconda. This allows all python libraries to only be installed in a virtual environment which then won't have any influence on other programs you are running. We will create a virtual environment using python 3. 

- Download Anaconda from https://www.continuum.io/downloads#linux::

- Install Anaconda:: 

    bash ~/Downloads/Anaconda3-4.3.0-Linux-x86_64.sh
    
- Enter 'yes' when prompted with the following question:

    Do you wish the installer to prepend the Anaconda install location to PATH in your /home/name/.bashrc ? [yes¦no]
    
- Restart the terminal.


- Create a Conda Environment with the name "roboy" and python 3::

    conda create --name roboy python=3

- To work on the created environment it has to be activated::

    source activate roboy

- When you want to leave the environmant you have to use::

    source deactivate

Dependencies
----------------

Now you should be working in your virtual environment. We then will install all requirements. We are working with python 3, because of tensorflow requirements.

- First clone the Vision repository and run the setup script to install most of the necessary dependencies::

    cd ~/
    git clone https://github.com/Roboy/Vision

    cd ~/Vision
    chmod +x setup.sh
    sudo ./setup.sh
 
- Download Cuda from https://developer.nvidia.com/cuda-downloads

- Install Cuda with instructions from http://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#axzz4rHIEa0GY


Build
----------------
To build doxygen documentation offline for viewing you can run::

    cd ~/Vision
    sphinx-build -b html ./docs ./build/docs


Please download the files 
    - SharedLibs
    - StaticLibs 
from https://drive.google.com/drive/folders/0B0cOyLVrawK5TFJhdGJvNE9wNzg

Compiling opencv from source (MacOS)
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


Compiling opencv from source (Linux)
-------------------------------------

You will need the following packages:

    - GCC 4.4.x or later
    - CMake 2.6 or higher
    - Git
    - GTK+2.x or higher, including headers (libgtk2.0-dev)
    - pkg-config
    - Python 2.6 or later and Numpy 1.5 or later with developer packages (python-dev, python-numpy)
    - ffmpeg or libav development packages: libavcodec-dev, libavformat-dev, libswscale-dev
    - [optional] libtbb2 libtbb-dev
    - [optional] libdc1394 2.x
    - [optional] libjpeg-dev, libpng-dev, libtiff-dev, libjasper-dev, libdc1394-22-dev
    
Step 1: The packages can be installed using Terminal as follows:
    
    [compiler] sudo apt-get install build-essential
    
    [required] sudo apt-get install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
    
    [optional] sudo apt-get install python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev
    
    
Step 2: Get the latest stable version of OpenCV from https://sourceforge.net/projects/opencvlibrary/

    2a: Download the source tarball and unpack it.
    
    2b: In terminal, cd into the working directory followed by cloning the OpenCV repository::
    
        cd ~/<my_working_directory>
        
        git clone https://github.com/opencv/opencv.git
    
Step 3: Building OpenCV from source using CMake:

    3a: Create a temporary directory, here denoted as <cmake_binary_dir>, where you want to put the generated Makefiles, project files as well the object files and output binaries.
    
    3b: Enter the <cmake_binary_dir> and type::
    
        cmake <path to the OpenCV source directory>
        
Step 4: Enter the created temporary directory (<cmake_binary_dir>) and proceed with::

    make
    
    sudo make install
    
    
Running the Vision module
--------------------------

Finally, to run the entire module, run the 'RoboyVision.py' script in the 'src' folder::

       python RoboyVision.py


