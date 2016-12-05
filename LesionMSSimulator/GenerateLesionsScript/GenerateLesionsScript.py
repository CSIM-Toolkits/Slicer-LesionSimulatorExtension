# Copyright 2016 Antonio Carlos da Silva Senra Filho and Fabricio Henrique Simozo
#
# Licensed under the Apache License, Version 2.0(the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http: // www.apache.org / licenses / LICENSE - 2.0
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

import os
import unittest
import sys
import platform
from os.path import expanduser
from user import home

import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging

#
# GenerateLesionsScript
#

class GenerateLesionsScript(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "Generate Lesions Script"
    self.parent.categories = ["MS Simulator"]
    self.parent.dependencies = []
    self.parent.contributors = ["Antonio Carlos da Silva Senra Filho (University of Sao Paulo), Fabricio Henrique Simozo (University of Sao Paulo)"]
    self.parent.helpText = """
    This scripted module is the main module for lesion simulation toolkit developed by the CSIM laboratory. Each subsection is specific for
    a certain lesion simulation pipeline. At moment, only Multiple Sclerosis lesions are available. More details, please visit the wikipage:
    https://www.slicer.org/wiki/Documentation/Nightly/Extensions/LesionSimulator
    """
    self.parent.acknowledgementText = """
    ...
""" # replace with organization, grant and thanks.

#
# GenerateLesionsScriptWidget
#

class GenerateLesionsScriptWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)

    # Instantiate and connect widgets ...

    #
    # Input Parameters Area
    #
    parametersInputCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersInputCollapsibleButton.text = "Input Parameters"
    self.layout.addWidget(parametersInputCollapsibleButton)

    # Layout within the dummy collapsible button
    parametersInputFormLayout = qt.QFormLayout(parametersInputCollapsibleButton)

    #
    # input T1 volume selector
    #
    self.inputT1Selector = slicer.qMRMLNodeComboBox()
    self.inputT1Selector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
    self.inputT1Selector.selectNodeUponCreation = True
    self.inputT1Selector.addEnabled = False
    self.inputT1Selector.removeEnabled = True
    self.inputT1Selector.noneEnabled = False
    self.inputT1Selector.showHidden = False
    self.inputT1Selector.showChildNodeTypes = False
    self.inputT1Selector.setMRMLScene(slicer.mrmlScene)
    self.inputT1Selector.setToolTip("A T1 weighted MRI image from a healthy individual.")
    parametersInputFormLayout.addRow("T1 Volume ", self.inputT1Selector)

    #
    # input T2 volume selector
    #
    self.inputT2Selector = slicer.qMRMLNodeComboBox()
    self.inputT2Selector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
    self.inputT2Selector.selectNodeUponCreation = False
    self.inputT2Selector.addEnabled = False
    self.inputT2Selector.removeEnabled = True
    self.inputT2Selector.noneEnabled = True
    self.inputT2Selector.showHidden = False
    self.inputT2Selector.showChildNodeTypes = False
    self.inputT2Selector.setMRMLScene(slicer.mrmlScene)
    self.inputT2Selector.setToolTip("A T2 weighted MRI image from a healthy individual.")
    parametersInputFormLayout.addRow("T2 Volume ", self.inputT2Selector)

    #
    # input FLAIR volume selector
    #
    self.inputFLAIRSelector = slicer.qMRMLNodeComboBox()
    self.inputFLAIRSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
    self.inputFLAIRSelector.selectNodeUponCreation = False
    self.inputFLAIRSelector.addEnabled = False
    self.inputFLAIRSelector.removeEnabled = True
    self.inputFLAIRSelector.noneEnabled = True
    self.inputFLAIRSelector.showHidden = False
    self.inputFLAIRSelector.showChildNodeTypes = False
    self.inputFLAIRSelector.setMRMLScene(slicer.mrmlScene)
    self.inputFLAIRSelector.setToolTip("A T2-FLAIR weighted MRI image from a healthy individual.")
    parametersInputFormLayout.addRow("T2-FLAIR Volume ", self.inputFLAIRSelector)

    #
    # input PD volume selector
    #
    self.inputPDSelector = slicer.qMRMLNodeComboBox()
    self.inputPDSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
    self.inputPDSelector.selectNodeUponCreation = False
    self.inputPDSelector.addEnabled = False
    self.inputPDSelector.removeEnabled = True
    self.inputPDSelector.noneEnabled = True
    self.inputPDSelector.showHidden = False
    self.inputPDSelector.showChildNodeTypes = False
    self.inputPDSelector.setMRMLScene(slicer.mrmlScene)
    self.inputPDSelector.setToolTip("A PD weighted MRI image from a healthy individual.")
    parametersInputFormLayout.addRow("PD Volume ", self.inputPDSelector)

    #
    # input DTI-FA volume selector
    #
    self.inputFASelector = slicer.qMRMLNodeComboBox()
    self.inputFASelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
    self.inputFASelector.selectNodeUponCreation = False
    self.inputFASelector.addEnabled = False
    self.inputFASelector.removeEnabled = True
    self.inputFASelector.noneEnabled = True
    self.inputFASelector.showHidden = False
    self.inputFASelector.showChildNodeTypes = False
    self.inputFASelector.setMRMLScene(slicer.mrmlScene)
    self.inputFASelector.setToolTip("A DTI-FA map from a healthy individual.")
    parametersInputFormLayout.addRow("DTI-FA Map ", self.inputFASelector)

    #
    # input DTI-ADC volume selector
    #
    self.inputADCSelector = slicer.qMRMLNodeComboBox()
    self.inputADCSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
    self.inputADCSelector.selectNodeUponCreation = False
    self.inputADCSelector.addEnabled = False
    self.inputADCSelector.removeEnabled = True
    self.inputADCSelector.noneEnabled = True
    self.inputADCSelector.showHidden = False
    self.inputADCSelector.showChildNodeTypes = False
    self.inputADCSelector.setMRMLScene(slicer.mrmlScene)
    self.inputADCSelector.setToolTip("A DTI-ADC map from a healthy individual.")
    parametersInputFormLayout.addRow("DTI-ADC Map ", self.inputADCSelector)

    #
    # output lesion label selector
    #
    self.outputLesionLabelSelector = slicer.qMRMLNodeComboBox()
    self.outputLesionLabelSelector.nodeTypes = ["vtkMRMLLabelMapVolumeNode"]
    self.outputLesionLabelSelector.selectNodeUponCreation = True
    self.outputLesionLabelSelector.addEnabled = True
    self.outputLesionLabelSelector.renameEnabled = True
    self.outputLesionLabelSelector.removeEnabled = True
    self.outputLesionLabelSelector.noneEnabled = True
    self.outputLesionLabelSelector.showHidden = False
    self.outputLesionLabelSelector.showChildNodeTypes = False
    self.outputLesionLabelSelector.setMRMLScene( slicer.mrmlScene )
    self.outputLesionLabelSelector.setToolTip( "Pick the output lesion label." )
    parametersInputFormLayout.addRow("Output Lesion Label ", self.outputLesionLabelSelector)

    #
    # Return inputs to original space
    #
    self.setReturnOriginalSpaceBooleanWidget = ctk.ctkCheckBox()
    self.setReturnOriginalSpaceBooleanWidget.setChecked(False)
    self.setReturnOriginalSpaceBooleanWidget.setToolTip(
      "Choose if you want to transform the final images to its original space. If not, all the input images will be in T1 space.")
    parametersInputFormLayout.addRow("Return output data in the original space",
                                      self.setReturnOriginalSpaceBooleanWidget)

    #
    # Is brain extracted?
    #
    self.setIsBETBooleanWidget = ctk.ctkCheckBox()
    self.setIsBETBooleanWidget.setChecked(False)
    self.setIsBETBooleanWidget.setToolTip(
      "Is the input data already brain extracted? This information is only used for MNI152 template, where it helps to the registration process.")
    parametersInputFormLayout.addRow("Is brain extraced?",
                                      self.setIsBETBooleanWidget)

    #
    # MS Lesion Simulation Parameters Area
    #
    parametersMSLesionSimulationCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersMSLesionSimulationCollapsibleButton.text = "MS Lesion Simulation Parameters"
    self.layout.addWidget(parametersMSLesionSimulationCollapsibleButton)

    # Layout within the dummy collapsible button
    parametersMSLesionSimulationFormLayout = qt.QFormLayout(parametersMSLesionSimulationCollapsibleButton)

    #
    # Lesion Load value
    #
    self.lesionLoadSliderWidget = ctk.ctkSliderWidget()
    self.lesionLoadSliderWidget.singleStep = 0.1
    self.lesionLoadSliderWidget.minimum = 5
    self.lesionLoadSliderWidget.maximum = 50
    self.lesionLoadSliderWidget.value = 10
    self.lesionLoadSliderWidget.setToolTip("Set the desired lesion load to be used for MS lesion generation.")
    parametersMSLesionSimulationFormLayout.addRow("Lesion Load", self.lesionLoadSliderWidget)

    #
    # Sigma
    #
    self.setLesionSigmaWidget = qt.QDoubleSpinBox()
    self.setLesionSigmaWidget.setMaximum(10)
    self.setLesionSigmaWidget.setMinimum(0.1)
    self.setLesionSigmaWidget.setSingleStep(0.01)
    self.setLesionSigmaWidget.setValue(1.0)
    self.setLesionSigmaWidget.setToolTip("Choose the Gaussian variance to be applied in the final lesion map. The scale is given in mm.")
    parametersMSLesionSimulationFormLayout.addRow("Sigma ", self.setLesionSigmaWidget)

    #
    # Homogeneity
    #
    self.setLesionHomogeneityWidget = qt.QDoubleSpinBox()
    self.setLesionHomogeneityWidget.setMaximum(10)
    self.setLesionHomogeneityWidget.setMinimum(0.1)
    self.setLesionHomogeneityWidget.setSingleStep(0.01)
    self.setLesionHomogeneityWidget.setValue(0.5)
    self.setLesionHomogeneityWidget.setToolTip("Choose the lesion homogeneity present in the lesion simulation. Lower values give a more heteorgenours lesion contrast. This parameter is related to a Gaussian variance given in mm.")
    parametersMSLesionSimulationFormLayout.addRow("Lesion Homogeneity ", self.setLesionHomogeneityWidget)

    #
    # Lesion Independent Variability
    #
    self.setLesionVariabilityWidget = qt.QDoubleSpinBox()
    self.setLesionVariabilityWidget.setMaximum(3)
    self.setLesionVariabilityWidget.setMinimum(0.1)
    self.setLesionVariabilityWidget.setSingleStep(0.01)
    self.setLesionVariabilityWidget.setValue(1.0)
    self.setLesionVariabilityWidget.setToolTip("Choose the lesion independent variability level that represents how distinct is each non-connected "
                                         "lesion regarding the voxel intensity gray level. This measure simulates the independent progression "
                                         "for each lesion, where a higher value indicates higher variability among lesions. The parameter is "
                                         "modulated by the normal standard deviation depending of the image type inserted.")
    parametersMSLesionSimulationFormLayout.addRow("Lesion Variability ", self.setLesionVariabilityWidget)

    #
    # Apply Button
    #
    self.applyButton = qt.QPushButton("Apply")
    self.applyButton.toolTip = "Run the algorithm."
    self.applyButton.enabled = True
    parametersInputFormLayout.addRow(self.applyButton)

    # connections
    self.applyButton.connect('clicked(bool)', self.onApplyButton)
    self.inputT1Selector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    # self.outputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)

    # Add vertical spacer
    self.layout.addStretch(1)

    # Refresh Apply button state
    self.onSelect()

  def cleanup(self):
    pass

  def onSelect(self):
    self.applyButton.enabled = self.inputT1Selector.currentNodeID != ""

  def onApplyButton(self):
    logic = GenerateLesionsScriptLogic()
    returnSpace = self.setReturnOriginalSpaceBooleanWidget.isChecked()
    isBET = self.setIsBETBooleanWidget.isChecked()
    lesionLoad = self.lesionLoadSliderWidget.value
    sigma = self.setLesionSigmaWidget.value
    homogeneity = self.setLesionHomogeneityWidget.value
    variability = self.setLesionVariabilityWidget.value
    logic.run(self.inputT1Selector.currentNode()
              , self.inputFLAIRSelector.currentNode()
              , self.inputT2Selector.currentNode()
              , self.inputPDSelector.currentNode()
              , self.inputFASelector.currentNode()
              , self.inputADCSelector.currentNode()
              , self.outputLesionLabelSelector.currentNode()
              , returnSpace
              , isBET
              , lesionLoad
              , sigma
              , homogeneity
              , variability)

#
# GenerateLesionsScriptLogic
#

class GenerateLesionsScriptLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def hasImageData(self,volumeNode):
    """This is an example logic method that
    returns true if the passed in volume
    node has valid image data
    """
    if not volumeNode:
      logging.debug('hasImageData failed: no volume node')
      return False
    if volumeNode.GetImageData() == None:
      logging.debug('hasImageData failed: no image data in volume node')
      return False
    return True


  def run(self, inputT1Volume, inputFLAIRVolume, inputT2Volume, inputPDVolume,
          inputFAVolume, inputADCVolume, outputLesionLabel, returnSpace, isBET,
          lesionLoad, sigma, homogeneity, variability):
    """
    Run the actual algorithm
    """


    logging.info('Processing started')
    slicer.util.showStatusMessage("Processing started")
    #
    # Data space normalization to T1 space
    #
    if inputT2Volume != None:
      slicer.util.showStatusMessage("Pre-processing: Conforming T2 volume to T1 space...")
      regT2toT1Transform = slicer.vtkMRMLLinearTransformNode()
      slicer.mrmlScene.AddNode(regT2toT1Transform)
      T2_t1 = slicer.vtkMRMLScalarVolumeNode()
      slicer.mrmlScene.AddNode(T2_t1)

      self.conformInputSpace(inputT1Volume, inputT2Volume, T2_t1, regT2toT1Transform)
    if inputFLAIRVolume != None:
      slicer.util.showStatusMessage("Pre-processing: Conforming T2-FLAIR volume to T1 space...")
      regFLAIRtoT1Transform = slicer.vtkMRMLLinearTransformNode()
      slicer.mrmlScene.AddNode(regFLAIRtoT1Transform)
      FLAIR_t1 = slicer.vtkMRMLScalarVolumeNode()
      slicer.mrmlScene.AddNode(FLAIR_t1)

      self.conformInputSpace(inputT1Volume, inputFLAIRVolume, FLAIR_t1, regFLAIRtoT1Transform)
    if inputPDVolume != None:
      slicer.util.showStatusMessage("Pre-processing: Conforming PD volume to T1 space...")
      regPDtoT1Transform = slicer.vtkMRMLLinearTransformNode()
      slicer.mrmlScene.AddNode(regPDtoT1Transform)
      PD_t1 = slicer.vtkMRMLScalarVolumeNode()
      slicer.mrmlScene.AddNode(PD_t1)

      self.conformInputSpace(inputT1Volume, inputPDVolume, PD_t1, regPDtoT1Transform)
    if inputFAVolume != None:
      slicer.util.showStatusMessage("Pre-processing: Conforming DTI-FA map to T1 space...")
      regFAtoT1Transform = slicer.vtkMRMLLinearTransformNode()
      slicer.mrmlScene.AddNode(regFAtoT1Transform)
      FA_t1 = slicer.vtkMRMLScalarVolumeNode()
      slicer.mrmlScene.AddNode(FA_t1)

      self.conformInputSpace(inputT1Volume, inputFAVolume, FA_t1, regFAtoT1Transform)
    if inputADCVolume != None:
      slicer.util.showStatusMessage("Pre-processing: Conforming DTI-ADC map to T1 space...")
      regADCtoT1Transform = slicer.vtkMRMLLinearTransformNode()
      slicer.mrmlScene.AddNode(regADCtoT1Transform)
      ADC_t1 = slicer.vtkMRMLScalarVolumeNode()
      slicer.mrmlScene.AddNode(ADC_t1)

      self.conformInputSpace(inputT1Volume, inputADCVolume, ADC_t1, regADCtoT1Transform)

    # Pre Pipeline: Get home and database path for module
    # from os.path import expanduser
    # userHome = expanduser("~")
    # databasePath = userHome+"/MSlesion_database"

    slicer.util.showStatusMessage("Step 1/5: Reading brain templates...")
    logging.info("Step 1/5: Reading brain templates...")
    if platform.system() is "Windows":
      home = expanduser("%userprofile%")
      databasePath = home + "\\MSlesion_database"
    else:
      home = expanduser("~")
      databasePath = home + "/MSlesion_database"


    #
    # Subject's White Matter mask estimative
    #
    slicer.util.showStatusMessage("Step 2/5: White matter estimative from subjects T1 image...")
    logging.info("Step 2/5: White matter estimative from subjects T1 image...")
    WMMask = slicer.vtkMRMLLabelMapVolumeNode()
    slicer.mrmlScene.AddNode(WMMask)
    self.doWhiteMatterMask(inputT1Volume,WMMask)

    #
    # Registration between Input Image and MNI Image Space
    #
    slicer.util.showStatusMessage("Step 3/5: MNI152 template to native space...")
    logging.info("Step 3/5: MNI152 template to native space...")
    if isBET:
      if platform.system() is "Windows":
        slicer.util.loadVolume(databasePath+"\\MNI152_T1_1mm_brain.nii.gz")
      else:
        slicer.util.loadVolume(databasePath + "/MNI152_T1_1mm_brain.nii.gz")
      MNINodeName = "MNI152_T1_1mm_brain"
      MNINode = slicer.util.getNode(MNINodeName)
    else:
      if platform.system() is "Windows":
        slicer.util.loadVolume(databasePath + "\\MNI152_T1_1mm.nii.gz")
      else:
        slicer.util.loadVolume(databasePath + "/MNI152_T1_1mm.nii.gz")
      MNINodeName = "MNI152_T1_1mm"
      MNINode = slicer.util.getNode(MNINodeName)

    MNI_t1 = slicer.vtkMRMLScalarVolumeNode()
    slicer.mrmlScene.AddNode(MNI_t1)
    regMNItoT1Transform = slicer.vtkMRMLBSplineTransformNode()
    slicer.mrmlScene.AddNode(regMNItoT1Transform)

    self.doNonLinearRegistration(inputT1Volume, MNINode, MNI_t1, regMNItoT1Transform)

    #
    # Find lesion mask using Probability Image, lesion labels and desired Lesion Load
    #
    slicer.util.showStatusMessage("Step 4/5: Simulating MS lesion map...")
    logging.info("Step 4/5: Simulating MS lesion map...")
    if outputLesionLabel != None:
      lesionMap = outputLesionLabel
    else:
      lesionMap = slicer.vtkMRMLLabelMapVolumeNode()
      slicer.mrmlScene.AddNode(lesionMap)
    if platform.system() is "Windows":
      slicer.util.loadVolume(databasePath + "\\USP-ICBM-MSpriors-46-1mm.nii.gz")
      probabilityNodeName = "USP-ICBM-MSpriors-46-1mm"
    else:
      slicer.util.loadVolume(databasePath+"/USP-ICBM-MSpriors-46-1mm.nii.gz")
      probabilityNodeName = "USP-ICBM-MSpriors-46-1mm"

    probabilityNode = slicer.util.getNode(probabilityNodeName)
    if platform.system() is "Windows":
      self.doGenerateMask(probabilityNode, lesionLoad, lesionMap, databasePath+"\\labels-database")
    else:
      self.doGenerateMask(probabilityNode, lesionLoad, lesionMap, databasePath + "/labels-database")


    # Transforming lesion map to native space
    self.applyRegistrationTransform(lesionMap,inputT1Volume,lesionMap,regMNItoT1Transform,False, True)

    # Removing wrong lesion location based on WM mask
    self.cutWrongLesions(lesionMap, WMMask,lesionMap)

    #
    # Generating lesions in each input image
    #
    slicer.util.showStatusMessage("Step 5/5: Applying lesion deformation on T1 volume...")
    logging.info("Step 5/5: Applying lesion deformation on T1 volume...")
    self.doSimulateLesions(inputT1Volume, "T1", lesionMap, inputT1Volume, sigma, homogeneity, variability)

    if inputFLAIRVolume != None:
      slicer.util.showStatusMessage("Step 5/5: Applying lesion deformation on T2-FLAIR volume...")
      logging.info("Step 5/5: Applying lesion deformation on T2-FLAIR volume...")
      self.doSimulateLesions(FLAIR_t1, "T2-FLAIR", lesionMap, inputFLAIRVolume, sigma, homogeneity, variability)
    if inputT2Volume != None:
      slicer.util.showStatusMessage("Step 5/5: Applying lesion deformation on T2 volume...")
      logging.info("Step 5/5: Applying lesion deformation on T2 volume...")
      self.doSimulateLesions(T2_t1, "T2", lesionMap, inputT2Volume, sigma, homogeneity, variability)
    if inputPDVolume != None:
      slicer.util.showStatusMessage("Step 5/5: Applying lesion deformation on PD volume...")
      logging.info("Step 5/5: Applying lesion deformation on PD volume...")
      self.doSimulateLesions(PD_t1, "PD", lesionMap, inputPDVolume, sigma, homogeneity, variability)
    if inputFAVolume != None:
      slicer.util.showStatusMessage("Step 5/5: Applying lesion deformation on DTI-FA map...")
      logging.info("Step 5/5: Applying lesion deformation on DTI-FA volume...")
      self.doSimulateLesions(FA_t1, "DTI-FA", lesionMap, inputFAVolume, sigma, homogeneity, variability)
    if inputADCVolume != None:
      slicer.util.showStatusMessage("Step 5/5: Applying lesion deformation on DTI-ADC map...")
      logging.info("Step 5/5: Applying lesion deformation on DTI-ADC volume...")
      self.doSimulateLesions(ADC_t1, "DTI-ADC", lesionMap, inputADCVolume, sigma, homogeneity, variability)

    #
    # Return inputs to its original space
    #
    if returnSpace:
      if inputT2Volume != None:
        slicer.util.showStatusMessage("post-processing: Returning T2 image space...")
        logging.info("post-processing: Returning T2 image space...")
        # T2 inverse transform
        self.applyRegistrationTransform(T2_t1,inputT2Volume,inputT2Volume,regT2toT1Transform,True,False)
      if inputFLAIRVolume != None:
        slicer.util.showStatusMessage("post-processing: Returning T2-FLAIR image space...")
        logging.info("post-processing: Returning T2-FLAIR image space...")
        # T2-FLAIR inverse transform
        self.applyRegistrationTransform(FLAIR_t1,inputFLAIRVolume,inputFLAIRVolume,regFLAIRtoT1Transform,True,False)
      if inputPDVolume != None:
        slicer.util.showStatusMessage("post-processing: Returning PD image space...")
        logging.info("post-processing: Returning PD image space...")
        # PD inverse transform
        self.applyRegistrationTransform(PD_t1, inputPDVolume, inputPDVolume, regPDtoT1Transform, True, False)
      if inputFAVolume != None:
        slicer.util.showStatusMessage("post-processing: Returning DTI-FA map space...")
        logging.info("post-processing: Returning DTI-FA image space...")
        # DTI-FA inverse transform
        self.applyRegistrationTransform(FA_t1, inputFAVolume, inputFAVolume, regFAtoT1Transform, True, False)
      if inputADCVolume != None:
        slicer.util.showStatusMessage("post-processing: Returning DTI-ADC map space...")
        logging.info("post-processing: Returning DTI-ADC image space...")
        # DTI-ADC inverse transform
        self.applyRegistrationTransform(ADC_t1, inputADCVolume, inputADCVolume, regADCtoT1Transform, True, False)


    # Removing unnecessary nodes
    slicer.mrmlScene.RemoveNode(MNI_t1)
    slicer.mrmlScene.RemoveNode(regMNItoT1Transform)
    slicer.mrmlScene.RemoveNode(probabilityNode)
    slicer.mrmlScene.RemoveNode(MNINode)
    slicer.mrmlScene.RemoveNode(WMMask)

    if outputLesionLabel == None:
      slicer.mrmlScene.RemoveNode(lesionMap)

    if inputFLAIRVolume != None:
      slicer.mrmlScene.RemoveNode(regT2toT1Transform)
      slicer.mrmlScene.RemoveNode(T2_t1)
    if inputT2Volume != None:
      slicer.mrmlScene.RemoveNode(regFLAIRtoT1Transform)
      slicer.mrmlScene.RemoveNode(FLAIR_t1)
    if inputPDVolume != None:
      slicer.mrmlScene.RemoveNode(regPDtoT1Transform)
      slicer.mrmlScene.RemoveNode(PD_t1)
    if inputFAVolume != None:
      slicer.mrmlScene.RemoveNode(regFAtoT1Transform)
      slicer.mrmlScene.RemoveNode(FA_t1)
    if inputADCVolume != None:
      slicer.mrmlScene.RemoveNode(regADCtoT1Transform)
      slicer.mrmlScene.RemoveNode(ADC_t1)

    slicer.util.showStatusMessage("Processing completed")
    logging.info('Processing completed')

    return True

  def doWhiteMatterMask(self, T1Volume, outputWMMask):
    # T1brain = slicer.vtkMRMLScalarVolumeNode()
    # slicer.mrmlScene.AddNode(T1brain)
    # betParams = {}
    # betParams["inputVolume"] = T1Volume.GetID()
    # betParams["outputVolume"] = T1brain.GetID()
    #
    # slicer.cli.run(slicer.modules.robexbrainextraction, None, betParams, wait_for_completion=True)

    #################################################################################################################
    #                                              Noise Attenuation                                                #
    #################################################################################################################
    inputSmoothVolume = slicer.vtkMRMLScalarVolumeNode()
    slicer.mrmlScene.AddNode(inputSmoothVolume)
    regParams = {}
    regParams["inputVolume"] = T1Volume.GetID()
    regParams["outputVolume"] = inputSmoothVolume.GetID()
    regParams["condutance"] = 10
    regParams["iterations"] = 5
    regParams["q"] = 1.2

    slicer.cli.run(slicer.modules.aadimagefilter, None, regParams, wait_for_completion=True)

    #################################################################################################################
    #                                             Bias Field Correction                                             #
    #################################################################################################################
    inputSmoothBiasVolume = slicer.vtkMRMLScalarVolumeNode()
    slicer.mrmlScene.AddNode(inputSmoothBiasVolume)
    regParams = {}
    regParams["inputImageName"] = inputSmoothVolume.GetID()
    regParams["outputImageName"] = inputSmoothBiasVolume.GetID()

    slicer.cli.run(slicer.modules.n4itkbiasfieldcorrection, None, regParams, wait_for_completion=True)

    #################################################################################################################
    #                                             Brain Tissue Segmentation                                         #
    #################################################################################################################
    regParams = {}
    regParams["inputVolume"] = inputSmoothBiasVolume.GetID()
    regParams["outputLabel"] = outputWMMask.GetID()
    regParams["imageModality"] = "T1"
    regParams["oneTissue"] = True
    regParams["typeTissue"] = "White Matter"

    slicer.cli.run(slicer.modules.basicbraintissues, None, regParams, wait_for_completion=True)

    #################################################################################################################
    #                                                 Label Smoothing                                               #
    #################################################################################################################
    regParams = {}
    regParams["labelToSmooth"] = 3
    regParams["gaussianSigma"] = 0.2
    regParams["inputVolume"] = outputWMMask.GetID()
    regParams["outputVolume"] = outputWMMask.GetID()

    slicer.cli.run(slicer.modules.labelmapsmoothing, None, regParams, wait_for_completion=True)

    # slicer.mrmlScene.RemoveNode(T1brain)
    slicer.mrmlScene.RemoveNode(inputSmoothVolume)
    slicer.mrmlScene.RemoveNode(inputSmoothBiasVolume)

  def conformInputSpace(self, fixedNode, movingNode, resultNode, transform):
    regParams = {}
    regParams["fixedVolume"] = fixedNode.GetID()
    regParams["movingVolume"] = movingNode.GetID()
    regParams["samplingPercentage"] = 0.002
    regParams["linearTransform"] = transform.GetID()
    regParams["outputVolume"] = resultNode.GetID()
    regParams["initializeTransformMode"] = "useMomentsAlign"
    regParams["useRigid"] = True
    regParams["useAffine"] = True

    slicer.cli.run(slicer.modules.brainsfit, None, regParams, wait_for_completion=True)

  def doNonLinearRegistration(self, fixedNode, movingNode, resultNode, transform):
    """
    Execute the BrainsFit registration
    :param fixedNode:
    :param movingNode:
    :param resultNode:
    :return:
    """
    regParams = {}
    regParams["fixedVolume"] = fixedNode.GetID()
    regParams["movingVolume"] = movingNode.GetID()
    regParams["samplingPercentage"] = 0.002
    regParams["splineGridSize"] = '3,3,3' # Coloquei um valor baixo para testar...
    regParams["outputVolume"] = resultNode.GetID()
    # regParams["linearTransform"] = transform.GetID()
    regParams["bsplineTransform"] = transform.GetID()
    regParams["initializeTransformMode"] = "useMomentsAlign"
    # regParams["histogramMatch"] = True
    regParams["useRigid"] = True
    regParams["useAffine"] = True
    regParams["useBSpline"] = True

    slicer.cli.run(slicer.modules.brainsfit, None, regParams, wait_for_completion=True)

  def doGenerateMask(self, probNode, lesionLoad, resultNode, databasePath):
    """
    Execute the GenerateMask CLI
    :param inputVolume:
    :param outputVolume:
    :param lesionLoad:
    :param databasePath:
    :return:
    """
    cliParams = {'inputVolume': probNode, 'outputVolume': resultNode.GetID(), 'lesionLoad': lesionLoad,
                 'databasePath': databasePath}
    return( slicer.cli.run(slicer.modules.generatemask, None, cliParams, wait_for_completion=True) )

  def cutWrongLesions(self,input1, input2, output):
    """
    Execute the Multiply Scalar Images CLI
    :param inputVolume1:
    :param inputVolume2:
    :param outputVolume:
    :param order:
    :return:
    """
    regParams = {}
    regParams["inputVolume1"] = input1.GetID()
    regParams["inputVolume2"] = input2.GetID()
    regParams["outputVolume"] = output.GetID()

    slicer.cli.run(slicer.modules.multiplyscalarvolumes, None, regParams, wait_for_completion=True)

  def doSimulateLesions(self, inputVolume, imageModality, lesionLabel, outputVolume, sigma, homogeneity, variability):
    """
    Execute the DeformImage CLI
    :param inputVolume:
    :param imageModality:
    :param lesionLabel:
    :param outputVolume:
    :param sigma:
    :param homogeneity:
    :param variability:
    :return:
    """
    params = {}
    params["inputVolume"] = inputVolume.GetID()
    params["imageModality"] = imageModality
    params["lesionLabel"] = lesionLabel.GetID()
    params["outputVolume"] = outputVolume.GetID()
    params["sigma"] = sigma
    params["homogeneity"] = homogeneity
    params["variability"] = variability

    slicer.cli.run(slicer.modules.deformimage, None, params, wait_for_completion=True)

  def applyRegistrationTransform(self, inputVolume, referenceVolume, outputVolume, warpTransform, doInverse, isLabelMap):
    """
    Execute the Resample Volume CLI
    :param inputVolume:
    :param referenceVolume:
    :param outputVolume:
    :param pixelType:
    :param warpTransform:
    :param inverseTransform:
    :param interpolationMode:
    :return:
    """
    params = {}
    params["inputVolume"] = inputVolume.GetID()
    params["referenceVolume"] = referenceVolume.GetID()
    params["outputVolume"] = outputVolume.GetID()
    params["warpTransform"] = warpTransform.GetID()
    params["inverseTransform"] = doInverse
    if isLabelMap:
      params["interpolationMode"] = "NearestNeighbor"
      params["pixelType"] = "binary"
    else:
      params["interpolationMode"] = "Linear"
      params["pixelType"] = "float"

    slicer.cli.run(slicer.modules.brainsresample, None, params, wait_for_completion=True)


class GenerateLesionsScriptTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_GenerateLesionsScript1()

  def test_GenerateLesionsScript1(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests should exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")
    #
    # first, get some data
    #
    import urllib
    downloads = (
        ('http://slicer.kitware.com/midas3/download?items=5767', 'FA.nrrd', slicer.util.loadVolume),
        )

    for url,name,loader in downloads:
      filePath = slicer.app.temporaryPath + '/' + name
      if not os.path.exists(filePath) or os.stat(filePath).st_size == 0:
        logging.info('Requesting download %s from %s...\n' % (name, url))
        urllib.urlretrieve(url, filePath)
      if loader:
        logging.info('Loading %s...' % (name,))
        loader(filePath)
    self.delayDisplay('Finished with download and loading')

    volumeNode = slicer.util.getNode(pattern="FA")
    logic = GenerateLesionsScriptLogic()
    self.assertTrue( logic.hasImageData(volumeNode) )
    self.delayDisplay('Test passed!')
