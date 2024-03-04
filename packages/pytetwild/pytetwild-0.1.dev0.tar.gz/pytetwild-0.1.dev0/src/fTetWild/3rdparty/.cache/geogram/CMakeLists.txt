# Distributed under the OSI-approved MIT License.  See accompanying
# file LICENSE or https://github.com/Crascit/DownloadProject for details.

cmake_minimum_required(VERSION 2.8.2)

project(geogram-download NONE)

include(ExternalProject)
ExternalProject_Add(geogram-download
                    GIT_CONFIG advice.detachedHead=false;GIT_REPOSITORY;https://github.com/Yixin-Hu/geogram;GIT_TAG;b613750341a6cdd31ae8df80ecfc26ac7ca1a6ad
                    SOURCE_DIR          "/home/alex/source/pytetwild/src/fTetWild/3rdparty//geogram"
                    BINARY_DIR          "/home/alex/source/pytetwild/geogram-build"
                    CONFIGURE_COMMAND   ""
                    BUILD_COMMAND       ""
                    INSTALL_COMMAND     ""
                    TEST_COMMAND        ""
)
