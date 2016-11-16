
#-----------------------------------------------------------------------------

cmake_minimum_required( VERSION 2.6 )

set(MODULE_NAME GenerateLesions)

if(NOT Slicer_SOURCE_DIR)
  find_package(Slicer REQUIRED)
  include(${Slicer_USE_FILE})
endif()


#-----------------------------------------------------------------------------
SEMMacroBuildCLI(
  NAME ${MODULE_NAME}
  LOGO_HEADER ${Slicer_SOURCE_DIR}/Resources/ITKLogo.h
  ADDITIONAL_SRCS


  TARGET_LIBRARIES ${ITK_LIBRARIES}
  )

#add_subdirectory(Texture)

#-----------------------------------------------------------------------------
if(BUILD_TESTING)
  add_subdirectory(Testing)
endif()

