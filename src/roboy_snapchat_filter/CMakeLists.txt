cmake_minimum_required(VERSION 2.8.3)
project(roboy_snapchat_filter)

SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -g")

## Find catkin macros and libraries
find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  message_generation
  roboy_communication_cognition
)


catkin_package(
  CATKIN_DEPENDS roscpp rospy std_msgs message_generation roboy_communication_cognition
)


#############
## Install ##
#############
## Mark executable scripts (Python etc.) for installation
## in contrast to setup.py, you can choose the destination
 install(PROGRAMS
   scripts/snapchat_server.py
   DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
 )

## Mark other files for installation (e.g. launch and bag files, etc.)
 install(DIRECTORY launch 
	DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})
