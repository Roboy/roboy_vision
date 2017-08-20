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
 *  Accessory solely for purTransform of this Software license.
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
 * AND EVEN IF ANY REMEDY FAILS OF ITS ESSENTIAL PURTransform.
 *
 * 5. Choice of Law
 * French law governs the interpretation of this Software license and any
 * claim that STEREOLABS has breached it, regardless of conflict of
 * law principles.
 *
 */

#ifndef __CORE_HPP__
#define __CORE_HPP__

#include <sl/types.hpp>

namespace sl {

    /**
     * \struct Resolution.
     * \brief Width and height of an array.
     */
    struct Resolution {
        size_t width;  /*!< array width in pixels  */
        size_t height; /*!< array height in pixels*/

        Resolution(size_t w_ = 0, size_t h_ = 0) {
            width = w_;
            height = h_;
        }

        /**
        * \brief Returns the area of the image.
        * \return The number of pixels of the array.
        */
        size_t area() {
            return width * height;
        }

        /**
        * \brief Tests if the given sl::Resolution has the same properties.
        * \return True if the sizes matches.
        */
        bool operator==(const Resolution &that)const {
            return ((width == that.width) && (height == that.height));
        }

        /**
        * \brief Tests if the given sl::Resolution has different properties.
        * \return True if the sizes are not equal.
        */
        bool operator!=(const Resolution &that)const {
            return ((width != that.width) || (height != that.height));
        }
    };

    /**
     * \struct CameraParameters
     * \brief Intrinsic parameters of a camera.
     * \note Similar to the CalibrationParameters, those parameters are taken from the settings file (SNXXX.conf) and are modified during the sl::Camera::open call (with or without Self-Calibration).
     * \n Those parameters given after sl::Camera::open call, represent the "new camera matrix" that fits/defines each image taken after rectification ( through retrieveImage).
     * \note fx,fy,cx,cy must be the same for Left and Right Camera once sl::Camera::open has been called. Since distortion is corrected during rectification, distortion should not be considered after sl::Camera::open call.
     */
    struct CameraParameters {
        float fx;              /*!< Focal length in pixels along x axis. */
        float fy;              /*!< Focal length in pixels along y axis. */
        float cx;              /*!< Optical center along x axis, defined in pixels (usually close to width/2). */
        float cy;              /*!< Optical center along y axis, defined in pixels (usually close to height/2). */
        double disto[5];       /*!< Distortion factor : [ k1, k2, p1, p2, k3 ]. Radial (k1,k2,k3) and Tangential (p1,p2) distortion.*/
        float v_fov;           /*!< Vertical field of view after stereo rectification, in degrees. */
        float h_fov;           /*!< Horizontal field of view after stereo rectification, in degrees.*/
        float d_fov;           /*!< Diagonal field of view after stereo rectification, in degrees.*/
        Resolution image_size; /*!< size in pixels of the images given by the camera.*/

        /**
        * \brief Setups the parameter of a camera.
        * \param focal_x : horizontal focal length.
        * \param focal_y : vertical focal length.
        * \param focal_x : horizontal optical center. 
        * \param focal_x : vertical optical center.
        */
        void SetUp(float focal_x, float focal_y, float center_x, float center_y) {
            fx = focal_x;
            fy = focal_y;
            cx = center_x;
            cy = center_y;
        }
    };

    /**
     * \struct CalibrationParameters
     * \brief Intrinsic parameters of each cameras and extrinsic (translation and rotation).
     * \note The calibration/rectification process, called during sl::Camera::open, is using the raw parameters defined in the SNXXX.conf file, where XXX is the ZED Serial Number.
     * \n Those values may be adjusted or not by the Self-Calibration to get a proper image alignment. After sl::Camera::open is done (with or without Self-Calibration activated) success, most of the stereo parameters (except Baseline of course) should be 0 or very close to 0.
     * \n It means that images after rectification process (given by retrieveImage()) are aligned as if they were taken by a "perfect" stereo camera, defined by the new CalibrationParameters.
     */
    struct CalibrationParameters {
        sl::float3 R;               /*!< Rotation (using Rodrigues' transformation) between the two sensors. Defined as 'tilt', 'convergence' and 'roll'.*/
        sl::float3 T;               /*!< Translation between the two sensors. T.x is the distance between the two cameras (baseline) in the sl::UNIT chosen during sl::Camera::open (mm, cm, meters, inches...).*/
        CameraParameters left_cam;  /*!< Intrinsic parameters of the left camera  */
        CameraParameters right_cam; /*!< Intrinsic parameters of the right camera  */
    };

    /**
    * \struct CameraInformation
    * \brief Camera specific parameters
    */
	struct CameraInformation {
		CalibrationParameters calibration_parameters; /*!< Intrinsic and Extrinsic stereo parameters for rectified images (default).  */
		CalibrationParameters calibration_parameters_raw; /*!< Intrinsic and Extrinsic stereo parameters for original images (unrectified).  */
		unsigned int serial_number = 0;               /*!< camera dependent serial number.  */
		unsigned int firmware_version = 0;            /*!< current firmware version of the camera. */
	};
    /**
     *  \enum MEM
     *  \ingroup Enumerations
     *  \brief List available memory type
     */
    enum MEM {
        MEM_CPU = 1, /*!< CPU Memory (Processor side).*/
        MEM_GPU = 2  /*!< GPU Memory (Graphic card side).*/
    };

    inline MEM operator|(MEM a, MEM b) {
        return static_cast<MEM>(static_cast<int>(a) | static_cast<int>(b));
    }

    /**
     *  \enum COPY_TYPE
     *  \ingroup Enumerations
     *  \brief List available copy operation on Mat
     */
    enum COPY_TYPE {
        COPY_TYPE_CPU_CPU, /*!< copy data from CPU to CPU.*/
        COPY_TYPE_CPU_GPU, /*!< copy data from CPU to GPU.*/
        COPY_TYPE_GPU_GPU, /*!< copy data from GPU to GPU.*/
        COPY_TYPE_GPU_CPU  /*!< copy data from GPU to CPU.*/
    };

    /**
     *  \enum MAT_TYPE
     *  \ingroup Enumerations
     *  \brief List available Mat formats.
     */
    enum MAT_TYPE {
        MAT_TYPE_32F_C1, /*!< float 1 channel.*/
		MAT_TYPE_32F_C2, /*!< float 2 channels.*/
		MAT_TYPE_32F_C3, /*!< float 3 channels.*/
		MAT_TYPE_32F_C4, /*!< float 4 channels.*/
		MAT_TYPE_8U_C1, /*!< unsigned char 1 channel.*/
		MAT_TYPE_8U_C2, /*!< unsigned char 2 channels.*/
        MAT_TYPE_8U_C3, /*!< unsigned char 3 channels.*/
		MAT_TYPE_8U_C4  /*!< unsigned char 4 channels.*/
    };
    
    /*! \class Mat
     *  \brief The Mat class can handle multiple matrix format from 1 to 4 channels, with different value types (float or uchar), and can be stored CPU and/or GPU side.
     * \n\n sl::Mat is defined in a row-major order:
     * \n - It means that, in the image buffer, the entire first row is stored first, followed by the entire second row, and so on.
     * \n\n The CPU and GPU buffer aren't automatically synchronized for performance reasons, you can use Mat::updateCPUfromGPU / Mat::updateGPUfromCPU to do it.
     * \n\n If you are using the GPU side of the Mat object, you need to make sure to call sl::Mat::free() before destroying the sl::Camera object.
     * \n The destruction of the sl::Camera object delete the CUDA context needed to free the GPU Mat memory.
     */
    class SL_CORE_EXPORT_DLL Mat {
    private:
        //  Array size.
        Resolution size;

        // Number of values by pixels.
        size_t channels = 0;

        // GPU Step of the Mat in Bytes.
        size_t step_gpu = 0;

        // CPU Step of the Mat in Bytes.
        size_t step_cpu = 0;

        // size in bytes of one pixel
        size_t pixel_bytes = 0;

        // Data format.
        MAT_TYPE data_type;

        // Type of allocated memory.
        MEM mem_type = sl::MEM_CPU;

        // Pointer to memory on HOST/CPU, if available.
        uchar1 *ptr_cpu = NULL;

        // Pointer to memory on DEVICE/GPU, if available.
        uchar1 *ptr_gpu = NULL;

        // Pointer to internal memory. internal use only
        uchar1 *ptr_internal = NULL;

        // Defines if the Mat is initialized.
        bool init = false;

        // Defines if the memory is owned (and thus freed) or shared.
        bool memory_owner = false;

    public:
        // Variable used in verbose mode to indicate witch Mat is printing informations.
        sl::String name;

        // Whether the MAT can display informations or not.
        bool verbose = false;

        /*!
        * \brief empty Mat default constructor.
        */
        Mat() {
        }

        /*!
         * \brief Mat constructor.
         * \param width : width of the matrix in pixels.
         * \param height : height of the matrix in pixels.
		 * \param mat_type : the type of the matrix (sl::MAT_TYPE_32F_C1,sl::MAT_TYPE_8U_C4...)
         * \param memory_type : defines where the buffer will be stored. (sl::MEM_CPU and/or sl::MEM_GPU).
         *  This function directly allocates the requested memory. It calls Mat::alloc.
         */
        Mat(size_t width, size_t height, MAT_TYPE mat_type, MEM memory_type = MEM_CPU);

        /*!
         * \brief Mat constructor from an existing data pointer.
         * \param width : width of the matrix in pixels.
         * \param height : height of the matrix in pixels.
		 * \param mat_type : the type of the matrix (sl::MAT_TYPE_32F_C1,sl::MAT_TYPE_8U_C4...)
         * \param ptr : pointer to the data array. (CPU or GPU).
         * \param step : step of the data array. (the Bytes size of one pixel row)
         * \param memory_type : defines where the buffer will be stored. (sl::MEM_CPU and/or sl::MEM_GPU).
         *  This function doesn't allocate the memory.
         */
        Mat(size_t width, size_t height, MAT_TYPE mat_type, sl::uchar1 *ptr, size_t step, MEM memory_type = MEM_CPU);

        /*!
         * \brief Mat constructor from two existing data pointers, CPU and GPU.
         * \param width : width of the matrix in pixels.
         * \param height : height of the matrix in pixels.
		 * \param mat_type : the type of the matrix (sl::MAT_TYPE_32F_C1,sl::MAT_TYPE_8U_C4...)
         * \param ptr_cpu : CPU pointer to the data array.
         * \param step_cpu : step of the CPU data array. (the Bytes size of one pixel row)
         * \param ptr_gpu : GPU pointer to the data array.
         * \param step_gpu : step of the GPU data array. (the Bytes size of one pixel row)
         *  This function doesn't allocate the memory.
         */
        Mat(size_t width, size_t height, MAT_TYPE mat_type, sl::uchar1 *ptr_cpu, size_t step_cpu, sl::uchar1 *ptr_gpu, size_t step_gpu);

        /*!
         * \brief Mat constructor.
         * \param resolution : the size of the matrix in pixels.
		 * \param mat_type : the type of the matrix (sl::MAT_TYPE_32F_C1,sl::MAT_TYPE_8U_C4...)
         * \param memory_type : defines where the buffer will be stored. (sl::MEM_CPU and/or sl::MEM_GPU).
         *  This function directly allocates the requested memory. It calls Mat::alloc.
         */
        Mat(sl::Resolution resolution, MAT_TYPE mat_type, MEM memory_type = MEM_CPU);

        /*!
         * \brief Mat constructor from an existing data pointer.
         * \param resolution : the size of the matrix in pixels.
		 * \param mat_type : the type of the matrix (sl::MAT_TYPE_32F_C1,sl::MAT_TYPE_8U_C4...)
         * \param ptr : pointer to the data array. (CPU or GPU).
         * \param step : step of the data array. (the Bytes size of one pixel row)
         * \param memory_type : defines where the buffer will be stored. (sl::MEM_CPU and/or sl::MEM_GPU).
         *  This function doesn't allocate the memory.
         */
        Mat(sl::Resolution resolution, MAT_TYPE mat_type, sl::uchar1 *ptr, size_t step, MEM memory_type = MEM_CPU);

        /*!
         * \brief Mat constructor from two existing data pointers, CPU and GPU.
         * \param resolution : the size of the matrix in pixels.
		 * \param mat_type : the type of the matrix (sl::MAT_TYPE_32F_C1,sl::MAT_TYPE_8U_C4...)
         * \param ptr_cpu : CPU pointer to the data array.
         * \param step_cpu : step of the CPU data array. (the Bytes size of one pixel row)
         * \param ptr_gpu : GPU pointer to the data array.
         * \param step_gpu : step of the GPU data array. (the Bytes size of one pixel row)
         *  This function doesn't allocate the memory.
         */
        Mat(sl::Resolution resolution, MAT_TYPE mat_type, sl::uchar1 *ptr_cpu, size_t step_cpu, sl::uchar1 *ptr_gpu, size_t step_gpu);

        /*!
         * \brief Mat constructor by copy (deep copy).
         * \param mat : the reference to the sl::Mat to copy.
         *  This function allocates and duplicates the data
         */
        Mat(const sl::Mat &mat);

        /*!
         * \brief Allocates the Mat memory.
         * \param width : width of the matrix in pixels
         * \param height : height of the matrix in pixels
		 * \param mat_type : the type of the matrix (sl::MAT_TYPE_32F_C1,sl::MAT_TYPE_8U_C4...)
         * \param memory_type : defines where the buffer will be stored. (sl::MEM_CPU and/or sl::MEM_GPU).
         * \warning It erases previously allocated memory.
         */
        void alloc(size_t width, size_t height, MAT_TYPE mat_type, MEM memory_type = MEM_CPU);

        /*!
         * \brief Allocates the Mat memory.
         * \param resolution : the size of the matrix in pixels.
		 * \param mat_type : the type of the matrix (sl::MAT_TYPE_32F_C1,sl::MAT_TYPE_8U_C4...)
         * \param memory_type : defines where the buffer will be stored. (sl::MEM_CPU and/or sl::MEM_GPU).
         * \warning It erases previously allocated memory.
         */
        void alloc(sl::Resolution resolution, MAT_TYPE mat_type, MEM memory_type = MEM_CPU);

        /*!
         * \brief Mat destructor. This function calls Mat::free to release owned memory.
         */
        ~Mat();

        /*!
         * \brief Free the owned memory.
         * \param memory_type : specify whether you want to free the sl::MEM_CPU and/or sl::MEM_GPU memory.
         */
        void free(MEM memory_type = MEM_CPU | MEM_GPU);

        /*!
         * \brief Performs a shallow copy.
         * \n This function doesn't copy the data array, it only copies the pointer.
         * \param that : the sl::Mat to be copied.
         * \return The new sl::Mat object which point to the same data as that.
         */
        Mat &operator=(const Mat &that);

        /*!
         * \brief Downloads data from DEVICE (GPU) to HOST (CPU), if possible.
         * \return sl::SUCCESS if everything went well, sl::ERROR_CODE_FAILURE otherwise.
         * \note If no CPU or GPU memory are available for this Mat, some are directly allocated.
         * \note If verbose sets, you have informations in case of failure.
         */
        ERROR_CODE updateCPUfromGPU();

        /*!
         * \brief Uploads data from HOST (CPU) to DEVICE (GPU), if possible.
         * \return sl::SUCCESS if everything went well, sl::ERROR_CODE_FAILURE otherwise.
         * \note If no CPU or GPU memory are available for this Mat, some are directly allocated.
         * \note If verbose sets, you have informations in case of failure.
         */
        ERROR_CODE updateGPUfromCPU();

        /*!
         * \brief Copies data an other Mat (deep copy).
         * \param dst : the Mat where the data will be copied.
         * \param cpyType : specify the memories that will be used for the copy.
         * \return sl::SUCCESS if everything went well, sl::ERROR_CODE_FAILURE otherwise.
         * \note If the destination is not allocated or has a not a compatible sl::MAT_TYPE or sl::Resolution, 
         * current memory is freed and new memory is directly allocated.
         */
        ERROR_CODE copyTo(Mat &dst, COPY_TYPE cpyType = COPY_TYPE_CPU_CPU) const;

        /*!
         * \brief Copies data from an other Mat (deep copy).
         * \param src : the Mat where the data will be copied from.
         * \param cpyType : specify the memories that will be used for the update.
         * \return sl::SUCCESS if everything went well, sl::ERROR_CODE_FAILURE otherwise.
         * \note If the current Mat is not allocated or has a not a compatible sl::MAT_TYPE or sl::Resolution with the source, 
         * current memory is freed and new memory is directly allocated.
         */
        ERROR_CODE setFrom(const Mat &src, COPY_TYPE cpyType = COPY_TYPE_CPU_CPU);

        /*!
         * \brief Reads an image from a file (only if sl::MEM_CPU is available on the current sl::Mat).
         * \param filePath : file path including the name and extension.
         * \return sl::SUCCESS if everything went well, sl::ERROR_CODE_FAILURE otherwise.
         * \note Supported sl::MAT_TYPE are : sl::MAT_TYPE_8U_C1, sl::MAT_TYPE_8U_C3 and sl::MAT_TYPE_8U_C4.
         * \nSupported input files format are PNG and JPEG.
         * \nIf verbose sets, you have informations in case of failure.
         */
        ERROR_CODE read(const char* filePath);

        /*!
         * \brief Writes the sl::Mat (only if sl::MEM_CPU is available) into a file as an image.
         * \param filePath : file path including the name and extension.
         * \return sl::SUCCESS if everything went well, sl::ERROR_CODE_FAILURE otherwise.
         * \note Supported sl::MAT_TYPE are : sl::MAT_TYPE_8U_C1, sl::MAT_TYPE_8U_C3 and sl::MAT_TYPE_8U_C4.
         * \nSupported output files format are PNG and JPEG.
         * \nIf verbose sets, you have informations in case of failure.
         */
        ERROR_CODE write(const char* filePath);

        /*!
         * \brief Fills the Mat with the given value.
         * \param value : the value to be copied all over the matrix.
         * \param memory_type : defines which buffer to fill, CPU and/or GPU.
         * This function overwrite all the matrix.
         * \note This function is templated for sl::uchar1, sl::uchar2, sl::uchar3, sl::uchar4, sl::float1, sl::float2, sl::float3, sl::float4.
         */
        template <typename T>
        ERROR_CODE setTo(T value, MEM memory_type = MEM_CPU);

        /*!
         * \brief Sets a value to a specific point in the matrix.
         * \param x : specify the column.
         * \param y : specify the row.
         * \param value : the value to be set.
         * \param memory_type : defines which memory will be updated.
         * \return sl::SUCCESS if everything went well, sl::ERROR_CODE_FAILURE otherwise.
         * \warning Not efficient for sl::MEM_GPU, use it on sparse data.
         * \note This function is templated for sl::uchar1, sl::uchar2, sl::uchar3, sl::uchar4, sl::float1, sl::float2, sl::float3, sl::float4.
         */
        template <typename N>
        ERROR_CODE setValue(size_t x, size_t y, N value, MEM memory_type = MEM_CPU);

        /*!
         * \brief Returns the value of a specific point in the matrix.
         * \param x : specify the column
         * \param y : specify the row
         * \param memory_type : defines which memory should be read.
         * \return sl::SUCCESS if everything went well, sl::ERROR_CODE_FAILURE otherwise.
         * \warning Not efficient for sl::MEM_GPU, use it on sparse data.
         * \note This function is templated for sl::uchar1, sl::uchar2, sl::uchar3, sl::uchar4, sl::float1, sl::float2, sl::float3, sl::float4.
         */
        template <typename N>
        ERROR_CODE getValue(size_t x, size_t y, N *value, MEM memory_type = MEM_CPU);

        /*!
         *  brief Returns the width of the matrix.
         * \return The width of the matrix in pixels.
         */
        inline size_t getWidth() const {
            return size.width;
        }

        /*!
         *  brief Returns the height of the matrix.
         * \return The height of the matrix in pixels.
         */
        inline size_t getHeight() const {
            return size.height;
        }

        /*!
         *  brief Returns the height of the matrix.
         * \return The height of the matrix in pixels.
         */
        inline Resolution getResolution() const {
            return size;
        }

        /*!
         *  brief Returns the number of values stored in one pixel.
         * \return The number of values in a pixel.
         */
        inline size_t getChannels() const {
            return channels;
        }

        /*!
         *  brief Returns the format of the matrix.
         * \return The format of the current Mat.
         */
        inline MAT_TYPE getDataType() const {
            return data_type;
        }

        /*!
         *  brief Returns the type of memory (CPU and/or GPU).
         * \return The type of allocated memory.
         */
        inline MEM getMemoryType() const {
            return mem_type;
        }

        /*!
         *  brief Returns the CPU or GPU data pointer.
         * \param memory_type : specify whether you want sl::MEM_CPU or sl::MEM_GPU step.
         * \return The pointer of the Mat data.
         */
        template <typename N>
        N *getPtr(MEM memory_type = MEM_CPU);

        /*!
         *  brief Returns the memory step in Bytes (the Bytes size of one pixel row).
         * \param memory_type : specify whether you want sl::MEM_CPU or sl::MEM_GPU step.
         * \return The step in bytes of the specified memory.
         */
        inline size_t getStepBytes(MEM memory_type = MEM_CPU) {
            switch (memory_type) {
            case MEM_CPU:
                return step_cpu;
            case MEM_GPU:
                return step_gpu;
            }
            return 0;
        }

        /*!
         *  brief Returns the memory step in number of elements (the number of values in one pixel row).
         * \param memory_type : specify whether you want sl::MEM_CPU or sl::MEM_GPU step.
         * \return The step in number of elements.
         */
        template <typename N>
        inline size_t getStep(MEM memory_type = MEM_CPU) {
            return getStepBytes(memory_type) / sizeof(N);
        }

        /*!
         *  brief Returns the memory step in number of elements (the number of values in one pixel row).
         * \param memory_type : specify whether you want sl::MEM_CPU or sl::MEM_GPU step.
         * \return The step in number of elements.
         */
        inline size_t getStep(MEM memory_type = MEM_CPU) {
            switch (data_type) {
            case sl::MAT_TYPE_32F_C1:
                return getStep<sl::float1>(memory_type);
            case sl::MAT_TYPE_32F_C2:
                return getStep<sl::float2>(memory_type);
            case sl::MAT_TYPE_32F_C3:
                return getStep<sl::float3>(memory_type);
            case sl::MAT_TYPE_32F_C4:
                return getStep<sl::float4>(memory_type);
            case sl::MAT_TYPE_8U_C1:
                return getStep<sl::uchar1>(memory_type);
            case sl::MAT_TYPE_8U_C2:
                return getStep<sl::uchar2>(memory_type);
            case sl::MAT_TYPE_8U_C3:
                return getStep<sl::uchar3>(memory_type);
            case sl::MAT_TYPE_8U_C4:
                return getStep<sl::uchar4>(memory_type);
            }
            return 0;
        }

        /*!
         *  brief Returns the size in bytes of one pixel.
         * \return The size in bytes of a pixel.
         */
        inline size_t getPixelBytes() {
            return pixel_bytes;
        }

        /*!
         *  brief Returns the size in bytes of a row.
         * \return The size in bytes of a row.
         */
        inline size_t getWidthBytes() {
            return pixel_bytes * size.width;
        }

        /*!
         *  brief Return the informations about the Mat into a sl::String.
         * \return A string containing the Mat informations.
         */
        sl::String getInfos();

        /*!
         *  brief Defines whether the Mat is initialized or not.
         * \return True if current Mat has been allocated (by the constructor or therefore).
         */
        inline bool isInit() {
            return init;
        }

        /*!
         *  brief Returns whether the Mat is the owner of the memory it access.
         * \n If not, the memory won't be freed if the Mat is destroyed.
         * \return True if the Mat is owning its memory, else false.
         */
        inline bool isMemoryOwner() {
            return memory_owner;
        }

        /*!
         * \brief Duplicates Mat by copy (deep copy).
         * \param src : the reference to the Mat to copy.
         *  This function copies the data array(s), it mark the new Mat as the memory owner.
         */
        void clone(const Mat &src);

    };

    class SL_CORE_EXPORT_DLL Rotation;
    class SL_CORE_EXPORT_DLL Translation;
    class SL_CORE_EXPORT_DLL Orientation;
    class SL_CORE_EXPORT_DLL Transform;

    /*! \class Rotation
     *  \brief The class Rotation is designed to contains rotation data from the tracking.
     *  \brief It inherits from the generic sl::Matrix3f
     */
    class SL_CORE_EXPORT_DLL Rotation : public Matrix3f {
    public:
        /*!
         * \brief empty Rotation default constructor.
         */
        Rotation();

        /*!
         *  brief Rotation copy constructor (deep copy).
         * \param rotation : the Rotation to copy.
         */
        Rotation(const Rotation &rotation);

        /*!
         *  brief Rotation copy constructor (deep copy).
         * \param mat : the mat to copy.
         */
        Rotation(const Matrix3f &mat);

        /*!
         *  brief Rotation constructor from an Orientation.
         * \n It converts the Orientation representation to the Rotation one.
         * \param orientation : the Orientation to be used.
         */
        Rotation(const Orientation &orientation);

        /*!
         *  brief Creates a Rotation representing the 3D rotation of angle around an arbitrary 3D axis.
         * \param angle : the rotation angle in rad.
         * \param axis : the 3D axis to rotate around.
         */
        Rotation(const float angle, const Translation &axis);

        /*!
         * \brief Sets the Rotation from an Orientation.
         * \param orientation : the Orientation containing the rotation to set.
         */
        void setOrientation(const Orientation &orientation);

        /*!
         * \brief Returns the Orientation corresponding to the current Rotation.
         * \return The rotation of the current orientation.
         */
        Orientation getOrientation();

        /*!
         * \brief Returns the rotation vector (Rx,Ry,Rz) corresponding to the current Rotation (using Rodrigues' transformation).
         * \return The rotation vector .
         */
        sl::Vector3<float> getRotationVector();

        /*!
         * \brief Sets the Rotation from a rotation vector (using Rodrigues' transformation).
         * \param vec_rot : the  Rotation Vector.
         */
        void setRotationVector(const sl::Vector3<float> &vec_rot);
    };

    /*! \class Translation
     *  \brief The class Translation is designed to contains translation data from the tracking.
     * \n\n sl::Translation is a vector as  [tx, ty, tz].
     * \n You can access the data with the 't' ptr or by element name as :
     *       tx, ty, tz  <-> | 0 1 2 |
     */
    class SL_CORE_EXPORT_DLL Translation : public Vector3<float> {
    public:
        /*!
         * \brief empty Translation default constructor.
         */
        Translation();

        /*!
         *  brief Translation copy constructor (deep copy).
         * \param translation : the Translation to copy.
         */
        Translation(const Translation &translation);

        /*!
         *  brief Translation constructor.
         * \param t1 : the x translation.
         * \param t2 : the y translation.
         * \param t3 : the z translation.
         */
        Translation(float t1, float t2, float t3);

        /*!
         *  brief Translation constructor.
         * \param in : vector.
         */
        Translation(Vector3<float> in);

        /*!
        *  brief Multiplication operator by an Orientation.
        * \param mat : Orientation.
        * \return The current Translation after being multiplied by the orientation.
        */
        Translation operator*(const Orientation &mat) const;

        /*!
         * \brief Normalizes the current translation.
         */
        void normalize();

        /*!
         *  brief Get the normalized version of a given Translation.
         * \param tr : the Translation to be used.
         * \return An other Translation object, which is equal to tr.normalize.
         */
        static Translation normalize(const Translation &tr);

        /*!
         * \brief Get the value at specific position in the Translation.
         * \param x : the position of the value
         * \return The value at the x position.
         */
        float &operator()(int x);
    };

    /*! \class Orientation
     *  \brief The class Orientation is designed to contains orientation data from the tracking.
     * \n\n sl::Orientation is a vector defined as [ox, oy, oz, ow].
     */
    class SL_CORE_EXPORT_DLL Orientation : public Vector4<float> {
    public:
        /*!
         * \brief empty Orientation default constructor.
         */
        Orientation();

        /*!
         *  brief Orientation copy constructor (deep copy).
         * \param orientation : the Orientation to copy.
         */
        Orientation(const Orientation &orientation);

        /*!
         *  brief Orientation copy constructor (deep copy).
         * \param in : the vector to copy.
         */
        Orientation(const Vector4<float> &in);

        /*!
         *  brief Orientation constructor from an Rotation.
         * \n It converts the Rotation representation to the Orientation one.
         * \param rotation : the Rotation to be used.
         */
        Orientation(const Rotation &rotation);

        /*!
         *  brief Orientation constructor from a vector represented by two Translation.
         * \param tr1 : the first point of the vector.
         * \param tr2 : the second point of the vector.
         */
        Orientation(const Translation &tr1, const Translation &tr2);

        /*!
         * \brief Returns the value at specific position in the Orientation.
         * \param x : the position of the value
         * \return The value at the x position.
         */
        float operator()(int x);

        /*!
        *  brief Multiplication operator by an Orientation.
         * \param orientation : the orientation.
         * \return The current orientation after being multiplied by the other orientation.
         */
        Orientation operator*(const Orientation &orientation) const;

        /*!
         * \brief Sets the orientation from a Rotation.
         * \param rotation : the Rotation to be used.
         */
        void setRotation(const Rotation &rotation);

        /*!
         * \brief Returns the current orientation as a Rotation.
         * \return The rotation computed from the orientation data.
         */
        Rotation getRotation() const;

        /*!
         * \brief Sets the current Orientation to identity.
         */
        void setIdentity();

        /*!
         * \brief Creates an Orientation initialized to identity.
         * \return An identity Orientation.
         */
        static Orientation identity();

        /*!
         * \brief Fills the current Orientation with zeros.
         */
        void setZeros();

        /*!
         * \brief Creates an Orientation filled with zeros.
         * \return An Orientation filled with zeros.
         */
        static Orientation zeros();

        /*!
         * \brief Normalizes the current Orientation.
         */
        void normalise();

        /*!
         * \brief Creates the normalized version of an existing Orientation.
         * \param orient : the Orientation to be used.
         * \return The normalized version of the Orientation.
         */
        static Orientation normalise(const Orientation &orient);
    };

    /*! \class Transform
     *  \brief The class Transform contains a 4x4 matrix that specifically contains a rotation 3x3 and a 3x1 translation.
     *  \brief It then contains the orientation as well. It can be used to create any type of Matrix4x4 or sl::Matrix4f that must be specifically used for handling a rotation and position information (OpenGL, Tracking...)
     *  \brief It inherits from the generic sl::Matrix4f
     */
    class SL_CORE_EXPORT_DLL Transform : public Matrix4f {
    public:
        /*!
         *  brief Transform default constructor.
         */
        Transform();

        /*!
         *  brief Transform copy constructor (deep copy).
         * \param motion : the Transform to copy.
         */
        Transform(const Transform &motion);

        /*!
         *  brief Transform copy constructor (deep copy).
         * \param mat : the Matrix4f to copy.
         */
        Transform(const Matrix4f &mat);

        /*!
         *  brief Transform constructor from a Rotation and a Translation.
         * \param rotation : the Rotation to copy.
         * \param translation : the Translation to copy.
         */
        Transform(const Rotation &rotation, const Translation &translation);

        /*!
         *  brief Transform constructor from an Orientation and a Translation.
         * \param orientation : the Orientation to copy.
         * \param translation : the Translation to copy.
         */
        Transform(const Orientation &orientation, const Translation &translation);

        /*!
         * \brief Sets the rotation of the current Transform from an Rotation.
         * \param rotation : the Rotation to be used.
         */
        void setRotation(const Rotation &rotation);

        /*!
         * \brief Returns the Rotation of the current Transform.
         * \return The Rotation created from the Transform values.
         * \warning The given Rotation contains a copy of the Transform values. Not references.
         */
        Rotation getRotation() const;

        /*!
         * \brief Sets the translation of the current Transform from an Translation.
         * \param translation : the Translation to be used.
         */
        void setTranslation(const Translation &translation);

        /*!
         * \brief Returns the Translation of the current Transform.
         * \return The Translation created from the Transform values.
         * \warning The given Translation contains a copy of the Transform values. Not references.
         */
        Translation getTranslation() const;

        /*!
         * \brief Sets the orientation of the current Transform from an Orientation.
         * \param orientation : the Orientation to be used.
         */
        void setOrientation(const Orientation &orientation);

        /*!
         * \brief Returns the Orientation of the current Transform.
         * \return The Orientation created from the Transform values.
         * \warning The given Orientation contains a copy of the Transform values. Not references.
         */
        Orientation getOrientation() const;

        /*!
         *  \brief Returns the vector Rotation (3x1) of the Transform.
         *  \return The rotation value for each axis (rx,ry,rz).
         */
        sl::Vector3<float> getRotationVector();

        /*!
         *  \brief Sets the Rotation 3x3 of the Transform with a 3x1 rotation vector (using Rodrigues' transformation).
         *  \param vec_rot : vector that contains the rotation value for each axis (rx,ry,rz).
         */
        void setRotationVector(const sl::Vector3<float> &vec_rot);
    };

    /// @cond
    class SL_CORE_EXPORT_DLL TextureImage {
    public:
        TextureImage(sl::Mat &img_, sl::Transform &path_);


        ~TextureImage() {
            img.free();
        }

        inline void clear() {
            img.free();
        }

        sl::Mat img;
        sl::Transform path;
    };
    /// @endcond

    /// @cond
    class SL_CORE_EXPORT_DLL TextureImagePool {
    public:
        TextureImagePool() {
        }

        ~TextureImagePool() {
            clear();
        }

        std::vector<TextureImage> v;

        int size() {
            return (int)v.size();
        }

        void stack(sl::Mat &image, sl::Transform &path);
        void concat(const TextureImagePool &that);
        TextureImagePool &operator=(const TextureImagePool &that);
        void clear();

    private:
        std::mutex mtx;
    };
    /// @endcond
}
#endif /* __CORE_HPP__ */
