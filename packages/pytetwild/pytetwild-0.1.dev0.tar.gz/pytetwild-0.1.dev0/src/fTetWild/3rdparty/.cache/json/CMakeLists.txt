# Distributed under the OSI-approved MIT License.  See accompanying
# file LICENSE or https://github.com/Crascit/DownloadProject for details.

cmake_minimum_required(VERSION 2.8.2)

project(json-download NONE)

include(ExternalProject)
ExternalProject_Add(json-download
                    GIT_CONFIG advice.detachedHead=false;GIT_REPOSITORY;https://github.com/jdumas/json;GIT_TAG;0901d33bf6e7dfe6f70fd9d142c8f5c6695c6c5b
                    SOURCE_DIR          "/home/alex/source/pytetwild/src/fTetWild/3rdparty//json"
                    BINARY_DIR          "/home/alex/source/pytetwild/json-build"
                    CONFIGURE_COMMAND   ""
                    BUILD_COMMAND       ""
                    INSTALL_COMMAND     ""
                    TEST_COMMAND        ""
)
