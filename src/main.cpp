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

#include "RoboyAdapter.h"
 
using namespace std;
using namespace cv;

RoboyAdapter * roboyAdapter;

bool sendSteeringMessage(Rect* rect);

int main(int argc, const char** argv)
{
	roboyAdapter = new RoboyAdapter(3333, "127.0.0.1");

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
        std::vector<Rect> faces;
 
        //find faces and store them in the vector array
        face_cascade.detectMultiScale(grayscaleFrame, faces, 1.1, 3, CV_HAAR_FIND_BIGGEST_OBJECT|CV_HAAR_SCALE_IMAGE, Size(30,30));
         
        Rect biggestRect;
        double biggest_area = 0;
        for ( Rect r : faces)
        {
            if (r.size().area() > biggestRect.size().area())
            {
                biggestRect = r;
            }
        }
        
        Point pt1(biggestRect.x + biggestRect.width, biggestRect.y + biggestRect.height);
        Point pt2(biggestRect.x, biggestRect.y);
 
        rectangle(captureFrame, pt1, pt2, cvScalar(0, 255, 0, 0), 1, 8, 0);

        sendSteeringMessage(&biggestRect);
/*
        //draw a rectangle for all found faces in the vector array on the original image
        for(int i = 0; i < faces.size(); i++)
        {
            Point pt1(faces[i].x + faces[i].width, faces[i].y + faces[i].height);
            Point pt2(faces[i].x, faces[i].y);
 
            rectangle(captureFrame, pt1, pt2, cvScalar(0, 255, 0, 0), 1, 8, 0);
        }
*/ 
        //print the output
        imshow("outputCapture", captureFrame);
 
        //pause for 33ms
        waitKey(33);
    }
 
    delete roboyAdapter;

    return 0;
}

bool sendSteeringMessage(Rect* rect){
	return roboyAdapter->sendSteerHeadMessage(1, 2, 3);
}
