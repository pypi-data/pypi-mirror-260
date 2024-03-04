# Distributed under the OSI-approved MIT License.  See accompanying
# file LICENSE or https://github.com/Crascit/DownloadProject for details.

cmake_minimum_required(VERSION 2.8.2)

project(tbb-download NONE)

include(ExternalProject)
ExternalProject_Add(tbb-download
                    GIT_CONFIG advice.detachedHead=false;GIT_REPOSITORY;https://github.com/wjakob/tbb.git;GIT_TAG;ddbe45cd3ad89df9a84cd77013d5898fc48b8e89
                    SOURCE_DIR          "/home/alex/source/pytetwild/src/fTetWild/3rdparty//tbb"
                    BINARY_DIR          "/home/alex/source/pytetwild/tbb-build"
                    CONFIGURE_COMMAND   ""
                    BUILD_COMMAND       ""
                    INSTALL_COMMAND     ""
                    TEST_COMMAND        ""
)
