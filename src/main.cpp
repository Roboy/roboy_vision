#include <opencv2/objdetect/objdetect.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
 
#include <iostream>
#include <stdio.h>

#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

#include <string>
#include <cmath>

#include "RoboyAdapter.h"
 
using namespace std;
using namespace cv;

#define IP_ADDRESS_RB "10.183.112.47"
#define IP_ADDREES_LO "127.0.0.1"
#define PORT		  30000

int main(int argc, const char** argv)
{
	double yaw = 0.0, pitch = 0.0, roll = 0.0;
	int dt = 33;

	RoboyAdapter roboyAdapter(IP_ADDRESS_RB, PORT);

	//create the cascade classifier object used for the face detection
    CascadeClassifier face_cascade;
    //use the haarcascade_frontalface_alt.xml library
    face_cascade.load("../haarcascade_frontalface_alt.xml");
 
    //setup video capture device and link it to the first capture device
    VideoCapture captureDevice;
    captureDevice.open(0);
 
    //setup image files used in the capture process
    Mat captureFrame;
    Mat grayscaleFrame;
 
    //create a window to present the results
    namedWindow("outputCapture", 1);
 
    //create a loop to capture and find faces
    while(true)
    {
        //capture a new image frame
        captureDevice>>captureFrame;
 
        //convert captured image to gray scale and equalize
        cvtColor(captureFrame, grayscaleFrame, CV_BGR2GRAY);
        equalizeHist(grayscaleFrame, grayscaleFrame);
 
        //create a vector array to store the face found
        vector<Rect> faces;
 
        //find faces and store them in the vector array
        face_cascade.detectMultiScale(grayscaleFrame, faces, 1.1, 3, CV_HAAR_FIND_BIGGEST_OBJECT|CV_HAAR_SCALE_IMAGE, Size(30,30));
         
	    if( faces.size() > 0 ) {
        	Rect biggestRect;
        	for ( Rect r : faces) {
				if (r.size().area() > biggestRect.size().area())
					biggestRect = r;
			}

			Point pt1 = biggestRect.br();
			Point pt2 = biggestRect.tl();

			rectangle(captureFrame, pt1, pt2, cvScalar(0, 255, 0, 0), 1, 8, 0);

			double u = (biggestRect.x + biggestRect.width * 0.5) / captureFrame.size().width - 0.5;
			double v = (biggestRect.y + biggestRect.height * 0.5) / captureFrame.size().height - 0.5;

			double epsylon = 1 / 12;

			if (abs(u) > epsylon) {
				u > 0 ? u = 1 : u = -1;
			} else {
				u = 0;
			}

			yaw += u;

//			yaw -= u * 12;
//			yaw -= 0.2 * dt * u;

			roboyAdapter.sendSteerHeadMessage(0, 0, floor(yaw+0.5));
        }

        //print the output
        imshow("outputCapture", captureFrame);
 
        //pause for 33ms
        waitKey(dt);
    }

    return 0;
}
