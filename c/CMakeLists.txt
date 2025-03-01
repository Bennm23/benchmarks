cmake_minimum_required(VERSION 3.22.0)

# set(CMAKE_C_FLAGS "-Wall -D__USE_POSIX199309")

project(main C)

add_executable(main main.c)

target_link_libraries(main rt)

