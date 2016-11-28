import os
import unittest
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
    self.parent.contributors = ["Antonio Carlos da Silva Senra Filho (CSIM - USP - RP), Fabricio Henrique Simozo (CSIM - USP - RP)"]
    self.parent.helpText = """
    This scripted module is the main module for MS artificial lesion generation.
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
    # Parameters Area
    #
    parametersCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersCollapsibleButton.text = "Parameters"
    self.layout.addWidget(parametersCollapsibleButton)

    # Layout within the dummy collapsible button
    parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)

    #
    # input volume selector
    #
    self.inputSelector = slicer.qMRMLNodeComboBox()
    self.inputSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
    self.inputSelector.selectNodeUponCreation = True
    self.inputSelector.addEnabled = False
    self.inputSelector.removeEnabled = False
    self.inputSelector.noneEnabled = False
    self.inputSelector.showHidden = False
    self.inputSelector.showChildNodeTypes = False
    self.inputSelector.setMRMLScene( slicer.mrmlScene )
    self.inputSelector.setToolTip( "Pick the input to the algorithm." )
    parametersFormLayout.addRow("Input Volume: ", self.inputSelector)

    #
    # output volume selector
    #
    self.outputSelector = slicer.qMRMLNodeComboBox()
    self.outputSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
    self.outputSelector.selectNodeUponCreation = True
    self.outputSelector.addEnabled = True
    self.outputSelector.removeEnabled = True
    self.outputSelector.noneEnabled = True
    self.outputSelector.showHidden = False
    self.outputSelector.showChildNodeTypes = False
    self.outputSelector.setMRMLScene( slicer.mrmlScene )
    self.outputSelector.setToolTip( "Pick the output to the algorithm." )
    parametersFormLayout.addRow("Output Volume: ", self.outputSelector)

    #
    # threshold value
    #
    self.lesionLoadSliderWidget = ctk.ctkSliderWidget()
    self.lesionLoadSliderWidget.singleStep = 1
    self.lesionLoadSliderWidget.minimum = 0
    self.lesionLoadSliderWidget.maximum = 100
    self.lesionLoadSliderWidget.value = 20
    self.lesionLoadSliderWidget.setToolTip("Set the desired lesion load to be used for MS lesion generation.")
    parametersFormLayout.addRow("Lesion load", self.lesionLoadSliderWidget)

    #
    # Apply Button
    #
    self.applyButton = qt.QPushButton("Apply")
    self.applyButton.toolTip = "Run the algorithm."
    self.applyButton.enabled = False
    parametersFormLayout.addRow(self.applyButton)

    # connections
    self.applyButton.connect('clicked(bool)', self.onApplyButton)
    self.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.outputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)

    # Add vertical spacer
    self.layout.addStretch(1)

    # Refresh Apply button state
    self.onSelect()

  def cleanup(self):
    pass

  def onSelect(self):
    self.applyButton.enabled = self.inputSelector.currentNode() and self.outputSelector.currentNode()

  def onApplyButton(self):
    logic = GenerateLesionsScriptLogic()
    lesionLoad = self.lesionLoadSliderWidget.value
    logic.run(self.inputSelector.currentNode(), self.outputSelector.currentNode(), lesionLoad)

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

  def isValidInputOutputData(self, inputVolumeNode, outputVolumeNode):
    """Validates if the output is not the same as input
    """
    if not inputVolumeNode:
      logging.debug('isValidInputOutputData failed: no input volume node defined')
      return False
    if not outputVolumeNode:
      logging.debug('isValidInputOutputData failed: no output volume node defined')
      return False
    if inputVolumeNode.GetID()==outputVolumeNode.GetID():
      logging.debug('isValidInputOutputData failed: input and output volume is the same. Create a new volume for output to avoid this error.')
      return False
    return True

  def run(self, inputVolume, outputVolume, lesionLoad):
    """
    Run the actual algorithm
    """

    if not self.isValidInputOutputData(inputVolume, outputVolume):
      slicer.util.errorDisplay('Input volume is the same as output volume. Choose a different output volume.')
      return False

    logging.info('Processing started')

    # Pre Pipeline: Get home and database path for module
    from os.path import expanduser
    userHome = expanduser("~")
    databasePath = userHome+"/MSlesion_database"

    # First Step: Registration between Input Image and MNI Image Space
    fixed = slicer.util.loadVolume(databasePath+"/MNI152_T1_1mm.nii.gz")
    fixedNodeName = "MNI152_T1_1mm"
    fixedNode = slicer.util.getNode(fixedNodeName)
    cliNode = self.doBrainsFit(fixedNode, inputVolume, inputVolume)

    # Second Step: Find lesion mask using Probability Image, lesion labels and desired Lesion Load
    probability = slicer.util.loadVolume(databasePath+"/USP-ICBM-MSpriors-46-1mm.nii.gz")
    probabilityNodeName = "USP-ICBM-MSpriors-46-1mm"
    probabilityNode = slicer.util.getNode(probabilityNodeName)
    cliNode1 = self.doGenerateMask(probabilityNode, lesionLoad, outputVolume, databasePath+"labels-database")

    logging.info('Processing completed')

    return True

  def doBrainsFit(self, fixedNode, movingNode, resultNode):
    """
    Execute the BrainsFit registration
    :param fixedNode:
    :param movingNode:
    :param resultNode:
    :return:
    """
    cliParams = {'fixedVolume': fixedNode, 'movingVolume': movingNode.GetID(), 'outputVolume': resultNode.GetID(),
                 'samplingPercentage': 0.002, 'useRigid': True, 'useBSpline': True}
    return( slicer.cli.run(slicer.modules.brainsfit, None, cliParams, wait_for_completion=True) )

  def doGenerateMask(self, probNode, lesionLoad, resultNode, databasePath):
    """
    Execute the BrainsFit registration
    :param fixedNode:
    :param movingNode:
    :param resultNode:
    :return:
    """
    cliParams = {'inputVolume': probNode, 'outputVolume': resultNode.GetID(), 'lesionLoad': lesionLoad,
                 'databasePath': databasePath}
    return( slicer.cli.run(slicer.modules.generatemask, None, cliParams, wait_for_completion=True) )


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
