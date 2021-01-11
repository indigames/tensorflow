cmake_minimum_required(VERSION 3.4.1)

file(TO_CMAKE_PATH $ENV{IGE_LIBS} IGE_LIBS)

if (NOT DEFINED APP_STYLE)
    set(APP_STYLE STATIC)
endif()

set(TARGET_NAME igeTFLite-static)

project(${TARGET_NAME})

set (TENSORFLOW_DIR ${CMAKE_CURRENT_SOURCE_DIR}/..)

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

set (PYTHON_INCLUDE_DIRS "${IGE_LIBS}/Python/Include")
if (MSVC)
	list(APPEND PYTHON_INCLUDE_DIRS "${IGE_LIBS}/Python/PC")
elseif (OSX)
	list(APPEND PYTHON_INCLUDE_DIRS "${IGE_LIBS}/Python/Mac")
elseif (ANDROID)
	list(APPEND PYTHON_INCLUDE_DIRS "${IGE_LIBS}/Python/Android")
elseif (IOS)
	list(APPEND PYTHON_INCLUDE_DIRS "${IGE_LIBS}/Python/IOS")
endif ()


file(GLOB SOURCES
    "${TENSORFLOW_DIR}/tensorflow/lite/python/interpreter_wrapper/*.h"
    "${TENSORFLOW_DIR}/tensorflow/lite/python/interpreter_wrapper/*.cc"
)

set(INCLUDES
    "${TENSORFLOW_DIR}"
    "${TENSORFLOW_DIR}/tensorflow"
    "${TENSORFLOW_DIR}/tensorflow/lite"
    "${IGE_LIBS}/pybind11/include"
    "${IGE_LIBS}/numpy/include"
    "${IGE_LIBS}/numpy/include/numpy/core/include"
    "${CMAKE_BINARY_DIR}/flatbuffers/include"
    "${PYTHON_INCLUDE_DIRS}"
)

add_library(${TARGET_NAME} ${APP_STYLE} ${SOURCES})
target_include_directories(${TARGET_NAME} PRIVATE ${INCLUDES})

add_subdirectory(${TENSORFLOW_DIR}/tensorflow/lite ${CMAKE_BINARY_DIR}/tensorflow-lite)
target_link_libraries(${TARGET_NAME} tensorflow-lite)
