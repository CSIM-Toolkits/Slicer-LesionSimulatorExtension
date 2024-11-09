cmake_minimum_required(VERSION 2.8.9)

project(LesionSimulator)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "https://www.slicer.org/wiki/Documentation/Nightly/Extensions/LesionSimulator")
set(EXTENSION_CATEGORY "Simulation")
set(EXTENSION_CONTRIBUTORS "Antonio Carlos da Silva Senra Filho (University of Sao Paulo), Fabrício Henrique Simozo (University of Sao Paulo)")
set(EXTENSION_DESCRIPTION "This extension offer a set of tools for brain lesion simulation, based on MRI images. At moment, the modules MS Lesion Simulator and MS Longitudinal Lesion Simulator are available, where it can simulate both baseline scan lesion volumes (given a lesion load) and longitudinal image simulations, respectively. In summary, a statistical lesion database is generated based on a set of manual lesion mark-ups, being non-linearly registered to MNI152 space (isotropic 1mm of voxel resolution). Using a small set of parameters (lesion load, lesion homogeneity, lesion intensity indenpendence and lesion variability), it is possible to generate a broad range of MS lesions patterns in multimodal MRI imaging techniques (at moment, T1, T2, T2-FLAIR, PD, DTI-FA and DTI-ADC images are provided). For more details about this project, please see the original paper (DOI: ) and the wiki page.")
set(EXTENSION_ICONURL "https://raw.githubusercontent.com/CSIM-Toolkits/Slicer-LesionSimulatorExtension/refs/heads/main/LesionSimulator.png")
set(EXTENSION_SCREENSHOTURLS "
https://raw.githubusercontent.com/CSIM-Toolkits/Slicer-LesionSimulatorExtension/refs/heads/main/docs/assets/LesionLoad_2mL.png 
https://raw.githubusercontent.com/CSIM-Toolkits/Slicer-LesionSimulatorExtension/refs/heads/main/docs/assets/LesionLoad_5mL.png 
https://raw.githubusercontent.com/CSIM-Toolkits/Slicer-LesionSimulatorExtension/refs/heads/main/docs/assets/LesionLoad_40mL.png 
https://raw.githubusercontent.com/CSIM-Toolkits/Slicer-LesionSimulatorExtension/refs/heads/main/docs/assets/3DLesionsOverlay.png 
https://raw.githubusercontent.com/CSIM-Toolkits/Slicer-LesionSimulatorExtension/refs/heads/main/docs/assets/MNI152_orig.png 
https://raw.githubusercontent.com/CSIM-Toolkits/Slicer-LesionSimulatorExtension/refs/heads/main/docs/assets/MNI152_lesionload40mL.png 
https://raw.githubusercontent.com/CSIM-Toolkits/Slicer-LesionSimulatorExtension/refs/heads/main/docs/assets/MNI152_orig_sag.png 
https://raw.githubusercontent.com/CSIM-Toolkits/Slicer-LesionSimulatorExtension/refs/heads/main/docs/assets/MNI152_lesionload40mL_sag.png
")

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(MSLesionSimulator)
add_subdirectory(GenerateMask)
add_subdirectory(DeformImage)
add_subdirectory(FilterMask)
add_subdirectory(MSLongitudinalExams)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_CPACK})
