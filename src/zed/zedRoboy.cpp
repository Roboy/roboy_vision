#include <sl/Camera.hpp>
#include "utils.hpp"

using namespace std;

sl::Camera InitCamera () {
 // Parse command line arguments and store them in a Option structure
    InfoOption modes;
    parse_args(argc, argv, modes);


    // Create a ZED camera and Configure parameters according to command line options
    sl::Camera zed;
    sl::InitParameters initParameters;
    if (!modes.recordingMode) initParameters.svo_input_filename = modes.svo_path.c_str();
    else initParameters.camera_fps = 30;

    if (!modes.computeDisparity) initParameters.depth_mode = sl::DEPTH_MODE_NONE;

    // Open the ZED
    sl::ERROR_CODE err = zed.open(initParameters);
    if (err != sl::SUCCESS) {
        cout << sl::errorCode2str(err) << endl;
        zed.close();
        return 1; // Quit if an error occurred
    }


    // If recording mode has been activated, enable the recording module.
    if (modes.recordingMode) {
        sl::ERROR_CODE err = zed.enableRecording(modes.svo_path.c_str(), sl::SVO_COMPRESSION_MODE::SVO_COMPRESSION_MODE_LOSSLESS);

        if (err != sl::SUCCESS) {
            std::cout << "Error while recording. " << errorCode2str(err) << " " << err << std::endl;
            if (err == sl::ERROR_CODE_SVO_RECORDING_ERROR) std::cout << " Note : This error mostly comes from a wrong path or missing writting permissions..." << std::endl;
            zed.close();
            return 1;
        }
    }


    // Setup key, images, times
    
    // Defines actions to do, according to options
    initActions(&zed, modes);

    return zed;

}


int main(int argc, char **argv){

InitCamera()
return 0

}
