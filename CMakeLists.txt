cmake_minimum_required(VERSION 3.15.0)
set(TARGET_NAME igeTFLite-static)

project(${TARGET_NAME})

set (TENSORFLOW_DIR ${CMAKE_CURRENT_SOURCE_DIR})

# [IGE]: tweaks for platforms
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED TRUE)

# Modules and install path (required by conan)
set(CMAKE_INSTALL_PREFIX ${CMAKE_BINARY_DIR}/install)
set(CMAKE_MODULE_PATH ${CMAKE_BINARY_DIR} ${CMAKE_MODULE_PATH})
set(CMAKE_PREFIX_PATH ${CMAKE_BINARY_DIR} ${CMAKE_PREFIX_PATH})

if(DEFINED ANDROID_PLATFORM)
    set (ANDROID 1)
    if(ANDROID_ABI STREQUAL "armeabi-v7a")
        add_compile_options(-marm -march=armv7-a -mtune=cortex-a15 -mfpu=neon-fp16 -mfloat-abi=softfp)
    elseif(ANDROID_ABI STREQUAL "x86")
        add_compile_options(-march=atom -m32 -msse -msse2 -msse3 -mssse3 -mfpmath=sse -mstackrealign)
    elseif(ANDROID_ABI STREQUAL "arm64-v8a")
        add_compile_options(-march=armv8-a+simd+sve -mtune=cortex-a53 -D__ARM_NEON -D__ARM_NEON__)
    elseif(ANDROID_ABI STREQUAL "x86_64")
        add_compile_options(-march=atom -m64 -msse -msse2 -msse3 -mssse3 -msse4.1 -msse4.2 -mfpmath=sse)
    endif()
    if(CMAKE_BUILD_TYPE STREQUAL "Release")
        add_compile_options(-g0 -Ofast)
    else(CMAKE_BUILD_TYPE STREQUAL "Debug")
        add_compile_options(-Og)
    endif()
elseif(MSVC)
    add_compile_options(/MP /std:c++17)
elseif(IOS)
    if(CMAKE_BUILD_TYPE STREQUAL "Release")
        add_compile_options(-g0 -Ofast)
    endif()
endif()
# [/IGE]

set(CMAKE_SKIP_INSTALL_ALL_DEPENDENCY true)

if(${APP_STYLE} MATCHES "SHARED")
    find_package (Python3 ${PYTHON_VERSION} EXACT REQUIRED COMPONENTS Development)
else()
    find_package(Python REQUIRED)
    set (Python3_INCLUDE_DIRS ${Python_INCLUDE_DIRS})
    set (Python3_LIBRARIES ${Python_LIBRARIES})
endif()


find_package(numpy REQUIRED)
find_package(pybind11 REQUIRED)

set(PYTHON_INCLUDE_DIRS ${Python3_INCLUDE_DIRS})

file(GLOB SOURCES
    "${TENSORFLOW_DIR}/tensorflow/lite/python/interpreter_wrapper/*.h"
    "${TENSORFLOW_DIR}/tensorflow/lite/python/interpreter_wrapper/*.cc"
)

set(INCLUDES
    "${TENSORFLOW_DIR}"
    "${TENSORFLOW_DIR}/tensorflow"
    "${TENSORFLOW_DIR}/tensorflow/lite"
    "${CMAKE_BINARY_DIR}/flatbuffers/include"
    "${PYTHON_INCLUDE_DIRS}"
    "${numpy_INCLUDE_DIRS}"
    "${pybind11_INCLUDE_DIRS}"
)

add_library(${TARGET_NAME} STATIC ${SOURCES})
target_include_directories(${TARGET_NAME} PRIVATE ${INCLUDES})

add_subdirectory(${TENSORFLOW_DIR}/tensorflow/lite ${CMAKE_BINARY_DIR}/tensorflow-lite)
target_link_libraries(${TARGET_NAME} tensorflow-lite)

# Install Targets
install(TARGETS
    ${TARGET_NAME}
    tensorflow-lite
    RUNTIME DESTINATION bin
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    PUBLIC_HEADER DESTINATION include
)

file(GLOB_RECURSE PUBLIC_INCLUDE_FILES "${CMAKE_CURRENT_SOURCE_DIR}/tensorflow/*.h*")
foreach(HEADER ${PUBLIC_INCLUDE_FILES})
    file(RELATIVE_PATH HEADER_RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}/tensorflow/" "${HEADER}")
    get_filename_component(DIR ${HEADER_RELATIVE} DIRECTORY)
    install(FILES ${HEADER} DESTINATION include/${DIR})
endforeach()

