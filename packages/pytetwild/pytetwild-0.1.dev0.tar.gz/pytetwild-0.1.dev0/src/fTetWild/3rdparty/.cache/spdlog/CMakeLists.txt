# Distributed under the OSI-approved MIT License.  See accompanying
# file LICENSE or https://github.com/Crascit/DownloadProject for details.

cmake_minimum_required(VERSION 2.8.2)

project(spdlog-download NONE)

include(ExternalProject)
ExternalProject_Add(spdlog-download
                    GIT_CONFIG advice.detachedHead=false;URL;https://github.com/gabime/spdlog/archive/v1.3.1.tar.gz;URL_MD5;3c17dd6983de2a66eca8b5a0b213d29f
                    SOURCE_DIR          "/home/alex/source/pytetwild/src/fTetWild/3rdparty//spdlog"
                    BINARY_DIR          "/home/alex/source/pytetwild/spdlog-build"
                    CONFIGURE_COMMAND   ""
                    BUILD_COMMAND       ""
                    INSTALL_COMMAND     ""
                    TEST_COMMAND        ""
)
