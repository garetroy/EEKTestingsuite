# Install script for directory: /global/cscratch1/sd/groberts/VisitKNLRebuild/src/databases/EEK

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

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/2.13.0/linux-x86_64/plugins/databases/libIEEKDatabase.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/2.13.0/linux-x86_64/plugins/databases/libIEEKDatabase.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/2.13.0/linux-x86_64/plugins/databases/libIEEKDatabase.so"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/2.13.0/linux-x86_64/plugins/databases" TYPE SHARED_LIBRARY FILES "/global/cscratch1/sd/groberts/VisitKNLRebuild/src/plugins/databases/libIEEKDatabase.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/2.13.0/linux-x86_64/plugins/databases/libIEEKDatabase.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/2.13.0/linux-x86_64/plugins/databases/libIEEKDatabase.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/2.13.0/linux-x86_64/plugins/databases/libIEEKDatabase.so"
         OLD_RPATH "/global/cscratch1/sd/groberts/VisitKNLRebuild/src/lib/.:/global/homes/g/groberts/third_party/vtk/6.1.0/linux-x86_64_icc-17.0.2/lib:/global/cscratch1/sd/groberts/VisitKNLRebuild/src/lib:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/2.13.0/linux-x86_64/plugins/databases/libIEEKDatabase.so")
    endif()
  endif()
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/2.13.0/linux-x86_64/plugins/databases/libMEEKDatabase.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/2.13.0/linux-x86_64/plugins/databases/libMEEKDatabase.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/2.13.0/linux-x86_64/plugins/databases/libMEEKDatabase.so"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/2.13.0/linux-x86_64/plugins/databases" TYPE SHARED_LIBRARY FILES "/global/cscratch1/sd/groberts/VisitKNLRebuild/src/plugins/databases/libMEEKDatabase.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/2.13.0/linux-x86_64/plugins/databases/libMEEKDatabase.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/2.13.0/linux-x86_64/plugins/databases/libMEEKDatabase.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/2.13.0/linux-x86_64/plugins/databases/libMEEKDatabase.so"
         OLD_RPATH "/global/cscratch1/sd/groberts/VisitKNLRebuild/src/lib/.:/global/homes/g/groberts/third_party/vtk/6.1.0/linux-x86_64_icc-17.0.2/lib:/global/cscratch1/sd/groberts/VisitKNLRebuild/src/lib:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/2.13.0/linux-x86_64/plugins/databases/libMEEKDatabase.so")
    endif()
  endif()
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/2.13.0/linux-x86_64/plugins/databases/libEEEKDatabase_ser.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/2.13.0/linux-x86_64/plugins/databases/libEEEKDatabase_ser.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/2.13.0/linux-x86_64/plugins/databases/libEEEKDatabase_ser.so"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/2.13.0/linux-x86_64/plugins/databases" TYPE SHARED_LIBRARY FILES "/global/cscratch1/sd/groberts/VisitKNLRebuild/src/plugins/databases/libEEEKDatabase_ser.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/2.13.0/linux-x86_64/plugins/databases/libEEEKDatabase_ser.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/2.13.0/linux-x86_64/plugins/databases/libEEEKDatabase_ser.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/2.13.0/linux-x86_64/plugins/databases/libEEEKDatabase_ser.so"
         OLD_RPATH "/global/cscratch1/sd/groberts/VisitKNLRebuild/src/lib/.:/global/homes/g/groberts/third_party/vtk/6.1.0/linux-x86_64_icc-17.0.2/lib:/global/cscratch1/sd/groberts/VisitKNLRebuild/src/lib:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/2.13.0/linux-x86_64/plugins/databases/libEEEKDatabase_ser.so")
    endif()
  endif()
endif()

