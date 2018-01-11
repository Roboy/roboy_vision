/*
 * SOFTWARE LICENSE
 * BY USING YOUR ZED CAMERA YOU AGREE TO THIS SOFTWARE LICENSE. BEFORE SETTING IT UP,
 * PLEASE READ THIS SOFTWARE LICENSE CAREFULLY. IF YOU DO NOT ACCEPT THIS
 * SOFTWARE LICENSE, DO NOT USE YOUR ZED CAMERA. RETURN IT TO UNUSED TO
 * STEREOLABS FOR A REFUND. Contact STEREOLABS at contact@stereolabs.com
 *
 * 1. Definitions
 *
 * "Authorized Accessory" means a STEREOLABS branded ZED, and a STEREOLABS
 * licensed, third party branded, ZED hardware accessory whose packaging
 * bears the official "Licensed for ZED" logo. The ZED Camera is an Authorized
 *  Accessory solely for purpose of this Software license.
 * "Software" means the Software Development Kit, pre-installed in the ZED
 * USB flash drive included in the ZED packaging, and including any
 * updates STEREOLABS may make available from time to time.
 * "Unauthorized Accessories" means all hardware accessories other than
 * an Authorized Accessory.
 * "Unauthorized Software" means any software not distributed by STEREOLABS.
 * "You" means the user of a ZED Camera.
 *
 * 2. License
 *
 * a. The Software is licensed to You, not sold. You are licensed to use the
 * Software only as pre-installed in Your ZED USB flash drive, and updated by
 * STEREOLABS from time to time. You may not copy or reverse engineer the Software.
 *
 * b. As conditions to this Software license, You agree that:
 *       i. You will use Your Software with ZED Camera only and not with any
 * other device (including). You will not use Unauthorized Accessories.
 * They may not work or may stop working permanently after a Software update.
 *       ii. You will not use or install any Unauthorized Software.
 * If You do, Your ZED Camera may stop working permanently at that time
 * or after a later Software update.
 *       iii. You will not attempt to defeat or circumvent any Software
 * technical limitation, security, or anti-piracy system. If You do,
 * Your ZED Camera may stop working permanently at that time or after a
 * later Software update.
 *       iv. STEREOLABS may use technical measures, including Software
 * updates, to limit use of the Software to the ZED Camera, to prevent
 * use of Unauthorized Accessories, and to protect the technical limitations,
 * security and anti-piracy systems in the ZED Camera.
 *       v. STEREOLABS may update the Software from time to time without
 * further notice to You, for example, to update any technical limitation,
 * security, or anti-piracy system.
 *
 * 3. Warranty
 * The Software is covered by the Limited Warranty for Your ZED Camera,
 * and STEREOLABS gives no other guarantee, warranty, or condition for
 * the Software. No one else may give any guarantee, warranty, or condition
 * on STEREOLABS's behalf.
 *
 * 4. EXCLUSION OF CERTAIN DAMAGES
 * STEREOLABS IS NOT RESPONSIBLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, OR
 * CONSEQUENTIAL DAMAGES; ANY LOSS OF DATA, PRIVACY, CONFIDENTIALITY, OR
 * PROFITS; OR ANY INABILITY TO USE THE SOFTWARE. THESE EXCLUSIONS APPLY
 * EVEN IF STEREOLABS HAS BEEN ADVISED OF THE POSSIBILITY OF THESE DAMAGES,
 * AND EVEN IF ANY REMEDY FAILS OF ITS ESSENTIAL PURPOSE.
 *
 * 5. Choice of Law
 * French law governs the interpretation of this Software license and any
 * claim that STEREOLABS has breached it, regardless of conflict of
 * law principles.
 *
 */

#ifndef __CAMERA_HPP__
#define __CAMERA_HPP__

#include "sl/Core.hpp"
#include "sl/Mesh.hpp"
#include "sl/defines.hpp"
#include <cuda.h>

#include <opencv2/opencv.hpp>

namespace sl {

    /**
     * \class InitParameters
     * \brief Parameters for ZED initialization. A default constructor is enable.
     */
    class SLSTEREO_EXPORT_DLL InitParameters {
    public:
        /**
         *	Define the chosen ZED resolution
         *	\n default : RESOLUTION_HD720
         */
        RESOLUTION camera_resolution;

        /**
         *	Requested FPS for this resolution. set as 0 will choose the default FPS for this resolution (see User guide).
         *	\n default : 0
         */
        int camera_fps;

        /**
         *  ONLY for LINUX : if multiple ZEDs are connected, it will choose the first zed listed (if zed_linux_id=0), the second listed (if zed_linux_id=1), ...
         *  Each ZED will create its own memory (CPU and GPU), therefore the number of ZED available will depend on the configuration of your computer.
         *  Currently not available for Windows
         *	\n default : 0
         */
        int camera_linux_id;

        /**
         *	Path with filename to the recorded SVO file
         */
        sl::String svo_input_filename;

        /**
         *	When enabled the timestamp is taken as reference to determine the reading framerate.
         * This mode simulates the live camera and consequently skipped frames if the computation framerate is too slow.
         *	\n default : false
         */
        bool svo_real_time_mode;

        /**
         *	Define the unit for all the metric values ( depth, point cloud, tracking).
         *	\n default : sl::UNIT::UNIT_MILLIMETER
         */
        UNIT coordinate_units;

        /**
         *	Define the coordinate system of the world frame (and the camera frame as well). 
         *  \n This defines the order of the axis of the coordinate system. see COORDINATE_SYSTEM for more information.
         *  \n default : COORDINATE_SYSTEM::COORDINATE_SYSTEM_IMAGE
         */
        COORDINATE_SYSTEM coordinate_system;

        /**
         *	Defines the quality of the depth map, affects the level of details and also the computation time.
         *	\n default : DEPTH_MODE::DEPTH_MODE_PERFORMANCE
         */
        DEPTH_MODE depth_mode;

        /**
         *	Specify the minimum depth information that will be computed, in the sl::UNIT you previously define.
         *	\n default : 70cm (-1)
         *  \warning The computation time is affected by the value, exponentially. The closer it gets the longer the disparity search will take.
         *  In case of limited computation power, consider increasing the value.
		 *  \note This value is used to calculate the disparity range estimation ( in pixels). Due to metric to pixel conversion, a small difference may occur with the value returned by getDepthMinRange().
         */
        float depth_minimum_distance;

        /**
         *	Defines if the image are horizontally flipped.
         *	\n default : 0
         */
        int camera_image_flip;

        /**
         *	If set to true, it will disable self-calibration and take the optional calibration parameters without optimizing them.
         *	It is advised to leave it as false, so that calibration parameters can be optimized.
         *	\n default : false
         */
        bool camera_disable_self_calib;

        /**
         *  Set the number of buffers in the internal grabbing process.
         *  \n decrease this number may reduce latency but can also produce more corrupted frames.
         *  \n default:  4
         *  \warning Linux Only, this parameter has no effect on Windows.
         */
        int camera_buffer_count_linux;

        /**
         *	If set to true, it will output some information about the current status of initialization.
         *	\n default : false
         */
        bool sdk_verbose;

        /**
         *	Defines the graphics card on which the computation will be done. The default value search the more powerful (most CUDA cores) usable GPU.
         *	\n default : -1
         */
        int sdk_gpu_id;

        /**
         * \brief Default constructor, set all parameters to their default and optimized values.
         */
        InitParameters(RESOLUTION camera_resolution_ = RESOLUTION_HD720,
                       int camera_fps_ = 0,
                       int camera_linux_id_ = 0,
                       sl::String svo_input_filename_ = sl::String(),
                       bool svo_real_time_mode_ = false,
                       DEPTH_MODE depth_mode_ = DEPTH_MODE_PERFORMANCE,
                       UNIT coordinate_units_ = UNIT_MILLIMETER,
                       COORDINATE_SYSTEM coordinate_system_ = COORDINATE_SYSTEM_IMAGE,
                       bool sdk_verbose_ = false,
                       int sdk_gpu_id_ = -1,
                       float depth_minimum_distance_ = -1.,
                       bool camera_disable_self_calib_ = false,
                       bool camera_image_flip_ = false,
                       int camera_buffer_count_linux_ = 4)
            : camera_resolution(camera_resolution_)
            , camera_fps(camera_fps_)
            , camera_linux_id(camera_linux_id_)
            , svo_input_filename(svo_input_filename_)
            , svo_real_time_mode(svo_real_time_mode_)
            , depth_mode(depth_mode_)
            , coordinate_units(coordinate_units_)
            , coordinate_system(coordinate_system_)
            , sdk_verbose(sdk_verbose_)
            , sdk_gpu_id(sdk_gpu_id_)
            , depth_minimum_distance(depth_minimum_distance_)
            , camera_disable_self_calib(camera_disable_self_calib_)
            , camera_image_flip(camera_image_flip_)
            , camera_buffer_count_linux(camera_buffer_count_linux_) {
        }

        /*!
         *  \brief Saves the current bunch of parameters into a file.
         *  \param filename : the path to the file in which the parameters will be stored.
         *  \return true if file was successfully saved, otherwise false.
         */
        bool save(sl::String filename);

        /*!
         *  \brief Loads the values of the parameters contained in a file.
         *  \param filename : the path to the file from which the parameters will be loaded.
         *  \return true if the file was successfully loaded, otherwise false.
         */
        bool load(sl::String filename);
    };

    /**
     * \class RuntimeParameters.
     * \brief Contains all the Camera::grab() parameters.
     */
    class SLSTEREO_EXPORT_DLL RuntimeParameters {
    public:
        /**
         *	Defines the type of disparity map, more info : sl::SENSING_MODE definition.
         */
        SENSING_MODE sensing_mode;

        /**
         * Defines if the depth map should be computed.
         * If false, only the images are available.
         */
        bool enable_depth;

        /**
         * Defines if the point cloud should be computed (including XYZRGBA).
         */
        bool enable_point_cloud;

        /**
         * Apply the current pose to the point cloud. It means that values of point cloud will be defined in world frame (as opposite to the camera frame).
         */
        bool move_point_cloud_to_world_frame;

        /**
         * \brief Default constructor, set all parameters to their default and optimized values.
         */
        RuntimeParameters(SENSING_MODE sensing_mode_ = SENSING_MODE::SENSING_MODE_STANDARD, bool enable_depth_ = true, bool enable_point_cloud_ = true, bool move_point_cloud_to_world_frame_ = false)
            : sensing_mode(sensing_mode_)
            , enable_depth(enable_depth_)
            , enable_point_cloud(enable_point_cloud_)
            , move_point_cloud_to_world_frame(move_point_cloud_to_world_frame_) {
        }

        /*!
         *  \brief Saves the current bunch of parameters into a file.
         *  \param filename : the path to the file in which the parameters will be stored.
         *  \return true if the file was successfully saved, otherwise false.
         */
        bool save(sl::String filename);

        /*!
         * \brief Loads the values of the parameters contained in a file.
         * \param filename : the path to the file from which the parameters will be loaded.
         * \return true if the file was successfully loaded, otherwise false.
         */
        bool load(sl::String filename);
    };

    /**
     * \class TrackingParameters
     * \brief Parameters for ZED tracking initialization.
     * \n A default constructor is enabled and set to its default parameters.
     * \note Parameters can be user adjusted.
     */
    class SLSTEREO_EXPORT_DLL TrackingParameters {
    public:
        /**
         * Position of the camera in the world frame when camera is started. By default it should be identity.
         * \note The camera frame (defines the reference frame for the camera) is by default positioned at the world frame when tracking is started.
         * \n Use this sl::Transform to place the camera frame in the world frame.
         * \n default : Identity matrix
         */
        sl::Transform initial_world_transform;

        /**
         * This mode enables the camera to learn and remember its surroundings. This helps correct motion tracking drift
         * and position different cameras relative to each other in space.
         * \warning : This mode requires few resources to run and greatly improves tracking accuracy. We recommend to leave it on by default.
         * \n default : true
         */
        bool enable_spatial_memory;

        /**
         * Area localization mode can record and load (if areaFilePath is specified) a file that describes the surroundings.
         * \note Loading an area file will start a searching phase during which the camera will try to position itself in the previously learned area.
         * \warning : The area file describes a specific location. If you are using an area file describing a different location, the tracking function will continuously search for a position and may not find a correct one.
         * \warning The '.area' file can only be used with the same depth mode (sl::MODE) as the one used during area recording.
         * \n default : NULL
         */
        sl::String area_file_path;

        /**
         * \brief  Default constructor, set all parameters to their default and optimized values.
         */
        TrackingParameters(sl::Transform init_pos = sl::Transform(), bool _enable_memory = true, sl::String _area_path = sl::String())
            : initial_world_transform(init_pos)
            , enable_spatial_memory(_enable_memory)
            , area_file_path(_area_path) {
        }

        /*!
         * \brief Saves the current bunch of parameters into a file.
         * \param filename : the path to the file in which the parameters will be stored.
         * \return true if the file was successfully saved, otherwise false.
         */
        bool save(sl::String filename);

        /*!
         *  \brief Loads the values of the parameters contained in a file.
         * \param filename : the path to the file from which the parameters will be loaded.
         * \return true if the file was successfully loaded, otherwise false.
         */
        bool load(sl::String filename);
    };

    /**
     * \class SpatialMappingParameters
     * \brief Parameters for ZED scanning initialization.
     * \n A default constructor is enabled and set to its default parameters.
     * \note Parameters can be user adjusted.
     */
    class SLSTEREO_EXPORT_DLL SpatialMappingParameters {
    public:
        typedef std::pair<float, float> interval;
        /**
         * \enum RESOLUTION
         * \ingroup Enumerations
         * \brief List the spatial mapping resolution presets.
         */
        typedef enum {
            RESOLUTION_HIGH,   /*!< Create a detail geometry, requires lots of memory.*/
            RESOLUTION_MEDIUM, /*!< Smalls variations in the geometry will disappear, useful for big object*/
            RESOLUTION_LOW     /*!< Keeps only huge variations of the geometry , useful outdoor.*/
        } RESOLUTION;

        /**
         * \enum RANGE
         * \ingroup Enumerations
         * \brief List the spatial mapping depth range presets.
         */
        typedef enum {
            RANGE_NEAR,   /*!< Only depth close to the camera will be used by the spatial mapping.*/
            RANGE_MEDIUM, /*!< Medium depth range.*/
            RANGE_FAR     /*!< Takes into account objects that are far, useful outdoor.*/
        } RANGE;

        /**
         * \brief Default constructor, set all parameters to their default and optimized values.
         */
        SpatialMappingParameters(RESOLUTION resolution = RESOLUTION_HIGH,
                                 RANGE range = RANGE_MEDIUM,
                                 int max_memory_usage_ = 2048, // Maximum RAM allowed in MB (power of 2, ex: 512, 1024, 2048...)
                                 bool save_texture_ = true) {
            max_memory_usage = max_memory_usage_;
            save_texture = save_texture_;
            set(resolution);
            set(range);
        }

        /*!
         * \brief Return the resolution corresponding to the given sl::SpatialMappingParameters::RESOLUTION preset.
         * \param resolution : the desired sl::SpatialMappingParameters::RESOLUTION.
         * \return The resolution in meter.
         */
        static float get(RESOLUTION resolution = RESOLUTION_HIGH) {
            float resolution_m = 0.5f;
            switch (resolution) {
            case SpatialMappingParameters::RESOLUTION_HIGH:
                resolution_m = 0.02f;
                break;
            case SpatialMappingParameters::RESOLUTION_MEDIUM:
                resolution_m = 0.05f;
                break;
            case SpatialMappingParameters::RESOLUTION_LOW:
                resolution_m = 0.08f;
                break;
            default:
                resolution_m = 0.05f;
                break;
            }
            return resolution_m;
        }

        /*!
        * \brief Sets the resolution corresponding to the given sl::SpatialMappingParameters::RESOLUTION preset.
        * \param resolution : the desired sl::SpatialMappingParameters::RESOLUTION.
        */
        void set(RESOLUTION resolution = RESOLUTION_HIGH) {
            resolution_meter = get(resolution);
        }

        /*!
         * \brief  Return the maximum value of depth corresponding to the given sl::SpatialMappingParameters::RANGE presets.
         * \param range : the desired sl::SpatialMappingParameters::RANGE.
         * \return The maximum value of depth.
         */
        static float get(RANGE range = RANGE_MEDIUM) {
            float range_max = 5.;
            switch (range) {
            case SpatialMappingParameters::RANGE_NEAR:
                range_max = 3.5f;
                break;
            case SpatialMappingParameters::RANGE_MEDIUM:
                range_max = 5.f;
                break;
            case SpatialMappingParameters::RANGE_FAR:
                range_max = 10.f;
                break;
            default:
                range_max = 5.f;
                break;
            }
            return range_max;
        }

        /*!
        * \brief Sets the maximum value of depth corresponding to the given sl::SpatialMappingParameters::RANGE presets.
        * \param range : the desired sl::SpatialMappingParameters::RANGE.
        */
        void set(RANGE range = RANGE_MEDIUM) {
            range_meter.second = get(range);
        }

        /*!
         * \brief The maximum CPU memory (in mega bytes) allocated for the meshing process (will fit your configuration in any case).
         */
        int max_memory_usage = 2048;

        /*!
         * \brief Set to true if you want be able to apply texture to your mesh after its creation.
         * \note This option will take more memory.
         */
        bool save_texture = true;
        
        /*!
        * \brief The minimal depth value allowed by the spatial mapping.
        */
        const interval allowed_min = std::make_pair(0.3f, 10.f);

        /*!
        * \brief The maximal depth value allowed by the spatial mapping.
        */
        const interval allowed_max = std::make_pair(2.f, 20.f);

        /*!
        * \brief Depth integration range in meters.
        * \n
        * range_meter.first  should fit interval::allowed_min.\n
        * range_meter.first will be set to sl::Camera::getDepthMinRangeValue if you do not change it.\n
        * range_meter.second  should fit interval::allowed_max.
        */
        interval range_meter = std::make_pair(0.7f, 5.f);

        /*!
        * \brief The resolutions allowed by the spatial mapping.
        */
        const interval allowed_resolution = std::make_pair(0.01f, 0.2f);

        /*!
        *  \brief Spatial mapping resolution in meters, should fit interval::allowed_resolution.
        */
        float resolution_meter = 0.03f;

        /*!
         * \brief Saves the current bunch of parameters into a file.
         * \param filename : the path to the file in which the parameters will be stored.
         * \return true if the file was successfully saved, otherwise false.
         */
        bool save(sl::String filename);

        /*!
         *  \brief Loads the values of the parameters contained in a file.
         * \param filename : the path to the file from which the parameters will be loaded.
         * \return true if the file was successfully loaded, otherwise false.
         */
        bool load(sl::String filename);
        

    };

    /**
     * \class Pose
     * \brief The class Pose contains the Motion tracking data which gives the position and orientation of the ZED in space
     *  (orientation/quaternion, rotation matrix, translation/position) and other connected values (timestamp, confidence).
     */
    class SLSTEREO_EXPORT_DLL Pose {
    public:
        /*!
         * \brief Default constructor which creates an empty Pose.
         */
        Pose();

        /*!
         *  \brief Pose constructor with deep copy.
         */
        Pose(const Pose &pose);

        /*!
         *  \brief Pose constructor with deep copy.
         */
        Pose(const sl::Transform &pose_data, unsigned long long mtimestamp = 0, int mconfidence = 0);

        /*!
         * \brief Pose destructor.
         */
        ~Pose();

        /*!
         * \brief Returns the camera translation from the pose.
         * \return The translation vector of the ZED position.
         */
        sl::Translation getTranslation();

        /*!
         * \brief Returns the camera orientation from the pose.
         * \return The orientation vector of the ZED position.
         */
        sl::Orientation getOrientation();

        /*!
         *  brief Returns the camera rotation (3x3) from the pose.
         * \return The rotation matrix of the ZED position.
         */
        sl::Rotation getRotation();

        /*!
         *  \brief Returns the camera rotation (3x1) of the pose.
         * \return The rotation vector of the ZED position.
         */
        sl::Vector3<float> getRotationVector();

        /*! boolean that indicates if tracking is activated or not. You should check that first if something wrong.*/
        bool valid;

        /*! Timestamp of the pose. This timestamp should be compared with the camera timestamp for synchronization.*/
        unsigned long long timestamp;

        /*! 4x4 Matrix which contains the rotation (3x3) and the translation. Orientation is extracted from this transform as well.*/
        sl::Transform pose_data;

        /*! Confidence/Quality of the pose estimation for the target frame
         * \n A confidence metric of the tracking [0-100], 0 means that the tracking is lost, 100 means that the tracking can be fully trusted.
         */
        int pose_confidence;
    };

    class CameraMemberHandler;

    /*! \class Camera
     *  \brief The main class to use the ZED camera.
     */
    class SLSTEREO_EXPORT_DLL Camera {
    public:
        /*!
         * \brief Default constructor which creates an empty Camera.
         */
        Camera();

        /*!
         *  \brief Camera destructor.
         */
        ~Camera();

        /*!
         * \brief Closes the camera and free the memory. 
         * Camera::open can then be called again to reset the camera if needed.
         */
        void close();

        /*!
         * \brief Opens the ZED camera in the desired mode (live/SVO), sets all the defined parameters, checks hardware requirements and launch internal self calibration.
         * \param init_parameters : a structure containing all the individual parameters
         *
         * \return An error code given informations about the
         * internal process, if SUCCESS is returned, the camera is ready to use.
         * Every other code indicates an error and the program should be stopped.
         * For more details see sl::ERROR_CODE.
         */
        ERROR_CODE open(InitParameters init_parameters = InitParameters());

        /*!
         * \brief Tests if the camera is opened and running
         * \return true if the ZED is already setup, otherwise false.
         */
        inline bool isOpened() {
            return opened;
        }

        /*!
         * \brief Grabs a new image, rectifies it and computes the
         * disparity map and optionally the depth map.
         * The grabbing function is typically called in the main loop.
         *
         * \param rt_parameters : a structure containing all the individual parameters.
         * \return An sl::SUCCESS if no problem was encountered,
         * sl::ERROR_CODE_NOT_A_NEW_FRAME otherwise if something wrong happens
         */
        ERROR_CODE grab(RuntimeParameters rt_parameters = RuntimeParameters());

        /*!
         * \brief Downloads the rectified image from the device and returns the CPU buffer.
         * The retrieve function should be called after the function Camera::grab
         *
         * \param mat : the Mat to store the image.
         * \param view  : defines the image side wanted (see sl::VIEW)
         * \param type : the memory type desired. sl::MEM_CPU by default.
         * \return SUCCESS if the method succeeded, ERROR_CODE_FAILURE if an error occurred.
         */
        ERROR_CODE retrieveImage(Mat &mat, VIEW view = VIEW_LEFT, MEM type = MEM_CPU);

        /*!
         * \brief Downloads the measure (disparity, depth or confidence of disparity)
         * from the device and returns the CPU buffer.
         * The retrieve function should be called after the function Camera::grab
         *
         * \param mat : the Mat to store the measures.
         * \param measure : defines the type wanted, such as disparity map,
         * depth map or the confidence (see sl::MEASURE)
         * \param type : the memory type desired. sl::MEM_CPU by default.
         * \return SUCCESS if the method succeeded, ERROR_CODE_FAILURE if an error occurred.
         */
        ERROR_CODE retrieveMeasure(Mat &mat, MEASURE measure = MEASURE_DEPTH, MEM type = MEM_CPU);

        /*!
         * \brief Sets a threshold for the disparity map confidence
         * (and by extension the depth map). The function should be called before
         * Camera::grab to be taken into account.
         * \param conf_threshold_value : a value in [1,100]. A lower value means more confidence and precision
         * (but less density), an upper value reduces the filtering (more density, less certainty).
         * Other value means no filtering.
         */
        void setConfidenceThreshold(int conf_threshold_value);

        /*!
         * \brief Returns the current confidence threshold value apply to the disparity map
         * (and by extension the depth map).
         * \return The current threshold value between 0 and 100.
         */
        int getConfidenceThreshold();

        /*!
         *  \brief Returns the CUDA context used for all the computation.
         *  \return The CUDA context created by the inner process.
         */
        CUcontext getCUDAContext();

        /*!
         *  \brief Returns the current image size.
         *  \return The image resolution.
         */
        Resolution getResolution();

        /*!
         *  \brief Sets the maximum distance of depth/disparity estimation (all values after this limit will be reported as TOO_FAR value).
         *  \param depth_max_range : maximum distance in the defined sl::UNIT.
         */
        void setDepthMaxRangeValue(float depth_max_range);

        /*!
         *  \brief Returns the current maximum distance of depth/disparity estimation.
         *  \return The current maximum distance that can be computed in the defined sl::UNIT.
         */
        float getDepthMaxRangeValue();

        /*!
         *  \brief Returns the closest measurable distance by the camera, according to the camera and the depth map parameters.
         *  \return The minimum distance that can be computed in the defined sl::UNIT.
         */
        float getDepthMinRangeValue();

        //@{
        /**  @name Camera infos */
        /*!
         * \brief Sets the position of the SVO file to a desired frame.
         * \param frame_number : the number of the desired frame to be decoded.
         * \note Works only if the camera is open in SVO playback mode.
         */
        void setSVOPosition(int frame_number);

        /*!
         *  \brief Returns the current position of the SVO file.
         * \return The current position in the SVO file as int (-1 if the SDK is not reading a SVO).
         * \note Works only if the camera is open in SVO reading mode.
         */
        int getSVOPosition();

        /*!
         * \brief Returns the number of frames in the SVO file.
         * \return The total number of frames in the SVO file (-1 if the SDK is not reading a SVO).
         * \note Works only if the camera is open in SVO reading mode.
         */
        int getSVONumberOfFrames();

        /*!
         * \brief Sets the value to the corresponding sl::CAMERA_SETTINGS (Gain, brightness, hue, exposure...).
         * \param settings : enum for the control mode.
         * \param value : value to set for the corresponding control.
         * \param use_default : will set default (or automatic) value if set to true (value (int) will not be taken into account).
         * \note Works only if the camera is open in live mode.
         */
        void setCameraSettings(CAMERA_SETTINGS settings, int value, bool use_default = false);

        /*!
         * \brief Returns the current value to the corresponding sl::CAMERA_SETTINGS (Gain, brightness, hue, exposure...).
         * \param setting : enum for the control mode.
         * \return The current value for the corresponding control (-1 if something wrong happened).
         * \note Works only if the camera is open in live mode.
         */
        int getCameraSettings(CAMERA_SETTINGS setting);

        /*!
         *  \brief Returns the current FPS of the camera.
         *  \return The current FPS (or recorded FPS for SVO). Return -1.f if something goes wrong.
         */
        float getCameraFPS();

        /*!
         * \brief Sets a new frame rate for the camera, or the closest available frame rate.
         * \param desired_fps : the new desired frame rate.
         * \note Works only if the camera is open in live mode.
         */
        void setCameraFPS(int desired_fps);

        /*!
         *  \brief Returns the current FPS of the application/callback.
         *  \n It is based on the difference of camera timestamps between two successful grab(). 
         *  \return The current FPS of the application (if grab leads the application) or callback (if ZED is called in a thread)
         */
        float getCurrentFPS();

        /*!
         *  \brief Returns the timestamp at the time the frame has been extracted from USB stream. (should be called after a grab()).
         *  \return The timestamp of the frame grab in ns. -1 if not available (SVO file without compression).
         *  \note SVO file from SDK 1.0.0 (with compression) contains the camera timestamp for each frame.
         */
        unsigned long long getCameraTimestamp();

        /*!
         *  \brief Returns the current timestamp at the time the function is called. Can be compared to the camera sl::Camera::getCameraTimestamp for synchronization.
         *  \n Use this function to compare the current timestamp and the camera timestamp, since they have the same reference (Computer start time).
         *  \return The current timestamp in ns.
         */
        unsigned long long getCurrentTimestamp();

        /*!
         *  \brief Returns the number of frame dropped since sl::Camera::grab has been called for the first time.
         *  \n Based on camera timestamp and FPS comparison.
         *  \return The number of frame dropped since first sl::Camera::grab call.
         */
        unsigned int getFrameDroppedCount();

        /*!
         * \brief Returns camera informations (calibration parameters, serial number and current firmware version).
         * \return CameraInformation containing the calibration parameters of the ZED, as well as serial number and firmware version
         * It also returns the ZED Serial Number (as uint) (Live or SVO) and the ZED Firmware version (as uint), 0 if the ZED is not connected.
         */
        CameraInformation getCameraInformation();
        //@}

        //@{
        /**  @name Self calibration */
        /*!
         * \brief Returns the current status of the self-calibration.
         * \return A status code given informations about the self calibration status.
         * For more details see sl::SELF_CALIBRATION_STATE.
         */
        SELF_CALIBRATION_STATE getSelfCalibrationState();

        /*!
         *  \brief Resets the self camera calibration. This function can be called at any time AFTER the sl::Camera::open function has been called.
         *  It will reset and calculate again correction for misalignment, convergence and color mismatch.
         *  It can be called after changing camera parameters without needing to restart your executable.
         *
         * if no problem was encountered, the camera will use new parameters. Otherwise, it will be the old ones.
         */
        void resetSelfCalibration();
        //@}

        // -----------------------------------------------------------------
        //                         Tracking functions:
        // -----------------------------------------------------------------
        //@{
        /**  @name Tracking */
        /*!
         *  \brief Initializes and start the tracking processes.
         *  \param tracking_params : Structure of sl::TrackingParameters, which defines specific parameters for tracking.
         *  \n default : Leave it empty to get best default parameters or create your own structure to change tracking parameters according to sl::TrackingParameters documentation.
         *  \return sl::ERROR_CODE_FAILURE if the sl::TrackingParameters::area_file_path file wasn't found, sl::SUCCESS otherwise.
         *  \warning The area localization is a beta feature, the behavior might change in the future.
         */
        ERROR_CODE enableTracking(TrackingParameters tracking_params = TrackingParameters());

        /*!
         *  \brief Fills the position of the camera frame in the world frame and return the current state of the Tracker.
         *  \note The camera frame is positioned at the back of the left eye of the ZED. 
         *  \param camera_pose (out) : the pose containing the position of the camera (path or position) and other information (timestamp, confidence)
         *  \param reference_frame : defines the reference from which you want the pose to be expressed.
         *  \return The current state of the tracking process.
         * 
         * \n Extract Rotation Matrix : camera_pose.getRotation();
         * \n Extract Translation Vector: camera_pose.getTranslation();
         * \n Convert to Orientation / quaternion : camera_pose.getOrientation();
         */
        sl::TRACKING_STATE getPosition(sl::Pose &camera_pose, REFERENCE_FRAME reference_frame = sl::REFERENCE_FRAME_WORLD);

        /*!
         *  \brief Returns the state of exportation of the area database (spatial memory).
         *  \return The current state of the exportation of the area file.
         */
        sl::AREA_EXPORT_STATE getAreaExportState();

        /*!
         *  \brief Disables motion tracking
         *  \param area_file_path (optional) : if set, save the spatial database in a '.area' file.
         * areaFilePath is the name and path of the database, e.g. : "path/to/file/myArea1.area".
         *
         *  \warning This feature is still in beta, you might encounter reloading issues.
         *  \n Please also note that the '.area' database depends on the depth map sl::SENSING_MODE chosen during the recording. The same mode must be used to reload the database.
         *  \note The saving is done asynchronously, the state can be get by getAreaExportState().
         */
        void disableTracking(sl::String area_file_path = "");

        /*!
         *  \brief Resets the tracking, re-initializes the path with the transformation matrix given.
         *  \note Please note that this function will also flush the area database built / loaded.
         */
        void resetTracking(sl::Transform &path);
        //@}

        // -----------------------------------------------------------------
        //                         Spatial Mapping functions:
        // -----------------------------------------------------------------
        //@{
        /**  @name Spatial Mapping */
        /*!
         *  \brief Initializes and starts the spatial mapping processes.
         * The spatial mapping will create a geometric representation of the scene based on both tracking data and 3D point clouds.
         * The resulting output is a sl::Mesh and can be obtained by the sl::Camera::extractWholeMesh function or with sl::Camera::retrieveMeshAsync after calling sl::Camera::requestMeshAsync.
         *  \param spatial_mapping_parameters : the structure containing all the specific parameters for the spatial mapping.
         *  \n default : Leave it empty to get best default parameters or initialize it from a preset. For more informations,
         * checkout the sl::SpatialMappingParameters documentation.
         *  \return sl::SUCCESS if everything went fine, sl::ERROR_CODE_FAILURE otherwise
         *  \warning The tracking needs to be enabled to create a map
         *  \warning The performance greatly depends on the input parameters.
         * If the mapping framerate is too slow in live mode, consider using a SVO file, or choose a coarser mesh resolution
         *  \note This features is using host memory (RAM) to store the 3D map,
         * the maximum amount of available memory allowed can be tweaked using the SpatialMappingParameters.
         */
        ERROR_CODE enableSpatialMapping(SpatialMappingParameters spatial_mapping_parameters = SpatialMappingParameters());

        /*!
         *  \brief Switches the pause status of the data integration mechanism for the spatial mapping.
         *  \param status : if true, the integration is paused. If false, the spatial mapping is resumed.
         */
        void pauseSpatialMapping(bool status);

        /*!
         *  \brief Returns the current spatial mapping state.
         *  \return status The current state of the spatial mapping process
         */
        SPATIAL_MAPPING_STATE getSpatialMappingState();

        // -----------------------------------------------------------------
        // Blocking (synchronous) function of mesh generation
        // -----------------------------------------------------------------
        /*!
         *  \brief Extracts the current mesh from the spatial mapping process.
         *  \note This function will return when the mesh has been created or updated. This is therefore a blocking function. You should either call it in a thread or at the end of the mapping process.
         *  Calling this function in the grab loop will block the depth and tracking computation and therefore gives bad results.
         *  \param mesh (out) : The mesh to be filled.
         *  \return sl::SUCCESS if the mesh is filled and available, otherwise sl::ERROR_CODE_FAILURE.
         */
        ERROR_CODE extractWholeMesh(sl::Mesh &mesh);

        // -----------------------------------------------------------------
        // Async functions of mesh generation ( *Async())
        // -----------------------------------------------------------------
        /*!
         *  \brief Starts the mesh generation process in a non blocking thread from the spatial mapping process.
         *  \note Only one mesh generation can be done at a time, consequently while the previous launch is not done every call will be ignored.
         */
        void requestMeshAsync();

        /*!
         *  \brief Returns the mesh generation status, useful to after calling requestMeshAsync.
         *  \return sl::SUCCESS if the mesh is ready and not yet retrieved, otherwise sl::ERROR_CODE_FAILURE.
         */
        ERROR_CODE getMeshRequestStatusAsync();

        /*!
         *  \brief Retrieves the generated mesh after calling requestMeshAsync.
         *  \param mesh (out) : The mesh to be filled.
         *  \return sl::SUCCESS if the mesh is retrieved, otherwise sl::ERROR_CODE_FAILURE.
         */
        ERROR_CODE retrieveMeshAsync(sl::Mesh &mesh);

        /*!
         *  \brief Disables the Spatial Mapping process.
         *  All the spatial mapping functions are disables, mesh cannot be retrieves after this call.
         */
        void disableSpatialMapping();
        //@}

        // -----------------------------------------------------------------
        //                 Specific When Recording mode is activated
        // -----------------------------------------------------------------
        //@{
        /**  @name Recorder */

        /*!
         *  \brief Creates a file for recording the current frames.
         *  \param video_filename : can be a *.svo file or a *.avi file (detected by the suffix name provided).
         *  \param compression_mode : can be one of the sl::SVO_COMPRESSION_MODE enum.
         *  \warning This function can be called multiple times during ZED lifetime, but if video_filename is already existing, the file will be erased.
         *  \return an sl::ERROR_CODE that defines if file was successfully created and can be filled with images.
         *  \n * sl::SUCCESS if file can be filled
         *  \n * sl::ERROR_CODE_SVO_RECORDING_ERROR if something wrong happens.
         */
        ERROR_CODE enableRecording(sl::String video_filename, SVO_COMPRESSION_MODE compression_mode = SVO_COMPRESSION_MODE_LOSSLESS);

        /*!
         *  \brief Records the current frame provided by grab() into the file.
         *  \warning grab() must be called before record() to take the last frame available. Otherwise, it will be the last grabbed frame.
         *  \return The recording state structure, for more details see sl::RecordingState.
         */
        sl::RecordingState record();

        /*!
         *  \brief Disables the recording and closes the generated file.
         */
        void disableRecording();
        //@}

        // -----------------------------------------------------------------
        //                         Utils (static)
        // -----------------------------------------------------------------
        /*!
         *  \brief Returns the version of the currently installed ZED SDK.
         *  \return The ZED SDK version as a string with the following format : MAJOR.MINOR.PATCH
         */
        static sl::String getSDKVersion();

        /*!
         *  \brief Checks if ZED cameras are connected, can be called before instantiating a Camera object.
         *  \return The number of connected ZED.
         *  \warning On Windows, only one ZED is accessible so this function will return 1 even if multiple ZED are connected.
         */
        static int isZEDconnected();

        /*!
         *  \brief Sticks the calling thread to a specific CPU core. This function is only available for Jetson TK1 and TX1.
         *  \param cpuCore : int that defines the core the thread must be run on. could be between 0 and 3. (cpu0,cpu1,cpu2,cpu3).
         *  \return sl::SUCCESS if stick is OK, otherwise status error.
         *  \warning Function only available for Jetson. On other platform, result will be always 0 and no operations are performed.
         */
        static sl::ERROR_CODE sticktoCPUCore(int cpu_core);

    private:
        ERROR_CODE openCamera(bool);
        bool nextImage(bool);
        int initMemory();
        bool initRectifier();
        CameraMemberHandler *h = 0;
        bool opened = false;
    };
    /*!
     *  \brief Writes the current depth map into a file.
     *  \param zed : the current camera object.
     *  \param format : the depth file format you desired.
     *  \param name : the name (path) in which the depth will be saved.
     *  \param factor : only for PNG and PGM, apply a gain to the depth value (default 1.).
     *  The maximum value is 65536, so you can set the Camera::setDepthClampValue to 20000 and give a factor to 3, Do not forget to scale (by 1./factor) the pixel value to get the real depth.
     *  The occlusions are represented by 0.
     *  \return False if something wrong happen, else return true.
     */
    extern "C" SLSTEREO_EXPORT_DLL bool saveDepthAs(sl::Camera &zed, sl::DEPTH_FORMAT format, sl::String name, float factor = 1.);

    /*!
     *  \brief Writes the current point cloud into a file
     *  \param zed : the current camera object.
     *  \param format : the point cloud file format you desired.
     *  \param name : the name (path) in which the point cloud will be saved.
     *  \param with_color : indicates if the color must be saved (default false). Not available for XYZ and VTK.
     *  \param keep_occluded_point : indicates if the non available data should be saved and set to 0 (default false), if set to true this give a Point Cloud with a size = height * width.
     *  \return False if something wrong happen, else return true.
     *  \note The color is not saved for XYZ and VTK files.
     */
    extern "C" SLSTEREO_EXPORT_DLL bool savePointCloudAs(sl::Camera &zed, sl::POINT_CLOUD_FORMAT format, sl::String name, bool with_color = false, bool keep_occluded_point = false);
}

#endif /* __CAMERA_HPP__ */
