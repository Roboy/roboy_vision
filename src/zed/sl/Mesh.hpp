#ifndef __MESH_HPP__
#define __MESH_HPP__

#include <vector>
#include <string>
#include <fstream>

#include <sl/Core.hpp>

#if defined(_WIN32)
#ifdef SL_SCANNING_EXPORT
#define SL_EXPORT_DLL __declspec(dllexport)
#else
#define SL_EXPORT_DLL __declspec(dllimport)
#endif
#elif __GNUC__
#define SL_EXPORT_DLL __attribute__((visibility("default")))
#else
#define SL_EXPORT_DLL
#endif

namespace sl {

    /*!
     *  \enum Mesh file format
     *  \ingroup Enumerations
     *  \brief List available mesh file formats.
     */
    typedef enum {
        MESH_FILE_PLY,     /*!<Contains only vertices and faces.*/
        MESH_FILE_PLY_BIN, /*!<Contains only vertices and faces, encoded in binary.*/
        MESH_FILE_OBJ,     /*!<Contains vertices, normals, faces and textures informations if possible.*/
        MESH_FILE_LAST
    } MESH_FILE_FORMAT;
    
    /*!
    *  \enum Mesh Texture format
    *  \ingroup Enumerations
    *  \brief List availables mesh texture formats.
    */
    typedef enum {
        MESH_TEXTURE_RGB,
        MESH_TEXTURE_RGBA,
        MESH_TEXTURE_LAST,
    } MESH_TEXTURE_FORMAT;

    /**
     * \class MeshFilterParameters
     * \brief Parameters for the optional filtering step of a sl::Mesh.
     * \n A default constructor is enabled and set to its default parameters.
     * \note Parameters can be user adjusted.
     */
    class SL_EXPORT_DLL MeshFilterParameters {
    public:
        /*!
         *  \enum Mesh filtering intensity.
         *  \ingroup Enumerations
         *  \brief List available mesh filtering intensity.
         */
        typedef enum {
            FILTER_LOW,    /*!<Soft decimation and smoothing.*/
            FILTER_MEDIUM, /*!<Decimate the number of faces and apply a soft smooth.*/
            FILTER_HIGH    /*!<Drasticly reduce the number of faces.*/
        } FILTER;

        /**
         * \brief Default constructor, set all parameters to their default and optimized values.
         */
        MeshFilterParameters(FILTER filtering_ = FILTER_LOW) {
            set(filtering_);
        }

        /*!
         * \brief Sets the filtering intensity
         * \param filtering_ : the desired sl::MeshFilterParameters::FILTER.
         */
        void set(FILTER filtering_ = FILTER_LOW) {
            filtering = filtering_;
        }

        FILTER filtering = FILTER::FILTER_LOW;

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
     * \class Mesh
     * \brief A mesh contains the geometric data of the scene computed by the spatial mapping.
     */
    class SL_EXPORT_DLL Mesh {
    /// @cond
        friend class CameraMemberHandler;
    /// @endcond

    public:
        /*!
         * \brief Default constructor which creates an empty Mesh.
         */
        Mesh();

        /*!
         * \brief Mesh destructor.
         */
        ~Mesh();

        /**
         *	Vertices are defined by a 3D point {x,y,z}.
         */
        std::vector<sl::float3> vertices;

        /**
         *	Triangles (or faces) contains the index of its three vertices. It corresponds to the 3 vertices of the triangle {v1, v2, v3}.
         */
        std::vector<sl::uint3> triangles;

        /**
         *	Normals are defined by three conponant, {nx, ny, nz}. Normals are defined for each vertices
         *  (Mesh::vertices and Mesh::normals are the same size).
         */
        std::vector<sl::float3> normals;

        /**
         *  Texture coordinates defines 2D points on a texture.
         */
        std::vector<sl::float2> uv;

        /**
         * \struct Indice.
         * \brief Store the index per faces of the associated vertices/normals/texture coordinates.
         * \note Contains data only after you call Mesh::applyTexture().
         */
        struct Indice {
            sl::uint3 v_vn_ind; /*!< vertices and normals indices.*/
            sl::uint3 uv_ind; /*!< texture coordinates indices.*/
        };

        /**
         * Store the list of vertices index affected to each texture image.
         * The first vector has the same size as Mesh::textures, the size of the second vector represents the number of faces associated to this texture.
         * By running over the second vector you can access the vertices/normals and texture coordinates of the current texture.
         * \note Contains data only after you call Mesh::applyTexture().
         */
        std::vector<std::vector<Indice>> material_indices;

        /**
         * \struct Texture
         * \brief Contains information about texture images associated to the Mesh.
         */
        struct Texture {
            std::string name;       /*!< The name of the file in which the texture is saved.*/
            sl::Mat texture;        /*!< A sl::Mat that contains the data of the texture.*/
            unsigned int indice_gl; /*!< useful for openGL binding reference (value not set by the SDK).*/
        };

        /**
         *  List of textures images.
         */
        std::vector<Texture> textures;

        /*!
         * \brief Filters the mesh according to the given parameters.
         * \param params : defines the filtering parameters, for more info checkout the sl::MeshFilterParameters documentation.
         * \return True if the filtering was successful, false otherwise.
         *
         * \note The filtering is a costly operation but the resulting mesh is significantly lighter and less noisy,
         * the parameters can be tweaked to get a mesh that fit better the final application.
         * For instance a collision mesh will need to have a coarser, more decimated resolution.
         */
        bool filter(MeshFilterParameters params = MeshFilterParameters());

        /*!
         *  \brief Applies texture to the mesh.
         * \return True if the texturing was successful, false otherwise.
         *
         * \warning SpatialMappingParams::saveTextureData must be set as true when enabling the spatial mapping to be able to apply the textures.
         * \warning The mesh should be filtered before calling this function since Mesh::filter will erased the textures,
         * the texturing is also significantly slower on non-filtered meshes.
         */
        bool applyTexture(MESH_TEXTURE_FORMAT texture_format = MESH_TEXTURE_RGB);

        /*!
         * \brief Saves the mesh into a file.
         * \param filename : the path and filename of the mesh
         * \param type : defines the file type (extension)
         * \return True if the file was successfully saved, false otherwise.
         * \note Only the sl::MESH_FILE_OBJ support the textures recording
         */
        bool save(std::string filename, MESH_FILE_FORMAT type = MESH_FILE_OBJ);

        /*!
         *  \brief Loads the mesh from a file.
         *  \param filename : the path and filename of the mesh.
         *  \retval true if the loading was successful, false otherwise.
         */
        bool load(const std::string filename);

        /*!
         *  \brief Clears all the mesh data (empty the vectors).
         */
        void clear();

    private:
        sl::TextureImagePool im_pool;
        sl::CameraParameters cam_param;
        float min_d, max_d;
        bool welded;
        size_t memory = 0;
    };
}

#endif /* MESH_HPP_ */