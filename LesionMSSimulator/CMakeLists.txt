cmake_minimum_required(VERSION 2.8.9)

project(LesionMSSimulator)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "http://slicer.org/slicerWiki/index.php/Documentation/Nightly/Extensions/LesionMSSimulator")
set(EXTENSION_CATEGORY "MS Simulator")
set(EXTENSION_CONTRIBUTORS "Antonio Carlos da Silva Senra Filho (CSIM - USP - RP), Fabrício Henrique Simozo (CSIM - USP - RP)")
set(EXTENSION_DESCRIPTION "This extension creates artificial MS lesion on input image.")
set(EXTENSION_ICONURL "http://www.example.com/Slicer/Extensions/LesionMSSimulator.png")
set(EXTENSION_SCREENSHOTURLS "http://www.example.com/Slicer/Extensions/LesionMSSimulator/Screenshots/1.png")

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(GenerateLesionsScript)
add_subdirectory(GenerateMask)
add_subdirectory(DeformImage)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_CPACK})
