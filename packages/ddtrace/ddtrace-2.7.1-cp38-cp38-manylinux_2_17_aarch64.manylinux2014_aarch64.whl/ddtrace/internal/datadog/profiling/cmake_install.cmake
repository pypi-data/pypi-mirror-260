# Install script for directory: /project/ddtrace/internal/datadog/profiling/dd_wrapper

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "0")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/opt/rh/devtoolset-10/root/usr/bin/objdump")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}/project/ddtrace/internal/datadog/profiling/libdd_wrapper.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/project/ddtrace/internal/datadog/profiling/libdd_wrapper.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}/project/ddtrace/internal/datadog/profiling/libdd_wrapper.so"
         RPATH "")
  endif()
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/project/ddtrace/internal/datadog/profiling/libdd_wrapper.so")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  file(INSTALL DESTINATION "/project/ddtrace/internal/datadog/profiling" TYPE SHARED_LIBRARY FILES "/project/build/ddtrace.internal.datadog.profiling/libdd_wrapper.so")
  if(EXISTS "$ENV{DESTDIR}/project/ddtrace/internal/datadog/profiling/libdd_wrapper.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/project/ddtrace/internal/datadog/profiling/libdd_wrapper.so")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/opt/rh/devtoolset-10/root/usr/bin/strip" "$ENV{DESTDIR}/project/ddtrace/internal/datadog/profiling/libdd_wrapper.so")
    endif()
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
endif()

