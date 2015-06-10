cmake_minimum_required(VERSION 3.1.0)

project( FaceDetection )

find_package( OpenCV REQUIRED )

include_directories(${CMAKE_SOURE_DIR}/src)

add_executable( facedetection src/main.cpp src/RoboyAdapter.cpp)
set_property(TARGET facedetection PROPERTY CXX_STANDARD 11)
target_link_libraries( facedetection ${OpenCV_LIBS} )
