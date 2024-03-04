
if(NOT "/home/alex/source/pytetwild/src/fTetWild/3rdparty/.cache/libigl/libigl-download-prefix/src/libigl-download-stamp/libigl-download-gitinfo.txt" IS_NEWER_THAN "/home/alex/source/pytetwild/src/fTetWild/3rdparty/.cache/libigl/libigl-download-prefix/src/libigl-download-stamp/libigl-download-gitclone-lastrun.txt")
  message(STATUS "Avoiding repeated git clone, stamp file is up to date: '/home/alex/source/pytetwild/src/fTetWild/3rdparty/.cache/libigl/libigl-download-prefix/src/libigl-download-stamp/libigl-download-gitclone-lastrun.txt'")
  return()
endif()

execute_process(
  COMMAND ${CMAKE_COMMAND} -E rm -rf "/home/alex/source/pytetwild/src/fTetWild/3rdparty//libigl"
  RESULT_VARIABLE error_code
  )
if(error_code)
  message(FATAL_ERROR "Failed to remove directory: '/home/alex/source/pytetwild/src/fTetWild/3rdparty//libigl'")
endif()

# try the clone 3 times in case there is an odd git clone issue
set(error_code 1)
set(number_of_tries 0)
while(error_code AND number_of_tries LESS 3)
  execute_process(
    COMMAND "/usr/bin/git"  clone --no-checkout --config "advice.detachedHead=false" --config "advice.detachedHead=false" "https://github.com/libigl/libigl.git" "libigl"
    WORKING_DIRECTORY "/home/alex/source/pytetwild/src/fTetWild/3rdparty"
    RESULT_VARIABLE error_code
    )
  math(EXPR number_of_tries "${number_of_tries} + 1")
endwhile()
if(number_of_tries GREATER 1)
  message(STATUS "Had to git clone more than once:
          ${number_of_tries} times.")
endif()
if(error_code)
  message(FATAL_ERROR "Failed to clone repository: 'https://github.com/libigl/libigl.git'")
endif()

execute_process(
  COMMAND "/usr/bin/git"  checkout 45cfc79fede992ea3923ded9de3c21d1c4faced1 --
  WORKING_DIRECTORY "/home/alex/source/pytetwild/src/fTetWild/3rdparty/libigl"
  RESULT_VARIABLE error_code
  )
if(error_code)
  message(FATAL_ERROR "Failed to checkout tag: '45cfc79fede992ea3923ded9de3c21d1c4faced1'")
endif()

set(init_submodules TRUE)
if(init_submodules)
  execute_process(
    COMMAND "/usr/bin/git"  submodule update --recursive --init 
    WORKING_DIRECTORY "/home/alex/source/pytetwild/src/fTetWild/3rdparty/libigl"
    RESULT_VARIABLE error_code
    )
endif()
if(error_code)
  message(FATAL_ERROR "Failed to update submodules in: '/home/alex/source/pytetwild/src/fTetWild/3rdparty/libigl'")
endif()

# Complete success, update the script-last-run stamp file:
#
execute_process(
  COMMAND ${CMAKE_COMMAND} -E copy
    "/home/alex/source/pytetwild/src/fTetWild/3rdparty/.cache/libigl/libigl-download-prefix/src/libigl-download-stamp/libigl-download-gitinfo.txt"
    "/home/alex/source/pytetwild/src/fTetWild/3rdparty/.cache/libigl/libigl-download-prefix/src/libigl-download-stamp/libigl-download-gitclone-lastrun.txt"
  RESULT_VARIABLE error_code
  )
if(error_code)
  message(FATAL_ERROR "Failed to copy script-last-run stamp file: '/home/alex/source/pytetwild/src/fTetWild/3rdparty/.cache/libigl/libigl-download-prefix/src/libigl-download-stamp/libigl-download-gitclone-lastrun.txt'")
endif()

