
if(NOT "/home/alex/source/pytetwild/src/fTetWild/3rdparty/.cache/json/json-download-prefix/src/json-download-stamp/json-download-gitinfo.txt" IS_NEWER_THAN "/home/alex/source/pytetwild/src/fTetWild/3rdparty/.cache/json/json-download-prefix/src/json-download-stamp/json-download-gitclone-lastrun.txt")
  message(STATUS "Avoiding repeated git clone, stamp file is up to date: '/home/alex/source/pytetwild/src/fTetWild/3rdparty/.cache/json/json-download-prefix/src/json-download-stamp/json-download-gitclone-lastrun.txt'")
  return()
endif()

execute_process(
  COMMAND ${CMAKE_COMMAND} -E rm -rf "/home/alex/source/pytetwild/src/fTetWild/3rdparty//json"
  RESULT_VARIABLE error_code
  )
if(error_code)
  message(FATAL_ERROR "Failed to remove directory: '/home/alex/source/pytetwild/src/fTetWild/3rdparty//json'")
endif()

# try the clone 3 times in case there is an odd git clone issue
set(error_code 1)
set(number_of_tries 0)
while(error_code AND number_of_tries LESS 3)
  execute_process(
    COMMAND "/usr/bin/git"  clone --no-checkout --config "advice.detachedHead=false" --config "advice.detachedHead=false" "https://github.com/jdumas/json" "json"
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
  message(FATAL_ERROR "Failed to clone repository: 'https://github.com/jdumas/json'")
endif()

execute_process(
  COMMAND "/usr/bin/git"  checkout 0901d33bf6e7dfe6f70fd9d142c8f5c6695c6c5b --
  WORKING_DIRECTORY "/home/alex/source/pytetwild/src/fTetWild/3rdparty/json"
  RESULT_VARIABLE error_code
  )
if(error_code)
  message(FATAL_ERROR "Failed to checkout tag: '0901d33bf6e7dfe6f70fd9d142c8f5c6695c6c5b'")
endif()

set(init_submodules TRUE)
if(init_submodules)
  execute_process(
    COMMAND "/usr/bin/git"  submodule update --recursive --init 
    WORKING_DIRECTORY "/home/alex/source/pytetwild/src/fTetWild/3rdparty/json"
    RESULT_VARIABLE error_code
    )
endif()
if(error_code)
  message(FATAL_ERROR "Failed to update submodules in: '/home/alex/source/pytetwild/src/fTetWild/3rdparty/json'")
endif()

# Complete success, update the script-last-run stamp file:
#
execute_process(
  COMMAND ${CMAKE_COMMAND} -E copy
    "/home/alex/source/pytetwild/src/fTetWild/3rdparty/.cache/json/json-download-prefix/src/json-download-stamp/json-download-gitinfo.txt"
    "/home/alex/source/pytetwild/src/fTetWild/3rdparty/.cache/json/json-download-prefix/src/json-download-stamp/json-download-gitclone-lastrun.txt"
  RESULT_VARIABLE error_code
  )
if(error_code)
  message(FATAL_ERROR "Failed to copy script-last-run stamp file: '/home/alex/source/pytetwild/src/fTetWild/3rdparty/.cache/json/json-download-prefix/src/json-download-stamp/json-download-gitclone-lastrun.txt'")
endif()

