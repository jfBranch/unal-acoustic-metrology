import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
import qrc_resources
import numpy as np
import acoustic_calibrations as ac
import ctypes

myappid = 'unal.acuscal.calibrators.1.0'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

__autor__ = 'Juan Felipe Maldonado'
__version__ = '1.0 Beta'


class AcousticCalibratorsUI(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        """
        Constructor method for create all the objects of the main window.
        """
        super().__init__(parent)
        self.centralWidget = QtWidgets.QWidget(self)
        self.centralWLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.tabWidget = QtWidgets.QTabWidget(self.centralWidget)
        self.standardsTab = QtWidgets.QWidget()
        self.gridLayout = QtWidgets.QGridLayout(self.standardsTab)
        self.saveStandardsInfo = QtWidgets.QPushButton(self.standardsTab)
        self.audioAnalyzerGroupBox = QtWidgets.QGroupBox(self.standardsTab)
        self.formLayout = QtWidgets.QFormLayout(self.audioAnalyzerGroupBox)
        self.analyzerBrandLabel = QtWidgets.QLabel(self.audioAnalyzerGroupBox)
        self.analyzerBrandLineEdit = QtWidgets.QLineEdit(self.audioAnalyzerGroupBox)
        self.analyzerModelLabel = QtWidgets.QLabel(self.audioAnalyzerGroupBox)
        self.analyzerModelLineEdit = QtWidgets.QLineEdit(self.audioAnalyzerGroupBox)
        self.analyzerSerialNumberLabel = QtWidgets.QLabel(self.audioAnalyzerGroupBox)
        self.analyzerSerialNumberLineEdit = QtWidgets.QLineEdit(self.audioAnalyzerGroupBox)
        self.analyzerIdentificationLabel = QtWidgets.QLabel(self.audioAnalyzerGroupBox)
        self.analyzerIdentificationLineEdit = QtWidgets.QLineEdit(self.audioAnalyzerGroupBox)
        self.analyzerGPIBBusLabel = QtWidgets.QLabel(self.audioAnalyzerGroupBox)
        self.analyzerGPIBBusLineEdit = QtWidgets.QLineEdit(self.audioAnalyzerGroupBox)
        self.analyzerGPIBChannelLabel = QtWidgets.QLabel(self.audioAnalyzerGroupBox)
        self.analyzerGPIBChannelComboBox = QtWidgets.QComboBox(self.audioAnalyzerGroupBox)
        self.analyzerSelfTestLabel = QtWidgets.QLabel(self.audioAnalyzerGroupBox)
        self.analyzerSelfTestCheckBox = QtWidgets.QCheckBox(self.audioAnalyzerGroupBox)
        self.micGroupBox = QtWidgets.QGroupBox(self.standardsTab)
        self.micGroupLayout = QtWidgets.QFormLayout(self.micGroupBox)
        self.micBrandLabel = QtWidgets.QLabel(self.micGroupBox)
        self.micBrandComboBox = QtWidgets.QComboBox(self.micGroupBox)
        self.micModelLabel = QtWidgets.QLabel(self.micGroupBox)
        self.micModelLineEdit = QtWidgets.QLineEdit(self.micGroupBox)
        self.micSerialNumberLabel = QtWidgets.QLabel(self.micGroupBox)
        self.micSerialNumberLineEdit = QtWidgets.QLineEdit(self.micGroupBox)
        self.micIdentificationLabel = QtWidgets.QLabel(self.micGroupBox)
        self.micIdentificationLineEdit = QtWidgets.QLineEdit(self.micGroupBox)
        self.micFreeFieldCorrectionLabel = QtWidgets.QLabel(self.micGroupBox)
        self.micFreeFieldCorrectionLineEdit = QtWidgets.QLineEdit(self.micGroupBox)
        self.multimeterGroupBox = QtWidgets.QGroupBox(self.standardsTab)
        self.multimeterGroupLayout = QtWidgets.QFormLayout(self.multimeterGroupBox)
        self.multimeterBrandLabel = QtWidgets.QLabel(self.multimeterGroupBox)
        self.multimeterBrandLineEdit = QtWidgets.QLineEdit(self.multimeterGroupBox)
        self.multimeterModelLabel = QtWidgets.QLabel(self.multimeterGroupBox)
        self.multimeterModelLineEdit = QtWidgets.QLineEdit(self.multimeterGroupBox)
        self.multimeterSerialNumberLabel = QtWidgets.QLabel(self.multimeterGroupBox)
        self.multimeterSerialNumberLineEdit = QtWidgets.QLineEdit(self.multimeterGroupBox)
        self.multimeterIdentificationLabel = QtWidgets.QLabel(self.multimeterGroupBox)
        self.multimeterIdentificationLineEdit = QtWidgets.QLineEdit(self.multimeterGroupBox)
        self.multimeterGPIBbusLabel = QtWidgets.QLabel(self.multimeterGroupBox)
        self.multimeterGPIBBusLineEdit = QtWidgets.QLineEdit(self.multimeterGroupBox)
        self.multimeterGPIBChannelLabel = QtWidgets.QLabel(self.multimeterGroupBox)
        self.multimeterGPIBChannelComboBox = QtWidgets.QComboBox(self.multimeterGroupBox)
        self.multimeterSelfTestLabel = QtWidgets.QLabel(self.multimeterGroupBox)
        self.multimeterSelfTestCheckBox = QtWidgets.QCheckBox(self.multimeterGroupBox)
        self.standardCalibratorGroupBox = QtWidgets.QGroupBox(self.standardsTab)
        self.standardGroupLayout = QtWidgets.QFormLayout(self.standardCalibratorGroupBox)
        self.standardBrandLabel = QtWidgets.QLabel(self.standardCalibratorGroupBox)
        self.standardModelLabel = QtWidgets.QLabel(self.standardCalibratorGroupBox)
        self.standardModelLineEdit = QtWidgets.QLineEdit(self.standardCalibratorGroupBox)
        self.standardSerialNumberLabel = QtWidgets.QLabel(self.standardCalibratorGroupBox)
        self.standardSerialNumberLineEdit = QtWidgets.QLineEdit(self.standardCalibratorGroupBox)
        self.standardIdentificationLabel = QtWidgets.QLabel(self.standardCalibratorGroupBox)
        self.standardIdentificationLineEdit = QtWidgets.QLineEdit(self.standardCalibratorGroupBox)
        self.standardClassLabel = QtWidgets.QLabel(self.standardCalibratorGroupBox)
        self.standardClassComboBox = QtWidgets.QComboBox(self.standardCalibratorGroupBox)
        self.standardAdaptorLabel = QtWidgets.QLabel(self.standardCalibratorGroupBox)
        self.standardAdaptorLineEdit = QtWidgets.QLineEdit(self.standardCalibratorGroupBox)
        self.standardLevelsLabel = QtWidgets.QLabel(self.standardCalibratorGroupBox)
        self.standardLevel94CheckBox = QtWidgets.QCheckBox(self.standardCalibratorGroupBox)
        self.standardLevel114CheckBox = QtWidgets.QCheckBox(self.standardCalibratorGroupBox)
        self.standardBrandComboBox = QtWidgets.QComboBox(self.standardCalibratorGroupBox)
        self.infoTab = QtWidgets.QWidget()
        self.infoTabLayout = QtWidgets.QGridLayout(self.infoTab)
        self.dutGroupBox = QtWidgets.QGroupBox(self.infoTab)
        self.dutGroupLayout = QtWidgets.QFormLayout(self.dutGroupBox)
        self.consecutiveLabel = QtWidgets.QLabel(self.dutGroupBox)
        self.consecutiveLineEdit = QtWidgets.QLineEdit(self.dutGroupBox)
        self.dutBrandLabel = QtWidgets.QLabel(self.dutGroupBox)
        self.dutBrandLineEdit = QtWidgets.QLineEdit(self.dutGroupBox)
        self.dutModelLabel = QtWidgets.QLabel(self.dutGroupBox)
        self.dutModelLineEdit = QtWidgets.QLineEdit(self.dutGroupBox)
        self.dutSerialNumberLabel = QtWidgets.QLabel(self.dutGroupBox)
        self.dutSerialNumberLineEdit = QtWidgets.QLineEdit(self.dutGroupBox)
        self.dutClassLabel = QtWidgets.QLabel(self.dutGroupBox)
        self.dutClassComboBox = QtWidgets.QComboBox(self.dutGroupBox)
        self.dutAdaptorLabel = QtWidgets.QLabel(self.dutGroupBox)
        self.dutAdaptorLineEdit = QtWidgets.QLineEdit(self.dutGroupBox)
        self.dutPressureCorrectionLabel = QtWidgets.QLabel(self.dutGroupBox)
        self.dutPressureCorrectionLineEdit = QtWidgets.QLineEdit(self.dutGroupBox)
        self.dutFreeFieldDifferenceLabel = QtWidgets.QLabel(self.dutGroupBox)
        self.dutFreeFieldDifferenceLineEdit = QtWidgets.QLineEdit(self.dutGroupBox)
        self.dutLevelsLabel = QtWidgets.QLabel(self.dutGroupBox)
        self.dutLevel94CheckBox = QtWidgets.QCheckBox(self.dutGroupBox)
        self.dutLevel114checkBox = QtWidgets.QCheckBox(self.dutGroupBox)
        self.dutIdentificationLabel = QtWidgets.QLabel(self.dutGroupBox)
        self.dutIdentificationLineEdit = QtWidgets.QLineEdit(self.dutGroupBox)
        self.customerGroupBox = QtWidgets.QGroupBox(self.infoTab)
        self.customerGroupLayout = QtWidgets.QFormLayout(self.customerGroupBox)
        self.customerNameLabel = QtWidgets.QLabel(self.customerGroupBox)
        self.customerNameLineEdit = QtWidgets.QLineEdit(self.customerGroupBox)
        self.addressLabel = QtWidgets.QLabel(self.customerGroupBox)
        self.addressLineEdit = QtWidgets.QLineEdit(self.customerGroupBox)
        self.cityLabel = QtWidgets.QLabel(self.customerGroupBox)
        self.cityLineEdit = QtWidgets.QLineEdit(self.customerGroupBox)
        self.countryLabel = QtWidgets.QLabel(self.customerGroupBox)
        self.countryLineEdit = QtWidgets.QLineEdit(self.customerGroupBox)
        self.postalCodeLabel = QtWidgets.QLabel(self.customerGroupBox)
        self.postalCodeLineEdit = QtWidgets.QLineEdit(self.customerGroupBox)
        self.contactNumberLabel = QtWidgets.QLabel(self.customerGroupBox)
        self.contactNumberLineEdit = QtWidgets.QLineEdit(self.customerGroupBox)
        self.saveDUTInfo = QtWidgets.QPushButton(self.infoTab)
        self.resultsTab = QtWidgets.QWidget()
        self.verticalLayout = QtWidgets.QVBoxLayout(self.resultsTab)
        self.levelsGroupBox = QtWidgets.QGroupBox(self.resultsTab)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.levelsGroupBox)
        self.level94radioButton = QtWidgets.QRadioButton(self.levelsGroupBox)
        self.level114radioButton = QtWidgets.QRadioButton(self.levelsGroupBox)
        self.instrumentTab = QtWidgets.QTabWidget(self.resultsTab)
        self.standardTab = QtWidgets.QWidget()
        self.standardTabLayout = QtWidgets.QGridLayout(self.standardTab)
        self.standard0ResultsLabel = QtWidgets.QLabel(self.standardTab)
        self.standard0ResultsTable = QtWidgets.QTableView(self.standardTab)
        self.standard120ResultsLabel = QtWidgets.QLabel(self.standardTab)
        self.standard120ResultsTable = QtWidgets.QTableView(self.standardTab)
        self.standard240ResultsLabel = QtWidgets.QLabel(self.standardTab)
        self.standard240ResultsTable = QtWidgets.QTableView(self.standardTab)
        self.standardAverageResultsLabel = QtWidgets.QLabel(self.standardTab)
        self.standardAverageResultsTable = QtWidgets.QTableView(self.standardTab)
        self.dutTab = QtWidgets.QWidget()
        self.dutTabLayout = QtWidgets.QGridLayout(self.dutTab)
        self.dut0ResultsLabel = QtWidgets.QLabel(self.dutTab)
        self.dut0ResultsTable = QtWidgets.QTableView(self.dutTab)
        self.dut120ResultsLabel = QtWidgets.QLabel(self.dutTab)
        self.dut120ResultsTable = QtWidgets.QTableView(self.dutTab)
        self.dut240ResultsLabel = QtWidgets.QLabel(self.dutTab)
        self.dut240ResultsTable = QtWidgets.QTableView(self.dutTab)
        self.dutAverageResultsLabel = QtWidgets.QLabel(self.dutTab)
        self.dutAverageResultsTable = QtWidgets.QTableView(self.dutTab)
        self.ambientConditionsTab = QtWidgets.QWidget()
        self.ambientTabLayout = QtWidgets.QVBoxLayout(self.ambientConditionsTab)
        self.meteorologicLabel = QtWidgets.QLabel(self.ambientConditionsTab)
        self.ambientTable = QtWidgets.QTableView(self.ambientConditionsTab)
        self.noiseLabel = QtWidgets.QLabel(self.ambientConditionsTab)
        self.standardNoiseLabel = QtWidgets.QLabel(self.ambientConditionsTab)
        self.standardNoiseTable = QtWidgets.QTableView(self.ambientConditionsTab)
        self.dutNoiseLabel = QtWidgets.QLabel(self.ambientConditionsTab)
        self.dutNoiseTable = QtWidgets.QTableView(self.ambientConditionsTab)
        self.generalStatusLayout = QtWidgets.QGridLayout()
        self.progressStatusLayout = QtWidgets.QVBoxLayout()
        self.measurementProgressLabel = QtWidgets.QLabel(self.centralWidget)
        self.measurementProgressBar = QtWidgets.QProgressBar(self.centralWidget)
        self.generalProgressLabel = QtWidgets.QLabel(self.centralWidget)
        self.generalProgressBar = QtWidgets.QProgressBar(self.centralWidget)
        self.stageLabel = QtWidgets.QLCDNumber(self.centralWidget)
        self.backStageToolButton = QtWidgets.QToolButton(self.centralWidget)
        self.advanceStageToolButton = QtWidgets.QToolButton(self.centralWidget)
        self.tokenLabel = QtWidgets.QLabel(self.centralWidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuCalibration = QtWidgets.QMenu(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.toolBar = QtWidgets.QToolBar(self)
        self.actionLoadCalibration = QtWidgets.QAction(self)
        self.actionSaveCalibration = QtWidgets.QAction(self)
        self.actionEmitCertificate = QtWidgets.QAction(self)
        self.actionSearchStandards = QtWidgets.QAction(self)
        self.actionStart = QtWidgets.QAction(self)
        self.actionPause = QtWidgets.QAction(self)
        self.actionRestart = QtWidgets.QAction(self)
        self.actionBackStage = QtWidgets.QAction(self)
        self.actionAdvanceStage = QtWidgets.QAction(self)
        self.actionSetStage = QtWidgets.QAction(self)
        self.actionSelfTest = QtWidgets.QAction(self)
        self.setup_ui()  # Calls method for setting up all printable objects of the main window

    def setup_ui(self) -> None:
        """
         This method sets up all the printable objects of the main window and basic GUI functionality.
        """
        self.setObjectName("MainWindow")
        self.setEnabled(True)
        self.resize(950, 700)
        self.setAutoFillBackground(False)
        self.setTabShape(QtWidgets.QTabWidget.Rounded)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/bruel4231.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.centralWidget.setObjectName("centralWidget")
        self.centralWLayout.setObjectName("centralWLayout")
        self.tabWidget.setObjectName("tabWidget")
        self.standardsTab.setObjectName("standardsTab")
        self.gridLayout.setObjectName("linearityGridLayout")
        self.saveStandardsInfo.setEnabled(True)
        self.saveStandardsInfo.setObjectName("saveStandardsInfo")
        self.gridLayout.addWidget(self.saveStandardsInfo, 1, 4, 1, 1)
        self.audioAnalyzerGroupBox.setObjectName("audioAnalyzerGroupBox")
        self.formLayout.setObjectName("formLayout")
        self.analyzerBrandLabel.setObjectName("analyzerBrandLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.analyzerBrandLabel)
        self.analyzerBrandLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.analyzerBrandLineEdit.setReadOnly(False)
        self.analyzerBrandLineEdit.setObjectName("analyzerBrandLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.analyzerBrandLineEdit)
        self.analyzerModelLabel.setObjectName("analyzerModelLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.analyzerModelLabel)
        self.analyzerModelLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.analyzerModelLineEdit.setReadOnly(False)
        self.analyzerModelLineEdit.setObjectName("analyzerModelLineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.analyzerModelLineEdit)
        self.analyzerSerialNumberLabel.setObjectName("analyzerSerialNumberLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.analyzerSerialNumberLabel)
        self.analyzerSerialNumberLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.analyzerSerialNumberLineEdit.setReadOnly(False)
        self.analyzerSerialNumberLineEdit.setObjectName("analyzerSerialNumberLineEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.analyzerSerialNumberLineEdit)
        self.analyzerIdentificationLabel.setObjectName("analyzerIdentificationLabel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.analyzerIdentificationLabel)
        self.analyzerIdentificationLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.analyzerIdentificationLineEdit.setReadOnly(False)
        self.analyzerIdentificationLineEdit.setObjectName("analyzerIdentificationLineEdit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.analyzerIdentificationLineEdit)
        self.analyzerGPIBBusLabel.setObjectName("analyzerGPIBBusLabel")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.analyzerGPIBBusLabel)
        self.analyzerGPIBBusLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.analyzerGPIBBusLineEdit.setReadOnly(False)
        self.analyzerGPIBBusLineEdit.setObjectName("analyzerGPIBBusLineEdit")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.analyzerGPIBBusLineEdit)
        self.analyzerGPIBChannelLabel.setObjectName("analyzerGPIBChannelLabel")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.analyzerGPIBChannelLabel)
        self.analyzerGPIBChannelComboBox.setEnabled(True)
        self.analyzerGPIBChannelComboBox.setObjectName("analyzerGPIBChannelComboBox")
        for i in range(23):
            self.analyzerGPIBChannelComboBox.addItem("")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.analyzerGPIBChannelComboBox)
        self.analyzerSelfTestLabel.setObjectName("analyzerSelfTestLabel")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.analyzerSelfTestLabel)
        self.analyzerSelfTestCheckBox.setEnabled(False)
        self.analyzerSelfTestCheckBox.setObjectName("analyzerSelfTestCheckBox")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.analyzerSelfTestCheckBox)
        self.gridLayout.addWidget(self.audioAnalyzerGroupBox, 0, 4, 1, 1)
        self.micGroupBox.setObjectName("micGroupBox")
        self.micGroupLayout.setObjectName("micGroupLayout")
        self.micBrandLabel.setObjectName("micBrandLabel")
        self.micGroupLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.micBrandLabel)
        self.micBrandComboBox.setObjectName("micBrandComboBox")
        self.micBrandComboBox.addItem("")
        self.micGroupLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.micBrandComboBox)
        self.micModelLabel.setObjectName("micModelLabel")
        self.micGroupLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.micModelLabel)
        self.micModelLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.micModelLineEdit.setReadOnly(False)
        self.micModelLineEdit.setObjectName("micModelLineEdit")
        self.micGroupLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.micModelLineEdit)
        self.micSerialNumberLabel.setObjectName("micSerialNumberLabel")
        self.micGroupLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.micSerialNumberLabel)
        self.micSerialNumberLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.micSerialNumberLineEdit.setReadOnly(False)
        self.micSerialNumberLineEdit.setObjectName("micSerialNumberLineEdit")
        self.micGroupLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.micSerialNumberLineEdit)
        self.micIdentificationLabel.setObjectName("micIdentificationLabel")
        self.micGroupLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.micIdentificationLabel)
        self.micIdentificationLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.micIdentificationLineEdit.setReadOnly(False)
        self.micIdentificationLineEdit.setObjectName("micIdentificationLineEdit")
        self.micGroupLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.micIdentificationLineEdit)
        self.micFreeFieldCorrectionLabel.setObjectName("micFreeFieldCorrectionLabel")
        self.micGroupLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.micFreeFieldCorrectionLabel)
        self.micFreeFieldCorrectionLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.micFreeFieldCorrectionLineEdit.setReadOnly(False)
        self.micFreeFieldCorrectionLineEdit.setObjectName("micFreeFieldCorrectionLineEdit")
        self.micGroupLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.micFreeFieldCorrectionLineEdit)
        self.gridLayout.addWidget(self.micGroupBox, 0, 1, 1, 1)
        self.multimeterGroupBox.setObjectName("multimeterGroupBox")
        self.multimeterGroupLayout.setObjectName("multimeterGroupLayout")
        self.multimeterBrandLabel.setObjectName("multimeterBrandLabel")
        self.multimeterGroupLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.multimeterBrandLabel)
        self.multimeterBrandLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.multimeterBrandLineEdit.setReadOnly(False)
        self.multimeterBrandLineEdit.setObjectName("multimeterBrandLineEdit")
        self.multimeterGroupLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.multimeterBrandLineEdit)
        self.multimeterModelLabel.setObjectName("multimeterModelLabel")
        self.multimeterGroupLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.multimeterModelLabel)
        self.multimeterModelLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.multimeterModelLineEdit.setReadOnly(False)
        self.multimeterModelLineEdit.setObjectName("multimeterModelLineEdit")
        self.multimeterGroupLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.multimeterModelLineEdit)
        self.multimeterSerialNumberLabel.setObjectName("multimeterSerialNumberLabel")
        self.multimeterGroupLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.multimeterSerialNumberLabel)
        self.multimeterSerialNumberLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.multimeterSerialNumberLineEdit.setReadOnly(False)
        self.multimeterSerialNumberLineEdit.setObjectName("multimeterSerialNumberLineEdit")
        self.multimeterGroupLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.multimeterSerialNumberLineEdit)
        self.multimeterIdentificationLabel.setObjectName("multimeterIdentificationLabel")
        self.multimeterGroupLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.multimeterIdentificationLabel)
        self.multimeterIdentificationLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.multimeterIdentificationLineEdit.setReadOnly(False)
        self.multimeterIdentificationLineEdit.setObjectName("multimeterIdentificationLineEdit")
        self.multimeterGroupLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.multimeterIdentificationLineEdit)
        self.multimeterGPIBbusLabel.setObjectName("multimeterGPIBbusLabel")
        self.multimeterGroupLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.multimeterGPIBbusLabel)
        self.multimeterGPIBBusLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.multimeterGPIBBusLineEdit.setReadOnly(False)
        self.multimeterGPIBBusLineEdit.setObjectName("multimeterGPIBBusLineEdit")
        self.multimeterGroupLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.multimeterGPIBBusLineEdit)
        self.multimeterGPIBChannelLabel.setObjectName("multimeterGPIBChannelLabel")
        self.multimeterGroupLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.multimeterGPIBChannelLabel)
        self.multimeterGPIBChannelComboBox.setEnabled(True)
        self.multimeterGPIBChannelComboBox.setObjectName("multimeterGPIBChannelComboBox")
        for i in range(23):
            self.multimeterGPIBChannelComboBox.addItem("")
        self.multimeterGroupLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.multimeterGPIBChannelComboBox)
        self.multimeterSelfTestLabel.setObjectName("multimeterSelfTestLabel")
        self.multimeterGroupLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.multimeterSelfTestLabel)
        self.multimeterSelfTestCheckBox.setEnabled(False)
        self.multimeterSelfTestCheckBox.setObjectName("multimeterSelfTestCheckBox")
        self.multimeterGroupLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.multimeterSelfTestCheckBox)
        self.gridLayout.addWidget(self.multimeterGroupBox, 0, 2, 1, 1)
        self.standardCalibratorGroupBox.setObjectName("standardCalibratorGroupBox")
        self.standardGroupLayout.setObjectName("standardGroupLayout")
        self.standardBrandLabel.setObjectName("standardBrandLabel")
        self.standardGroupLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.standardBrandLabel)
        self.standardModelLabel.setObjectName("standardModelLabel")
        self.standardGroupLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.standardModelLabel)
        self.standardModelLineEdit.setEnabled(True)
        self.standardModelLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.standardModelLineEdit.setReadOnly(False)
        self.standardModelLineEdit.setObjectName("standardModelLineEdit")
        self.standardGroupLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.standardModelLineEdit)
        self.standardSerialNumberLabel.setObjectName("standardSerialNumberLabel")
        self.standardGroupLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.standardSerialNumberLabel)
        self.standardSerialNumberLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.standardSerialNumberLineEdit.setReadOnly(False)
        self.standardSerialNumberLineEdit.setObjectName("standardSerialNumberLineEdit")
        self.standardGroupLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.standardSerialNumberLineEdit)
        self.standardIdentificationLabel.setObjectName("standardIdentificationLabel")
        self.standardGroupLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.standardIdentificationLabel)
        self.standardIdentificationLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.standardIdentificationLineEdit.setReadOnly(False)
        self.standardIdentificationLineEdit.setObjectName("standardIdentificationLineEdit")
        self.standardGroupLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.standardIdentificationLineEdit)
        self.standardClassLabel.setObjectName("standardClassLabel")
        self.standardGroupLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.standardClassLabel)
        self.standardClassComboBox.setEnabled(True)
        self.standardClassComboBox.setObjectName("standardClassComboBox")
        self.standardClassComboBox.addItem("")
        self.standardClassComboBox.addItem("")
        self.standardGroupLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.standardClassComboBox)
        self.standardAdaptorLabel.setObjectName("standardAdaptorLabel")
        self.standardGroupLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.standardAdaptorLabel)
        self.standardAdaptorLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.standardAdaptorLineEdit.setReadOnly(False)
        self.standardAdaptorLineEdit.setObjectName("standardAdaptorLineEdit")
        self.standardGroupLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.standardAdaptorLineEdit)
        self.standardLevelsLabel.setObjectName("standardLevelsLabel")
        self.standardGroupLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.standardLevelsLabel)
        self.standardLevel94CheckBox.setEnabled(True)
        self.standardLevel94CheckBox.setObjectName("standardLevel94CheckBox")
        self.standardGroupLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.standardLevel94CheckBox)
        self.standardLevel114CheckBox.setEnabled(True)
        self.standardLevel114CheckBox.setChecked(False)
        self.standardLevel114CheckBox.setObjectName("standardLevel114CheckBox")
        self.standardGroupLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.standardLevel114CheckBox)
        self.standardBrandComboBox.setObjectName("standardBrandComboBox")
        self.standardBrandComboBox.addItem("")
        self.standardBrandComboBox.addItem("")
        self.standardGroupLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.standardBrandComboBox)
        self.gridLayout.addWidget(self.standardCalibratorGroupBox, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 4, 1, 1)
        self.tabWidget.addTab(self.standardsTab, "")
        self.infoTab.setObjectName("infoTab")
        self.infoTabLayout.setObjectName("infoTabLayout")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.infoTabLayout.addItem(spacerItem1, 2, 0, 1, 1)
        self.dutGroupBox.setObjectName("dutGroupBox")
        self.dutGroupLayout.setObjectName("dutGroupLayout")
        self.consecutiveLabel.setObjectName("consecutiveLabel")
        self.dutGroupLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.consecutiveLabel)
        self.consecutiveLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.consecutiveLineEdit.setObjectName("consecutiveLineEdit")
        self.dutGroupLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.consecutiveLineEdit)
        self.dutBrandLabel.setObjectName("dutBrandLabel")
        self.dutGroupLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.dutBrandLabel)
        self.dutBrandLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.dutBrandLineEdit.setObjectName("dutBrandLineEdit")
        self.dutGroupLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.dutBrandLineEdit)
        self.dutModelLabel.setObjectName("dutModelLabel")
        self.dutGroupLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.dutModelLabel)
        self.dutModelLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.dutModelLineEdit.setObjectName("dutModelLineEdit")
        self.dutGroupLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.dutModelLineEdit)
        self.dutSerialNumberLabel.setObjectName("dutSerialNumberLabel")
        self.dutGroupLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.dutSerialNumberLabel)
        self.dutSerialNumberLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.dutSerialNumberLineEdit.setObjectName("dutSerialNumberLineEdit")
        self.dutGroupLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.dutSerialNumberLineEdit)
        self.dutIdentificationLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.dutIdentificationLabel.setObjectName("dutIdentificationLabel")
        self.dutGroupLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.dutIdentificationLabel)
        self.dutIdentificationLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.dutIdentificationLineEdit.setObjectName("dutIdentificationLineEdit")
        self.dutGroupLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.dutIdentificationLineEdit)
        self.dutClassLabel.setObjectName("dutClassLabel")
        self.dutGroupLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.dutClassLabel)
        self.dutClassComboBox.setObjectName("dutClassComboBox")
        self.dutClassComboBox.addItem("")
        self.dutClassComboBox.addItem("")
        self.dutGroupLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.dutClassComboBox)
        self.dutAdaptorLabel.setObjectName("dutAdaptorLabel")
        self.dutGroupLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.dutAdaptorLabel)
        self.dutAdaptorLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.dutAdaptorLineEdit.setObjectName("dutAdaptorLineEdit")
        self.dutGroupLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.dutAdaptorLineEdit)
        self.dutPressureCorrectionLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.dutPressureCorrectionLabel.setObjectName('dutPressureCorrectionLabel')
        self.dutGroupLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.dutPressureCorrectionLabel)
        self.dutPressureCorrectionLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.dutPressureCorrectionLineEdit.setObjectName('dutPressureCorrectionLineEdit')
        self.dutGroupLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.dutPressureCorrectionLineEdit)
        self.dutLevelsLabel.setObjectName("dutLevelsLabel")
        self.dutFreeFieldDifferenceLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.dutFreeFieldDifferenceLabel.setObjectName("dutFreeFieldDifferenceLabel")
        self.dutGroupLayout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.dutFreeFieldDifferenceLabel)
        self.dutFreeFieldDifferenceLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.dutFreeFieldDifferenceLineEdit.setObjectName("dutFreeFieldDifferenceLineEdite")
        self.dutGroupLayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.dutFreeFieldDifferenceLineEdit)
        self.dutGroupLayout.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.dutLevelsLabel)
        self.dutLevel94CheckBox.setChecked(True)
        self.dutLevel94CheckBox.setObjectName("dutLevel94CheckBox")
        self.dutGroupLayout.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.dutLevel94CheckBox)
        self.dutLevel114checkBox.setObjectName("dutLevel114checkBox")
        self.dutGroupLayout.setWidget(10, QtWidgets.QFormLayout.FieldRole, self.dutLevel114checkBox)
        self.infoTabLayout.addWidget(self.dutGroupBox, 0, 0, 1, 1, QtCore.Qt.AlignVCenter)
        self.customerGroupBox.setObjectName("customerGroupBox")
        self.customerGroupLayout.setObjectName("customerGroupLayout")
        self.customerNameLabel.setObjectName("customerNameLabel")
        self.customerGroupLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.customerNameLabel)
        self.customerNameLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.customerNameLineEdit.setObjectName("customerNameLineEdit")
        self.customerGroupLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.customerNameLineEdit)
        self.addressLabel.setObjectName("addressLabel")
        self.customerGroupLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.addressLabel)
        self.addressLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.addressLineEdit.setObjectName("addressLineEdit")
        self.customerGroupLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.addressLineEdit)
        self.cityLabel.setObjectName("cityLabel")
        self.customerGroupLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.cityLabel)
        self.cityLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.cityLineEdit.setObjectName("cityLineEdit")
        self.customerGroupLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.cityLineEdit)
        self.countryLabel.setObjectName("countryLabel")
        self.customerGroupLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.countryLabel)
        self.countryLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.countryLineEdit.setObjectName("countryLineEdit")
        self.customerGroupLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.countryLineEdit)
        self.postalCodeLabel.setObjectName("postalCodeLabel")
        self.customerGroupLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.postalCodeLabel)
        self.postalCodeLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.postalCodeLineEdit.setObjectName("postalCodeLineEdit")
        self.customerGroupLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.postalCodeLineEdit)
        self.contactNumberLabel.setObjectName("contactNumberLabel")
        self.customerGroupLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.contactNumberLabel)
        self.contactNumberLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.contactNumberLineEdit.setObjectName("contactNumberLineEdit")
        self.customerGroupLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.contactNumberLineEdit)
        self.infoTabLayout.addWidget(self.customerGroupBox, 0, 1, 1, 1)
        self.saveDUTInfo.setObjectName("saveDUTInfo")
        self.infoTabLayout.addWidget(self.saveDUTInfo, 1, 1, 1, 1)
        self.tabWidget.addTab(self.infoTab, "")
        self.tabWidget.addTab(self.resultsTab, "")
        self.resultsTab.setObjectName("resultsTab")
        self.resultsTab.setEnabled(False)
        self.verticalLayout.setObjectName("verticalLayout")
        self.levelsGroupBox.setObjectName("levelsGroupBox")
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.level94radioButton.setChecked(True)
        self.level94radioButton.setObjectName("level94radioButton")
        self.horizontalLayout.addWidget(self.level94radioButton)
        self.level114radioButton.setEnabled(False)
        self.level114radioButton.setObjectName("level114radioButton")
        self.horizontalLayout.addWidget(self.level114radioButton)
        self.verticalLayout.addWidget(self.levelsGroupBox)
        self.instrumentTab.setObjectName("instrumentTab")
        self.standardTab.setObjectName("standardTab")
        self.standardTabLayout.setObjectName("standardTabLayout")
        self.standard0ResultsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.standard0ResultsLabel.setObjectName("standard0ResultsLabel")
        self.standardTabLayout.addWidget(self.standard0ResultsLabel, 0, 1, 1, 1)
        self.standard120ResultsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.standard120ResultsLabel.setObjectName("standard120ResultsLabel")
        self.standardTabLayout.addWidget(self.standard120ResultsLabel, 0, 2, 1, 1)
        self.standard240ResultsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.standard240ResultsLabel.setObjectName("standard240ResultsLabel")
        self.standardTabLayout.addWidget(self.standard240ResultsLabel, 0, 3, 1, 1)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.standard0ResultsTable.setFont(font)
        self.standard0ResultsTable.setObjectName("standard0ResultsTable")
        self.standardTabLayout.addWidget(self.standard0ResultsTable, 1, 1, 1, 1)
        self.standard120ResultsTable.setFont(font)
        self.standard120ResultsTable.setObjectName("standard120ResultsTable")
        self.standardTabLayout.addWidget(self.standard120ResultsTable, 1, 2, 1, 1)
        self.standard240ResultsTable.setFont(font)
        self.standard240ResultsTable.setObjectName("standard240ResultsTable")
        self.standardTabLayout.addWidget(self.standard240ResultsTable, 1, 3, 1, 1)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.standardAverageResultsLabel.setFont(font)
        self.standardAverageResultsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.standardAverageResultsLabel.setObjectName("standardAverageResultsLabel")
        self.standardTabLayout.addWidget(self.standardAverageResultsLabel, 2, 1, 1, 3)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.standardAverageResultsTable.setFont(font)
        self.standardAverageResultsTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.standardAverageResultsTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.standardAverageResultsTable.setObjectName("standardAverageResulsTable")
        self.standardTabLayout.addWidget(self.standardAverageResultsTable, 3, 1, 1, 3)
        self.instrumentTab.addTab(self.standardTab, "")
        self.dutTab.setObjectName("dutTab")
        self.dutTabLayout.setObjectName("dutTabLayout")
        self.dut0ResultsLabel = QtWidgets.QLabel(self.dutTab)
        self.dut0ResultsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.dut0ResultsLabel.setObjectName("dut0ResultsLabel")
        self.dutTabLayout.addWidget(self.dut0ResultsLabel, 0, 1, 1, 1)
        self.dut120ResultsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.dut120ResultsLabel.setObjectName("dut120ResultsLabel")
        self.dutTabLayout.addWidget(self.dut120ResultsLabel, 0, 2, 1, 1)
        self.dut240ResultsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.dut240ResultsLabel.setObjectName("dut240ResultsLabel")
        self.dutTabLayout.addWidget(self.dut240ResultsLabel, 0, 3, 1, 1)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.dut0ResultsTable.setFont(font)
        self.dut0ResultsTable.setObjectName("dut0ResultsTable")
        self.dutTabLayout.addWidget(self.dut0ResultsTable, 1, 1, 1, 1)
        self.dut120ResultsTable.setFont(font)
        self.dut120ResultsTable.setObjectName("dut120ResultsTable")
        self.dutTabLayout.addWidget(self.dut120ResultsTable, 1, 2, 1, 1)
        self.dut240ResultsTable.setFont(font)
        self.dut240ResultsTable.setObjectName("dut240ResultsTable")
        self.dutTabLayout.addWidget(self.dut240ResultsTable, 1, 3, 1, 1)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.dutAverageResultsLabel.setFont(font)
        self.dutAverageResultsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.dutAverageResultsLabel.setObjectName("dutAverageResultsLabel")
        self.dutTabLayout.addWidget(self.dutAverageResultsLabel, 2, 1, 1, 3)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.dutAverageResultsTable.setFont(font)
        self.dutAverageResultsTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.dutAverageResultsTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.dutAverageResultsTable.setObjectName("dutAverageResultsTable")
        self.dutTabLayout.addWidget(self.dutAverageResultsTable, 3, 1, 1, 3)
        self.instrumentTab.addTab(self.dutTab, "")
        self.ambientConditionsTab.setObjectName("ambientConditionsTab")
        self.ambientTabLayout.setObjectName("ambientTabLayout")
        self.meteorologicLabel.setObjectName("meteorologicLabel")
        font = QtGui.QFont()
        font.setBold(True)
        self.meteorologicLabel.setFont(font)
        self.ambientTabLayout.addWidget(self.meteorologicLabel)
        self.ambientTable.setObjectName("ambientTable")
        self.ambientTabLayout.addWidget(self.ambientTable)
        self.noiseLabel.setObjectName("noiseLabel")
        self.noiseLabel.setFont(font)
        self.ambientTabLayout.addWidget(self.noiseLabel)
        self.standardNoiseLabel.setObjectName("standardNoiseLabel")
        self.ambientTabLayout.addWidget(self.standardNoiseLabel)
        self.standardNoiseTable.setObjectName("standardNoiseTable")
        self.standardNoiseTable.verticalHeader().setVisible(False)
        self.ambientTabLayout.addWidget(self.standardNoiseTable)
        self.dutNoiseLabel.setObjectName("dutNoiseLabel")
        self.ambientTabLayout.addWidget(self.dutNoiseLabel)
        self.dutNoiseTable.setObjectName("dutNoiseTable")
        self.dutNoiseTable.verticalHeader().setVisible(False)
        self.ambientTabLayout.addWidget(self.dutNoiseTable)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.ambientTabLayout.addItem(spacerItem2)
        self.instrumentTab.addTab(self.ambientConditionsTab, "")
        self.verticalLayout.addWidget(self.instrumentTab)
        self.centralWLayout.addWidget(self.tabWidget)
        self.generalStatusLayout.setObjectName("generalStatusLayout")
        self.progressStatusLayout.setObjectName("progressStatusLayout")
        font = QtGui.QFont()
        font.setPointSize(7)
        self.measurementProgressLabel.setFont(font)
        self.measurementProgressLabel.setObjectName("measurementProgressLabel")
        self.progressStatusLayout.addWidget(self.measurementProgressLabel)
        font = QtGui.QFont()
        font.setPointSize(6)
        self.measurementProgressBar.setFont(font)
        self.measurementProgressBar.setMaximum(100)
        self.measurementProgressBar.setProperty("value", 0)
        self.measurementProgressBar.setObjectName("measurementProgressBar")
        self.progressStatusLayout.addWidget(self.measurementProgressBar)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.generalProgressLabel.setFont(font)
        self.generalProgressLabel.setObjectName("generalProgressLabel")
        self.progressStatusLayout.addWidget(self.generalProgressLabel)
        font = QtGui.QFont()
        font.setPointSize(6)
        self.generalProgressBar.setFont(font)
        self.generalProgressBar.setMaximum(100)
        self.generalProgressBar.setProperty("value", 0)
        self.generalProgressBar.setObjectName("generalProgressBar")
        self.progressStatusLayout.addWidget(self.generalProgressBar)
        self.generalStatusLayout.addLayout(self.progressStatusLayout, 2, 3, 1, 1)
        self.stageLabel.setMinimumSize(QtCore.QSize(70, 40))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.stageLabel.setFont(font)
        self.stageLabel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.stageLabel.setLineWidth(0)
        self.stageLabel.setSmallDecimalPoint(False)
        self.stageLabel.setDigitCount(2)
        self.stageLabel.setMode(QtWidgets.QLCDNumber.Dec)
        self.stageLabel.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
        self.stageLabel.setProperty("value", 0.0)
        self.stageLabel.setProperty("intValue", 0)
        self.stageLabel.setObjectName("stageLabel")
        self.generalStatusLayout.addWidget(self.stageLabel, 2, 1, 1, 1)
        self.backStageToolButton.setArrowType(QtCore.Qt.LeftArrow)
        self.backStageToolButton.setObjectName("backStageToolButton")
        self.backStageToolButton.setEnabled(False)
        self.generalStatusLayout.addWidget(self.backStageToolButton, 2, 0, 1, 1)
        self.advanceStageToolButton.setArrowType(QtCore.Qt.RightArrow)
        self.advanceStageToolButton.setObjectName("advanceStageToolButton")
        self.advanceStageToolButton.setEnabled(False)
        self.generalStatusLayout.addWidget(self.advanceStageToolButton, 2, 2, 1, 1)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.tokenLabel.setFont(font)
        self.tokenLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.tokenLabel.setObjectName("tokenLabel")
        self.generalStatusLayout.addWidget(self.tokenLabel, 1, 1, 1, 1)
        self.centralWLayout.addLayout(self.generalStatusLayout)
        self.setCentralWidget(self.centralWidget)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile.setObjectName("menuFile")
        self.menuTools.setObjectName("menuTools")
        self.menuCalibration.setObjectName("menuCalibration")
        self.setMenuBar(self.menubar)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.toolBar.setObjectName("toolBar")
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.insertToolBarBreak(self.toolBar)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLoadCalibration.setIcon(icon)
        self.actionLoadCalibration.setObjectName("actionLoadCalibration")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSaveCalibration.setIcon(icon1)
        self.actionSaveCalibration.setObjectName("actionSaveCalibration")
        self.actionSaveCalibration.setEnabled(False)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/certificate.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionEmitCertificate.setIcon(icon2)
        self.actionEmitCertificate.setObjectName("actionEmitCertificate")
        self.actionEmitCertificate.setEnabled(False)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/searchInstruments.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSearchStandards.setIcon(icon3)
        self.actionSearchStandards.setObjectName("actionSearchStandards")
        self.actionSearchStandards.setEnabled(False)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionStart.setIcon(icon4)
        self.actionStart.setObjectName("actionStart")
        self.actionStart.setEnabled(False)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPause.setIcon(icon5)
        self.actionPause.setObjectName("actionPause")
        self.actionPause.setEnabled(False)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRestart.setIcon(icon6)
        self.actionRestart.setObjectName("actionRestart")
        self.actionRestart.setEnabled(False)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/back.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionBackStage.setIcon(icon7)
        self.actionBackStage.setObjectName("actionBackStage")
        self.actionBackStage.setEnabled(False)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icons/next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAdvanceStage.setIcon(icon8)
        self.actionAdvanceStage.setObjectName("actionAdvanceStage")
        self.actionAdvanceStage.setEnabled(False)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/icons/goTo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSetStage.setIcon(icon9)
        self.actionSetStage.setObjectName("actionSetStage")
        self.actionSetStage.setEnabled(False)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/icons/test.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSelfTest.setIcon(icon10)
        self.actionSelfTest.setObjectName("actionSelfTest")
        self.actionSelfTest.setEnabled(False)
        self.menuFile.addAction(self.actionLoadCalibration)
        self.menuFile.addAction(self.actionSaveCalibration)
        self.menuTools.addAction(self.actionSearchStandards)
        self.menuTools.addAction(self.actionSelfTest)
        self.menuTools.addAction(self.actionEmitCertificate)
        self.menuCalibration.addAction(self.actionStart)
        self.menuCalibration.addAction(self.actionPause)
        self.menuCalibration.addAction(self.actionRestart)
        self.menuCalibration.addAction(self.actionBackStage)
        self.menuCalibration.addAction(self.actionAdvanceStage)
        self.menuCalibration.addAction(self.actionSetStage)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuCalibration.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.toolBar.addAction(self.actionLoadCalibration)
        self.toolBar.addAction(self.actionSaveCalibration)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionSearchStandards)
        self.toolBar.addAction(self.actionSelfTest)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionBackStage)
        self.toolBar.addAction(self.actionStart)
        self.toolBar.addAction(self.actionPause)
        self.toolBar.addAction(self.actionAdvanceStage)
        self.toolBar.addAction(self.actionSetStage)
        self.toolBar.addAction(self.actionRestart)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionEmitCertificate)

        self.translate_ui()
        self.set_tap_order()
        self.tabWidget.setCurrentIndex(0)
        self.instrumentTab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)

        # Connecting signals
        self.multimeterModelLineEdit.returnPressed.connect(self.enable_search_standards)
        self.multimeterModelLineEdit.editingFinished.connect(self.enable_search_standards)
        self.analyzerModelLineEdit.returnPressed.connect(self.enable_search_standards)
        self.analyzerModelLineEdit.editingFinished.connect(self.enable_search_standards)

    def translate_ui(self) -> None:
        """
        This method sets the text of all printable objects of the main window.
        """
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Calibración de calibrador acústico"))
        self.saveStandardsInfo.setText(_translate("MainWindow", "Guardar"))
        self.audioAnalyzerGroupBox.setTitle(_translate("MainWindow", "ANALIZADOR DE AUDIO"))
        self.analyzerBrandLabel.setText(_translate("MainWindow", "Marca:"))
        self.analyzerModelLabel.setText(_translate("MainWindow", "Modelo:"))
        self.analyzerSerialNumberLabel.setText(_translate("MainWindow", "Número de serie:"))
        self.analyzerIdentificationLabel.setText(_translate("MainWindow", "Identificación:"))
        self.analyzerGPIBBusLabel.setText(_translate("MainWindow", "Bus GPIB:"))
        self.analyzerGPIBChannelLabel.setText(_translate("MainWindow", "Canal GPIB:"))
        for i in range(22):
            self.analyzerGPIBChannelComboBox.setItemText(i + 1, _translate("MainWindow", str(i + 1)))
        self.analyzerSelfTestLabel.setText(_translate("MainWindow", "Auto-verificación"))
        self.micGroupBox.setTitle(_translate("MainWindow", "MICRÓFONO"))
        self.micBrandLabel.setText(_translate("MainWindow", "Marca:"))
        self.micBrandComboBox.setItemText(0, _translate("MainWindow", "GRAS"))
        self.micModelLabel.setText(_translate("MainWindow", "Modelo:"))
        self.micSerialNumberLabel.setText(_translate("MainWindow", "Número de serie:"))
        self.micIdentificationLabel.setText(_translate("MainWindow", "Identificación:"))
        self.micFreeFieldCorrectionLabel.setText(_translate("MainWindow", "Corrección de campo libre:"))
        self.multimeterGroupBox.setTitle(_translate("MainWindow", "MULTÍMETRO"))
        self.multimeterBrandLabel.setText(_translate("MainWindow", "Marca:"))
        self.multimeterModelLabel.setText(_translate("MainWindow", "Modelo:"))
        self.multimeterSerialNumberLabel.setText(_translate("MainWindow", "Número de serie:"))
        self.multimeterIdentificationLabel.setText(_translate("MainWindow", "Identificación:"))
        self.multimeterGPIBbusLabel.setText(_translate("MainWindow", "Bus GPIB:"))
        self.multimeterGPIBChannelLabel.setText(_translate("MainWindow", "Canal GPIB:"))
        for i in range(22):
            self.multimeterGPIBChannelComboBox.setItemText(i + 1, _translate("MainWindow", str(i + 1)))
        self.multimeterSelfTestLabel.setText(_translate("MainWindow", "Auto-verificación"))
        self.standardCalibratorGroupBox.setTitle(_translate("MainWindow", "CALIBRADOR ACÚSTICO"))
        self.standardBrandLabel.setText(_translate("MainWindow", "Marca:"))
        self.standardModelLabel.setText(_translate("MainWindow", "Modelo:"))
        self.standardSerialNumberLabel.setText(_translate("MainWindow", "Número de serie:"))
        self.standardIdentificationLabel.setText(_translate("MainWindow", "Identificación:"))
        self.standardClassLabel.setText(_translate("MainWindow", "Clase:"))
        self.standardClassComboBox.setItemText(0, _translate("MainWindow", "1"))
        self.standardClassComboBox.setItemText(1, _translate("MainWindow", "2"))
        self.standardAdaptorLabel.setText(_translate("MainWindow", "Adaptador:"))
        self.standardLevelsLabel.setText(_translate("MainWindow", "Niveles:"))
        self.standardLevel94CheckBox.setText(_translate("MainWindow", "94 dB"))
        self.standardLevel114CheckBox.setText(_translate("MainWindow", "114 dB"))
        self.standardBrandComboBox.setItemText(0, _translate("MainWindow", "01dB"))
        self.standardBrandComboBox.setItemText(1, _translate("MainWindow", "Brüel & Kjær"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.standardsTab), _translate("MainWindow", "Patrones"))
        self.dutGroupBox.setTitle(_translate("MainWindow", "ÍTEM DE CALIBRACIÓN"))
        self.consecutiveLabel.setText(_translate("MainWindow", "Consecutivo:"))
        self.dutBrandLabel.setText(_translate("MainWindow", "Marca:"))
        self.dutModelLabel.setText(_translate("MainWindow", "Modelo:"))
        self.dutSerialNumberLabel.setText(_translate("MainWindow", "Número de serie:"))
        self.dutClassLabel.setText(_translate("MainWindow", "Clase:"))
        self.dutClassComboBox.setCurrentText(_translate("MainWindow", "1"))
        self.dutClassComboBox.setItemText(0, _translate("MainWindow", "1"))
        self.dutClassComboBox.setItemText(1, _translate("MainWindow", "2"))
        self.dutAdaptorLabel.setText(_translate("MainWindow", "Adaptador:"))
        self.dutPressureCorrectionLabel.setText(_translate("MainWindow", "Corrección por presión:"))
        self.dutFreeFieldDifferenceLabel.setText(_translate("MainWindow", "Diferencia en campo libre:"))
        self.dutLevelsLabel.setText(_translate("MainWindow", "Niveles:"))
        self.dutLevel94CheckBox.setText(_translate("MainWindow", "94 dB"))
        self.dutLevel114checkBox.setText(_translate("MainWindow", "114 dB"))
        self.dutIdentificationLabel.setText(_translate("MainWindow", "Identificación:"))
        self.customerGroupBox.setTitle(_translate("MainWindow", "CLIENTE"))
        self.customerNameLabel.setText(_translate("MainWindow", "Nombre:"))
        self.addressLabel.setText(_translate("MainWindow", "Dirección:"))
        self.cityLabel.setText(_translate("MainWindow", "Ciudad:"))
        self.countryLabel.setText(_translate("MainWindow", "País:"))
        self.postalCodeLabel.setText(_translate("MainWindow", "Código Postal:"))
        self.contactNumberLabel.setText(_translate("MainWindow", "Contacto:"))
        self.saveDUTInfo.setText(_translate("MainWindow", "Guardar"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.infoTab), _translate("MainWindow", "Información IBC"))
        self.levelsGroupBox.setTitle(_translate("MainWindow", "NIVELES"))
        self.level94radioButton.setText(_translate("MainWindow", "94 dB"))
        self.level114radioButton.setText(_translate("MainWindow", "114 dB"))
        self.standard0ResultsLabel.setText(_translate("MainWindow", "0°"))
        self.standard240ResultsLabel.setText(_translate("MainWindow", "240°"))
        self.standard120ResultsLabel.setText(_translate("MainWindow", "120°"))
        self.standardAverageResultsLabel.setText(_translate("MainWindow", "Promedios"))
        self.instrumentTab.setTabText(self.instrumentTab.indexOf(self.standardTab), _translate("MainWindow", "Patrón"))
        self.dut0ResultsLabel.setText(_translate("MainWindow", "0°"))
        self.dut120ResultsLabel.setText(_translate("MainWindow", "120°"))
        self.dut240ResultsLabel.setText(_translate("MainWindow", "240°"))
        self.dutAverageResultsLabel.setText(_translate("MainWindow", "Promedios"))
        self.instrumentTab.setTabText(self.instrumentTab.indexOf(self.dutTab), _translate("MainWindow", "IBC"))
        self.meteorologicLabel.setText(_translate("MainWindow", "Meteorología:"))
        self.noiseLabel.setText(_translate("MainWindow", "Ruido de fondo:"))
        self.standardNoiseLabel.setText(_translate("MainWindow", "Patrón:"))
        self.dutNoiseLabel.setText(_translate("MainWindow", "IBC:"))
        self.instrumentTab.setTabText(self.instrumentTab.indexOf(self.ambientConditionsTab),
                                      _translate("MainWindow", "Condiciones Ambientales"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.resultsTab), _translate("MainWindow", "Resultados"))
        self.measurementProgressLabel.setText(_translate("MainWindow", "Progreso de medición"))
        self.generalProgressLabel.setText(_translate("MainWindow", "Progreso general"))
        self.backStageToolButton.setText(_translate("MainWindow", "..."))
        self.advanceStageToolButton.setText(_translate("MainWindow", "..."))
        self.tokenLabel.setText(_translate("MainWindow", "TOKEN"))
        self.menuFile.setTitle(_translate("MainWindow", "Archivo"))
        self.menuTools.setTitle(_translate("MainWindow", "Herramientas"))
        self.menuCalibration.setTitle(_translate("MainWindow", "Calibración"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionLoadCalibration.setText(_translate("MainWindow", "Cargar calibración"))
        self.actionSaveCalibration.setText(_translate("MainWindow", "Guardar calibración"))
        self.actionEmitCertificate.setText(_translate("MainWindow", "Generar certificado de calibración"))
        self.actionSearchStandards.setText(_translate("MainWindow", "Buscar patrones"))
        self.actionStart.setText(_translate("MainWindow", "Iniciar"))
        self.actionPause.setText(_translate("MainWindow", "Pausar"))
        self.actionRestart.setText(_translate("MainWindow", "Reiniciar"))
        self.actionBackStage.setText(_translate("MainWindow", "Etapa anterior"))
        self.actionAdvanceStage.setText(_translate("MainWindow", "Etapa siguiente"))
        self.actionSetStage.setText(_translate("MainWindow", "Ir a la etapa"))
        self.actionSelfTest.setText(_translate("MainWindow", "Auto-verificar patrones"))

    def set_tap_order(self):
        # TODO: Definir el oren de Tab para los LineEdit de la GUI.
        pass

    def enable_search_standards(self) -> None:
        """
        Method for enabling the search standards action guarantying there is info to execute it.
        """
        if self.multimeterModelLineEdit.displayText() != "" and self.analyzerModelLineEdit.displayText() != "":
            self.actionSearchStandards.setEnabled(True)
        else:
            self.actionSearchStandards.setEnabled(False)


class GUIController(object):
    # Temporal preset acoustic standards
    __cal21 = ac.AcousticCalibrator('01dB', 'CAL21', '34565022', '6885620', 'BAC21', 1, np.array([[94, 1000]]), 0)
    __cal21.set_calibration_results(level_results=np.array([[93.99], [-0.01], [0.26]]),
                                    freq_results=np.array([[1003.03], [0.3], [0.21]]),
                                    thd_results=np.array([[1.42], ['-'], [0.27]]))
    __bruel4231 = ac.AcousticCalibrator('Brüel & Kjær', '4231', '3026575', '0100389124', 'UC0210', 1,
                                        nominal_values=np.array([[94, 1000], [114, 1000]]),
                                        pressure_influence=-0.04 / (50 - 101.3))
    __bruel4231.set_calibration_results(level_results=np.array([[94.00, 114.01], [0, 0.01], [0.09, 0.09]]),
                                        freq_results=np.array([[1000.01, 1000.01], [0.001, 0.001], [0.001, 0.001]]),
                                        thd_results=np.array([[0.33, 0.19], ['-', '-'], [0.25, 0.25]]))
    __gras40CE = {'Brand': 'GRAS', 'Model': '40CE', 'S/N': '233270', 'ID': '1520159', 'Correction': -0.212}

    def __init__(self, gui: QtWidgets.QMainWindow):
        self._gui = gui
        self._TESTER = ac.AcousticCalibratorsPeriodicTester()  # Instantiates the tester of acoustic calibrators (model)
        self.calibrationThread = QtCore.QThread()  # This is the thread that will run all the calibration tasks
        self.save_standards_state = 1  # Instance attribute to save the state of standards info saving button
        self.save_DUT_info_sate = 1  # Instance attribute to save the state of dut info saving button
        self.self_test_passed = False
        self.standard_calibrator = self.__bruel4231  # Default initialization of standard calibration
        self.DMM_info = {}
        self.AA_info = {}
        # Sets the temporal initial filling data
        self.fill_standard_calibrator_info()
        self.fill_mic_info()
        # This data frame stores temporally the real time emitted measurement values by the signal
        self.acquired_values = pd.DataFrame(columns=['V [mV]', 'SPL [dB]', 'f [Hz]', 'THD+N [%]'])
        self.standard_averaged_values = pd.DataFrame(data=np.nan * np.ones((4, 4)),
                                                     index=['V [mV]', 'SPL [dB]', 'f [Hz]', 'THD+N [%]'],
                                                     columns=['0°', '120°', '240°', 'TOTAL'])
        self.dut_averaged_values = pd.DataFrame(data=np.nan * np.ones((4, 4)),
                                                index=['V [mV]', 'SPL [dB]', 'f [Hz]', 'THD+N [%]'],
                                                columns=['0°', '120°', '240°', 'TOTAL'])
        self.searchStandardWorker = QtCore.QObject()  # This is the worker for searching standards
        self.searchStandardThread = QtCore.QThread()  # This is the parallel thread for searching standards
        self.selfTesterWorker = QtCore.QObject()  # This is the worker for self-testing
        self.selfTesterThread = QtCore.QThread()  # This is the parallel thread for self-testing
        self._connect_signals()

    def _connect_signals(self):
        """
        With this method the controller connect signals and slots for setting view objects and use the model.
        """
        self._gui.saveStandardsInfo.clicked.connect(self.save_standards_info)
        self._gui.saveDUTInfo.clicked.connect(self.save_dut_info)
        self._gui.actionSelfTest.triggered.connect(self.self_test)
        self._gui.standardBrandComboBox.currentIndexChanged.connect(self.fill_standard_calibrator_info)
        self._gui.actionSearchStandards.triggered.connect(self.search_standards)
        self._gui.actionStart.triggered.connect(self.start)
        self._gui.actionPause.triggered.connect(self.pause)

        self._TESTER.moveToThread(self.calibrationThread)
        self.calibrationThread.started.connect(self._TESTER.run_main_sequence)
        self._TESTER.measurementProgress.connect(self._gui.measurementProgressBar.setValue)
        self._TESTER.calibrationProgress.connect(lambda x: self._gui.generalProgressBar.setValue(int(x / 19 * 100)))
        self._TESTER.calibrationProgress.connect(self.sequence_control)
        self._TESTER.calibrationProgress.connect(self._gui.stageLabel.display)
        self._TESTER.calibrationProgress.connect(self.calibrationThread.quit)
        self._TESTER.invalidMeasurementValue.connect(self.invalid_measurement)
        self._TESTER.invalidMeasurementValue.connect(self.calibrationThread.quit)
        self._TESTER.calibrationProgress.connect(self.update_noise_values)
        self._TESTER.realTimeValues.connect(self.update_real_time_values)

    def fill_mic_info(self) -> None:
        """
        Temporal method for filling information of the reference microphone.
        """
        self._gui.micModelLineEdit.setText(self.__gras40CE['Model'])
        self._gui.micSerialNumberLineEdit.setText(self.__gras40CE['S/N'])
        self._gui.micIdentificationLineEdit.setText(self.__gras40CE['ID'])
        self._gui.micFreeFieldCorrectionLineEdit.setText(str(self.__gras40CE['Correction']))

    def fill_standard_calibrator_info(self) -> None:
        """
        Temporal method for filling information of the standard calibrator depending on the selected item of ComboBox.
        :return: None
        """
        if self._gui.standardBrandComboBox.currentIndex() == 0:
            self.standard_calibrator = self.__cal21
        else:
            self.standard_calibrator = self.__bruel4231

        self._gui.standardModelLineEdit.setText(self.standard_calibrator.info['Model'])
        self._gui.standardSerialNumberLineEdit.setText(self.standard_calibrator.info['S/N'])
        self._gui.standardIdentificationLineEdit.setText(self.standard_calibrator.info['ID'])
        self._gui.standardClassComboBox.setCurrentIndex(self.standard_calibrator.cl - 1)
        self._gui.standardAdaptorLineEdit.setText(self.standard_calibrator.info['Adaptor'])
        levels = self.standard_calibrator.nominal_values.drop_duplicates(subset='Level')
        self._gui.standardLevel94CheckBox.setChecked(
            True) if 94 in levels.values else self._gui.standardLevel94CheckBox.setChecked(False)
        self._gui.standardLevel114CheckBox.setChecked(
            True) if 114 in levels.values else self._gui.standardLevel114CheckBox.setChecked(False)

    def save_standards_info(self) -> None:
        """
        Method that catch the standards information and save that in the TESTER object.
        Also enables and disables the corresponding objects and actions.
        """
        self.DMM_info = {'Brand': self._gui.multimeterBrandLineEdit.displayText(),
                         'Model': self._gui.multimeterModelLineEdit.displayText(),
                         'S/N': self._gui.multimeterSerialNumberLineEdit.displayText(),
                         'ID': self._gui.multimeterIdentificationLineEdit.displayText(),
                         'GPIB bus': self._gui.multimeterGPIBBusLineEdit.displayText(),
                         'GPIB channel': self._gui.multimeterGPIBChannelComboBox.currentText()}

        self.AA_info = {'Brand': self._gui.analyzerBrandLineEdit.displayText(),
                        'Model': self._gui.analyzerModelLineEdit.displayText(),
                        'S/N': self._gui.analyzerSerialNumberLineEdit.displayText(),
                        'ID': self._gui.analyzerIdentificationLineEdit.displayText(),
                        'GPIB bus': self._gui.analyzerGPIBBusLineEdit.displayText(),
                        'GPIB channel': self._gui.analyzerGPIBChannelComboBox.currentText()}

        # Dual function of the save button: 1 for save, 2 for edit
        if self.save_standards_state == 1:
            if "" not in self.DMM_info.values() and "" not in self.AA_info.values():  # Checks complete info
                self._TESTER.set_standard_calibrator(self.standard_calibrator)
                self._TESTER.set_mic(self.__gras40CE)
                self._TESTER.set_standards(self.DMM_info, self.AA_info)
                self._gui.saveStandardsInfo.setText('Editar')
                self._gui.standardCalibratorGroupBox.setEnabled(False)
                self._gui.micGroupBox.setEnabled(False)
                self._gui.multimeterGroupBox.setEnabled(False)
                self._gui.audioAnalyzerGroupBox.setEnabled(False)
                self.save_standards_state = 2
                model = PandasTableModel(
                    self._TESTER.standard_noise_values.iloc[[self._TESTER.current_level]].fillna(""))
                self._gui.standardNoiseTable.setModel(model)
                model = PandasTableModel(self.standard_averaged_values.fillna(""))
                self._gui.standardAverageResultsTable.setModel(model)
                QtWidgets.QMessageBox.information(self._gui, 'Información', 'Información guardada correctamente.')
                self._gui.actionSelfTest.setEnabled(True)
            else:
                QtWidgets.QMessageBox.warning(self._gui, 'Advertencia',
                                              'La información de los patrones no está completa.')
        else:
            # TODO: Incluir control de edición cuando ya ha iniciado la calibración
            self._gui.standardCalibratorGroupBox.setEnabled(True)
            self._gui.micGroupBox.setEnabled(True)
            self._gui.multimeterGroupBox.setEnabled(True)
            self._gui.audioAnalyzerGroupBox.setEnabled(True)
            self.save_standards_state = 1
            self._gui.saveStandardsInfo.setText('Guardar')

    def save_dut_info(self) -> None:
        """
        Method that catch the DUT and customer information and save that in the TESTER object.
        Also enables and disables the corresponding objects and actions.
        """
        levels = []  # Nominal levels array
        if self._gui.dutLevel94CheckBox.isChecked():
            levels.append([94, 1000])  # By default I'm assuming capacity for calibrate only 94 and 114 dB, 1 kHz.
        if self._gui.dutLevel114checkBox.isChecked():
            levels.append([114, 1000])
        dut_info = {'Consecutive': self._gui.consecutiveLineEdit.displayText(),
                    'Brand': self._gui.dutBrandLineEdit.displayText(),
                    'Model': self._gui.dutModelLineEdit.displayText(),
                    'S/N': self._gui.dutSerialNumberLineEdit.displayText(),
                    'ID': self._gui.dutIdentificationLineEdit.displayText(),
                    'Class': int(self._gui.dutClassComboBox.currentText()),
                    'Adaptor': self._gui.dutAdaptorLineEdit.displayText(),
                    'Pressure Correction': 0 if self._gui.dutPressureCorrectionLineEdit.displayText() == "" else eval(
                        self._gui.dutPressureCorrectionLineEdit.displayText()),
                    'Free Field Difference:': 0 if self._gui.dutFreeFieldDifferenceLineEdit.displayText() == "" else (
                        float(self._gui.dutFreeFieldDifferenceLineEdit.displayText()))}
        dut = ac.AcousticCalibrator(brand=dut_info['Brand'], model=dut_info['Model'], sn=dut_info['S/N'],
                                    identification=dut_info['ID'], adaptor=dut_info['Adaptor'], cl=dut_info['Class'],
                                    nominal_values=np.array(levels),
                                    pressure_influence=dut_info['Pressure Correction'],
                                    free_field_difference=dut_info['Free Field Difference:'])
        customer_info = {'Name': self._gui.customerNameLineEdit.displayText(),
                         'Address': self._gui.addressLineEdit.displayText(),
                         'City': self._gui.cityLineEdit.displayText(),
                         'Country': self._gui.consecutiveLineEdit.displayText(),
                         'Postal code': self._gui.postalCodeLineEdit.displayText(),
                         'Contact': self._gui.contactNumberLineEdit.displayText()}

        # Dual function of the save button: 1 for save, 2 for edit.
        if self.save_DUT_info_sate == 1:
            if "" not in dut_info.values() and "" not in customer_info.values():  # Checks complete info
                self._TESTER.set_dut(dut)
                self._TESTER.set_consecutive(dut_info['Consecutive'])
                self._TESTER.set_customer_info(customer_info)
                self.save_DUT_info_sate = 2
                self._gui.saveDUTInfo.setText('Editar')
                self._gui.dutGroupBox.setEnabled(False)
                self._gui.customerGroupBox.setEnabled(False)
                self._gui.level94radioButton.setEnabled(self._gui.dutLevel94CheckBox.isChecked())
                self._gui.level114radioButton.setEnabled(self._gui.dutLevel114checkBox.isChecked())
                QtWidgets.QMessageBox.information(self._gui, 'Información',
                                                  'La información del IBC y del cliente se guardó correctamente')
                model = PandasTableModel(self._TESTER.dut_noise_values.iloc[[self._TESTER.current_level]].fillna(""))
                self._gui.dutNoiseTable.setModel(model)
                model = PandasTableModel(self.dut_averaged_values.fillna(""))
                self._gui.dutAverageResultsTable.setModel(model)
                if self.self_test_passed and self.save_standards_state == 2:
                    self._gui.actionStart.setEnabled(True)
                    self._gui.resultsTab.setEnabled(True)
            else:
                QtWidgets.QMessageBox.warning(self._gui, 'Advertencia',
                                              'La información del IBC o del cliente no está completa.')
        else:
            # TODO: Incluir control de edición cuando ya ha iniciado la calibración
            self._gui.dutGroupBox.setEnabled(True)
            self._gui.customerGroupBox.setEnabled(True)
            self.save_DUT_info_sate = 1
            self._gui.saveDUTInfo.setText('Guardar')

    def self_test(self) -> None:
        """
        This method executes the self-test routine of multimeter and anlyzer in a parallel thread.
        """
        self.selfTesterThread = QtCore.QThread()  # This is the parallel thread for self-testing
        self.selfTesterWorker = SelfTester(self._TESTER.DMM, self._TESTER.AA)
        self.selfTesterWorker.moveToThread(self.selfTesterThread)
        self.selfTesterThread.started.connect(self.selfTesterWorker.self_test)
        self.selfTesterWorker.progress.connect(self._gui.measurementProgressBar.setValue)
        self.selfTesterWorker.finished.connect(self.show_self_test_results)
        self.selfTesterWorker.finished.connect(self.selfTesterThread.quit)
        self.selfTesterWorker.finished.connect(self.selfTesterWorker.deleteLater)
        self.selfTesterThread.finished.connect(self.selfTesterThread.deleteLater)
        self._gui.measurementProgressLabel.setText('Progreso de auto-verificación')
        self.selfTesterThread.start()

    def show_self_test_results(self, results: tuple) -> None:
        """
        This method presents the results of self-test of multimeter and analyzer on the corresponding check boxes.
        This is executed when the parallel thread finished.
        :param results: tuple of booleans that describe the results of test, passed or no.
        :return: None
        """
        self._gui.multimeterSelfTestCheckBox.setChecked(results[0])
        self._gui.analyzerSelfTestCheckBox.setChecked(results[1])
        self._gui.measurementProgressLabel.setText('Progreso de medición')
        self._gui.measurementProgressBar.setValue(0)
        self.self_test_passed = results[0] and results[1]
        if self.save_standards_state == 2 and self.save_DUT_info_sate == 2 and self.self_test_passed:
            self._gui.actionStart.setEnabled(True)
            self._gui.resultsTab.setEnabled(True)

    def search_standards(self) -> None:
        """
        This method search for the indicated models of multimeter and analyzer in the available VISA resources.
        """
        self.selfTesterThread = QtCore.QThread()
        resources = self._TESTER.resource_manager.list_resources()  # List all available resources
        self.searchStandardWorker = StandardsSearcher(DMM_model=self._gui.multimeterModelLineEdit.displayText(),
                                                      AA_model=self._gui.analyzerModelLineEdit.displayText(),
                                                      resources=resources,
                                                      resource_manager=self._TESTER.resource_manager)
        self.searchStandardWorker.moveToThread(self.searchStandardThread)
        self.searchStandardThread.started.connect(self.searchStandardWorker.search)
        self.searchStandardWorker.progress.connect(self._gui.measurementProgressBar.setValue)
        self.searchStandardWorker.finished.connect(self.fill_standards_info)
        self.searchStandardWorker.finished.connect(self.searchStandardThread.quit)
        self.searchStandardWorker.finished.connect(self.searchStandardWorker.deleteLater)
        self.searchStandardThread.finished.connect(self.searchStandardThread.deleteLater)
        self._gui.measurementProgressLabel.setText('Progreso de búsqueda')
        self.searchStandardThread.start()

    def fill_standards_info(self, data_found: tuple) -> None:
        """
        This method is executed when the parallel process of searching finished. This validates the existing of the
        instrument and fill the information available.
        :param data_found: tuple of booleans that indicates if the multimeter and the analyzer was founded.
        :return: None
        """
        if not data_found[0]:
            QtWidgets.QMessageBox.warning(self._gui, 'Advertencia', 'Multímetro no encontrado.')
        if not data_found[1]:
            QtWidgets.QMessageBox.warning(self._gui, 'Advertencia', 'Analizador de audio no encontrado.')
        if data_found[0] and data_found[1]:
            self._gui.multimeterBrandLineEdit.setText(self.searchStandardWorker.data['DMM']['Brand'])
            self._gui.multimeterSerialNumberLineEdit.setText(self.searchStandardWorker.data['DMM']['S/N'])
            self._gui.multimeterGPIBBusLineEdit.setText(self.searchStandardWorker.data['DMM']['GPIB bus'])
            self._gui.multimeterGPIBChannelComboBox.setCurrentIndex(
                int(self.searchStandardWorker.data['DMM']['GPIB channel']))
            self._gui.analyzerBrandLineEdit.setText(self.searchStandardWorker.data['AA']['Brand'])
            self._gui.analyzerSerialNumberLineEdit.setText(self.searchStandardWorker.data['AA']['S/N'])
            self._gui.analyzerGPIBBusLineEdit.setText(self.searchStandardWorker.data['AA']['GPIB bus'])
            self._gui.analyzerGPIBChannelComboBox.setCurrentIndex(
                int(self.searchStandardWorker.data['AA']['GPIB channel']))
        self._gui.measurementProgressLabel.setText('Progreso de medición')
        self._gui.measurementProgressBar.setValue(0)

    def update_noise_values(self) -> None:
        """
        This method is executed on every calibration progress signal, but checks if the stage corresponds to a
        background noise measurement, then shows the results on the GUI. NOTE: The stage evaluated is one before, so,
        this method is "post-process".
        """
        # If the current stage corresponds to the standard calibrator
        if any([self._TESTER.stage == stage for stage in [3, 6, 9]]):
            self.show_standard_noise_values()
        elif any([self._TESTER.stage == stage for stage in [4, 7, 10]]):
            self.show_averaged_standard_values()
        elif any([self._TESTER.stage == stage for stage in [12, 15, 18]]):
            self.show_dut_noise_values()
        elif any([self._TESTER.stage == stage for stage in [13, 16, 19]]):
            self.show_averaged_dut_values()

    def show_standard_noise_values(self) -> None:
        """
        This is a simple method for setting the QTableView model with the updated standard acoustic calibrator
        background noise measurement results.
        """
        noise_values = self._TESTER.standard_noise_values.iloc[[self._TESTER.current_level]].round(2)
        model = PandasTableModel(noise_values.fillna(""))
        self._gui.standardNoiseTable.setModel(model)

    def show_dut_noise_values(self) -> None:
        """
        This is a simple method for setting the QTableView model with the updated customer's acoustic calibrator
        background noise measurement results.
        """
        noise_values = self._TESTER.dut_noise_values.iloc[[self._TESTER.current_level]].round(2)
        model = PandasTableModel(noise_values.fillna(""))
        self._gui.dutNoiseTable.setModel(model)

    def show_averaged_standard_values(self) -> None:
        df = self._TESTER.standard_measurement_values[self._TESTER.current_level].mean()
        # Reindexing for an easy mean calculation
        iterables = [['0°', '120°', '240°'], ['V [mV]', 'SPL [dB]', 'f [Hz]', 'THD+N [%]']]
        index = pd.MultiIndex.from_product(iterables, names=['Orientation', 'Quantities'])
        df.index = index
        for degree in ['0°', '120°', '240°']:
            self.standard_averaged_values[degree] = df[degree]
        self.standard_averaged_values['TOTAL'] = self.standard_averaged_values.iloc[:, 0:3].mean(axis=1)
        self.standard_averaged_values.loc['V [mV]'] *= 1000  # Convert volts to milli volts
        self.standard_averaged_values.loc['V [mV]'] = self.standard_averaged_values.loc['V [mV]'].round(3)
        self.standard_averaged_values.loc['SPL [dB]'] = self.standard_averaged_values.loc['SPL [dB]'].round(2)
        self.standard_averaged_values.loc['f [Hz]'] = self.standard_averaged_values.loc['f [Hz]'].round(3)
        self.standard_averaged_values.loc['THD+N [%]'] = self.standard_averaged_values.loc['THD+N [%]'].round(2)
        model = PandasTableModel(self.standard_averaged_values.fillna(""))
        self._gui.standardAverageResultsTable.setModel(model)

    def show_averaged_dut_values(self) -> None:
        df = self._TESTER.dut_measurement_values[self._TESTER.current_level].mean()
        # Reindexing for an easy mean calculation
        iterables = [['0°', '120°', '240°'], ['V [mV]', 'SPL [dB]', 'f [Hz]', 'THD+N [%]']]
        index = pd.MultiIndex.from_product(iterables, names=['Orientation', 'Quantities'])
        df.index = index
        for degree in ['0°', '120°', '240°']:
            self.dut_averaged_values[degree] = df[degree]
        # Compute new partial mean SPL as a logarithmic average
        levels = pd.Series(data=np.nan * np.ones(3), index=['0°', '120°', '240°'])
        ref_lev = self.standard_averaged_values.loc['SPL [dB]', 'TOTAL']
        for i in range(3):
            level = self._TESTER.volt2level(self.dut_averaged_values.iloc[0, i],
                                            self._TESTER.microphone['Sensibility'][self._TESTER.current_level], ref_lev)
            level = level - self._TESTER.dut.free_field_difference - self._TESTER.dut.pressure_influence * (
                    75 - 102.3) - self._TESTER.microphone['Correction']
            levels.iat[i] = level
        self.dut_averaged_values.iloc[1, 0:3] = levels
        self.dut_averaged_values['TOTAL'] = self.dut_averaged_values.iloc[:, 0:3].mean(axis=1)
        # Compute new marginal mean SPL as a logarithmic average
        v = self._TESTER.dut_measurement_values[self._TESTER.current_level].loc[:, (slice(None), "V [V]")].mean().mean()
        level = self._TESTER.volt2level(v, self._TESTER.microphone['Sensibility'][self._TESTER.current_level], ref_lev)
        level = level - self._TESTER.dut.free_field_difference - self._TESTER.dut.pressure_influence * (
                75 - 102.3) - self._TESTER.microphone['Correction']
        self.dut_averaged_values.loc['SPL [dB]', 'TOTAL'] = level
        self.dut_averaged_values.loc['V [mV]'] *= 1000  # Convert volts to milli volts
        self.dut_averaged_values.loc['V [mV]'] = self.dut_averaged_values.loc['V [mV]'].round(3)
        self.dut_averaged_values.loc['SPL [dB]'] = self.dut_averaged_values.loc['SPL [dB]'].round(2)
        self.dut_averaged_values.loc['f [Hz]'] = self.dut_averaged_values.loc['f [Hz]'].round(3)
        self.dut_averaged_values.loc['THD+N [%]'] = self.dut_averaged_values.loc['THD+N [%]'].round(2)
        model = PandasTableModel(self.dut_averaged_values.fillna(""))
        self._gui.dutAverageResultsTable.setModel(model)

    def update_real_time_values(self, values: tuple) -> None:
        """
        This method is called on every real-time signal emission for reporting measurement values,
        on the quantities' measurement stages, both for standard or customer's calibrator.
        :param values: A tuple with the real-time results of voltage, level, frequency and THD+N
        :return: None
        """
        if any([stage == self._TESTER.stage for stage in [3, 6, 9, 12, 15, 18]]):
            # This is for standard acoustic calibrator
            # Constructs an array with the rounded values
            rounded = pd.DataFrame(data=np.array([[round(values[0] * 1000, 3), round(values[1], 2),
                                                   round(values[2], 3), round(values[3], 2)]]),
                                   columns=['V [mV]', 'SPL [dB]', 'f [Hz]', 'THD+N [%]'])
            self.acquired_values = self.acquired_values.append(rounded)
            self.acquired_values.index = np.array(range(1, len(self.acquired_values) + 1))  # Reindex for table model
            model = PandasTableModel(self.acquired_values)
            # Shows the values depending on the orientation of the calibrator
            # If the stage corresponds to the standard calibrator
            if self._TESTER.stage == 3:
                self._gui.standard0ResultsTable.setModel(model)
            elif self._TESTER.stage == 6:
                self._gui.standard120ResultsTable.setModel(model)
            elif self._TESTER.stage == 9:
                self._gui.standard240ResultsTable.setModel(model)
            # If the stage corresponds to the customer's calibrator
            elif self._TESTER.stage == 12:
                self._gui.dut0ResultsTable.setModel(model)
            elif self._TESTER.stage == 15:
                self._gui.dut120ResultsTable.setModel(model)
            elif self._TESTER.stage == 18:
                self._gui.dut240ResultsTable.setModel(model)

    def start(self) -> None:
        """
        This method is launched when the start action is triggered.
        This starts or resumes the calibration sequence and controls the GUI buttons.
        """
        self._gui.actionStart.setEnabled(False)
        self._gui.actionPause.setEnabled(True)
        # If the sequence was paused, It don't shows instructions again; just resumes the sequence
        if self._TESTER.state < 2:
            self.sequence_control()
        self._TESTER.set_state(1)

    def pause(self) -> None:
        """
        This method pauses the calibration sequence and controls the GUI buttons.
        """
        self._gui.actionPause.setEnabled(False)
        self._gui.actionStart.setEnabled(True)
        self._TESTER.set_state(2)

    def sequence_control(self) -> None:
        """
        This is the controller method of the principal calibration sequence.
        This method  also shows the corresponding calibration instructions on every stage.
        For your reference consult the GRAFCET.
        """
        if self._TESTER.stage == 0:
            self.calibrationThread.start()
        elif self._TESTER.stage == 1:
            instruction = InstructionDialog(self._gui,
                                            '1. Acople el calibrador acústico de referencia en la dirección de 0°.' +
                                            '\n2. Encienda el calibrador acústico de referencia.')
            self.eval_answer(instruction)
        elif self._TESTER.stage == 2:
            instruction = InstructionDialog(self._gui, 'Apague el calibrador acústico de referencia.')
            self.eval_answer(instruction)
        elif any([self._TESTER.stage == stage for stage in [3, 6, 9]]):
            instruction = InstructionDialog(self._gui, 'Encienda el calibrador acústico de referencia.')
            self.eval_answer(instruction)
            self.acquired_values = pd.DataFrame(columns=['V [mV]', 'SPL [dB]', 'f [Hz]', 'THD+N [%]'])
        elif any([self._TESTER.stage == stage for stage in [4, 7, 10]]):
            instruction = InstructionDialog(self._gui, 'Apague y desacople el calibrador acústico de referencia.')
            self.eval_answer(instruction)
        elif any([self._TESTER.stage == stage for stage in [5, 8]]):
            instruction = InstructionDialog(self._gui,
                                            f'Rote el calibrador acústico de referencia 120°' +
                                            'y acóplelo al micrófono. \nManténgalo apagado.')
            self.eval_answer(instruction)
        elif self._TESTER.stage == 11:
            instruction = InstructionDialog(self._gui, 'Acople el calibrador acústico del cliente.' +
                                            '\nAsegúrese de que el calibrador esté apagado.')
            self.eval_answer(instruction)
        elif any([self._TESTER.stage == stage for stage in [12, 15, 18]]):
            instruction = InstructionDialog(self._gui, 'Encienda el calibrador acústico del cliente.')
            self.eval_answer(instruction)
            self.acquired_values = pd.DataFrame(columns=['V [mV]', 'SPL [dB]', 'f [Hz]', 'THD+N [%]'])
        elif any([self._TESTER.stage == stage for stage in [13, 16]]):
            instruction = InstructionDialog(self._gui, 'Apague y desacople el calibrador acústico del cliente.')
            self.eval_answer(instruction)
        elif any([self._TESTER.stage == stage for stage in [14, 17]]):
            instruction = InstructionDialog(self._gui,
                                            f'Rote el calibrador acústico de del cliente 120°' +
                                            'y acóplelo al micrófono. \nManténgalo apagado.')
            self.eval_answer(instruction)
        elif self._TESTER.stage == 19:
            QtWidgets.QMessageBox.information(self._gui, 'Información', '!SECUENCIA FINALIZADA¡')
            self._gui.actionPause.setEnabled(False)

    def eval_answer(self, instruction) -> None:
        """
        This is a simple method for evaluate the user response to a given instruction.
        :param instruction: Dialog object
        :return: None
        """
        if instruction.exec() == QtWidgets.QMessageBox.Ok:
            self.calibrationThread.start()
        else:
            self._gui.actionStart.setEnabled(True)
            self._gui.actionPause.setEnabled(False)

    def invalid_measurement(self, value) -> None:
        """
        This method is intended to be used when a measurement value is invalid and is menester retry the measurement.
        According to the IEC 60942 and some practical purposes, just a few stages of the GRAFCET require this to can
        continue with the calibration process.
        :param value: Invalid measurement value
        :return: None
        """
        if self._TESTER.stage == 1:
            instruction = InstructionDialog(self._gui,
                                            f'Sensibilidad de {round(value * 1000, 3)} mV/Pa no aceptable' +
                                            '\n ¿Repetir medición?')
            instruction.setIcon(QtWidgets.QMessageBox.Critical)
            self.eval_answer(instruction)
        if any([self._TESTER.stage == stage for stage in [2, 5, 8, 11, 14, 17]]):
            instruction = InstructionDialog(self._gui,
                                            f'Ruido de fondo de {round(value, 2)} dB mayor a 65 dB.' +
                                            '\n ¿Repetir medición?')
            instruction.setIcon(QtWidgets.QMessageBox.Critical)
            self.eval_answer(instruction)


class StandardsSearcher(QtCore.QObject):
    """
    QObject for searching standards running in a parallel thread.
    """
    finished = QtCore.pyqtSignal(tuple)
    progress = QtCore.pyqtSignal(int)

    def __init__(self, DMM_model: str, AA_model: str, resources: tuple, resource_manager: ac.visa.ResourceManager):
        super().__init__()
        self.DMM_model = DMM_model
        self.AA_model = AA_model
        self.resources = resources
        self._resource_manager = resource_manager
        self.data = {'DMM': {'Brand': '',
                             'S/N': '',
                             'GPIB bus': '',
                             'GPIB channel': ''},
                     'AA': {'Brand': '',
                            'S/N': '',
                            'GPIB bus': '',
                            'GPIB channel': ''}}

    def search(self) -> None:
        """
        Method for searching the given models between the available VISA resources.
        :return: None
        """
        i = 0
        multimeter_found = False
        analyzer_found = False
        for res in self.resources:  # Search for the Arbitrary Function Generator
            i += int(1 / len(self.resources) * 100)
            self.progress.emit(i)  # Signal for updating the progress bar
            try:
                instrument = self._resource_manager.open_resource(res)
                idn = instrument.query('*IDN?')
            except ac.visa.errors.VisaIOError:
                continue

            # Check if the current resource is the specified multimeter model
            if self.DMM_model in idn and 'GPIB' in res:
                idn_data = idn.split(',')
                self.data['DMM']['Brand'] = idn_data[0]
                self.data['DMM']['S/N'] = idn_data[2]
                res_data = res.split("::")
                self.data['DMM']['GPIB bus'] = res_data[0].replace("GPIB", "")
                self.data['DMM']['GPIB channel'] = res_data[1]
                multimeter_found = True
            # Check if the current resource is the specified analyzer model
            if self.AA_model in idn and 'GPIB' in res:
                idn_data = idn.split(',')
                self.data['AA']['Brand'] = idn_data[0]
                self.data['AA']['S/N'] = idn_data[2]
                res_data = res.split("::")
                self.data['AA']['GPIB bus'] = res_data[0].replace("GPIB", "")
                self.data['AA']['GPIB channel'] = res_data[1]
                analyzer_found = True

        self.finished.emit((multimeter_found, analyzer_found))


class SelfTester(QtCore.QObject):
    """
    QObject for execute self-test routine of every instrument in a parallel thread.
    """
    finished = QtCore.pyqtSignal(tuple)
    progress = QtCore.pyqtSignal(int)

    def __init__(self, DMM: ac.visa.Resource, AA: ac.visa.Resource):
        super().__init__()
        self._DMM = DMM
        self._AA = AA

    def self_test(self):
        dmm_pass = self._DMM.query('*TST?')  # Run self-test on multimeter
        dmm_pass = not bool(int(dmm_pass))
        self.progress.emit(50)
        aa_pass = self._AA.query('*TST?')  # Run self-test on analyzer
        aa_pass = bool(int(aa_pass))
        self.progress.emit(100)
        self.finished.emit((dmm_pass, aa_pass))


class InstructionDialog(QtWidgets.QMessageBox):
    """
    This is a simple dialog box class that shows instructions on the way.
    This includes both Ok and Abort buttons and inherits from the QMessageBox class.
    """
    def __init__(self, parent, dialog: str):
        super().__init__(parent=parent)
        self.setWindowTitle('Instrucción')
        self.setText(dialog)
        self.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Abort)
        self.setIcon(QtWidgets.QMessageBox.Information)


class PandasTableModel(QtCore.QAbstractTableModel):
    """
    This class is the implementation of a table model.
    The model is created from a Pandas DataFrame.
    """
    def __init__(self, df, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self._df = df

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if orientation == QtCore.Qt.Horizontal:
            try:
                return self._df.columns.tolist()[section]
            except (IndexError,):
                return QtCore.QVariant()
        elif orientation == QtCore.Qt.Vertical:
            try:
                # return self.df.index.tolist()
                return self._df.index.tolist()[section]
            except (IndexError,):
                return QtCore.QVariant()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if not index.isValid():
            return QtCore.QVariant()

        if role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(str(self._df.iat[index.row(), index.column()]))

        elif role == QtCore.Qt.TextAlignmentRole:
            return Qt.AlignCenter

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.index)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.columns)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = AcousticCalibratorsUI()
    Controller = GUIController(MainWindow)
    MainWindow.showMaximized()
    sys.exit(app.exec_())
