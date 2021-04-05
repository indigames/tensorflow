cmake_minimum_required(VERSION 3.4.1)
set(TARGET_NAME igeTFLite-static)

set (CMAKE_CXX_STANDARD 17)

project(${TARGET_NAME})

set (TENSORFLOW_DIR ${CMAKE_CURRENT_SOURCE_DIR})

# [IGE]: tweaks for platforms
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

# [IGE]: try include conan build config
if(EXISTS ${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
    include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
    conan_basic_setup()
endif()
# [/IGE]

set(PYTHON_INCLUDE_DIRS "${CONAN_INCLUDE_DIRS}")

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
)

add_library(${TARGET_NAME} STATIC ${SOURCES})
target_include_directories(${TARGET_NAME} PRIVATE ${INCLUDES})

add_subdirectory(${TENSORFLOW_DIR}/tensorflow/lite ${CMAKE_BINARY_DIR}/tensorflow-lite)
target_link_libraries(${TARGET_NAME} tensorflow-lite)
