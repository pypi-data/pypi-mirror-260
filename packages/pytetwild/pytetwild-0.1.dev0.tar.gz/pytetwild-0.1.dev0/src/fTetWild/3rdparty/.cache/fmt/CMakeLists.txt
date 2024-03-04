# Distributed under the OSI-approved MIT License.  See accompanying
# file LICENSE or https://github.com/Crascit/DownloadProject for details.

cmake_minimum_required(VERSION 2.8.2)

project(fmt-download NONE)

include(ExternalProject)
ExternalProject_Add(fmt-download
                    GIT_CONFIG advice.detachedHead=false;URL;https://github.com/fmtlib/fmt/archive/5.3.0.tar.gz;URL_MD5;1015bf3ff2a140dfe03de50ee2469401
                    SOURCE_DIR          "/home/alex/source/pytetwild/src/fTetWild/3rdparty//fmt"
                    BINARY_DIR          "/home/alex/source/pytetwild/fmt-build"
                    CONFIGURE_COMMAND   ""
                    BUILD_COMMAND       ""
                    INSTALL_COMMAND     ""
                    TEST_COMMAND        ""
)
