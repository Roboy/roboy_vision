
# Setup to run on roboy NUKE for final

#run ros services with python2
#source /home/roboy/Vision/devel/setup.bash
#rosrun vision_service face_detector.py 
#rosrun vision_service recognizer.py

# source roboy conda environment
source /home/roboy/anaconda3/bin/activate roboy

# export path to be used for dirty communication workaround
export VISION_COMM_PATH=/home/roboy/Vision/PYTHON3_COMM/

# added library pathes to system path
export PYTHONPATH="/home/roboy/anaconda3/envs/roboy/lib/python3.6/site-packages:$PYTHONPATH:/home/roboy/Vision/"

#run face detection
python src/face_detection.py



