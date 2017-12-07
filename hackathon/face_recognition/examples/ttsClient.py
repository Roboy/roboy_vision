#!/usr/bin/env python


import rospy


import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from roboy_communication_cognition.srv import Talk

def ts_client(TextToTalk):
	rospy.wait_for_service("/roboy/cognition/speech/synthesis/talk")
	try:
		ts = rospy.ServiceProxy('/roboy/cognition/speech/synthesis/talk', Talk)
		resp = ts(TextToTalk)
		print resp.success

	except rospy.ServiceException, e:
		print "Service call failed: %s"%e

if __name__ == "__main__":
	ts_client("robotender")
