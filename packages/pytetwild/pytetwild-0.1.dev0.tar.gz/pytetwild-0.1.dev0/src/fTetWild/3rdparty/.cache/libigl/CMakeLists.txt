# Distributed under the OSI-approved MIT License.  See accompanying
# file LICENSE or https://github.com/Crascit/DownloadProject for details.

cmake_minimum_required(VERSION 2.8.2)

project(libigl-download NONE)

include(ExternalProject)
ExternalProject_Add(libigl-download
                    GIT_CONFIG advice.detachedHead=false;GIT_REPOSITORY;https://github.com/libigl/libigl.git;GIT_TAG;45cfc79fede992ea3923ded9de3c21d1c4faced1
                    SOURCE_DIR          "/home/alex/source/pytetwild/src/fTetWild/3rdparty//libigl"
                    BINARY_DIR          "/home/alex/source/pytetwild/libigl-build"
                    CONFIGURE_COMMAND   ""
                    BUILD_COMMAND       ""
                    INSTALL_COMMAND     ""
                    TEST_COMMAND        ""
)
