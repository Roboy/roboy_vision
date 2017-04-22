cmake_minimum_required(VERSION 2.8.3)
project(vision_service)

find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  rospy
  std_msgs
  message_generation
)

add_message_files(
  FILES 
  vision_object.msg
)

add_service_files(
  FILES
  wakeup.srv
  recognition.srv
)

generate_messages(
  DEPENDENCIES
  geometry_msgs
  std_msgs
)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES vision_service
  CATKIN_DEPENDS message_runtime geometry_msgs rospy std_msgs
#  DEPENDS system_lib
)

###########
## Build ##
###########

include_directories(
  ${catkin_INCLUDE_DIRS}
)

