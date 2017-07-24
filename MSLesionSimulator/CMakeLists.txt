#-----------------------------------------------------------------------------
set(MODULE_NAME MSLesionSimulator)

#-----------------------------------------------------------------------------
set(MODULE_PYTHON_SCRIPTS
  ${MODULE_NAME}.py
  )

file(GLOB MSSimulator_50_100_DATA RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}" "Resources/MSlesion_database/labels-database/50-100/*.nii.gz")
file(GLOB MSSimulator_100_500_DATA RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}" "Resources/MSlesion_database/labels-database/100-500/*.nii.gz")
file(GLOB MSSimulator_500_1000_DATA RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}" "Resources/MSlesion_database/labels-database/500-1000/*.nii.gz")
file(GLOB MSSimulator_1000_5000_DATA RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}" "Resources/MSlesion_database/labels-database/1000-5000/*.nii.gz")
file(GLOB MSSimulator_5000_more_DATA RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}" "Resources/MSlesion_database/labels-database/5000-more/*.nii.gz")
file(GLOB MSSimulator_BrainTemplates_DATA RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}" "Resources/MSlesion_database/*.nii.gz")
set(MODULE_PYTHON_RESOURCES
  Resources/Icons/${MODULE_NAME}.png
  ${MSSimulator_50_100_DATA}
  ${MSSimulator_100_500_DATA}
  ${MSSimulator_500_1000_DATA}
  ${MSSimulator_1000_5000_DATA}
  ${MSSimulator_5000_more_DATA}
  ${MSSimulator_BrainTemplates_DATA}
  )

#-----------------------------------------------------------------------------
slicerMacroBuildScriptedModule(
  NAME ${MODULE_NAME}
  SCRIPTS ${MODULE_PYTHON_SCRIPTS}
  RESOURCES ${MODULE_PYTHON_RESOURCES}
  WITH_GENERIC_TESTS
  )

#-----------------------------------------------------------------------------
if(BUILD_TESTING)

  # Register the unittest subclass in the main script as a ctest.
  # Note that the test will also be available at runtime.
  slicer_add_python_unittest(SCRIPT ${MODULE_NAME}.py)

  # Additional build-time testing
  add_subdirectory(Testing)
endif()
