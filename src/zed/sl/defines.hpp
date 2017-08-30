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

#ifndef __DEFINES_HPP__
#define __DEFINES_HPP__

#include <cstdint>
#include <cstring>
#include <iostream>
#include <vector>

#ifdef _WIN32
#include <Windows.h>
#include <direct.h>
#else /* _WIN32 */
#include <limits>
#include <unistd.h>
#endif /* _WIN32 */

#if defined WIN32
#if defined(SL_SDK_EXPORT)
#define SLSTEREO_EXPORT_DLL __declspec(dllexport)
#else
#define SLSTEREO_EXPORT_DLL __declspec(dllimport)
#endif
#elif __GNUC__
#define SLSTEREO_EXPORT_DLL __attribute__((visibility("default")))
#if defined(__arm__) || defined(__aarch64__)
#define _SL_JETSON_
#endif
#endif

#define TOO_FAR INFINITY
#define TOO_CLOSE -INFINITY
#define OCCLUSION_VALUE NAN
//macro to detect wrong data measure
#define isValidMeasure(v) (std::isfinite(v))

const int ZED_SDK_MAJOR_VERSION = 2;
const int ZED_SDK_MINOR_VERSION = 0;
const int ZED_SDK_PATCH_VERSION = 1;

namespace sl {

    /*! \defgroup Enumerations Public enumeration types */

    /**
     * \enum RESOLUTION
     * \ingroup Enumerations
     * \brief List available video resolutions
     * \warning Since v1.0, VGA mode has been updated to WVGA (from 640*480 to 672*376) and requires a firmware update to function (>= 1142). Firmware can be updated in the ZED Explorer.
     * \warning NVIDIA Jetson boards do not support all ZED video resolutions and framerates. For more information, please read the on-line API documentation.
     */
    typedef enum {
        RESOLUTION_HD2K,   /*!< 2208*1242, available framerates: 15 fps.*/
        RESOLUTION_HD1080, /*!< 1920*1080, available framerates: 15, 30 fps.*/
        RESOLUTION_HD720,  /*!< 1280*720, available framerates: 15, 30, 60 fps.*/
        RESOLUTION_VGA,    /*!< 672*376, available framerates: 15, 30, 60, 100 fps.*/
        RESOLUTION_LAST
    } RESOLUTION;

    /**
     *  \enum CAMERA_SETTINGS
     *  \ingroup Enumerations
     *  \brief List available camera settings for the ZED camera (contrast, hue, saturation, gain...).
     *  \brief Each enum defines one of those settings.
     */
    typedef enum {
        CAMERA_SETTINGS_BRIGHTNESS,        /*!< Defines the brightness control. Affected value should be between 0 and 8.*/
        CAMERA_SETTINGS_CONTRAST,          /*!< Defines the contrast control. Affected value should be between 0 and 8.*/
        CAMERA_SETTINGS_HUE,               /*!< Defines the hue control. Affected value should be between 0 and 11.*/
        CAMERA_SETTINGS_SATURATION,        /*!< Defines the saturation control. Affected value should be between 0 and 8.*/
        CAMERA_SETTINGS_GAIN,              /*!< Defines the gain control. Affected value should be between 0 and 100 for manual control. If ZED_EXPOSURE is set to -1, the gain is in auto mode too.*/
        CAMERA_SETTINGS_EXPOSURE,          /*!< Defines the exposure control. A -1 value enable the AutoExposure/AutoGain control,as the boolean parameter (default) does. Affected value should be between 0 and 100 for manual control.*/
        CAMERA_SETTINGS_WHITEBALANCE,      /*!< Defines the color temperature control. Affected value should be between 2800 and 6500 with a step of 100. A value of -1 set the AWB ( auto white balance), as the boolean parameter (default) does.*/
        CAMERA_SETTINGS_AUTO_WHITEBALANCE, /*!< Defines the status of white balance (automatic or manual). A value of 0 disable the AWB, while 1 activate it.*/
        CAMERA_SETTINGS_LAST
    } CAMERA_SETTINGS;

    /**
     *  \enum SELF_CALIBRATION_STATE
     *  \ingroup Enumerations
     *  \brief Status for self calibration. Since v0.9.3, self-calibration is done in background and start in the sl::Camera::open or Reset function.
     *  \brief You can follow the current status for the self-calibration any time once ZED object has been construct.
     */
    typedef enum {
        SELF_CALIBRATION_STATE_NOT_STARTED, /*!< Self calibration has not run yet (no sl::Camera::open or sl::Camera::resetSelfCalibration called).*/
        SELF_CALIBRATION_STATE_RUNNING,     /*!< Self calibration is currently running.*/
        SELF_CALIBRATION_STATE_FAILED,      /*!< Self calibration has finished running but did not manage to get accurate values. Old parameters are taken instead.*/
        SELF_CALIBRATION_STATE_SUCCESS,     /*!< Self calibration has finished running and did manage to get accurate values. New parameters are set.*/
        SELF_CALIBRATION_STATE_LAST
    } SELF_CALIBRATION_STATE;

    /**
     *  \enum DEPTH_MODE
     *  \ingroup Enumerations
     *  \brief List available depth computation modes.
     */
    typedef enum {
        DEPTH_MODE_NONE,        /*!< This mode does not compute any depth map. Only rectified stereo images will be available.*/
        DEPTH_MODE_PERFORMANCE, /*!< Fastest mode for depth computation.*/
        DEPTH_MODE_MEDIUM,      /*!< Balanced quality mode. Depth map is robust in any environment and requires medium resources for computation.*/
        DEPTH_MODE_QUALITY,     /*!< Best quality mode. Requires more compute power.*/
        DEPTH_MODE_LAST
    } DEPTH_MODE;

    /**
     *  \enum SENSING_MODE
     *  \ingroup Enumerations
     *  \brief List available depth sensing modes.
     */
    typedef enum {
        SENSING_MODE_STANDARD, /*!< This mode outputs ZED standard depth map that preserves edges and depth accuracy.
            * Applications example: Obstacle detection, Automated navigation, People detection, 3D reconstruction.*/
        SENSING_MODE_FILL,     /*!< This mode outputs a smooth and fully dense depth map.
            * Applications example: AR/VR, Mixed-reality capture, Image post-processing.*/
        SENSING_MODE_LAST
    } SENSING_MODE;

    /**
     *  \enum UNIT
     *  \ingroup Enumerations
     *  \brief Enumerate for available metric unit of the depth.
     */
    typedef enum {
        UNIT_MILLIMETER,
        UNIT_CENTIMETER,
        UNIT_METER,
        UNIT_INCH,
        UNIT_FOOT,
        UNIT_LAST
    } UNIT;

    /**
     *  \enum COORDINATE_SYSTEM
     *  \ingroup Enumerations
     *  \brief List available coordinates systems for positional tracking and points cloud representation.
     *  \brief Positional tracking is provided in the given coordinates system.
     */
    typedef enum {
        COORDINATE_SYSTEM_IMAGE,             /*!< Standard coordinates system in computer vision. Used in OpenCV : see here : http://docs.opencv.org/2.4/modules/calib3d/doc/camera_calibration_and_3d_reconstruction.html */
        COORDINATE_SYSTEM_LEFT_HANDED_Y_UP,  /*!< Left-Handed with Y up and Z forward. Used in Unity with DirectX. */
        COORDINATE_SYSTEM_RIGHT_HANDED_Y_UP, /*!< Right-Handed with Y pointing up and Z backward. Used in OpenGL. */
        COORDINATE_SYSTEM_RIGHT_HANDED_Z_UP, /*!< Right-Handed with Z pointing up and Y forward. Used in 3DSMax. */
        COORDINATE_SYSTEM_LEFT_HANDED_Z_UP,  /*!< Left-Handed with Z axis pointing up and X forward. Used in Unreal Engine. */
        COORDINATE_SYSTEM_LAST
    } COORDINATE_SYSTEM;

    /**
     *  \enum MEASURE
     *  \ingroup Enumerations
     *  \brief List retrievable measures.
     */
    typedef enum {
        MEASURE_DISPARITY,  /*!< Disparity map,  1 channel, FLOAT.*/
        MEASURE_DEPTH,      /*!< Depth map,  1 channel, FLOAT.*/
        MEASURE_CONFIDENCE, /*!< Certainty/confidence of the disparity map,  1 channel, FLOAT.*/
        MEASURE_XYZ,        /*!< Point cloud, 4 channels, FLOAT, channel 4 is empty.*/
        MEASURE_XYZRGBA,    /*!< Colored point cloud, 4 channels, FLOAT, channel 4 contains color in R-G-B-A order.*/
        MEASURE_XYZBGRA,    /*!< Colored point cloud, 4 channels, FLOAT, channel 4 contains color in B-G-R-A order.*/
        MEASURE_XYZARGB,    /*!< Colored point cloud, 4 channels, FLOAT, channel 4 contains color in A-R-G-B order.*/
        MEASURE_XYZABGR,    /*!< Colored point cloud, 4 channels, FLOAT, channel 4 contains color in A-B-G-R order.*/
        MEASURE_LAST
    } MEASURE;

    /**
     *  \enum VIEW
     *  \ingroup Enumerations
     *  \brief List available views.
     */
    typedef enum {
        VIEW_LEFT,                   /*!< Rectified left image. */
        VIEW_RIGHT,                  /*!< Rectified right image. */
        VIEW_LEFT_GRAY,              /*!< Rectified left grayscale image. */
        VIEW_RIGHT_GRAY,             /*!< Rectified right grayscale image. */
        VIEW_LEFT_UNRECTIFIED,       /*!< Raw left image. */
        VIEW_RIGHT_UNRECTIFIED,      /*!< Raw right image. */
        VIEW_LEFT_UNRECTIFIED_GRAY,  /*!< Raw left grayscale image. */
        VIEW_RIGHT_UNRECTIFIED_GRAY, /*!< Raw right grayscale image. */
        VIEW_SIDE_BY_SIDE,           /*!< Left and right image (the image width is therefore doubled). */
        VIEW_DEPTH,                  /*!< Normalized depth image. */
        VIEW_CONFIDENCE,             /*!< Normalized confidence image. */
        VIEW_LAST
    } VIEW;

    /**
     *  \enum DEPTH_FORMAT
     *  \ingroup Enumerations
     *  \brief List available file formats for saving depth maps.
     */
    typedef enum {
        DEPTH_FORMAT_PNG, /*!< PNG image format in 16bits. 32bits depth is mapped to 16bits color image to preserve the consistency of the data range.*/
        DEPTH_FORMAT_PFM, /*!< stream of bytes, graphic image file format.*/
        DEPTH_FORMAT_PGM, /*!< gray-scale image format.*/
        DEPTH_FORMAT_LAST
    } DEPTH_FORMAT;

    /**
     *  \enum POINT_CLOUD_FORMAT
     *  \ingroup Enumerations
     *  \brief List available file formats for saving point clouds. Stores the spatial coordinates (x,y,z) of each pixel and optionally its RGB color.
     */
    typedef enum {
        POINT_CLOUD_FORMAT_XYZ_ASCII, /*!< Generic point cloud file format, without color information.*/
        POINT_CLOUD_FORMAT_PCD_ASCII, /*!< Point Cloud Data file, with color information.*/
        POINT_CLOUD_FORMAT_PLY_ASCII, /*!< PoLYgon file format, with color information.*/
        POINT_CLOUD_FORMAT_VTK_ASCII, /*!< Visualization ToolKit file, without color information.*/
        POINT_CLOUD_FORMAT_LAST
    } POINT_CLOUD_FORMAT;

    /**
     *  \enum TRACKING_STATE
     *  \ingroup Enumerations
     *  \brief List the different states of positional tracking.
     */
    typedef enum {
        TRACKING_STATE_SEARCHING,   /*!< The camera is searching for a previously known position to locate itself.*/
        TRACKING_STATE_OK,          /*!< Positional tracking is working normally.*/
        TRACKING_STATE_OFF,         /*!< Positional tracking is not enabled.*/
        TRACKING_STATE_FPS_TOO_LOW, /*!< Effective FPS is too low to give proper results for motion tracking. Consider using PERFORMANCES parameters (DEPTH_MODE_PERFORMANCE, low camera resolution (VGA,HD720))*/
        TRACKING_STATE_LAST
    } TRACKING_STATE;

    /**
     *  \enum AREA_EXPORT_STATE
     *  \ingroup Enumerations
     *  \brief List the different states of spatial memory area export.
     */
    typedef enum {
        AREA_EXPORT_STATE_SUCCESS,                 /*!< The spatial memory file has been successfully created.*/
        AREA_EXPORT_STATE_RUNNING,                 /*!< The spatial memory is currently written.*/
        AREA_EXPORT_STATE_NOT_STARTED,             /*!< The spatial memory file exportation has not been called.*/
        AREA_EXPORT_STATE_FILE_EMPTY,              /*!< The spatial memory contains no data, the file is empty.*/
        AREA_EXPORT_STATE_FILE_ERROR,              /*!< The spatial memory file has not been written because of a wrong file name.*/
        AREA_EXPORT_STATE_SPATIAL_MEMORY_DISABLED, /*!< The spatial memory learning is disable, no file can be created.*/
        AREA_EXPORT_STATE_LAST
    } AREA_EXPORT_STATE;

    /**
     *  \enum REFERENCE_FRAME
     *  \ingroup Enumerations
     *  \brief Define which type of position matrix is used to store camera path and pose.
     */
    typedef enum {
        REFERENCE_FRAME_WORLD,  /*!< The transform of sl::Pose will contains the motion with reference to the world frame (previously called PATH).*/
        REFERENCE_FRAME_CAMERA, /*!< The transform of sl::Pose will contains the motion with reference to the previous camera frame (previously called POSE).*/
        REFERENCE_FRAME_LAST
    } REFERENCE_FRAME;

    /**
     *  \enum SPATIAL_MAPPING_STATE
     *  \ingroup Enumerations
     *  \brief Gives the spatial mapping state.
     */
    typedef enum {
        SPATIAL_MAPPING_STATE_INITIALIZING,      /*!< The spatial mapping is initializing.*/
        SPATIAL_MAPPING_STATE_OK,                /*!< The depth and tracking data were correctly integrated in the fusion algorithm.*/
        SPATIAL_MAPPING_STATE_NOT_ENOUGH_MEMORY, /*!< The maximum memory dedicated to the scanning has been reach, the mesh will no longer be updated.*/
        SPATIAL_MAPPING_STATE_NOT_ENABLED,       /*!< Camera::enableSpatialMapping() wasn't called (or the scanning was stopped and not relaunched).*/
        SPATIAL_MAPPING_STATE_FPS_TOO_LOW,       /*!< Effective FPS is too low to give proper results for spatial mapping. Consider using PERFORMANCES parameters (DEPTH_MODE_PERFORMANCE, low camera resolution (VGA,HD720), spatial mapping low resolution)*/
        SPATIAL_MAPPING_STATE_LAST
    } SPATIAL_MAPPING_STATE;

    /**
     *  \enum SVO_COMPRESSION_MODE
     *  \ingroup Enumerations
     *  \brief List available compression modes for SVO recording.
     *  \brief sl::SVO_COMPRESSION_MODE_LOSSLESS is an improvement of previous lossless compression (used in ZED Explorer), even if size may be bigger, compression time is much faster.
     */
    typedef enum {
        SVO_COMPRESSION_MODE_RAW,      /*!< RAW images, no compression.*/
        SVO_COMPRESSION_MODE_LOSSLESS, /*!< new Lossless, with PNG/ZSTD based compression : avg size = 42% of RAW).*/
        SVO_COMPRESSION_MODE_LOSSY,    /*!< new Lossy, with JPEG based compression : avg size = 22% of RAW).*/
        SVO_COMPRESSION_MODE_LAST
    } SVO_COMPRESSION_MODE;

    /**
     * \struct RecordingState
     * \brief Recording structure that contains information about SVO.
     */
    struct RecordingState {
        bool status;                      /*!< status of current frame. May be true for success or false if frame could not be written in the SVO file.*/
        double current_compression_time;  /*!< compression time for the current frame in ms.*/
        double current_compression_ratio; /*!< compression ratio (% of raw size) for the current frame.*/
        double average_compression_time;  /*!< average compression time in ms since beginning of recording.*/
        double average_compression_ratio; /*!< compression ratio (% of raw size) since beginning of recording.*/
    };

    /*! Available video modes for the ZED camera  */
    static std::vector<std::pair<int, int>> cameraResolution = [] {
        std::vector<std::pair<int, int>> v;
        v.emplace_back(2208, 1242); // sl::RESOLUTION_HD2K
        v.emplace_back(1920, 1080); // sl::RESOLUTION_HD1080
        v.emplace_back(1280, 720);  // sl::RESOLUTION_HD720
        v.emplace_back(672, 376);   // sl::RESOLUTION_VGA
        return v;
    }();

    ///////////////////////////////////////////////////////////////////////////////////////////////////////

    //@{

    /**  @name ENUM to string */

    static inline std::string resolution2str(RESOLUTION res) {
        std::string output;
        switch (res) {
        case RESOLUTION::RESOLUTION_HD2K:
            output = "HD2K";
            break;
        case RESOLUTION::RESOLUTION_HD1080:
            output = "HD1080";
            break;
        case RESOLUTION::RESOLUTION_HD720:
            output = "HD720";
            break;
        case RESOLUTION::RESOLUTION_VGA:
            output = "VGA";
            break;
        default:
            output = "Unknown";
            break;
        }
        return output;
    }

    static inline std::string statusCode2str(SELF_CALIBRATION_STATE stat) {
        std::string output;
        switch (stat) {
        case SELF_CALIBRATION_STATE::SELF_CALIBRATION_STATE_NOT_STARTED:
            output = "Self calibration:  Not Started";
            break;
        case SELF_CALIBRATION_STATE::SELF_CALIBRATION_STATE_RUNNING:
            output = "Self calibration:  Running";
            break;
        case SELF_CALIBRATION_STATE::SELF_CALIBRATION_STATE_FAILED:
            output = "Self calibration:  Failed";
            break;
        case SELF_CALIBRATION_STATE::SELF_CALIBRATION_STATE_SUCCESS:
            output = "Self calibration:  Success";
            break;
        default:
            output = "Undefined Self calibration status";
            break;
        }
        return output;
    }

    static inline DEPTH_MODE str2mode(std::string mode) {
        DEPTH_MODE output = DEPTH_MODE_PERFORMANCE;
        if (!mode.compare("None"))
            output = DEPTH_MODE_NONE;
        if (!mode.compare("Performance"))
            output = DEPTH_MODE_PERFORMANCE;
        if (!mode.compare("Medium"))
            output = DEPTH_MODE_MEDIUM;
        if (!mode.compare("Quality"))
            output = DEPTH_MODE_QUALITY;
        return output;
    }

    static inline std::string depthMode2str(DEPTH_MODE mode) {
        std::string output;
        switch (mode) {
        case DEPTH_MODE::DEPTH_MODE_NONE:
            output = "None";
            break;
        case DEPTH_MODE::DEPTH_MODE_PERFORMANCE:
            output = "Performance";
            break;
        case DEPTH_MODE::DEPTH_MODE_MEDIUM:
            output = "Medium";
            break;
        case DEPTH_MODE::DEPTH_MODE_QUALITY:
            output = "Quality";
            break;
        }
        return output;
    }

    static inline std::string sensingMode2str(SENSING_MODE mode) {
        std::string output;
        switch (mode) {
        case SENSING_MODE::SENSING_MODE_STANDARD:
            output = "Standard";
            break;
        case SENSING_MODE::SENSING_MODE_FILL:
            output = "Fill";
            break;
        default:
            break;
        }
        return output;
    }

    static inline std::string unit2str(UNIT unit) {
        std::string output;
        switch (unit) {
        case UNIT::UNIT_MILLIMETER:
            output = "Millimeter";
            break;
        case UNIT::UNIT_CENTIMETER:
            output = "Centimeter";
            break;
        case UNIT::UNIT_METER:
            output = "Meter";
            break;
        case UNIT::UNIT_INCH:
            output = "Inch";
            break;
        case UNIT::UNIT_FOOT:
            output = "Feet";
            break;
        }
        return output;
    }

    static inline UNIT str2unit(std::string unit) {
        UNIT output = UNIT_MILLIMETER;
        if (!unit.compare("Millimeter"))
            output = UNIT_MILLIMETER;
        if (!unit.compare("Centimeter"))
            output = UNIT_CENTIMETER;
        if (!unit.compare("Meter"))
            output = UNIT_METER;
        if (!unit.compare("Inch"))
            output = UNIT_INCH;
        if (!unit.compare("Feet"))
            output = UNIT_FOOT;
        return output;
    }

    static inline std::string trackingState2str(TRACKING_STATE state) {
        std::string output;
        switch (state) {
        case TRACKING_STATE_SEARCHING:
            output = "Tracking state: Searching";
            break;
        case TRACKING_STATE_OK:
            output = "Tracking state: OK";
            break;
        case TRACKING_STATE_OFF:
            output = "Tracking state: OFF";
            break;
        case TRACKING_STATE_FPS_TOO_LOW:
            output = "Tracking state: FPS too low";
            break;
        default:
            output = "";
            break;
        }
        return output;
    }

    static inline std::string spatialMappingState2str(SPATIAL_MAPPING_STATE state) {
        std::string output;
        switch (state) {
        case SPATIAL_MAPPING_STATE_INITIALIZING:
            output = "Spatial Mapping state: Initializing";
            break;
        case SPATIAL_MAPPING_STATE_OK:
            output = "Spatial Mapping state: OK";
            break;
        case SPATIAL_MAPPING_STATE_NOT_ENOUGH_MEMORY:
            output = "Spatial Mapping state: Not Enough Memory";
            break;
        case SPATIAL_MAPPING_STATE_NOT_ENABLED:
            output = "Spatial Mapping state: Not Enabled";
            break;
        case SPATIAL_MAPPING_STATE_FPS_TOO_LOW:
            output = "Spatial Mapping state: FPS too low";
            break;
        default:
            output = "";
            break;
        }
        return output;
    }
    //@}
};

#endif /*__DEFINES_HPP__*/
