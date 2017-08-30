/**********************************
 **Using ZED with OpenCV
 **********************************/

#include <iostream>

// OpenCV
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

// ZED
#include <zed/Camera.hpp>

// Input from keyboard
char keyboard = ' ';

int main(int argc, char** argv)
{
	// Initialize ZED color stream in HD and depth in Performance mode
	sl::zed::Camera* zed = new sl::zed::Camera(sl::zed::HD1080);
	sl::zed::ERRCODE err = zed->init(sl::zed::MODE::PERFORMANCE, 0, true);

	// Quit if an error occurred
	if (err != sl::zed::SUCCESS) {
		std::cout << "Unable to init the ZED:" << errcode2str(err) << std::endl;
		delete zed;
		return 1;
	}

	// Initialize color image and depth
	int width = zed->getImageSize().width;
	int height = zed->getImageSize().height;
	cv::Mat image(height, width, CV_8UC4,1);
	cv::Mat depth(height, width, CV_8UC4,1);

	// Create OpenCV windows
	cv::namedWindow("Image", cv::WINDOW_AUTOSIZE);
	cv::namedWindow("Depth", cv::WINDOW_AUTOSIZE);

	// Settings for windows
	cv::Size displaySize(720, 404);
	cv::Mat imageDisplay(displaySize, CV_8UC4);
	cv::Mat depthDisplay(displaySize, CV_8UC4);

	// Loop until 'q' is pressed
	while (keyboard != 'q') {

		// Grab frame and compute depth in FILL sensing mode
		if (!zed->grab(sl::zed::SENSING_MODE::FILL))
		{

			// Retrieve left color image
			sl::zed::Mat left = zed->retrieveImage(sl::zed::SIDE::LEFT);
			memcpy(image.data,left.data,width*height*4*sizeof(uchar));

			// Retrieve depth map
			sl::zed::Mat depthmap = zed->normalizeMeasure(sl::zed::MEASURE::DEPTH);
			memcpy(depth.data,depthmap.data,width*height*4*sizeof(uchar));

			// Display image in OpenCV window
			cv::resize(image, imageDisplay, displaySize);
			cv::imshow("Image", imageDisplay);

			// Display depth map in OpenCV window
			cv::resize(depth, depthDisplay, displaySize);
			cv::imshow("Depth", depthDisplay);
		}

		keyboard = cv::waitKey(30);

	}

	delete zed;

}
