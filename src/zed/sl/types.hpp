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
 * "Unauthorized Accessories" means all hardware accessories b than
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
 * b. As conditions to this Software license, You agree a:
 *       i. You will use Your Software with ZED Camera only and not with any
 * b device (including). You will not use Unauthorized Accessories.
 * They may not work or may stop working permanently after a Software update.
 *       ii. You will not use or install any Unauthorized Software.
 * If You do, Your ZED Camera may stop working permanently at a time
 * or after a later Software update.
 *       iii. You will not attempt to defeat or circumvent any Software
 * technical limitation, security, or anti-piracy system. If You do,
 * Your ZED Camera may stop working permanently at a time or after a
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
 * and STEREOLABS gives no b guarantee, warranty, or condition for
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
 * claim a STEREOLABS has breached it, regardless of conflict of
 * law principles.
 *
 */

#ifndef __TYPES_HPP__
#define __TYPES_HPP__

#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <ctime>
#include <ctype.h>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <memory.h>
#include <mutex>
#include <sstream>
#include <thread>
#include <vector>

#include <cuda.h>
#include <cuda_runtime.h>
#include <cuda_runtime_api.h>
#include <device_launch_parameters.h>

#if defined _WIN32
#if defined SL_CORE_EXPORT
#define SL_CORE_EXPORT_DLL __declspec(dllexport)
#else
#define SL_CORE_EXPORT_DLL
#endif
#elif __GNUC__
#define SL_CORE_EXPORT_DLL __attribute__((visibility("default")))
#if defined(__arm__) || defined(__aarch64__)
#define _SL_JETSON_
#endif
#endif

#ifdef _WIN32
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <Windows.h>
#define __CUSTOM__PRETTY__FUNC__ __FUNCSIG__
#define __FILENAME__ (strrchr(__FILE__, '\\') ? strrchr(__FILE__, '\\') + 1 : __FILE__)
#else
#include <unistd.h>
#define __CUSTOM__PRETTY__FUNC__ __PRETTY_FUNCTION__
#define __FILENAME__ (strrchr(__FILE__, '/') ? strrchr(__FILE__, '/') + 1 : __FILE__)
#endif

#if defined(__CUDACC__) && defined(__CUDA_ARCH__)
#define _FCT_CPU_GPU_ __device__ // for CUDA device code
#define IS_FINITE(x) isfinite(x)
#else
#define _FCT_CPU_GPU_
#define IS_FINITE(x) std::isfinite(x)
#endif

#ifndef ZEDcudaSafeCall
#define ZEDcudaSafeCall(err) sl::__cudaSafeCall(err, /*__FILENAME__*/ __CUSTOM__PRETTY__FUNC__, __FILENAME__, __LINE__)
namespace sl {

    static inline cudaError __cudaSafeCall(cudaError err, const char *func, const char *file, const int line) {
        if (err != cudaSuccess) {
            printf("in %s : cuda error [%d]: %s.\n", func, err, cudaGetErrorString(err));
            return err;
        } else
            return cudaError::cudaSuccess;
    }
}
#endif

// Stereolabs namespace
namespace sl {

    /**
    *  \enum ERROR_CODE
    *  \ingroup Enumerations
    *  \brief List error codes in the ZED SDK.
    */
    typedef enum {
        SUCCESS,                                   /*!< Standard code for successful behavior.*/
        ERROR_CODE_FAILURE,                        /*!< Standard code for unsuccessful behavior.*/
        ERROR_CODE_NO_GPU_COMPATIBLE,              /*!< No GPU found or CUDA capability of the device is not supported.*/
        ERROR_CODE_NOT_ENOUGH_GPUMEM,              /*!< Not enough GPU memory for this depth mode
                                      * please try a faster mode (such as PERFORMANCE mode).*/
        ERROR_CODE_CAMERA_NOT_DETECTED,            /*!< The ZED camera is not plugged or detected.*/
        ERROR_CODE_INVALID_RESOLUTION,             /*!< For Jetson only, resolution not yet supported (USB3.0 bandwidth).*/
        ERROR_CODE_LOW_USB_BANDWIDTH,              /*!< This issue can occurs when you use multiple ZED or a USB 2.0 port (bandwidth issue).*/
        ERROR_CODE_CALIBRATION_FILE_NOT_AVAILABLE, /*!< ZED calibration file is not found on the host machine. Use ZED Explorer or ZED Calibration to get one.*/
        ERROR_CODE_INVALID_SVO_FILE,               /*!< The provided SVO file is not valid.*/
        ERROR_CODE_SVO_RECORDING_ERROR,            /*!< An recorder related error occurred (not enough free storage, invalid file).*/
        ERROR_CODE_INVALID_COORDINATE_SYSTEM,      /*!< The requested coordinate system is not available.*/
        ERROR_CODE_INVALID_FIRMWARE,               /*!< The firmware of the ZED is out of date. Update to the latest version.*/
        ERROR_CODE_NOT_A_NEW_FRAME,                /*!< in grab() only, the current call return the same frame as last call. Not a new frame.*/
        ERROR_CODE_CUDA_ERROR,                     /*!< in grab() only, a CUDA error has been detected in the process. Activate verbose in sl::Camera::open for more info.*/
        ERROR_CODE_CAMERA_NOT_INITIALIZED,         /*!< in grab() only, ZED SDK is not initialized. Probably a missing call to sl::Camera::open.*/
        ERROR_CODE_NVIDIA_DRIVER_OUT_OF_DATE,      /*!<your NVIDIA driver is too old and not compatible with your current CUDA version. */
        ERROR_CODE_INVALID_FUNCTION_CALL,          /*!<the call of the function is not valid in the current context. Could be a missing call of sl::Camera::open. */
        ERROR_CODE_CORRUPTED_SDK_INSTALLATION,     /*!< The SDK wasn't able to load its dependencies, the installer should be launched. */
        ERROR_CODE_LAST
    } ERROR_CODE;

    static inline std::string errorCode2str(ERROR_CODE err) {
        std::string output;
        switch (err) {
        case ERROR_CODE::SUCCESS:
            output = "Error code:  Success";
            break;
        case ERROR_CODE::ERROR_CODE_FAILURE:
            output = "Error code:  Failure";
            break;
        case ERROR_CODE::ERROR_CODE_NO_GPU_COMPATIBLE:
            output = "Error code:  No GPU Compatible";
            break;
        case ERROR_CODE::ERROR_CODE_NOT_ENOUGH_GPUMEM:
            output = "Error code:  Not Enough GPUMEM";
            break;
        case ERROR_CODE::ERROR_CODE_CAMERA_NOT_DETECTED:
            output = "Error code:  Camera Not Detected";
            break;
        case ERROR_CODE::ERROR_CODE_INVALID_RESOLUTION:
            output = "Error code:  Invalid Resolution";
            break;
        case ERROR_CODE::ERROR_CODE_LOW_USB_BANDWIDTH:
            output = "Error code: Low USB Bandwidth";
            break;
        case ERROR_CODE::ERROR_CODE_CALIBRATION_FILE_NOT_AVAILABLE:
            output = "Error Code: Calibration File Not Available";
            break;
        case ERROR_CODE::ERROR_CODE_INVALID_SVO_FILE:
            output = "Error code:  Invalid SVO File";
            break;
        case ERROR_CODE::ERROR_CODE_SVO_RECORDING_ERROR:
            output = "Error code:  SVO Recording Error";
            break;
        case ERROR_CODE::ERROR_CODE_INVALID_COORDINATE_SYSTEM:
            output = "Error code:  Invalid Coordinate System";
            break;
        case ERROR_CODE::ERROR_CODE_INVALID_FIRMWARE:
            output = "Error code:  Invalid Firmware";
            break;
        case ERROR_CODE::ERROR_CODE_NOT_A_NEW_FRAME:
            output = "Error code:  No New Frame";
            break;
        case ERROR_CODE::ERROR_CODE_CUDA_ERROR:
            output = "Error code:  Cuda Error";
            break;
        case ERROR_CODE::ERROR_CODE_CAMERA_NOT_INITIALIZED:
            output = "Error code:  Camera Not Initialized";
            break;
        case ERROR_CODE::ERROR_CODE_NVIDIA_DRIVER_OUT_OF_DATE:
            output = "Error code:   Nvidia Driver Out Of Date";
            break;
        case ERROR_CODE::ERROR_CODE_INVALID_FUNCTION_CALL:
            output = "Error code:  Invalid Function Call";
            break;
        case ERROR_CODE::ERROR_CODE_CORRUPTED_SDK_INSTALLATION:
            output = "Error code:  Corrupted SDK Installation";
            break;
        }
        return output;
    }

    /*!
    * \brief Tells the program to wait for x ms.
    * \param time : the number of ms to wait.
    */
    inline void sleep_ms(int time) {
#if _WIN32
        Sleep(time);
#else
        usleep(time * 1000);
#endif
    }

    /// @cond
    class SL_CORE_EXPORT_DLL String {
    public:
        String() {
        }

        String(const String &str) {
            set(str.get());
        }

        String(const char *data) {
            set(data);
        }

        void set(const char *data) {
            clean();
            if (data) {
                if (strlen(data)) {
                    size = strlen(data) + 1;
                    p_data = new char[size];
                    strncpy(p_data, data, size);
                }
            }
        }

        const char *get() const {
            return p_data;
        }

        bool empty() const {
            return (!size || p_data[0] == '\0');
        }

        String &operator=(const String &str1) {
            set(str1.get());
            return *this;
        }

        String &operator=(const char *data) {
            set(data);
            return *this;
        }

        operator const char *() {
            return get();
        }

        ~String() {
            clean();
        }

    private:
        char *p_data = 0;
        size_t size = 0;

        void clean() {
            if (size && p_data) delete[] p_data;
            size = 0;
            p_data = 0;
        }
    };
    
    template <typename T, int l>
    struct Storage_ {
        T v[l];
    };

    template <typename T>
    struct Size2_ {
        union {
            struct {
                T x, y;
            };
            T v[2];
            Storage_<T, 2> components;
        };
    };

    template <typename T>
    struct Size3_ {
        union {
            struct {
                T x, y, z;
            };
            struct {
                T r, g, b;
            };
            struct {
                T tx, ty, tz;
            };
            T v[3];
            Storage_<T, 3> components;
        };
    };

    template <typename T>
    struct Size4_ {
        union {
            struct {
                T x, y, z, w;
            };
            struct {
                T r, g, b, a;
            };
            struct {
                T ox, oy, oz, ow;
            };
            T v[4];
            Storage_<T, 4> components;
        };
    };

    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////                 ////////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////     VECTOR      ////////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////                 ////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    /*! \class Vector2
     *  \brief The class Vector2 represents a three dimensions vector for both CPU and GPU.
     */
    template <typename T>
    class Vector2 : public Size2_<T> {
    public:
        /********************************************************
         *  Basics*
         ********************************************************/

        inline __host__ __device__ int size() const {
            return 2;
        }

        inline __host__ __device__ Vector2() {
        }

        inline __host__ __device__ Vector2(const T &t) {
            this->x = t;
            this->y = t;
        }

        inline __host__ __device__ Vector2(const T *tp) {
            this->x = tp[0];
            this->y = tp[1];
        }

        inline __host__ __device__ Vector2(const T v0, const T v1) {
            this->x = v0;
            this->y = v1;
        }

        inline __host__ __device__ Vector2<T>(const Vector2<T> &v) {
            this->x = v.x;
            this->y = v.y;
        }

        inline __host__ __device__ const T *ptr() const {
            return &this->v[0];
        }

        inline __host__ __device__ Vector2 &setValues(const T *b) {
            this->x = b[0];
            this->y = b[1];
            return *this;
        }

        inline __host__ __device__ T &operator[](int i) {
            return this->v[i];
        }

        /********************************************************
         *  Operator overloading *
         ********************************************************/

        inline __host__ __device__ Vector2<T> &operator*=(T d) {
            this->x *= d;
            this->y *= d;
            return *this;
        }

        inline __host__ __device__ Vector2<T> &operator*=(const Vector2<T> &b) {
            this->x *= b.x;
            this->y *= b.y;
            return *this;
        }

        inline __host__ __device__ Vector2<T> &operator/=(T d) {
            if (d == 0) return this;
            this->x /= d;
            this->y /= d;
            return *this;
        }

        inline __host__ __device__ Vector2<T> &operator/=(const Vector2<T> &b) {
            this->x /= b.x;
            this->y /= b.y;
            return *this;
        }

        inline __host__ __device__ Vector2<T> &operator+=(const Vector2<T> &b) {
            this->x += b.x;
            this->y += b.y;
            return *this;
        }

        inline __host__ __device__ Vector2<T> &operator-=(const Vector2<T> &b) {
            this->x -= b.x;
            this->y -= b.y;
            return *this;
        }

        /********************************************************
         *  Math *
         ********************************************************/

        /*!
         * \brief returns the norm of the vector
         */
        inline __host__ __device__ float norm() {
            return sqrt(this->x * this->x + this->y * this->y);
        }

        /*!
         * \brief returns the squared norm of the vector
         */
        inline __host__ __device__ float square() {
            return (this->x * this->x + this->y * this->y);
        }

        /*!
         * \brief returns the sum of the vector
         */
        inline __host__ __device__ float sum() {
            return (this->x + this->y);
        }

        /*!
         * \brief returns the dot product of two vector
         */
        inline __host__ __device__ float dot(const Vector2<T> &a, const Vector2<T> &b) {
            return (a.x * b.x + a.y * b.y);
        }

        /*!
         * \brief returns the distance between two vector
         */
        inline __host__ __device__ float distance(const Vector2<T> &a, const Vector2<T> &b) {
            return sqrt(pow(a.x - b.x, 2) + pow(a.y - b.y, 2));
        }
    };

    /************************
     * Public overload
     **********************/
    template <typename T>
    inline __host__ __device__ Vector2<T> &operator+(const Vector2<T> &a, const Vector2<T> &b) {
        Vector2<T> tmp(a);
        return tmp += b;
    }

    template <typename T>
    inline __host__ __device__ Vector2<T> operator-(const Vector2<T> &a, const Vector2<T> &b) {
        Vector2<T> tmp(a);
        return tmp -= b;
    }

    template <typename T>
    inline __host__ __device__ Vector2<T> operator*(const Vector2<T> &a, T b) {
        Vector2<T> tmp(a);
        return tmp *= b;
    }

    template <typename T>
    inline __host__ __device__ Vector2<T> operator*(T a, const Vector2<T> &b) {
        Vector2<T> tmp(a);
        return tmp *= b;
    }

    template <typename T>
    inline __host__ __device__ Vector2<T> operator*(const Vector2<T> &a, const Vector2<T> &b) {
        Vector2<T> tmp(a);
        return tmp *= b;
    }

    template <typename T>
    inline __host__ __device__ Vector2<T> operator/(const Vector2<T> &a, T b) {
        Vector2<T> tmp(a);
        return tmp /= b;
    }

    template <typename T>
    inline __host__ __device__ Vector2<T> operator/(const Vector2<T> &a, const Vector2<T> &b) {
        Vector2<T> tmp(a);
        return tmp /= b;
    }

    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    /*! \class Vector3
     *  \brief The class Vector3 represents a three dimensions vector for both CPU and GPU.
     */
    template <typename T>
    class Vector3 : public Size3_<T> {
    public:
        /********************************************************
         *  Basics*
         ********************************************************/

        inline __host__ __device__ int size() const {
            return 3;
        }

        inline __host__ __device__ Vector3() {
        }

        inline __host__ __device__ Vector3(const T &t) {
            this->x = t;
            this->y = t;
            this->z = t;
        }

        inline __host__ __device__ Vector3(const T *tp) {
            this->x = tp[0];
            this->y = tp[1];
            this->z = tp[2];
        }

        inline __host__ __device__ Vector3(const T v0, const T v1, const T v2) {
            this->x = v0;
            this->y = v1;
            this->z = v2;
        }

        inline __host__ __device__ Vector3<T>(const Vector3<T> &v) {
            this->x = v.x;
            this->y = v.y;
            this->z = v.z;
        }

        inline __host__ __device__ Vector3<T>(const Vector2<T> &v, const T d = 0) {
            this->x = v.x;
            this->y = v.y;
            this->z = d;
        }

        inline __host__ __device__ const T *ptr() const {
            return &this->v[0];
        }

        inline __host__ __device__ Vector3<T> &setValues(const T *b) {
            this->x = b[0];
            this->y = b[1];
            this->z = b[2];
            return *this;
        }

        inline __host__ __device__ T &operator[](int i) {
            return this->v[i];
        }

        /********************************************************
         *  Operator overloading *
         ********************************************************/

        inline __host__ __device__ Vector3<T> &operator+=(T d) {
            this->x += d;
            this->y += d;
            this->z += d;
            return *this;
        }

        inline __host__ __device__ Vector3<T> &operator+=(const Vector3<T> &b) {
            this->x += b.x;
            this->y += b.y;
            this->z += b.z;
            return *this;
        }

        inline __host__ __device__ Vector3<T> &operator-=(T d) {
            this->x -= d;
            this->y -= d;
            this->z -= d;
            return *this;
        }

        inline __host__ __device__ Vector3<T> &operator-=(const Vector3<T> &b) {
            this->x -= b.x;
            this->y -= b.y;
            this->z -= b.z;
            return *this;
        }

        inline __host__ __device__ Vector3<T> &operator*=(T d) {
            this->x *= d;
            this->y *= d;
            this->z *= d;
            return *this;
        }

        inline __host__ __device__ Vector3<T> &operator*=(const Vector3<T> &b) {
            this->x *= b.x;
            this->y *= b.y;
            this->z *= b.z;
            return *this;
        }

        inline __host__ __device__ Vector3<T> &operator/=(T d) {
            if (d == 0) return *this;
            this->x /= d;
            this->y /= d;
            this->z /= d;
            return *this;
        }

        inline __host__ __device__ Vector3<T> &operator/=(const Vector3<T> &b) {
            if (b.x != 0) this->x /= b.x;
            if (b.y != 0) this->y /= b.y;
            if (b.z != 0) this->z /= b.z;
            return *this;
        }

        /********************************************************
         *  Math *
         ********************************************************/

        /*!
         * \brief returns the norm of the vector
         */
        inline __host__ __device__ float norm() {
            return sqrt(this->x * this->x + this->y * this->y + this->z * this->z);
        }

        /*!
         * \brief returns the squared norm of the vector
         */
        inline __host__ __device__ float square() {
            return (this->x * this->x + this->y * this->y + this->z * this->z);
        }

        /*!
         * \brief returns the sum of the vector
         */
        inline __host__ __device__ float sum() {
            return (this->x + this->y + this->z);
        }

        /*!
         * \brief returns the dot product of two vector
         */
        static inline __host__ __device__ float dot(const Vector3<T> &a, const Vector3<T> &b) {
            return (a.x * b.x + a.y * b.y + a.z * b.z);
        }

        /*!
         * \brief returns the distance between two vector
         */
        static inline __host__ __device__ float distance(const Vector3<T> &a, const Vector3<T> &b) {
            return sqrt(pow(a.x - b.x, 2) + pow(a.y - b.y, 2) + pow(a.z - b.z, 2));
        }

        /*!
         * \brief returns the cross product between two vector
         */
        static inline __host__ __device__ Vector3<T> cross(const Vector3<T> &a, const Vector3<T> &b) {
            Vector3<T> r;
            r.x = a.y * b.z - a.z * b.y;
            r.y = a.z * b.x - a.x * b.z;
            r.z = a.x * b.y - a.y * b.x;
            return r;
        }
    };

    template <typename T>
    inline __host__ __device__ Vector3<T> operator+(const Vector3<T> &a, const Vector3<T> &b) {
        Vector3<T> tmp(a);
        return tmp += b;
    }

    template <typename T>
    inline __host__ __device__ Vector3<T> operator-(const Vector3<T> &a, const Vector3<T> &b) {
        Vector3<T> tmp(a);
        return tmp -= b;
    }

    template <typename T>
    inline __host__ __device__ Vector3<T> operator*(const Vector3<T> &a, T b) {
        Vector3<T> tmp(a);
        return tmp *= b;
    }

    template <typename T>
    inline __host__ __device__ Vector3<T> operator*(T a, const Vector3<T> &b) {
        Vector3<T> tmp(a);
        return tmp *= b;
    }

    template <typename T>
    inline __host__ __device__ Vector3<T> operator*(const Vector3<T> &a, const Vector3<T> &b) {
        Vector3<T> tmp(a);
        return tmp *= b;
    }

    template <typename T>
    inline __host__ __device__ Vector3<T> operator/(const Vector3<T> &a, T b) {
        Vector3<T> tmp(a);
        return tmp /= b;
    }

    template <typename T>
    inline __host__ __device__ Vector3<T> operator/(const Vector3<T> &a, const Vector3<T> &b) {
        Vector3<T> tmp(a);
        return tmp /= b;
    }

    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    /*! \class Vector4
     *  \brief The class Vector4 represents a four dimensions vector for both CPU and GPU.
     */
    template <typename T>
    class Vector4 : public Size4_<T> {
    public:
        /********************************************************
         *  Basics*
         ********************************************************/
        inline __host__ __device__ int size() const {
            return 4;
        }

        inline __host__ __device__ Vector4() {
        }

        inline __host__ __device__ Vector4(const T &t) {
            this->x = t;
            this->y = t;
            this->z = t;
            this->w = t;
        }

        inline __host__ __device__ Vector4(const T *tp) {
            this->x = tp[0];
            this->y = tp[1];
            this->z = tp[2];
            this->w = tp[3];
        }

        inline __host__ __device__ Vector4(const T v0, const T v1, const T v2, const T v3) {
            this->x = v0;
            this->y = v1;
            this->z = v2;
            this->w = v3;
        }

        inline __host__ __device__ Vector4<T>(const Vector3<T> &v, const T d = 0) {
            this->x = v.x;
            this->y = v.y;
            this->z = v.z;
            this->z = d;
        }

        inline __host__ __device__ const T *ptr() const {
            return &this->v[0];
        }

        inline __host__ __device__ Vector4<T> &setValues(const T *b) {
            this->x = b[0];
            this->y = b[1];
            this->z = b[2];
            this->w = b[3];
            return *this;
        }

        inline __host__ __device__ T &operator[](int i) {
            return this->v[i];
        }

        inline __host__ __device__ const T &operator[](int i) const {
            return this->v[i];
        }

        /********************************************************
         *  Operator overloading *
         ********************************************************/

        inline __host__ __device__ Vector4<T> &operator+=(T d) {
            this->x += d;
            this->y += d;
            this->z += d;
            this->w += d;
            return *this;
        }

        inline __host__ __device__ Vector4<T> &operator+=(const Vector4<T> &b) {
            this->x += b.x;
            this->y += b.y;
            this->z += b.z;
            this->w += b.w;
            return *this;
        }

        inline __host__ __device__ Vector4<T> &operator-=(T d) {
            this->x -= d;
            this->y -= d;
            this->z -= d;
            this->w -= d;
            return *this;
        }

        inline __host__ __device__ Vector4<T> &operator-=(const Vector4<T> &b) {
            this->x -= b.x;
            this->y -= b.y;
            this->z -= b.z;
            this->w -= b.w;
            return *this;
        }

        inline __host__ __device__ Vector4<T> &operator*=(T d) {
            this->x *= d;
            this->y *= d;
            this->z *= d;
            return *this;
        }

        inline __host__ __device__ Vector4<T> &operator*=(const Vector4<T> &b) {
            this->x *= b.x;
            this->y *= b.y;
            this->z *= b.z;
            this->w *= b.w;
            return *this;
        }

        inline __host__ __device__ Vector4<T> &operator/=(T d) {
            if (d == 0) return *this;
            this->x /= d;
            this->y /= d;
            this->z /= d;
            this->w /= d;
            return *this;
        }

        inline __host__ __device__ Vector4<T> &operator/=(const Vector4<T> &b) {
            if (b.x != 0) this->x /= b.x;
            if (b.y != 0) this->y /= b.y;
            if (b.z != 0) this->z /= b.z;
            if (b.w != 0) this->w /= b.w;

            return *this;
        }

        /********************************************************
         *  Math *
         ********************************************************/

        /*!
         * \brief returns the norm of the vector
         */
        inline __host__ __device__ float norm() {
            return sqrt(this->x * this->x + this->y * this->y + this->z * this->z + this->w * this->w);
        }

        /*!
         * \brief returns the squared norm of the vector
         */
        inline __host__ __device__ float square() {
            return (this->x * this->x + this->y * this->y + this->z * this->z + this->w * this->w);
        }

        /*!
         * \brief returns the sum of the vector
         */
        inline __host__ __device__ float sum() {
            return (this->x + this->y + this->z);
        }

        /*!
         * \brief returns the dot product of two vector
         */
        static inline __host__ __device__ float dot(const Vector4<T> &a, const Vector4<T> &b) {
            return (a.x * b.x + a.y * b.y + a.z * b.z + a.w * b.w);
        }

        /*!
         * \brief returns the distance between two vector
         */
        static inline __host__ __device__ float distance(const Vector4<T> &a, const Vector4<T> &b) {
            return sqrt(pow(a.x - b.x, 2) + pow(a.y - b.y, 2) + pow(a.z - b.z, 2) + pow(a.w - b.w, 2));
        }
    };

    template <typename T>
    inline __host__ __device__ Vector4<T> operator-(const Vector4<T> &b) {
        Vector4<T> tmp;
        tmp.x = -b.x;
        tmp.y = -b.y;
        tmp.z = -b.z;
        tmp.w = -b.w;
        return tmp;
    }

    template <typename T>
    inline __host__ __device__ Vector4<T> operator+(const Vector4<T> &a, const Vector4<T> &b) {
        Vector4<T> tmp(a);
        return tmp += b;
    }

    template <typename T>
    inline __host__ __device__ Vector4<T> operator-(const Vector4<T> &a, const Vector4<T> &b) {
        Vector4<T> tmp(a);
        return tmp -= b;
    }

    template <typename T>
    inline __host__ __device__ Vector4<T> operator*(const Vector4<T> &a, T b) {
        Vector4<T> tmp(a);
        return tmp *= b;
    }

    template <typename T>
    inline __host__ __device__ Vector4<T> operator*(T a, const Vector4<T> &b) {
        Vector4<T> tmp(a);
        return tmp *= b;
    }

    template <typename T>
    inline __host__ __device__ Vector4<T> operator*(const Vector4<T> &a, const Vector4<T> &b) {
        Vector4<T> tmp(a);
        return tmp *= b;
    }

    template <typename T>
    inline __host__ __device__ Vector4<T> operator/(const Vector4<T> &a, T b) {
        Vector4<T> tmp(a);
        return tmp /= b;
    }

    template <typename T>
    inline __host__ __device__ Vector4<T> operator/(const Vector4<T> &a, const Vector4<T> &b) {
        Vector4<T> tmp(a);
        return tmp /= b;
    }
    /// @endcond

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////                 ////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////     NEW TYPES   ////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////                 ////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#ifndef float1
    typedef float float1;
#endif

#ifndef float2
    typedef Vector2<float> float2;
#endif

#ifndef float3
    typedef Vector3<float> float3;
#endif

#ifndef float4
    typedef Vector4<float> float4;
#endif

#ifndef uchar1
    typedef unsigned char uchar1;
#endif

#ifndef uchar2
    typedef Vector2<unsigned char> uchar2;
#endif

#ifndef uchar3
    typedef Vector3<unsigned char> uchar3;
#endif

#ifndef uchar4
    typedef Vector4<unsigned char> uchar4;
#endif

#ifndef double1
    typedef double double1;
#endif

#ifndef double2
    typedef Vector2<double> double2;
#endif

#ifndef double3
    typedef Vector3<double> double3;
#endif

#ifndef double4
    typedef Vector4<double> double4;
#endif

#ifndef uint1
    typedef unsigned int uint1;
#endif

#ifndef uint2
    typedef Vector2<unsigned int> uint2;
#endif

#ifndef uint3
    typedef Vector3<unsigned int> uint3;
#endif

#ifndef uint4
    typedef Vector4<unsigned int> uint4;
#endif

    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////                 ////////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////     MATRIX      ////////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////                 ////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    /*! \class Matrix3f
     *  \brief The class Matrix3f represent a generic three-dimensional matrix
     *
     * \n\n sl::Matrix3f is defined in a row-major order:
     * \n - It means that, in the value buffer, the entire first row is stored first, followed by the entire second row, and so on.
     * \n - you can access the data with the 'r' ptr or by element name as :
     *       r00, r01, r02       | 0 1 2 |
     *       r10, r11, r12  <-> r| 3 4 5 |
     *       r20, r21, r21       | 6 7 8 |
     */
    class SL_CORE_EXPORT_DLL Matrix3f {
    public:
        static const int nbElem = 9;
        union {
            // access inner data by dedicated ref.
            struct {
                float r00, r01, r02, r10, r11, r12, r20, r21, r22;
            };
            // ptr to inner data
            float r[nbElem];
        };

        /*!
         * \brief Matrix3f default constructor.
         */
        Matrix3f();

        /*!
         * \brief Matrix3f copy constructor (deep copy).
         */
        Matrix3f(float data[]);

        /*!
         *  brief Matrix3f copy constructor (deep copy).
         * \param rotation : the Matrix3f to copy.
         */
        Matrix3f(const Matrix3f &mat);

        /*!
         *  brief Gives the result of the multiplication between two Matrix3f
         */
        Matrix3f operator*(const Matrix3f &mat) const;

        /*!
		*  brief Gives the result of the multiplication between a Matrix3f and a scalar.
		*/
        Matrix3f operator*(const double &scalar) const;

        /*!
		*  brief Test two Matrix3f equality.
		*/
        bool operator==(const Matrix3f &mat) const;

        /*!
		*  brief Test two Matrix3f inequality.
		*/
        bool operator!=(const Matrix3f &mat) const;

        /*!
         * \brief Gets access to a specific point in the Matrix3f (read / write).
         * \param u : specify the row
         * \param v : specify the column
         * \return The value at the u, v coordinates.
         */
        float &operator()(int u, int v);

        /*!
         * \brief Sets the Matrix3f to its inverse.
         */
        void inverse();

        /*!
         * \brief Returns the inverse of a Matrix3f.
         * \param rotation : the Matrix3f to compute the inverse from.
         * \return The inverse of the given Matrix3f
         */
        static Matrix3f inverse(const Matrix3f &rotation);

        /*!
         * \brief Sets the RotationArray to its transpose.
         */
        void transpose();

        /*!
         * \brief Returns the transpose of a Matrix3f.
         * \param rotation : the Matrix3f to compute the transpose from.
         * \return The transpose of the given Matrix3f
         */
        static Matrix3f transpose(const Matrix3f &rotation);

        /*!
         * \brief Sets the Matrix3f to identity.
         */
        void setIdentity();

        /*!
         * \brief Creates an identity Matrix3f.
         * \return A Matrix3f set to identity.
         */
        static Matrix3f identity();

        /*!
         * \brief Sets the Matrix3f to zero.
         */
        void setZeros();

        /*!
         * \brief Creates a Matrix3f filled with zeros.
         * \return A Matrix3f set to zero.
         */
        static Matrix3f zeros();

        /*!
         * \brief Return the components of the Matrix3f in a sl::String.
         * \return A sl::String containing the components of the current Matix3f.
         */
        sl::String getInfos();

        /*!
         * \brief Name of the matrix (optional).
         */
        sl::String matrix_name;
    };

    /*! \class Matrix4f
     *  \brief The class Matrix4f represent a generic fourth-dimensional matrix.
     *
     * \n\n sl::Matrix4f is defined in a row-major order:
     * \n - It means that, in the value buffer, the entire first row is stored first, followed by the entire second row, and so on.
     * \n - you can access the data by the 'm' ptr or by the element name as :
     *       r00, r01, r02, tx        | 0  1  2  3  |
     *       r10, r11, r12, ty   <-> m| 4  5  6  7  |
     *       r20, r21, r22, tz        | 8  9  10 11 |
     *       m30, m31, m32, m33       | 12 13 14 15 |      */

    class SL_CORE_EXPORT_DLL Matrix4f {
    public:
        static const int nbElem = 16;
        union {
            // access inner data by dedicated ref.
            struct {
                float r00, r01, r02, tx, r10, r11, r12, ty, r20, r21, r22, tz, m30, m31, m32, m33;
            };
            // ptr to inner data.
            float m[nbElem];
        };

        /*!
         * \brief Matrix4f default constructor.
         */
        Matrix4f();

        /*!
         * \brief Matrix4f copy constructor (deep copy).
         */
        Matrix4f(float data[]);

        /*!
         *  brief Matrix4f copy constructor (deep copy).
         * \param rotation : the Matrix4f to copy.
         */
        Matrix4f(const Matrix4f &mat);

        /*!
         *  brief Gives the result of the multiplication between two Matrix4f.
         */
        Matrix4f operator*(const Matrix4f &mat) const;

        /*!
         *  brief Gives the result of the multiplication between a Matrix4f and a scalar.
         */
        Matrix4f operator*(const double &scalar) const;

        /*!
         *  brief Test two Matrix4f equality.
         */
        bool operator==(const Matrix4f &mat) const;

        /*!
         *  brief Test two Matrix4f inequality.
         */
        bool operator!=(const Matrix4f &mat) const;

        /*!
         * \brief Gets access to a specific point in the Matrix4f (read / write).
         * \param u : specify the row.
         * \param v : specify the column.
         * \return The value at  the u, v coordinates.
         */
        float &operator()(int u, int v);

        /*!
         * \brief Sets the Matrix4f to its inverse.
         * \return SUCCESS if the inverse has been computed, ERROR_CODE_FAILURE is not (det = 0).
         */
        ERROR_CODE inverse();

        /*!
         * \brief Creates the inverse of a Matrix4f.
         * \param rotation : the Matrix4f to compute the inverse from.
         * \return The inverse of the given Matrix4f.
         */
        static Matrix4f inverse(const Matrix4f &mat);

        /*!
         * \brief Sets the Matrix4f to its transpose.
         */
        void transpose();

        /*!
         * \brief Creates the transpose of a Matrix4f.
         * \param rotation : the Matrix4f to compute the transpose from.
         * \return The transpose of the given Matrix4f.
         */
        static Matrix4f transpose(const Matrix4f &mat);

        /*!
         * \brief Sets the Matrix4f to identity.
         */
        void setIdentity();

        /*!
         * \brief Creates an identity Matrix4f.
         * \return A Matrix4f set to identity.
         */
        static Matrix4f identity();

        /*!
         * \brief Sets the Matrix4f to zero.
         */
        void setZeros();

        /*!
         * \brief Creates a Matrix4f filled with zeros.
         * \return A Matrix4f set to zero.
         */
        static Matrix4f zeros();

        /*!
         * \brief Sets a 3x3 Matrix inside the Matrix4f.
         * \note Can be used to set the rotation matrix when the matrix4f is a pose or an isometric matrix.
         * \param sl::Matrix3f  : sub matrix to put inside the Matrix4f.
         * \param row : index of the row to start the 3x3 block. Must be 0 or 1.
         * \param column : index of the column to start the 3x3 block. Must be 0 or 1.
         * \return SUCCESS if everything went well, ERROR_CODE_FAILURE otherwise.
         */
        ERROR_CODE setSubMatrix3f(sl::Matrix3f input, int row = 0, int column = 0);

        /*!
         * \brief Sets a 3x1 Vector inside the Matrix4f at the specified column index.
         * \note Can be used to set the Translation/Position matrix when the matrix4f is a pose or an isometry.
         * \param sl::Vector3  : sub vector to put inside the Matrix4f.
         * \param column : index of the column to start the 3x3 block. By default, it is the last column (translation for a Pose).
         * \return SUCCESS if everything went well, ERROR_CODE_FAILURE otherwise.
         */
        ERROR_CODE setSubVector3f(sl::Vector3<float> input, int column = 3);

        /*!
         * \brief Sets a 4x1 Vector inside the Matrix4f at the specified column index.
         * \note Can be used to set the Translation/Position matrix when the matrix4f is a pose or an isometry.
         * \param sl::Vector4  : sub vector to put inside the Matrix4f.
         * \param column : index of the column to start the 3x3 block. By default, it is the last column (translation for a Pose).
         * \return SUCCESS if everything went well, ERROR_CODE_FAILURE otherwise.
         */
        ERROR_CODE setSubVector4f(sl::Vector4<float> input, int column = 3);

        /*!
         * \brief Return the components of the Matrix4f in a sl::String.
         * \return A sl::String containing the components of the current Matrix4f.
         */
        sl::String getInfos();

        /*!
         * \brief Name of the matrix (optional).
         */
        sl::String matrix_name;
    };

    /////////////////////////////////////////////////////////////////////////////////////////////////////////

    template <typename T>
    std::ostream &operator<<(std::ostream &os, const Vector2<T> &v2) {
        os << v2.x << " " << v2.y << "\n";
        return os;
    }

    template <typename T>
    std::ostream &operator<<(std::ostream &os, const Vector3<T> &v3) {
        os << v3.x << " " << v3.y << " " << v3.z << "\n";
        return os;
    }

    template <typename T>
    std::ostream &operator<<(std::ostream &os, const Vector4<T> &v4) {
        os << v4.x << " " << v4.y << " " << v4.z << " " << v4.w << "\n";
        return os;
    }

#define TIMING
#ifdef TIMING
#define INIT_TIMER auto start = std::chrono::high_resolution_clock::now();
#define START_TIMER start = std::chrono::high_resolution_clock::now();
#define DEF_START_TIMER auto start = std::chrono::high_resolution_clock::now();
#define STOP_TIMER(name) std::cout << name << " " << std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::high_resolution_clock::now() - start).count() << " ms " << std::endl;
#else
#define INIT_TIMER
#define START_TIMER
#define DEF_START_TIMER
#define STOP_TIMER(name)
#endif

}
#endif /* __TYPES_HPP__ */
