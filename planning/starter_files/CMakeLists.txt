project(MotionPlanning)

cmake_minimum_required (VERSION 3.10)

# -g allows for gdb debugging
# turn on -03 for best performance
add_definitions(-std=c++14 -O3)

set(CXX_FLAGS "-pthread -fPIC -DNDEBUG -Wall -Wextra")
set(CMAKE_CXX_FLAGS "${CXX_FLAGS} -Wl,-Bstatic -lboost_filesystem -Wl,-Bdynamic")

set(sources main.cpp behavior_planner_FSM.cpp motion_planner.cpp cubic_spiral.cpp spiral_base.cpp integral.cpp spiral_equations.cpp cost_functions.cpp utils.cpp velocity_profile_generator.cpp )

# Use includes and libs from CARLA_SOURCE_DIR.
set(CARLALIB_DIR ${CMAKE_SOURCE_DIR}/libcarla-install/lib)
# set(carla_libs  ${CARLALIB_DIR}/libboost_filesystem.a ${CARLALIB_DIR}/libboost_program_options.a ${CARLALIB_DIR}/libboost_python38.a ${CARLALIB_DIR}/libboost_system.a ${CARLALIB_DIR}/libcarla_client.a ${CARLALIB_DIR}/librpc.a ${CARLALIB_DIR}/libDebugUtils.a ${CARLALIB_DIR}/libDetour.a ${CARLALIB_DIR}/libDetourCrowd.a ${CARLALIB_DIR}/libDetourTileCache.a ${CARLALIB_DIR}/libRecast.a)

set(LIBUV_INCLUDE_DIR /usr/include/uv.h)   # Path to the uv.h directory
set(LIBUV_LIBRARY /usr/lib/x86_64-linux-gnu/libuv.so)  # Path to the libuv library

set(carla_libs ${CARLALIB_DIR}/libboost_filesystem.a ${CARLALIB_DIR}/libboost_program_options.a ${CARLALIB_DIR}/libboost_python38.a ${CARLALIB_DIR}/libboost_system.a ${CARLALIB_DIR}/libcarla_client.a ${CARLALIB_DIR}/librpc.a ${CARLALIB_DIR}/libDebugUtils.a ${CARLALIB_DIR}/libDetour.a ${CARLALIB_DIR}/libDetourCrowd.a ${CARLALIB_DIR}/libDetourTileCache.a ${CARLALIB_DIR}/libRecast.a)

include_directories(/usr/local/include)
link_directories(/usr/local/lib)

include_directories(eigen-3.3.7)

include_directories(libcarla-install/include)
include_directories(libcarla-install/include/system)
include_directories(rpclib/include)

link_directories(libcarla-install/lib)

if(${CMAKE_SYSTEM_NAME} MATCHES "Darwin")

endif(${CMAKE_SYSTEM_NAME} MATCHES "Darwin")

add_executable(spiral_planner ${sources} )

target_link_libraries(spiral_planner z ssl uv uWS ${carla_libs} gtest glog boost_filesystem lapack)
