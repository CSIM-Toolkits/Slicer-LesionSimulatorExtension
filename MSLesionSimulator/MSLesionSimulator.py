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
# MSLesionSimulator
#

class MSLesionSimulator(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "MS Lesion Simulator"
    self.parent.categories = ["Simulation"]
    self.parent.dependencies = []
    self.parent.contributors = ["Antonio Carlos da Silva Senra Filho (University of Sao Paulo), Fabricio Henrique Simozo (University of Sao Paulo)"]
    self.parent.helpText = """
    This scripted module is the main module for Multiple Sclerosis lesion simulation toolkit developed by the CSIM laboratory. More details, please visit the wikipage:
    https://www.slicer.org/wiki/Documentation/Nightly/Extensions/LesionSimulator
    """
    self.parent.acknowledgementText = """
    ...
""" # replace with organization, grant and thanks.

#
# MSLesionSimulatorWidget
#

class MSLesionSimulatorWidget(ScriptedLoadableModuleWidget):
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
    self.inputT1Selector.noneEnabled = True
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
    # Return inputs to original space
    #
    self.setReturnOriginalSpaceBooleanWidget = ctk.ctkCheckBox()
    self.setReturnOriginalSpaceBooleanWidget.setChecked(False)
    self.setReturnOriginalSpaceBooleanWidget.setToolTip(
      "Choose if you want to transform the final images to its original space. If not, all the input images will be in T1 space. NOTE: This choice only takes "
      "effect on the baseline MS lesion simulation, i.e. the longitudinal lesion simulation (if checked) will always return the data using the T1 space.")
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
    # Lesion Load value
    #
    self.lesionLoadSliderWidget = ctk.ctkSliderWidget()
    self.lesionLoadSliderWidget.singleStep = 1
    self.lesionLoadSliderWidget.minimum = 5
    self.lesionLoadSliderWidget.maximum = 50
    self.lesionLoadSliderWidget.value = 10
    self.lesionLoadSliderWidget.setToolTip("Set the desired lesion load to be used for MS lesion generation.")
    parametersInputFormLayout.addRow("Lesion Load", self.lesionLoadSliderWidget)

    #
    # MS Longitudinal Lesion Simulation Parameters Area
    #
    parametersMSLongitudinalLesionSimulationCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersMSLongitudinalLesionSimulationCollapsibleButton.text = "MS Longitudinal Lesion Simulation Parameters"
    self.layout.addWidget(parametersMSLongitudinalLesionSimulationCollapsibleButton)

    # Layout within the dummy collapsible button
    parametersMSLongitudinalLesionSimulationFormLayout = qt.QFormLayout(parametersMSLongitudinalLesionSimulationCollapsibleButton)

    #
    # Simulate follow-up?
    #
    self.setSimulateFollowUpBooleanWidget = ctk.ctkCheckBox()
    self.setSimulateFollowUpBooleanWidget.setChecked(False)
    self.setSimulateFollowUpBooleanWidget.setToolTip(
      "Simulate an additional longitudinal sequence (given the same input data)? If checked, the MS Lesion Simulator tool will recreate a sequence of exams with "
      "longitudinal MS lesion pattern.")
    parametersMSLongitudinalLesionSimulationFormLayout.addRow("Simulate Longitudinal Exams?",
                                      self.setSimulateFollowUpBooleanWidget)

    #
    # Follow-ups
    #
    self.followUpsSliderWidget = ctk.ctkSliderWidget()
    self.followUpsSliderWidget.singleStep = 1
    self.followUpsSliderWidget.minimum = 2
    self.followUpsSliderWidget.maximum = 6
    self.followUpsSliderWidget.value = 2
    self.followUpsSliderWidget.setToolTip("Set the desired number of follow-up acquisitions that will be simulated.")
    parametersMSLongitudinalLesionSimulationFormLayout.addRow("Follow-ups", self.followUpsSliderWidget)

    #
    # Balance: Hypointense to isointense lesions
    #
    self.setBalanceHypo2IsoWidget = qt.QSpinBox()
    self.setBalanceHypo2IsoWidget.setMaximum(100)
    self.setBalanceHypo2IsoWidget.setMinimum(1)
    self.setBalanceHypo2IsoWidget.setSingleStep(0.1)
    self.setBalanceHypo2IsoWidget.setValue(56)
    self.setBalanceHypo2IsoWidget.setToolTip(
      "Set the percentage of lesions that will change its original signal state along the follow-ups.")
    parametersMSLongitudinalLesionSimulationFormLayout.addRow("Changing Contrast Balance ", self.setBalanceHypo2IsoWidget)

    #
    # output follow-ups selector
    #
    self.outputFollowUpsSelector = ctk.ctkDirectoryButton()
    self.outputFollowUpsSelector.setToolTip("Output folder where follow-up image files will be saved.")
    if platform.system() is "Windows":
      home = expanduser("%userprofile%")
    else:
      home = expanduser("~")
    self.outputFollowUpsSelector.directory = home
    parametersMSLongitudinalLesionSimulationFormLayout.addRow("Output Follow-Up ", self.outputFollowUpsSelector)

    #
    # Advanced Parameters Area
    #
    parametersAdvancedParametersCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersAdvancedParametersCollapsibleButton.text = "Advanced Parameters"
    self.layout.addWidget(parametersAdvancedParametersCollapsibleButton)
    parametersAdvancedParametersCollapsibleButton.click()

    # Layout within the dummy collapsible button
    parametersAdvancedParametersFormLayout = qt.QFormLayout(parametersAdvancedParametersCollapsibleButton)

    #
    # White Matter Threshold
    #
    self.setWMThresholdWidget = qt.QDoubleSpinBox()
    self.setWMThresholdWidget.setMaximum(5)
    self.setWMThresholdWidget.setMinimum(0.1)
    self.setWMThresholdWidget.setSingleStep(0.01)
    self.setWMThresholdWidget.setValue(1.5)
    self.setWMThresholdWidget.setToolTip("Set the White Matter threshold used to refine the simulated lesion map. The simulation supose that the MS lesions"
                                         "belongs only in the White Matter space. This variable is related to the voxel intensity and the White Matter probability"
                                         " distribution (standard deviation).")
    parametersAdvancedParametersFormLayout.addRow("White Matter Threshold ", self.setWMThresholdWidget)

    #
    # Percentage Sampling Area
    #
    self.setPercSamplingQWidget = qt.QDoubleSpinBox()
    self.setPercSamplingQWidget.setDecimals(4)
    self.setPercSamplingQWidget.setMaximum(1)
    self.setPercSamplingQWidget.setMinimum(0.0001)
    self.setPercSamplingQWidget.setSingleStep(0.001)
    self.setPercSamplingQWidget.setValue(0.05)
    self.setPercSamplingQWidget.setToolTip("Percentage of voxel used in registration.")
    parametersAdvancedParametersFormLayout.addRow("Percentage Of Samples ", self.setPercSamplingQWidget)

    #
    # BSpline Grid
    #
    self.setBSplineGridWidget = qt.QLineEdit()
    self.setBSplineGridWidget.setText('5,5,5')
    self.setBSplineGridWidget.setToolTip("Set the BSpline grid for non linear structural adjustments.")
    parametersAdvancedParametersFormLayout.addRow("BSpline Grid ", self.setBSplineGridWidget)

    #
    # Initiation Method Area
    #
    self.setInitiationRegistrationBooleanWidget = ctk.ctkComboBox()
    self.setInitiationRegistrationBooleanWidget.addItem("useCenterOfHeadAlign")
    self.setInitiationRegistrationBooleanWidget.addItem("Off")
    self.setInitiationRegistrationBooleanWidget.addItem("useMomentsAlign")
    self.setInitiationRegistrationBooleanWidget.addItem("useGeometryAlign")
    self.setInitiationRegistrationBooleanWidget.setToolTip(
      "Initialization method used for the MNI152 registration.")
    parametersAdvancedParametersFormLayout.addRow("Initiation Method ", self.setInitiationRegistrationBooleanWidget)

    #
    # Apply Button
    #
    self.applyButton = qt.QPushButton("Apply")
    self.applyButton.toolTip = "Run the algorithm."
    self.applyButton.enabled = False
    parametersInputFormLayout.addRow(self.applyButton)

    # connections
    self.applyButton.connect('clicked(bool)', self.onApplyButton)
    self.inputT1Selector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.inputT2Selector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.inputFLAIRSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.inputPDSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)

    # Add vertical spacer
    self.layout.addStretch(1)

    # Refresh Apply button state
    self.onSelect()

  def cleanup(self):
    pass

  def onSelect(self):
    self.applyButton.enabled = self.inputT1Selector.currentNode()\
                               or self.inputT2Selector.currentNode()\
                               or self.inputFLAIRSelector.currentNode()\
                               or self.inputPDSelector.currentNode()

  def onApplyButton(self):
    logic = MSLesionSimulatorLogic()
    returnSpace = self.setReturnOriginalSpaceBooleanWidget.isChecked()
    isBET = self.setIsBETBooleanWidget.isChecked()
    lesionLoad = self.lesionLoadSliderWidget.value
    # sigma = self.setLesionSigmaWidget.value
    # variability = self.setLesionVariabilityWidget.value
    isLongitudinal = self.setSimulateFollowUpBooleanWidget.isChecked()
    numberFollowUp = self.followUpsSliderWidget.value
    balanceHI = self.setBalanceHypo2IsoWidget.value
    outputFolder = self.outputFollowUpsSelector.directory
    cutFraction = self.setWMThresholdWidget.value
    samplingPerc = self.setPercSamplingQWidget.value
    grid = self.setBSplineGridWidget.text
    initiationMethod = self.setInitiationRegistrationBooleanWidget.currentText
    logic.run(self.inputT1Selector.currentNode()
              , self.inputFLAIRSelector.currentNode()
              , self.inputT2Selector.currentNode()
              , self.inputPDSelector.currentNode()
              , self.inputFASelector.currentNode()
              , self.inputADCSelector.currentNode()
              , returnSpace
              , isBET
              , lesionLoad
              , isLongitudinal
              , numberFollowUp
              , balanceHI
              , outputFolder
              , cutFraction
              , samplingPerc
              , grid
              , initiationMethod)

#
# MSLesionSimulatorLogic
#

class MSLesionSimulatorLogic(ScriptedLoadableModuleLogic):
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
          inputFAVolume, inputADCVolume, returnSpace, isBET,
          lesionLoad, isLongitudinal, numberFollowUp, balanceHI, outputFolder,
          cutFraction, samplingPerc, grid, initiationMethod):
    """
    Run the actual algorithm
    """

    #
    # Defines reference image modality based on pre-defined order
    #

    if inputT1Volume is not None:
      referenceVolume = inputT1Volume
      logging.info('T1 volume found. Will be used as reference space.')
    elif inputT2Volume is not None:
      referenceVolume = inputT2Volume
      logging.info('T2 volume found. Will be used as reference space.')
    elif inputFLAIRVolume is not None:
      referenceVolume = inputFLAIRVolume
      logging.info('FLAIR volume found. Will be used as reference space.')
    elif inputPDVolume is not None:
      referenceVolume = inputPDVolume
      logging.info('PD volume found. Will be used as reference space.')
    else:
      logging.info('ERROR: At least one structural image should be provided. Aborting.')
      return False

    logging.info('Processing started')
    slicer.util.showStatusMessage("Processing started")
    #
    # Data space normalization to T1 space
    #
    volumesLogic = slicer.modules.volumes.logic()

    if inputT2Volume is not None and inputT2Volume is not referenceVolume:
      try:
        slicer.util.showStatusMessage("Pre-processing: Conforming T2 volume to reference space...")
        regT2toRefTransform = slicer.vtkMRMLLinearTransformNode()
        slicer.mrmlScene.AddNode(regT2toRefTransform)
        clonedT2Volume = volumesLogic.CloneVolume(slicer.mrmlScene, inputT2Volume, "Cloned T2")

        self.conformInputSpace(referenceVolume, inputT2Volume, inputT2Volume, regT2toRefTransform)
      except:
        logging.info("Exception caught when trying to conform T2 image to reference space.")
    if inputFLAIRVolume is not None and inputFLAIRVolume is not referenceVolume:
      try:
        slicer.util.showStatusMessage("Pre-processing: Conforming T2-FLAIR volume to reference space...")
        regFLAIRtoRefTransform = slicer.vtkMRMLLinearTransformNode()
        slicer.mrmlScene.AddNode(regFLAIRtoRefTransform)
        clonedFLAIRVolume = volumesLogic.CloneVolume(slicer.mrmlScene, inputFLAIRVolume, "Cloned FLAIR")

        self.conformInputSpace(referenceVolume, inputFLAIRVolume, inputFLAIRVolume, regFLAIRtoRefTransform)
      except:
        logging.info("Exception caught when trying to create node for T2-FLAIR image in reference space.")
    if inputPDVolume is not None and inputPDVolume is not referenceVolume:
      try:
        slicer.util.showStatusMessage("Pre-processing: Conforming PD volume to reference space...")
        regPDtoRefTransform = slicer.vtkMRMLLinearTransformNode()
        slicer.mrmlScene.AddNode(regPDtoRefTransform)
        clonedPDVolume = volumesLogic.CloneVolume(slicer.mrmlScene, inputPDVolume, "Cloned PD")

        self.conformInputSpace(referenceVolume, inputPDVolume, inputPDVolume, regPDtoRefTransform)
      except:
        logging.info("Exception caught when trying to create node for PD image in reference space.")
    if inputFAVolume is not None:
      try:
        slicer.util.showStatusMessage("Pre-processing: Conforming DTI-FA map to reference space...")
        regFAtoRefTransform = slicer.vtkMRMLLinearTransformNode()
        slicer.mrmlScene.AddNode(regFAtoRefTransform)
        clonedFAVolume = volumesLogic.CloneVolume(slicer.mrmlScene, inputFAVolume, "Cloned FA")

        self.conformInputSpace(referenceVolume, inputFAVolume, inputFAVolume, regFAtoRefTransform)
      except:
        logging.info("Exception caught when trying to create node for FA image in reference space.")
    if inputADCVolume is not None:
      try:
        slicer.util.showStatusMessage("Pre-processing: Conforming DTI-ADC map to reference space...")
        regADCtoRefTransform = slicer.vtkMRMLLinearTransformNode()
        slicer.mrmlScene.AddNode(regADCtoRefTransform)
        clonedADCVolume = volumesLogic.CloneVolume(slicer.mrmlScene, inputADCVolume, "Cloned ADC")

        self.conformInputSpace(referenceVolume, inputADCVolume, inputADCVolume, regADCtoRefTransform)
      except:
        logging.info("Exception caught when trying to create node for ADC image in reference space.")

    slicer.util.showStatusMessage("Step 1/4: Reading brain templates...")
    logging.info("Step 1/5: Reading brain templates...")

    modulePath = os.path.dirname(slicer.modules.mslesionsimulator.path)

    if platform.system() is "Windows":

      databasePath = modulePath + "\\Resources\\MSlesion_database"
    else:

      databasePath = modulePath + "/Resources/MSlesion_database"

    #
    # Registration between Input Image and MNI Image Space
    #
    slicer.util.showStatusMessage("Step 2/4: MNI152 template to native space...")
    logging.info("Step 3/5: MNI152 template to native space...")
    if isBET:
      if platform.system() is "Windows":
        (readSuccess, MNINode)=slicer.util.loadVolume(databasePath+"\\MNI152_T1_1mm_brain.nii.gz",{},True)
      else:
        (readSuccess,MNINode)=slicer.util.loadVolume(databasePath + "/MNI152_T1_1mm_brain.nii.gz",{},True)
    else:
      if platform.system() is "Windows":
        (readSuccess, MNINode)=slicer.util.loadVolume(databasePath + "\\MNI152_T1_1mm.nii.gz",{},True)
      else:
        (readSuccess, MNINode)=slicer.util.loadVolume(databasePath + "/MNI152_T1_1mm.nii.gz",{},True)

    MNI_ref = slicer.vtkMRMLScalarVolumeNode()
    slicer.mrmlScene.AddNode(MNI_ref)
    regMNItoRefTransform = slicer.vtkMRMLBSplineTransformNode()
    slicer.mrmlScene.AddNode(regMNItoRefTransform)

    self.doNonLinearRegistration(referenceVolume, MNINode, MNI_ref, regMNItoRefTransform, samplingPerc, grid, initiationMethod)

    #
    # Find lesion mask using Probability Image, lesion labels and desired Lesion Load
    #
    slicer.util.showStatusMessage("Step 3/4: Simulating MS lesion map...")
    logging.info("Step 4/5: Simulating MS lesion map...")

    lesionMap = slicer.vtkMRMLLabelMapVolumeNode()
    slicer.mrmlScene.AddNode(lesionMap)
    if platform.system() is "Windows":
      self.doGenerateMask(MNINode, lesionLoad, lesionMap, databasePath+"\\labels-database")
    else:
      self.doGenerateMask(MNINode, lesionLoad, lesionMap, databasePath + "/labels-database")


    # Transforming lesion map to native space

    # Get transform logic for hardening transforms
    transformLogic = slicer.vtkSlicerTransformLogic()

    self.applyRegistrationTransform(lesionMap,referenceVolume,lesionMap,regMNItoRefTransform,False, True)
    transformLogic.hardenTransform(lesionMap)

    # Filtering lesion map to minimize or exclude regions outside of WM
    if inputT1Volume is not None:
      # Lesion Map: T1
      lesionMapT1 = slicer.vtkMRMLLabelMapVolumeNode()
      slicer.mrmlScene.AddNode(lesionMapT1)
      lesionMapT1.SetName("T1_lesion_label")
      self.doFilterMask(inputT1Volume, lesionMap, lesionMapT1, cutFraction)

    if inputFLAIRVolume is not None:
      # Lesion Map: T2-FLAIR
      lesionMapFLAIR = slicer.vtkMRMLLabelMapVolumeNode()
      slicer.mrmlScene.AddNode(lesionMapFLAIR)
      lesionMapFLAIR.SetName("T2FLAIR_lesion_label")
      self.doFilterMask(inputFLAIRVolume, lesionMap, lesionMapFLAIR, cutFraction)

    if inputT2Volume is not None:
      # Lesion Map: T2
      lesionMapT2 = slicer.vtkMRMLLabelMapVolumeNode()
      slicer.mrmlScene.AddNode(lesionMapT2)
      lesionMapT2.SetName("T2_lesion_label")
      self.doFilterMask(inputT2Volume, lesionMap, lesionMapT2, cutFraction)

    if inputPDVolume is not None:
      # Lesion Map: PD
      lesionMapPD = slicer.vtkMRMLLabelMapVolumeNode()
      slicer.mrmlScene.AddNode(lesionMapPD)
      lesionMapPD.SetName("PD_lesion_label")
      self.doFilterMask(inputPDVolume, lesionMap, lesionMapPD, cutFraction)

    if inputFAVolume is not None:
      # Lesion Map: DTI-FA
      lesionMapFA = slicer.vtkMRMLLabelMapVolumeNode()
      slicer.mrmlScene.AddNode(lesionMapFA)
      lesionMapFA.SetName("FA_lesion_label")
      self.doFilterMask(inputFAVolume, lesionMap, lesionMapFA, cutFraction)

    if inputADCVolume is not None:
      # Lesion Map: DTI-FA
      lesionMapADC = slicer.vtkMRMLLabelMapVolumeNode()
      slicer.mrmlScene.AddNode(lesionMapADC)
      lesionMapADC.SetName("ADC_lesion_label")
      self.doFilterMask(inputADCVolume, lesionMap, lesionMapADC, cutFraction)


    #
    # Generating lesions in each input image
    #
    # List of parameters: Sigma
    Sigma= {}
    Sigma["T1"]=0.75
    Sigma["T2"]=0.75
    Sigma["PD"]=0.75
    Sigma["T2FLAIR"]=0.75
    Sigma["DTI-FA"]=1.5
    Sigma["DTI-ADC"]=1.3

    variability = 0.5

    if not isLongitudinal:
      if inputT1Volume is not None:
        try:
          slicer.util.showStatusMessage("Step 4/4: Applying lesion deformation on T1 volume...")
          logging.info("Step 5/5: Applying lesion deformation on T1 volume...")
          self.doSimulateLesions(inputT1Volume, "T1", lesionMapT1, inputT1Volume, Sigma["T1"], variability)
        except:
          logging.info("Exception caught when trying to apply lesion deformation in T1 volume.")
      if inputFLAIRVolume is not None:
        try:
          slicer.util.showStatusMessage("Step 4/4: Applying lesion deformation on T2-FLAIR volume...")
          logging.info("Step 5/5: Applying lesion deformation on T2-FLAIR volume...")
          self.doSimulateLesions(inputFLAIRVolume, "T2-FLAIR", lesionMapFLAIR, inputFLAIRVolume, Sigma["T2FLAIR"], variability)
        except:
          logging.info("Exception caught when trying to apply lesion deformation in T2-FLAIR volume.")
      if inputT2Volume is not None:
        try:
          slicer.util.showStatusMessage("Step 4/4: Applying lesion deformation on T2 volume...")
          logging.info("Step 5/5: Applying lesion deformation on T2 volume...")
          self.doSimulateLesions(inputT2Volume, "T2", lesionMapT2, inputT2Volume, Sigma["T2"], variability)
        except:
          logging.info("Exception caught when trying to apply lesion deformation in T2 volume.")
      if inputPDVolume is not None:
        try:
          slicer.util.showStatusMessage("Step 4/4: Applying lesion deformation on PD volume...")
          logging.info("Step 5/5: Applying lesion deformation on PD volume...")
          self.doSimulateLesions(inputPDVolume, "PD", lesionMapPD, inputPDVolume, Sigma["PD"], variability)
        except:
          logging.info("Exception caught when trying to apply lesion deformation in PD volume.")
      if inputFAVolume is not None:
        try:
          slicer.util.showStatusMessage("Step 4/4: Applying lesion deformation on DTI-FA map...")
          logging.info("Step 5/5: Applying lesion deformation on DTI-FA volume...")
          self.doSimulateLesions(inputFAVolume, "DTI-FA", lesionMapFA, inputFAVolume, Sigma["DTI-FA"], variability)
        except:
          logging.info("Exception caught when trying to apply lesion deformation in FA volume.")
      if inputADCVolume is not None:
        try:
          slicer.util.showStatusMessage("Step 4/4: Applying lesion deformation on DTI-ADC map...")
          logging.info("Step 5/5: Applying lesion deformation on DTI-ADC volume...")
          self.doSimulateLesions(inputADCVolume, "DTI-ADC", lesionMapADC, inputADCVolume, Sigma["DTI-ADC"], variability)
        except:
          logging.info("Exception caught when trying to apply lesion deformation in ADC volume.")
    else:
      #
      # Simulate Longitudinal Exams
      #
      if inputT1Volume is not None:
        try:
          slicer.util.showStatusMessage("Extra: Generating longitudinal lesion deformation on T1 volume...")
          logging.info("Extra: Generating longitudinal lesion deformation on T1 volume......")
          self.doLongitudinalExams(inputT1Volume, "T1", lesionMapT1, outputFolder, numberFollowUp, balanceHI, Sigma["T1"], variability)
        except:
          logging.info("Exception caught when trying to generate longitudinal lesion deformation in T1 volume.")
      if inputFLAIRVolume is not None:
        try:
          slicer.util.showStatusMessage("Extra: Generating longitudinal lesion deformation on T2-FLAIR volume...")
          logging.info("Extra: Generating longitudinal lesion deformation on T2-FLAIR volume......")
          self.doLongitudinalExams(inputFLAIRVolume, "T2-FLAIR", lesionMapFLAIR, outputFolder, numberFollowUp, balanceHI, Sigma["T2FLAIR"], variability)
        except:
          logging.info("Exception caught when trying to generate longitudinal lesion deformation in T2-FLAIR volume.")
      if inputT2Volume is not None:
        try:
          slicer.util.showStatusMessage("Extra: Generating longitudinal lesion deformation on T2 volume...")
          logging.info("Extra: Generating longitudinal lesion deformation on T2 volume...")
          self.doLongitudinalExams(inputT2Volume, "T2", lesionMapT2, outputFolder, numberFollowUp, balanceHI, Sigma["T2"], variability)
        except:
          logging.info("Exception caught when trying to generate longitudinal lesion deformation in T2 volume.")
      if inputPDVolume is not None:
        try:
          slicer.util.showStatusMessage("Extra: Generating longitudinal lesion deformation on PD volume...")
          logging.info("Extra: Generating longitudinal lesion deformation on PD volume...")
          self.doLongitudinalExams(inputPDVolume, "PD", lesionMapPD, outputFolder, numberFollowUp, balanceHI, Sigma["PD"], variability)
        except:
          logging.info("Exception caught when trying to generate longitudinal lesion deformation in PD volume.")
      if inputFAVolume is not None:
        try:
          slicer.util.showStatusMessage("Extra: Generating longitudinal lesion deformation on DTI-FA volume...")
          logging.info("Extra: Generating longitudinal lesion deformation on DTI-FA volume...")
          self.doLongitudinalExams(inputFAVolume, "DTI-FA", lesionMapFA, outputFolder, numberFollowUp, balanceHI, Sigma["DTI-FA"], variability)
        except:
          logging.info("Exception caught when trying to generate longitudinal lesion deformation in FA volume.")
      if inputADCVolume is not None:
        try:
          slicer.util.showStatusMessage("Extra: Generating longitudinal lesion deformation on DTI-ADC volume...")
          logging.info("Extra: Generating longitudinal lesion deformation on DTI-ADC volume...")
          self.doLongitudinalExams(inputADCVolume, "DTI-ADC", lesionMapADC, outputFolder, numberFollowUp, balanceHI, Sigma["DTI-ADC"], variability)
        except:
          logging.info("Exception caught when trying to generate longitudinal lesion deformation in ADC volume.")

    #
    # Return inputs to its original space
    #
    if returnSpace:
      if inputT2Volume is not None and inputT2Volume is not referenceVolume:
        try:
          slicer.util.showStatusMessage("post-processing: Returning T2 image space...")
          logging.info("post-processing: Returning T2 image space...")
          # T2 inverse transform
          self.applyRegistrationTransform(inputT2Volume,clonedT2Volume,inputT2Volume,regT2toRefTransform,True,False)
        except:
          logging.info("Exception caught when trying to return T2 image space.")
      if inputFLAIRVolume is not None and inputFLAIRVolume is not referenceVolume:
        try:
          slicer.util.showStatusMessage("post-processing: Returning T2-FLAIR image space...")
          logging.info("post-processing: Returning T2-FLAIR image space...")
          # T2-FLAIR inverse transform
          self.applyRegistrationTransform(inputFLAIRVolume,clonedFLAIRVolume,inputFLAIRVolume,regFLAIRtoRefTransform,True,False)
        except:
          logging.info("Exception caught when trying to return T2-FLAIR image space.")
      if inputPDVolume is not None and inputPDVolume is not referenceVolume:
        try:
          slicer.util.showStatusMessage("post-processing: Returning PD image space...")
          logging.info("post-processing: Returning PD image space...")
          # PD inverse transform
          self.applyRegistrationTransform(inputPDVolume, clonedPDVolume, inputPDVolume, regPDtoRefTransform, True, False)
        except:
          logging.info("Exception caught when trying to return PD image space.")
      if inputFAVolume is not None:
        try:
          slicer.util.showStatusMessage("post-processing: Returning DTI-FA map space...")
          logging.info("post-processing: Returning DTI-FA image space...")
          # DTI-FA inverse transform
          self.applyRegistrationTransform(inputFAVolume, clonedFAVolume, inputFAVolume, regFAtoRefTransform, True, False)
        except:
          logging.info("Exception caught when trying to return FA image space.")
      if inputADCVolume is not None:
        try:
          slicer.util.showStatusMessage("post-processing: Returning DTI-ADC map space...")
          logging.info("post-processing: Returning DTI-ADC image space...")
          # DTI-ADC inverse transform
          self.applyRegistrationTransform(inputADCVolume, clonedADCVolume, inputADCVolume, regADCtoRefTransform, True, False)
        except:
          logging.info("Exception caught when trying to return ADC image space.")

    # Removing unnecessary nodes
    slicer.mrmlScene.RemoveNode(MNI_ref)
    slicer.mrmlScene.RemoveNode(regMNItoRefTransform)
    slicer.mrmlScene.RemoveNode(MNINode)
    slicer.mrmlScene.RemoveNode(lesionMap)

    if inputFLAIRVolume is not None and inputFLAIRVolume is not referenceVolume:
      try:
        slicer.mrmlScene.RemoveNode(regFLAIRtoRefTransform)
        slicer.mrmlScene.RemoveNode(clonedFLAIRVolume)
      except:
        logging.info('Exception caught when trying to delete FLAIR in T1 space node.')
    if inputT2Volume is not None and inputT2Volume is not referenceVolume:
      try:
        slicer.mrmlScene.RemoveNode(regT2toRefTransform)
        slicer.mrmlScene.RemoveNode(clonedT2Volume)
      except:
        logging.info('Exception caught when trying to delete T2 in T1 space node.')
    if inputPDVolume is not None and inputPDVolume is not referenceVolume:
      try:
        slicer.mrmlScene.RemoveNode(regPDtoRefTransform)
        slicer.mrmlScene.RemoveNode(clonedPDVolume)
      except:
        logging.info('Exception caught when trying to delete PD in T1 space node.')
    if inputFAVolume is not None:
      try:
        slicer.mrmlScene.RemoveNode(regFAtoRefTransform)
        slicer.mrmlScene.RemoveNode(clonedFAVolume)
      except:
        logging.info('Exception caught when trying to delete FA in T1 space node.')
    if inputADCVolume is not None:
      try:
        slicer.mrmlScene.RemoveNode(regADCtoRefTransform)
        slicer.mrmlScene.RemoveNode(clonedADCVolume)
      except:
        logging.info('Exception caught when trying to delete ADC in T1 space node.')

    slicer.util.showStatusMessage("Processing completed")
    logging.info('Processing completed')

    return True


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

  def doNonLinearRegistration(self, fixedNode, movingNode, resultNode, transform, samplePerc, grid, initiationMethod):
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
    regParams["samplingPercentage"] = samplePerc
    regParams["splineGridSize"] = grid
    regParams["outputVolume"] = resultNode.GetID()
    # regParams["linearTransform"] = transform.GetID()
    regParams["bsplineTransform"] = transform.GetID()
    regParams["initializeTransformMode"] = initiationMethod
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

  def doFilterMask(self, inputVolume, inputMask, resultMask, cutFactor):
    """
    Execute the FilterMask CLI
    :param inputVolume:
    :param inputMask:
    :param resultMask:
    :return:
    """
    cliParams = {'inputVolume': inputVolume, 'inputMask': inputMask, 'outputVolume': resultMask, 'cutFactor': cutFactor}
    return( slicer.cli.run(slicer.modules.filtermask, None, cliParams, wait_for_completion=True) )

  def doSimulateLesions(self, inputVolume, imageModality, lesionLabel, outputVolume, sigma, variability):
    """
    Execute the DeformImage CLI
    :param inputVolume:
    :param imageModality:
    :param lesionLabel:
    :param outputVolume:
    :param sigma:
    :param variability:
    :return:
    """
    params = {}
    params["inputVolume"] = inputVolume.GetID()
    params["imageModality"] = imageModality
    params["lesionLabel"] = lesionLabel.GetID()
    params["outputVolume"] = outputVolume.GetID()
    params["sigma"] = sigma
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

  def doLongitudinalExams(self, inputVolume, imageModality, lesionLabel, outputFolder, numberFollowUp, balanceHI, sigma, variability):
    """
    Execute the SimulateLongitudinalLesions CLI
    :param inputVolume:
    :param imageModality:
    :param lesionLabel:
    :param numberFollowUp:
    :param balanceHI:
    :param outputFolder:
    :param variability:
    :param sigma:
    :return:
    """
    params = {}
    params["inputVolume"] = inputVolume.GetID()
    params["imageModality"] = imageModality
    params["lesionLabel"] = lesionLabel.GetID()
    params["numberFollowUp"] = numberFollowUp
    params["balanceHI"] = balanceHI
    params["outputFolder"] = outputFolder
    params["sigma"] = sigma
    params["variability"] = variability

    slicer.cli.run(slicer.modules.mslongitudinalexams, None, params, wait_for_completion=True)

class MSLesionSimulatorTest(ScriptedLoadableModuleTest):
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
    self.test_MSLesionSimulator1()

  def test_MSLesionSimulator1(self):
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
    logic = MSLesionSimulatorLogic()
    self.assertTrue( logic.hasImageData(volumeNode) )
    self.delayDisplay('Test passed!')
