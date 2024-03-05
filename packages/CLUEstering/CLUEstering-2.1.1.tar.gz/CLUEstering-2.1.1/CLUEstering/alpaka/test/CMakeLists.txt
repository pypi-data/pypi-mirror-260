cmake_minimum_required(VERSION 3.16.0)

project(convolutional_kernels_tests)

# Set the C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Set the C++ flags
string(APPEND CMAKE_CXX_FLAGS "-Wall -Wextra -g")

# Set the folder for the executable
# set(EXECUTABLE_OUTPUT_PATH ../)

include(FetchContent)
# Get doctest
FetchContent_Declare(doctest
  GIT_REPOSITORY https://github.com/doctest/doctest.git
  GIT_TAG 7b9885133108ae301ddd16e2651320f54cafeba7
)
FetchContent_GetProperties(doctest)
if(NOT doctest_POPULATED)
  FetchContent_Populate(doctest)
endif()

# add as executable all cc files
# to be used when adding new tests
# file(GLOB SOURCES "*.cc")

# Define the executable
# add_executable(tests.out ${SOURCES}) # to be used when adding new tests
add_executable(tests.out test_kernels.cc)
target_include_directories(test.out SYSTEM PRIVATE ${doctest_SOURCE_DIR}/doctest)
target_include_directories(tests.out PRIVATE ../)
