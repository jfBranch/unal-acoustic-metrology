import functools
import os
import logging
import numpy as np
import pandas as pd
import cv2 as cv
import qrc_resources
import ctypes
import pickle
import acoustic_calibrations as ac
from queue import Queue
from PyQt5 import QtCore, QtGui, QtWidgets
from time import sleep

myappid = 'unal.acuscal.sonometers.1.0'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

__autor__ = 'Juan Felipe Maldonado'
__version__ = '1.0 Beta'
logging.basicConfig(
    format='%(asctime)s.%(msecs)03d   %(message)s',
    level=logging.INFO,
    datefmt='%H:%M:%S')
mutex = QtCore.QMutex()


class SonometersCalibrationUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        """
        Constructor method for create all the objects of the main window.
        """
        super().__init__(parent)
        self.centralWidget = QtWidgets.QWidget(self)
        self.gridCentralLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.videoScene = QtWidgets.QGraphicsScene()
        q_pixmap = QtGui.QPixmap()
        self.videoPixmap = self.videoScene.addPixmap(q_pixmap)
        self.roi = GraphicsRectItem(250, 200, 200, 100)
        self.videoScene.addItem(self.roi)
        self.videoView = QtWidgets.QGraphicsView(self.videoScene, self.centralWidget)
        self.gridStatusLayout = QtWidgets.QGridLayout()
        self.testLabel = QtWidgets.QLabel(self.centralWidget)
        self.previousTestToolButton = QtWidgets.QToolButton(self.centralWidget)
        self.nextTestToolButton = QtWidgets.QToolButton(self.centralWidget)
        self.lcdNumber = QtWidgets.QLCDNumber(self.centralWidget)
        self.verticalStatusLayout = QtWidgets.QVBoxLayout()
        self.measurementProgressLabel = QtWidgets.QLabel(self.centralWidget)
        self.measurementProgressBar = QtWidgets.QProgressBar(self.centralWidget)
        self.generalProgressLabel = QtWidgets.QLabel(self.centralWidget)
        self.generalProgressBar = QtWidgets.QProgressBar(self.centralWidget)
        self.streamingButton = QtWidgets.QPushButton(self.centralWidget)
        self.videoLabel = QtWidgets.QLabel(self.centralWidget)
        self.line = QtWidgets.QFrame(self.centralWidget)
        self.parentTabWidget = QtWidgets.QTabWidget(self.centralWidget)
        self.standardsTab = QtWidgets.QWidget()
        self.standardsGridLayout = QtWidgets.QGridLayout(self.standardsTab)
        self.decadeBoxGroupBox = QtWidgets.QGroupBox(self.standardsTab)
        self.decadeBoxFormLayout = QtWidgets.QFormLayout(self.decadeBoxGroupBox)
        self.decadeBoxBrandLabel = QtWidgets.QLabel(self.decadeBoxGroupBox)
        self.decadeBoxBrandLineEdit = QtWidgets.QLineEdit(self.decadeBoxGroupBox)
        self.decadeBoxModelLabel = QtWidgets.QLabel(self.decadeBoxGroupBox)
        self.decadeBoxModelLineEdit = QtWidgets.QLineEdit(self.decadeBoxGroupBox)
        self.decadeBoxSerialNumberLabel = QtWidgets.QLabel(self.decadeBoxGroupBox)
        self.decadeBoxSerialNumberLineEdit = QtWidgets.QLineEdit(self.decadeBoxGroupBox)
        self.decadeBoxIdentificationLabel = QtWidgets.QLabel(self.decadeBoxGroupBox)
        self.decadeBoxIdentificationLineEdit = QtWidgets.QLineEdit(self.decadeBoxGroupBox)
        self.afgGroupBox = QtWidgets.QGroupBox(self.standardsTab)
        self.afgFormLayout = QtWidgets.QFormLayout(self.afgGroupBox)
        self.afgBrandLabel = QtWidgets.QLabel(self.afgGroupBox)
        self.afgBrandLineEdit = QtWidgets.QLineEdit(self.afgGroupBox)
        self.afgModelLabel = QtWidgets.QLabel(self.afgGroupBox)
        self.afgModelLineEdit = QtWidgets.QLineEdit(self.afgGroupBox)
        self.afgSerialNumberLabel = QtWidgets.QLabel(self.afgGroupBox)
        self.afgSerialNumberLineEdit = QtWidgets.QLineEdit(self.afgGroupBox)
        self.afgIdentificationLabel = QtWidgets.QLabel(self.afgGroupBox)
        self.afgIdentificationLineEdit = QtWidgets.QLineEdit(self.afgGroupBox)
        self.afgGPIBbusLabel = QtWidgets.QLabel(self.afgGroupBox)
        self.afgGPIBbusLineEdit = QtWidgets.QLineEdit(self.afgGroupBox)
        self.afgGPIBChannelLabel = QtWidgets.QLabel(self.afgGroupBox)
        self.afgGPIBChannelComboBox = QtWidgets.QComboBox(self.afgGroupBox)
        self.afgSelfTestLabel = QtWidgets.QLabel(self.afgGroupBox)
        self.afgSelfTestCheckBox = QtWidgets.QCheckBox(self.afgGroupBox)
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
        self.saveStandardsInfo = QtWidgets.QPushButton(self.standardsTab)
        self.infoTab = QtWidgets.QWidget()
        self.infoGridLayout = QtWidgets.QGridLayout(self.infoTab)
        self.preampGroupBox = QtWidgets.QGroupBox(self.infoTab)
        self.preampFormLayout = QtWidgets.QFormLayout(self.preampGroupBox)
        self.preampBrandLabel = QtWidgets.QLabel(self.preampGroupBox)
        self.preampBrandLineEdit = QtWidgets.QLineEdit(self.preampGroupBox)
        self.preampModelLabel = QtWidgets.QLabel(self.preampGroupBox)
        self.preampModelLineEdit = QtWidgets.QLineEdit(self.preampGroupBox)
        self.preampSerialLabel = QtWidgets.QLabel(self.preampGroupBox)
        self.preampSerialLineEdit = QtWidgets.QLineEdit(self.preampGroupBox)
        self.customerGroupBox = QtWidgets.QGroupBox(self.infoTab)
        self.customerFormLayout = QtWidgets.QFormLayout(self.customerGroupBox)
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
        self.dutGroupBox = QtWidgets.QGroupBox(self.infoTab)
        self.dutFormLayout = QtWidgets.QFormLayout(self.dutGroupBox)
        self.consecutiveLabel = QtWidgets.QLabel(self.dutGroupBox)
        self.consecutiveLineEdit = QtWidgets.QLineEdit(self.dutGroupBox)
        self.dutBrandLabel = QtWidgets.QLabel(self.dutGroupBox)
        self.dutBrandLineEdit = QtWidgets.QLineEdit(self.dutGroupBox)
        self.dutModelLabel = QtWidgets.QLabel(self.dutGroupBox)
        self.dutModelLineEdit = QtWidgets.QLineEdit(self.dutGroupBox)
        self.dutSerialNumberLabel = QtWidgets.QLabel(self.dutGroupBox)
        self.dutSerialNumberLineEdit = QtWidgets.QLineEdit(self.dutGroupBox)
        self.dutIdentificationLabel = QtWidgets.QLabel(self.dutGroupBox)
        self.dutIdentificationLineEdit = QtWidgets.QLineEdit(self.dutGroupBox)
        self.dutClassLabel = QtWidgets.QLabel(self.dutGroupBox)
        self.dutClassComboBox = QtWidgets.QComboBox(self.dutGroupBox)
        self.supplyULimitLabel = QtWidgets.QLabel(self.dutGroupBox)
        self.supplyULimitLineEdit = QtWidgets.QLineEdit(self.dutGroupBox)
        self.supplyLLimitLabel = QtWidgets.QLabel(self.dutGroupBox)
        self.supplyLLimitLineEdit = QtWidgets.QLineEdit(self.dutGroupBox)
        self.referenceLevelLabel = QtWidgets.QLabel(self.dutGroupBox)
        self.referenceLevelLineEdit = QtWidgets.QLineEdit(self.dutGroupBox)
        self.lu1kHzLabel = QtWidgets.QLabel(self.dutGroupBox)
        self.lu1kHzLineEdit = QtWidgets.QLineEdit(self.dutGroupBox)
        self.lu8kHzLabel = QtWidgets.QLabel(self.dutGroupBox)
        self.lu8kHzLineEdit = QtWidgets.QLineEdit(self.dutGroupBox)
        self.li8kHzLabel = QtWidgets.QLabel(self.dutGroupBox)
        self.li8kHzLineEdit = QtWidgets.QLineEdit(self.dutGroupBox)
        self.startPointLabel = QtWidgets.QLabel(self.dutGroupBox)
        self.startPointLineEdit = QtWidgets.QLineEdit(self.dutGroupBox)
        self.screenRateLabel = QtWidgets.QLabel(self.dutGroupBox)
        self.screenRateLineEdit = QtWidgets.QLineEdit(self.dutGroupBox)
        self.loadFreeFieldPushButton = QtWidgets.QPushButton(self.dutGroupBox)
        self.micGroupBox = QtWidgets.QGroupBox(self.infoTab)
        self.micFormLayout = QtWidgets.QFormLayout(self.micGroupBox)
        self.micBrandLabel = QtWidgets.QLabel(self.micGroupBox)
        self.micBrandLineEdit = QtWidgets.QLineEdit(self.micGroupBox)
        self.micModelLabel = QtWidgets.QLabel(self.micGroupBox)
        self.micModelLineEdit = QtWidgets.QLineEdit(self.micGroupBox)
        self.micSerialNumberLabel = QtWidgets.QLabel(self.micGroupBox)
        self.micSerialNumberLineEdit = QtWidgets.QLineEdit(self.micGroupBox)
        self.preTestsTab = QtWidgets.QWidget()
        self.preTestVLayout = QtWidgets.QVBoxLayout(self.preTestsTab)
        self.supplyLabel = QtWidgets.QLabel(self.preTestsTab)
        self.supplyGridLayout = QtWidgets.QGridLayout()
        self.electricTestsLabel = QtWidgets.QLabel(self.preTestsTab)
        self.beforeLabel = QtWidgets.QLabel(self.preTestsTab)
        self.afterLabel = QtWidgets.QLabel(self.preTestsTab)
        self.afterElecUnitsLabel = QtWidgets.QLabel(self.preTestsTab)
        self.beforeAcusUnitsLabel = QtWidgets.QLabel(self.preTestsTab)
        self.beforeElecValLabel = QtWidgets.QLabel(self.preTestsTab)
        self.beforeAcusValLabel = QtWidgets.QLabel(self.preTestsTab)
        self.acousticTestsLabel = QtWidgets.QLabel(self.preTestsTab)
        self.afterElecValLabel = QtWidgets.QLabel(self.preTestsTab)
        self.afterAcusValLabel = QtWidgets.QLabel(self.preTestsTab)
        self.afterAcusUnitsLabel = QtWidgets.QLabel(self.preTestsTab)
        self.beforeElecUnitsLabel = QtWidgets.QLabel(self.preTestsTab)
        self.supplyVLine1 = QtWidgets.QFrame(self.preTestsTab)
        self.supplyVLine2 = QtWidgets.QFrame(self.preTestsTab)
        self.preliminarHLine1 = QtWidgets.QFrame(self.preTestsTab)
        self.calIndLabel = QtWidgets.QLabel(self.preTestsTab)
        self.calIndGridLayout = QtWidgets.QGridLayout()
        self.initAdjUnitsLabel = QtWidgets.QLabel(self.preTestsTab)
        self.adjLabel = QtWidgets.QLabel(self.preTestsTab)
        self.beforeAdjLabel = QtWidgets.QLabel(self.preTestsTab)
        self.afterAdjLabel = QtWidgets.QLabel(self.preTestsTab)
        self.initAdjLabel = QtWidgets.QLabel(self.preTestsTab)
        self.adjEdit = QtWidgets.QLineEdit(self.preTestsTab)
        self.adjSaveButton = QtWidgets.QPushButton(self.preTestsTab)
        self.repliesLabel = QtWidgets.QLabel(self.preTestsTab)
        df = pd.DataFrame(np.empty((3, 3), dtype=str), columns=range(1, 4))
        self.adjTableModel = EditablePandasTableModel(df)
        self.adjTableView = QtWidgets.QTableView(self.preTestsTab)
        self.preliminarHLine2 = QtWidgets.QFrame(self.preTestsTab)
        self.vRefTitleLabel = QtWidgets.QLabel(self.preTestsTab)
        self.vRefGridLayout = QtWidgets.QGridLayout()
        self.vuRefLineEdit = QtWidgets.QLineEdit(self.preTestsTab)
        self.vuRefLabel = QtWidgets.QLabel(self.preTestsTab)
        self.vRefVLine1 = QtWidgets.QFrame(self.preTestsTab)
        self.vRefLabel = QtWidgets.QLabel(self.preTestsTab)
        self.vRefValueLabel = QtWidgets.QLabel(self.preTestsTab)
        self.lvRefLabel = QtWidgets.QLabel(self.preTestsTab)
        self.viRefLineEdit = QtWidgets.QLineEdit(self.preTestsTab)
        self.viRefLabel = QtWidgets.QLabel(self.preTestsTab)
        self.vRefVLine3 = QtWidgets.QFrame(self.preTestsTab)
        self.vRefVLine2 = QtWidgets.QFrame(self.preTestsTab)
        self.lvValueLabel = QtWidgets.QLabel(self.preTestsTab)
        self.vRefButton = QtWidgets.QPushButton(self.preTestsTab)
        self.saveVRefButton = QtWidgets.QPushButton(self.preTestsTab)
        self.vRefVLine4 = QtWidgets.QFrame(self.preTestsTab)
        self.weightingsTab = QtWidgets.QWidget()
        self.weightingsGridLayout = QtWidgets.QGridLayout(self.weightingsTab)
        self.aWTableView = QtWidgets.QTableView(self.weightingsTab)
        self.zWeightLabel = QtWidgets.QLabel(self.weightingsTab)
        self.cWeightLabel = QtWidgets.QLabel(self.weightingsTab)
        self.cWTableView = QtWidgets.QTableView(self.weightingsTab)
        self.zWTableView = QtWidgets.QTableView(self.weightingsTab)
        self.aWeightLabel = QtWidgets.QLabel(self.weightingsTab)
        self.fW1kGridLayout = QtWidgets.QGridLayout()
        self.fWVLine4 = QtWidgets.QFrame(self.weightingsTab)
        self.bW1kHzLevLabel = QtWidgets.QLabel(self.weightingsTab)
        self.aW1kHzLabel = QtWidgets.QLabel(self.weightingsTab)
        self.aW1kHzLevLabel = QtWidgets.QLabel(self.weightingsTab)
        self.bW1kHzLabel = QtWidgets.QLabel(self.weightingsTab)
        self.aW1kHzRLevLabel = QtWidgets.QLabel(self.weightingsTab)
        self.cW1kHzLabel = QtWidgets.QLabel(self.weightingsTab)
        self.cW1kHzLevLabel = QtWidgets.QLabel(self.weightingsTab)
        self.fWRLevLabel = QtWidgets.QLabel(self.weightingsTab)
        self.cW1kHzRLevLabel = QtWidgets.QLabel(self.weightingsTab)
        self.fWLevLabel = QtWidgets.QLabel(self.weightingsTab)
        self.bW1kHzRLevLabel = QtWidgets.QLabel(self.weightingsTab)
        self.fWVLine2 = QtWidgets.QFrame(self.weightingsTab)
        self.fWVLine3 = QtWidgets.QFrame(self.weightingsTab)
        self.fWVLine1 = QtWidgets.QFrame(self.weightingsTab)
        self.fWHLine = QtWidgets.QFrame(self.weightingsTab)
        self.fW1kHzLabel = QtWidgets.QLabel(self.weightingsTab)
        self.weightingsVLine = QtWidgets.QFrame(self.weightingsTab)
        self.tWGridLayout = QtWidgets.QGridLayout()
        self.tWHLine1 = QtWidgets.QFrame(self.weightingsTab)
        self.slowWLevLabel = QtWidgets.QLabel(self.weightingsTab)
        self.slowWRLevLabel = QtWidgets.QLabel(self.weightingsTab)
        self.eqWLevLineEdit = QtWidgets.QLineEdit(self.weightingsTab)
        self.eqWRLevLabel = QtWidgets.QLabel(self.weightingsTab)
        self.fastWRLevLabel = QtWidgets.QLabel(self.weightingsTab)
        self.fastWLevLabel = QtWidgets.QLabel(self.weightingsTab)
        self.slowWLabel = QtWidgets.QLabel(self.weightingsTab)
        self.tWRLevLabel = QtWidgets.QLabel(self.weightingsTab)
        self.fastWLabel = QtWidgets.QLabel(self.weightingsTab)
        self.tWLevLabel = QtWidgets.QLabel(self.weightingsTab)
        self.tWVLine1 = QtWidgets.QFrame(self.weightingsTab)
        self.eqWLabel = QtWidgets.QLabel(self.weightingsTab)
        self.tWHLine2 = QtWidgets.QFrame(self.weightingsTab)
        self.tWVLine3 = QtWidgets.QFrame(self.weightingsTab)
        self.tWVLine4 = QtWidgets.QFrame(self.weightingsTab)
        self.tW1kHzLabel = QtWidgets.QLabel(self.weightingsTab)
        self.linearityTab = QtWidgets.QWidget()
        self.linearityGridLayout = QtWidgets.QGridLayout(self.linearityTab)
        self.linearityTableView = QtWidgets.QTableView(self.linearityTab)
        self.ambientConditionsTab = QtWidgets.QWidget()
        self.ambientGridLayout = QtWidgets.QGridLayout(self.ambientConditionsTab)
        self.ambientTableView = QtWidgets.QTableView(self.ambientConditionsTab)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuCalibration = QtWidgets.QMenu(self.menubar)
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.toolBar = QtWidgets.QToolBar(self)
        self.actionLoadCalibration = QtWidgets.QAction(self)
        self.actionSaveCalibration = QtWidgets.QAction(self)
        self.actionSearchStandards = QtWidgets.QAction(self)
        self.actionSelfTest = QtWidgets.QAction(self)
        self.actionEmitCertificate = QtWidgets.QAction(self)
        self.actionStart = QtWidgets.QAction(self)
        self.actionPause = QtWidgets.QAction(self)
        self.actionRestart = QtWidgets.QAction(self)
        self.actionNextPoint = QtWidgets.QAction(self)
        self.actionPreviousPoint = QtWidgets.QAction(self)
        self.actionNextTest = QtWidgets.QAction(self)
        self.actionPreviousTest = QtWidgets.QAction(self)
        self.actionGoToTest = QtWidgets.QAction(self)
        self.actionGoToPoint = QtWidgets.QAction(self)
        self.setup_ui()  # Calls method for setting up all printable objects of the main window

    def setup_ui(self) -> None:
        """
         This method sets up all the printable objects of the main window and basic GUI functionality.
        """
        self.setObjectName("self")
        self.resize(1320, 700)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/slm_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.centralWidget.setObjectName("centralWidget")
        self.gridCentralLayout.setObjectName("gridCentralLayout")
        self.videoView.setMinimumSize(QtCore.QSize(280, 0))
        self.videoView.setMaximumSize(QtCore.QSize(380, 16777215))
        self.videoView.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.videoView.setObjectName("videoView")
        self.videoView.setScene(self.videoScene)
        self.gridCentralLayout.addWidget(self.videoView, 2, 1, 1, 1)
        self.gridStatusLayout.setObjectName("gridStatusLayout")
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.testLabel.setFont(font)
        self.testLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.testLabel.setObjectName("testLabel")
        self.gridStatusLayout.addWidget(self.testLabel, 1, 1, 1, 1)
        self.previousTestToolButton.setArrowType(QtCore.Qt.LeftArrow)
        self.previousTestToolButton.setObjectName("previousTestToolButton")
        self.gridStatusLayout.addWidget(self.previousTestToolButton, 2, 0, 1, 1)
        self.nextTestToolButton.setArrowType(QtCore.Qt.RightArrow)
        self.nextTestToolButton.setObjectName("nextTestToolButton")
        self.gridStatusLayout.addWidget(self.nextTestToolButton, 2, 2, 1, 1)
        self.lcdNumber.setMinimumSize(QtCore.QSize(70, 40))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.lcdNumber.setFont(font)
        self.lcdNumber.setLineWidth(0)
        self.lcdNumber.setDigitCount(2)
        self.lcdNumber.setObjectName("lcdNumber")
        self.gridStatusLayout.addWidget(self.lcdNumber, 2, 1, 1, 1)
        self.verticalStatusLayout.setObjectName("verticalStatusLayout")
        font = QtGui.QFont()
        font.setPointSize(7)
        self.measurementProgressLabel.setFont(font)
        self.measurementProgressLabel.setObjectName("measurementProgressLabel")
        self.verticalStatusLayout.addWidget(self.measurementProgressLabel)
        font = QtGui.QFont()
        font.setPointSize(6)
        self.measurementProgressBar.setFont(font)
        self.measurementProgressBar.setProperty("value", 0)
        self.measurementProgressBar.setObjectName("measurementProgressBar")
        self.verticalStatusLayout.addWidget(self.measurementProgressBar)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.generalProgressLabel.setFont(font)
        self.generalProgressLabel.setObjectName("generalProgressLabel")
        self.verticalStatusLayout.addWidget(self.generalProgressLabel)
        font = QtGui.QFont()
        font.setPointSize(6)
        self.generalProgressBar.setFont(font)
        self.generalProgressBar.setProperty("value", 0)
        self.generalProgressBar.setObjectName("generalProgressBar")
        self.verticalStatusLayout.addWidget(self.generalProgressBar)
        self.gridStatusLayout.addLayout(self.verticalStatusLayout, 2, 3, 1, 1)
        self.gridCentralLayout.addLayout(self.gridStatusLayout, 7, 0, 1, 2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.streamingButton.setFont(font)
        self.streamingButton.setObjectName("streamingButton")
        self.gridCentralLayout.addWidget(self.streamingButton, 3, 1, 1, 1)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.videoLabel.setFont(font)
        self.videoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.videoLabel.setObjectName("videoLabel")
        self.gridCentralLayout.addWidget(self.videoLabel, 1, 1, 1, 1)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridCentralLayout.addWidget(self.line, 6, 0, 1, 2)
        self.parentTabWidget.setMinimumSize(QtCore.QSize(650, 0))
        self.parentTabWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.parentTabWidget.setObjectName("parentTabWidget")
        self.standardsTab.setObjectName("standardsTab")
        self.standardsGridLayout.setObjectName("standardsGridLayout")
        self.decadeBoxGroupBox.setObjectName("decadeBoxGroupBox")
        self.decadeBoxFormLayout.setObjectName("decadeBoxFormLayout")
        self.decadeBoxBrandLabel.setObjectName("decadeBoxBrandLabel")
        self.decadeBoxFormLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.decadeBoxBrandLabel)
        self.decadeBoxBrandLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.decadeBoxBrandLineEdit.setReadOnly(False)
        self.decadeBoxBrandLineEdit.setObjectName("decadeBoxBrandLineEdit")
        self.decadeBoxFormLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.decadeBoxBrandLineEdit)
        self.decadeBoxModelLabel.setObjectName("decadeBoxModelLabel")
        self.decadeBoxFormLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.decadeBoxModelLabel)
        self.decadeBoxModelLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.decadeBoxModelLineEdit.setReadOnly(True)
        self.decadeBoxModelLineEdit.setObjectName("decadeBoxModelLineEdit")
        self.decadeBoxFormLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.decadeBoxModelLineEdit)
        self.decadeBoxSerialNumberLabel.setObjectName("decadeBoxSerialNumberLabel")
        self.decadeBoxFormLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.decadeBoxSerialNumberLabel)
        self.decadeBoxSerialNumberLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.decadeBoxSerialNumberLineEdit.setReadOnly(False)
        self.decadeBoxSerialNumberLineEdit.setObjectName("decadeBoxSerialNumberLineEdit")
        self.decadeBoxFormLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.decadeBoxSerialNumberLineEdit)
        self.decadeBoxIdentificationLabel.setObjectName("decadeBoxIdentificationLabel")
        self.decadeBoxFormLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.decadeBoxIdentificationLabel)
        self.decadeBoxIdentificationLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.decadeBoxIdentificationLineEdit.setReadOnly(False)
        self.decadeBoxIdentificationLineEdit.setObjectName("decadeBoxIdentificationLineEdit")
        self.decadeBoxFormLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.decadeBoxIdentificationLineEdit)
        self.standardsGridLayout.addWidget(self.decadeBoxGroupBox, 0, 1, 1, 1)
        self.afgGroupBox.setObjectName("afgGroupBox")
        self.afgFormLayout.setObjectName("afgFormLayout")
        self.afgBrandLabel.setObjectName("afgBrandLabel")
        self.afgFormLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.afgBrandLabel)
        self.afgBrandLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.afgBrandLineEdit.setReadOnly(False)
        self.afgBrandLineEdit.setObjectName("afgBrandLineEdit")
        self.afgFormLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.afgBrandLineEdit)
        self.afgModelLabel.setObjectName("afgModelLabel")
        self.afgFormLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.afgModelLabel)
        self.afgModelLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.afgModelLineEdit.setObjectName("afgModelLineEdit")
        self.afgFormLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.afgModelLineEdit)
        self.afgSerialNumberLabel.setObjectName("afgSerialNumberLabel")
        self.afgFormLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.afgSerialNumberLabel)
        self.afgSerialNumberLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.afgSerialNumberLineEdit.setReadOnly(False)
        self.afgSerialNumberLineEdit.setObjectName("afgSerialNumberLineEdit")
        self.afgFormLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.afgSerialNumberLineEdit)
        self.afgIdentificationLabel.setObjectName("afgIdentificationLabel")
        self.afgFormLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.afgIdentificationLabel)
        self.afgIdentificationLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.afgIdentificationLineEdit.setReadOnly(False)
        self.afgIdentificationLineEdit.setObjectName("afgIdentificationLineEdit")
        self.afgFormLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.afgIdentificationLineEdit)
        self.afgGPIBbusLabel.setObjectName("afgGPIBbusLabel")
        self.afgFormLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.afgGPIBbusLabel)
        self.afgGPIBbusLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.afgGPIBbusLineEdit.setReadOnly(False)
        self.afgGPIBbusLineEdit.setObjectName("afgGPIBbusLineEdit")
        self.afgFormLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.afgGPIBbusLineEdit)
        self.afgGPIBChannelLabel.setObjectName("afgGPIBChannelLabel")
        self.afgFormLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.afgGPIBChannelLabel)
        self.afgGPIBChannelComboBox.setEnabled(True)
        self.afgGPIBChannelComboBox.setObjectName("afgGPIBChannelComboBox")
        for i in range(23):
            self.afgGPIBChannelComboBox.addItem("")
        self.afgFormLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.afgGPIBChannelComboBox)
        self.afgSelfTestLabel.setObjectName("afgSelfTestLabel")
        self.afgFormLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.afgSelfTestLabel)
        self.afgSelfTestCheckBox.setEnabled(False)
        self.afgSelfTestCheckBox.setObjectName("afgSelfTestCheckBox")
        self.afgFormLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.afgSelfTestCheckBox)
        self.standardsGridLayout.addWidget(self.afgGroupBox, 0, 0, 1, 1)
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
        self.standardsGridLayout.addWidget(self.multimeterGroupBox, 1, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.standardsGridLayout.addItem(spacerItem, 2, 1, 1, 1)
        self.saveStandardsInfo.setObjectName("saveStandardsInfo")
        self.standardsGridLayout.addWidget(self.saveStandardsInfo, 2, 1, 1, 1)
        self.parentTabWidget.addTab(self.standardsTab, "")
        self.infoTab.setObjectName("infoTab")
        self.infoGridLayout.setObjectName("infoGridLayout")
        self.preampGroupBox.setObjectName("preampGroupBox")
        self.preampFormLayout.setObjectName("preampFormLayout")
        self.preampBrandLabel.setObjectName("preampBrandLabel")
        self.preampFormLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.preampBrandLabel)
        self.preampBrandLineEdit.setObjectName("preampBrandLineEdit")
        self.preampFormLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.preampBrandLineEdit)
        self.preampBrandLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.preampModelLabel.setObjectName("preampModelLabel")
        self.preampFormLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.preampModelLabel)
        self.preampModelLineEdit.setObjectName("preampModelLineEdit")
        self.preampFormLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.preampModelLineEdit)
        self.preampModelLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.preampSerialLabel.setObjectName("preampSerialLabel")
        self.preampFormLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.preampSerialLabel)
        self.preampSerialLineEdit.setObjectName("preampSerialLineEdit")
        self.preampFormLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.preampSerialLineEdit)
        self.preampSerialLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.infoGridLayout.addWidget(self.preampGroupBox, 1, 1, 1, 1)
        self.customerGroupBox.setObjectName("customerGroupBox")
        self.customerFormLayout.setObjectName("customerFormLayout")
        self.customerNameLabel.setObjectName("customerNameLabel")
        self.customerFormLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.customerNameLabel)
        self.customerNameLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.customerNameLineEdit.setObjectName("customerNameLineEdit")
        self.customerFormLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.customerNameLineEdit)
        self.addressLabel.setObjectName("addressLabel")
        self.customerFormLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.addressLabel)
        self.addressLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.addressLineEdit.setObjectName("addressLineEdit")
        self.customerFormLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.addressLineEdit)
        self.cityLabel.setObjectName("cityLabel")
        self.customerFormLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.cityLabel)
        self.cityLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.cityLineEdit.setObjectName("cityLineEdit")
        self.customerFormLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.cityLineEdit)
        self.countryLabel.setObjectName("countryLabel")
        self.customerFormLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.countryLabel)
        self.countryLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.countryLineEdit.setObjectName("countryLineEdit")
        self.customerFormLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.countryLineEdit)
        self.postalCodeLabel.setObjectName("postalCodeLabel")
        self.customerFormLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.postalCodeLabel)
        self.postalCodeLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.postalCodeLineEdit.setObjectName("postalCodeLineEdit")
        self.customerFormLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.postalCodeLineEdit)
        self.contactNumberLabel.setObjectName("contactNumberLabel")
        self.customerFormLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.contactNumberLabel)
        self.contactNumberLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.contactNumberLineEdit.setObjectName("contactNumberLineEdit")
        self.customerFormLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.contactNumberLineEdit)
        self.infoGridLayout.addWidget(self.customerGroupBox, 0, 1, 1, 1)
        self.saveDUTInfo.setObjectName("saveDUTInfo")
        self.infoGridLayout.addWidget(self.saveDUTInfo, 3, 0, 1, 1)
        self.dutGroupBox.setObjectName("dutGroupBox")
        self.dutFormLayout.setObjectName("dutFormLayout")
        self.consecutiveLabel.setObjectName("consecutiveLabel")
        self.dutFormLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.consecutiveLabel)
        self.consecutiveLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.consecutiveLineEdit.setObjectName("consecutiveLineEdit")
        self.dutFormLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.consecutiveLineEdit)
        self.dutBrandLabel.setObjectName("dutBrandLabel")
        self.dutFormLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.dutBrandLabel)
        self.dutBrandLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.dutBrandLineEdit.setObjectName("dutBrandLineEdit")
        self.dutFormLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.dutBrandLineEdit)
        self.dutModelLabel.setObjectName("dutModelLabel")
        self.dutFormLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.dutModelLabel)
        self.dutModelLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.dutModelLineEdit.setObjectName("dutModelLineEdit")
        self.dutFormLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.dutModelLineEdit)
        self.dutSerialNumberLabel.setObjectName("dutSerialNumberLabel")
        self.dutFormLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.dutSerialNumberLabel)
        self.dutSerialNumberLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.dutSerialNumberLineEdit.setObjectName("dutSerialNumberLineEdit")
        self.dutFormLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.dutSerialNumberLineEdit)
        self.dutIdentificationLabel.setObjectName("dutIdentificationLabel")
        self.dutFormLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.dutIdentificationLabel)
        self.dutIdentificationLineEdit.setObjectName("dutIdentificationLineEdit")
        self.dutFormLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.dutIdentificationLineEdit)
        self.dutIdentificationLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.dutClassLabel.setObjectName("dutClassLabel")
        self.dutFormLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.dutClassLabel)
        self.dutClassComboBox.setObjectName("dutClassComboBox")
        self.dutClassComboBox.addItem("")
        self.dutClassComboBox.addItem("")
        self.dutFormLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.dutClassComboBox)
        self.supplyULimitLabel.setObjectName("supplyULimitLabel")
        self.dutFormLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.supplyULimitLabel)
        self.supplyULimitLineEdit.setObjectName("supplyULimitLineEdit")
        self.dutFormLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.supplyULimitLineEdit)
        self.supplyULimitLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.supplyLLimitLabel.setObjectName("supplyLLimitLabel")
        self.dutFormLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.supplyLLimitLabel)
        self.supplyLLimitLineEdit.setObjectName("supplyLLimitLineEdit")
        self.dutFormLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.supplyLLimitLineEdit)
        self.supplyLLimitLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.referenceLevelLabel.setObjectName("referenceLevelLabel")
        self.dutFormLayout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.referenceLevelLabel)
        self.referenceLevelLineEdit.setObjectName("referenceLevelLineEdit")
        self.dutFormLayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.referenceLevelLineEdit)
        self.referenceLevelLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lu1kHzLabel.setObjectName("lu1kHzLabel")
        self.dutFormLayout.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.lu1kHzLabel)
        self.lu1kHzLineEdit.setObjectName("lu1kHzLineEdit")
        self.dutFormLayout.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.lu1kHzLineEdit)
        self.lu1kHzLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lu8kHzLabel.setObjectName("lu8kHzLabel")
        self.dutFormLayout.setWidget(10, QtWidgets.QFormLayout.LabelRole, self.lu8kHzLabel)
        self.lu8kHzLineEdit.setObjectName("lu8kHzLineEdit")
        self.dutFormLayout.setWidget(10, QtWidgets.QFormLayout.FieldRole, self.lu8kHzLineEdit)
        self.lu8kHzLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.li8kHzLabel.setObjectName("li8kHzLabel")
        self.dutFormLayout.setWidget(11, QtWidgets.QFormLayout.LabelRole, self.li8kHzLabel)
        self.li8kHzLineEdit.setObjectName("li8kHzLineEdit")
        self.dutFormLayout.setWidget(11, QtWidgets.QFormLayout.FieldRole, self.li8kHzLineEdit)
        self.li8kHzLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.startPointLabel.setObjectName("startPointLabel")
        self.dutFormLayout.setWidget(12, QtWidgets.QFormLayout.LabelRole, self.startPointLabel)
        self.startPointLineEdit.setObjectName("startPointLineEdit")
        self.dutFormLayout.setWidget(12, QtWidgets.QFormLayout.FieldRole, self.startPointLineEdit)
        self.startPointLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.screenRateLabel.setObjectName('screenRateLabel')
        self.dutFormLayout.setWidget(13, QtWidgets.QFormLayout.LabelRole, self.screenRateLabel)
        self.screenRateLineEdit.setObjectName('screenRateLineEdit')
        self.dutFormLayout.setWidget(13, QtWidgets.QFormLayout.FieldRole, self.screenRateLineEdit)
        self.screenRateLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.loadFreeFieldPushButton.setObjectName("loadFreeFieldPushButton")
        self.dutFormLayout.setWidget(14, QtWidgets.QFormLayout.SpanningRole, self.loadFreeFieldPushButton)
        self.infoGridLayout.addWidget(self.dutGroupBox, 0, 0, 3, 1)
        self.micGroupBox.setObjectName("micGroupBox")
        self.micFormLayout.setObjectName("micFormLayout")
        self.micBrandLabel.setObjectName("micBrandLabel")
        self.micFormLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.micBrandLabel)
        self.micBrandLineEdit.setObjectName("micBrandLineEdit")
        self.micFormLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.micBrandLineEdit)
        self.micBrandLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.micModelLabel.setObjectName("micModelLabel")
        self.micFormLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.micModelLabel)
        self.micModelLineEdit.setObjectName("micModelLineEdit")
        self.micFormLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.micModelLineEdit)
        self.micModelLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.micSerialNumberLabel.setObjectName("micSerialNumberLabel")
        self.micFormLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.micSerialNumberLabel)
        self.micSerialNumberLineEdit.setObjectName("micSerialNumberLineEdit")
        self.micFormLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.micSerialNumberLineEdit)
        self.micSerialNumberLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.infoGridLayout.addWidget(self.micGroupBox, 2, 1, 2, 1)
        self.parentTabWidget.addTab(self.infoTab, "")
        self.preTestsTab.setObjectName("preTestsTab")
        self.preTestVLayout.setObjectName("preTestVLayout")
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.supplyLabel.setFont(font)
        self.supplyLabel.setObjectName("supplyLabel")
        self.preTestVLayout.addWidget(self.supplyLabel)
        self.supplyGridLayout.setContentsMargins(-1, 0, -1, -1)
        self.supplyGridLayout.setHorizontalSpacing(6)
        self.supplyGridLayout.setObjectName("supplyGridLayout")
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.electricTestsLabel.setFont(font)
        self.electricTestsLabel.setObjectName("electricTestsLabel")
        self.supplyGridLayout.addWidget(self.electricTestsLabel, 3, 0, 1, 1)
        self.beforeLabel.setMinimumSize(QtCore.QSize(150, 0))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.beforeLabel.setFont(font)
        self.beforeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.beforeLabel.setObjectName("beforeLabel")
        self.supplyGridLayout.addWidget(self.beforeLabel, 1, 1, 1, 2)
        self.afterLabel.setMinimumSize(QtCore.QSize(150, 0))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.afterLabel.setFont(font)
        self.afterLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.afterLabel.setObjectName("afterLabel")
        self.supplyGridLayout.addWidget(self.afterLabel, 1, 4, 1, 2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.afterElecUnitsLabel.setFont(font)
        self.afterElecUnitsLabel.setObjectName("afterElecUnitsLabel")
        self.supplyGridLayout.addWidget(self.afterElecUnitsLabel, 3, 5, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.supplyGridLayout.addItem(spacerItem1, 1, 8, 3, 1)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.beforeAcusUnitsLabel.setFont(font)
        self.beforeAcusUnitsLabel.setObjectName("beforeAcusUnitsLabel")
        self.supplyGridLayout.addWidget(self.beforeAcusUnitsLabel, 2, 2, 1, 1)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.beforeElecValLabel.setFont(font)
        self.beforeElecValLabel.setText("")
        self.beforeElecValLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.beforeElecValLabel.setObjectName("beforeElecValLabel")
        self.supplyGridLayout.addWidget(self.beforeElecValLabel, 3, 1, 1, 1)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.beforeAcusValLabel.setFont(font)
        self.beforeAcusValLabel.setText("")
        self.beforeAcusValLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.beforeAcusValLabel.setObjectName("beforeAcusValLabel")
        self.supplyGridLayout.addWidget(self.beforeAcusValLabel, 2, 1, 1, 1)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.acousticTestsLabel.setFont(font)
        self.acousticTestsLabel.setObjectName("acousticTestsLabel")
        self.supplyGridLayout.addWidget(self.acousticTestsLabel, 2, 0, 1, 1)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.afterElecValLabel.setFont(font)
        self.afterElecValLabel.setText("")
        self.afterElecValLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.afterElecValLabel.setObjectName("afterElecValLabel")
        self.supplyGridLayout.addWidget(self.afterElecValLabel, 3, 4, 1, 1)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.afterAcusValLabel.setFont(font)
        self.afterAcusValLabel.setText("")
        self.afterAcusValLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.afterAcusValLabel.setObjectName("afterAcusValLabel")
        self.supplyGridLayout.addWidget(self.afterAcusValLabel, 2, 4, 1, 1)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.afterAcusUnitsLabel.setFont(font)
        self.afterAcusUnitsLabel.setObjectName("afterAcusUnitsLabel")
        self.supplyGridLayout.addWidget(self.afterAcusUnitsLabel, 2, 5, 1, 1)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.beforeElecUnitsLabel.setFont(font)
        self.beforeElecUnitsLabel.setObjectName("beforeElecUnitsLabel")
        self.supplyGridLayout.addWidget(self.beforeElecUnitsLabel, 3, 2, 1, 1)
        self.supplyVLine1.setFrameShape(QtWidgets.QFrame.VLine)
        self.supplyVLine1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.supplyVLine1.setObjectName("supplyVLine1")
        self.supplyGridLayout.addWidget(self.supplyVLine1, 1, 3, 3, 1)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.supplyVLine2.setFrameShape(QtWidgets.QFrame.VLine)
        self.supplyVLine2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.supplyVLine2.setObjectName("supplyVLine2")
        self.supplyGridLayout.addWidget(self.supplyVLine2, 1, 6, 3, 1)
        self.preTestVLayout.addLayout(self.supplyGridLayout)
        self.preliminarHLine1.setFrameShape(QtWidgets.QFrame.HLine)
        self.preliminarHLine1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.preliminarHLine1.setObjectName("preliminarHLine1")
        self.preTestVLayout.addWidget(self.preliminarHLine1)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.calIndLabel.setFont(font)
        self.calIndLabel.setObjectName("calIndLabel")
        self.preTestVLayout.addWidget(self.calIndLabel)
        self.calIndGridLayout.setObjectName("calIndGridLayout")
        font = QtGui.QFont()
        font.setPointSize(8)
        self.initAdjUnitsLabel.setFont(font)
        self.initAdjUnitsLabel.setObjectName("initAdjUnitsLabel")
        self.calIndGridLayout.addWidget(self.initAdjUnitsLabel, 0, 2, 1, 1)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.adjLabel.setFont(font)
        self.adjLabel.setObjectName("adjLabel")
        self.calIndGridLayout.addWidget(self.adjLabel, 4, 0, 1, 1)
        self.adjLabel.setAlignment(QtCore.Qt.AlignTop)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.beforeAdjLabel.setFont(font)
        self.beforeAdjLabel.setObjectName("beforeAdjLabel")
        self.calIndGridLayout.addWidget(self.beforeAdjLabel, 3, 0, 1, 1)
        self.beforeAdjLabel.setAlignment(QtCore.Qt.AlignTop)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.afterAdjLabel.setFont(font)
        self.afterAdjLabel.setObjectName("afterAdjLabel")
        self.calIndGridLayout.addWidget(self.afterAdjLabel, 5, 0, 1, 1)
        self.afterAdjLabel.setAlignment(QtCore.Qt.AlignTop)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.initAdjLabel.setFont(font)
        self.initAdjLabel.setObjectName("initAdjLabel")
        self.calIndGridLayout.addWidget(self.initAdjLabel, 0, 0, 1, 1)
        self.adjEdit.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.adjEdit.setFont(font)
        self.adjEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.adjEdit.setObjectName("adjEdit")
        self.calIndGridLayout.addWidget(self.adjEdit, 0, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.calIndGridLayout.addItem(spacerItem2, 0, 3, 1, 1)
        self.adjSaveButton.setObjectName("adjSaveButton")
        self.calIndGridLayout.addWidget(self.adjSaveButton, 0, 4, 1, 1)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.repliesLabel.setFont(font)
        self.repliesLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.repliesLabel.setObjectName("repliesLabel")
        self.calIndGridLayout.addWidget(self.repliesLabel, 1, 1, 1, 4)
        self.adjTableView.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.adjTableView.setFont(font)
        self.adjTableView.setObjectName("adjTableView")
        self.calIndGridLayout.addWidget(self.adjTableView, 2, 1, 4, 4)
        self.adjTableView.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.adjTableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.adjTableView.verticalHeader().setVisible(False)
        self.adjTableView.setModel(self.adjTableModel)
        self.preTestVLayout.addLayout(self.calIndGridLayout)
        self.preliminarHLine2.setFrameShape(QtWidgets.QFrame.HLine)
        self.preliminarHLine2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.preliminarHLine2.setObjectName("preliminarHLine2")
        self.preTestVLayout.addWidget(self.preliminarHLine2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.vRefTitleLabel.setFont(font)
        self.vRefTitleLabel.setObjectName("vRefTitleLabel")
        self.preTestVLayout.addWidget(self.vRefTitleLabel)
        self.vRefGridLayout.setObjectName("vRefGridLayout")
        self.vuRefLineEdit.setMaximumSize(QtCore.QSize(100, 16777215))
        self.vuRefLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.vuRefLineEdit.setObjectName("vuRefLineEdit")
        self.vRefGridLayout.addWidget(self.vuRefLineEdit, 1, 2, 1, 1)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.vuRefLabel.setFont(font)
        self.vuRefLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.vuRefLabel.setObjectName("vuRefLabel")
        self.vRefGridLayout.addWidget(self.vuRefLabel, 0, 2, 1, 1)
        self.vRefVLine1.setFrameShape(QtWidgets.QFrame.VLine)
        self.vRefVLine1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.vRefVLine1.setObjectName("vRefVLine1")
        self.vRefGridLayout.addWidget(self.vRefVLine1, 0, 1, 2, 1)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.vRefLabel.setFont(font)
        self.vRefLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.vRefLabel.setObjectName("vRefLabel")
        self.vRefGridLayout.addWidget(self.vRefLabel, 0, 6, 1, 1)
        self.vRefValueLabel.setText("")
        self.vRefValueLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.vRefValueLabel.setObjectName("vRefValueLabel")
        self.vRefGridLayout.addWidget(self.vRefValueLabel, 1, 6, 1, 1)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lvRefLabel.setFont(font)
        self.lvRefLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.lvRefLabel.setObjectName("lvRefLabel")
        self.vRefGridLayout.addWidget(self.lvRefLabel, 0, 4, 1, 1)
        self.viRefLineEdit.setMaximumSize(QtCore.QSize(100, 16777215))
        self.viRefLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.viRefLineEdit.setObjectName("viRefLineEdit")
        self.vRefGridLayout.addWidget(self.viRefLineEdit, 1, 0, 1, 1)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.viRefLabel.setFont(font)
        self.viRefLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.viRefLabel.setObjectName("viRefLabel")
        self.vRefGridLayout.addWidget(self.viRefLabel, 0, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.vRefGridLayout.addItem(spacerItem3, 0, 10, 2, 1)
        self.vRefVLine3.setFrameShape(QtWidgets.QFrame.VLine)
        self.vRefVLine3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.vRefVLine3.setObjectName("vRefVLine3")
        self.vRefGridLayout.addWidget(self.vRefVLine3, 0, 5, 2, 1)
        self.vRefVLine2.setFrameShape(QtWidgets.QFrame.VLine)
        self.vRefVLine2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.vRefVLine2.setObjectName("vRefVLine2")
        self.vRefGridLayout.addWidget(self.vRefVLine2, 0, 3, 2, 1)
        self.lvValueLabel.setText("")
        self.lvValueLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.lvValueLabel.setObjectName("lvValueLabel")
        self.vRefGridLayout.addWidget(self.lvValueLabel, 1, 4, 1, 1)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.vRefButton.setFont(font)
        self.vRefButton.setObjectName("vRefButton")
        self.vRefGridLayout.addWidget(self.vRefButton, 0, 8, 2, 1)
        self.saveVRefButton.setFont(font)
        self.saveVRefButton.setObjectName("saveVRefButton")
        self.vRefGridLayout.addWidget(self.saveVRefButton, 0, 9, 2, 1)
        self.vRefVLine4.setFrameShape(QtWidgets.QFrame.VLine)
        self.vRefVLine4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.vRefVLine4.setObjectName("vRefVLine4")
        self.vRefGridLayout.addWidget(self.vRefVLine4, 0, 7, 2, 1)
        self.preTestVLayout.addLayout(self.vRefGridLayout)
        self.parentTabWidget.addTab(self.preTestsTab, "")
        self.preTestsTab.setEnabled(True)
        self.weightingsTab.setObjectName("weightingsTab")
        self.weightingsTab.setEnabled(False)
        self.weightingsGridLayout.setObjectName("weightingsGridLayout")
        self.aWTableView.setObjectName("aWTableView")
        self.weightingsGridLayout.addWidget(self.aWTableView, 1, 0, 1, 1)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.zWeightLabel.setFont(font)
        self.zWeightLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.zWeightLabel.setObjectName("zWeightLabel")
        self.weightingsGridLayout.addWidget(self.zWeightLabel, 4, 0, 1, 1)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.cWeightLabel.setFont(font)
        self.cWeightLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.cWeightLabel.setObjectName("cWeightLabel")
        self.weightingsGridLayout.addWidget(self.cWeightLabel, 2, 0, 1, 1)
        self.cWTableView.setObjectName("cWTableView")
        self.weightingsGridLayout.addWidget(self.cWTableView, 3, 0, 1, 1)
        self.zWTableView.setObjectName("zWTableView")
        self.weightingsGridLayout.addWidget(self.zWTableView, 5, 0, 1, 1)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.aWeightLabel.setFont(font)
        self.aWeightLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.aWeightLabel.setObjectName("aWeightLabel")
        self.weightingsGridLayout.addWidget(self.aWeightLabel, 0, 0, 1, 1)
        self.fW1kGridLayout.setObjectName("fW1kGridLayout")
        self.fWVLine4.setFrameShape(QtWidgets.QFrame.VLine)
        self.fWVLine4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.fWVLine4.setObjectName("fWVLine4")
        self.fW1kGridLayout.addWidget(self.fWVLine4, 2, 1, 5, 1)
        self.bW1kHzLevLabel.setText("")
        self.bW1kHzLevLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.bW1kHzLevLabel.setObjectName("bW1kHzLevLabel")
        self.fW1kGridLayout.addWidget(self.bW1kHzLevLabel, 4, 2, 1, 1)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.aW1kHzLabel.setFont(font)
        self.aW1kHzLabel.setObjectName("aW1kHzLabel")
        self.fW1kGridLayout.addWidget(self.aW1kHzLabel, 2, 0, 1, 1)
        self.aW1kHzLevLabel.setText("")
        self.aW1kHzLevLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.aW1kHzLevLabel.setObjectName("aW1kHzLevLabel")
        self.fW1kGridLayout.addWidget(self.aW1kHzLevLabel, 2, 2, 1, 1)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.bW1kHzLabel.setFont(font)
        self.bW1kHzLabel.setObjectName("bW1kHzLabel")
        self.fW1kGridLayout.addWidget(self.bW1kHzLabel, 4, 0, 1, 1)
        self.aW1kHzRLevLabel.setText("")
        self.aW1kHzRLevLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.aW1kHzRLevLabel.setObjectName("aW1kHzRLevLabel")
        self.fW1kGridLayout.addWidget(self.aW1kHzRLevLabel, 2, 4, 1, 1)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.cW1kHzLabel.setFont(font)
        self.cW1kHzLabel.setObjectName("cW1kHzLabel")
        self.fW1kGridLayout.addWidget(self.cW1kHzLabel, 6, 0, 1, 1)
        self.cW1kHzLevLabel.setText("")
        self.cW1kHzLevLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.cW1kHzLevLabel.setObjectName("cW1kHzLevLabel")
        self.fW1kGridLayout.addWidget(self.cW1kHzLevLabel, 6, 2, 1, 1)
        self.fWRLevLabel.setMinimumSize(QtCore.QSize(75, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.fWRLevLabel.setFont(font)
        self.fWRLevLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.fWRLevLabel.setObjectName("fWRLevLabel")
        self.fW1kGridLayout.addWidget(self.fWRLevLabel, 0, 4, 1, 1)
        self.cW1kHzRLevLabel.setText("")
        self.cW1kHzRLevLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.cW1kHzRLevLabel.setObjectName("cW1kHzRLevLabel")
        self.fW1kGridLayout.addWidget(self.cW1kHzRLevLabel, 6, 4, 1, 1)
        self.fWLevLabel.setMinimumSize(QtCore.QSize(75, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.fWLevLabel.setFont(font)
        self.fWLevLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.fWLevLabel.setObjectName("fWLevLabel")
        self.fW1kGridLayout.addWidget(self.fWLevLabel, 0, 2, 1, 1)
        self.bW1kHzRLevLabel.setText("")
        self.bW1kHzRLevLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.bW1kHzRLevLabel.setObjectName("bW1kHzRLevLabel")
        self.fW1kGridLayout.addWidget(self.bW1kHzRLevLabel, 4, 4, 1, 1)
        self.fWVLine2.setFrameShape(QtWidgets.QFrame.VLine)
        self.fWVLine2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.fWVLine2.setObjectName("fWVLine2")
        self.fW1kGridLayout.addWidget(self.fWVLine2, 0, 1, 1, 1)
        self.fWVLine3.setFrameShape(QtWidgets.QFrame.VLine)
        self.fWVLine3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.fWVLine3.setObjectName("fWVLine3")
        self.fW1kGridLayout.addWidget(self.fWVLine3, 0, 3, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.fW1kGridLayout.addItem(spacerItem4, 5, 2, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.fW1kGridLayout.addItem(spacerItem5, 3, 2, 1, 1)
        self.fWVLine1.setFrameShape(QtWidgets.QFrame.VLine)
        self.fWVLine1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.fWVLine1.setObjectName("fWVLine1")
        self.fW1kGridLayout.addWidget(self.fWVLine1, 2, 3, 5, 1)
        self.fWHLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.fWHLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.fWHLine.setObjectName("fWHLine")
        self.fW1kGridLayout.addWidget(self.fWHLine, 1, 0, 1, 5)
        self.weightingsGridLayout.addLayout(self.fW1kGridLayout, 1, 2, 1, 1)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.fW1kHzLabel.setFont(font)
        self.fW1kHzLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.fW1kHzLabel.setObjectName("fW1kHzLabel")
        self.weightingsGridLayout.addWidget(self.fW1kHzLabel, 0, 2, 1, 1)
        self.weightingsVLine.setFrameShape(QtWidgets.QFrame.VLine)
        self.weightingsVLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.weightingsVLine.setObjectName("weightingsVLine")
        self.weightingsGridLayout.addWidget(self.weightingsVLine, 0, 1, 6, 1)
        self.tWGridLayout.setObjectName("tWGridLayout")
        self.tWHLine1.setFrameShape(QtWidgets.QFrame.HLine)
        self.tWHLine1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.tWHLine1.setObjectName("tWHLine1")
        self.tWGridLayout.addWidget(self.tWHLine1, 1, 1, 1, 5)
        self.slowWLevLabel.setText("")
        self.slowWLevLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.slowWLevLabel.setObjectName("slowWLevLabel")
        self.tWGridLayout.addWidget(self.slowWLevLabel, 4, 3, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.tWGridLayout.addItem(spacerItem6, 3, 3, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.tWGridLayout.addItem(spacerItem7, 5, 3, 1, 1)
        self.slowWRLevLabel.setText("")
        self.slowWRLevLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.slowWRLevLabel.setObjectName("slowWRLevLabel")
        self.tWGridLayout.addWidget(self.slowWRLevLabel, 4, 5, 1, 1)
        self.eqWLevLineEdit.setText("")
        self.eqWLevLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.eqWLevLineEdit.setObjectName("eqWLevLineEdit")
        self.tWGridLayout.addWidget(self.eqWLevLineEdit, 6, 3, 1, 1)
        self.eqWLevLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.eqWRLevLabel.setText("")
        self.eqWRLevLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.eqWRLevLabel.setObjectName("eqWRLevLabel")
        self.tWGridLayout.addWidget(self.eqWRLevLabel, 6, 5, 1, 1)
        self.fastWRLevLabel.setText("")
        self.fastWRLevLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.fastWRLevLabel.setObjectName("fastWRLevLabel")
        self.tWGridLayout.addWidget(self.fastWRLevLabel, 2, 5, 1, 1)
        self.fastWLevLabel.setText("")
        self.fastWLevLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.fastWLevLabel.setObjectName("fastWLevLabel")
        self.tWGridLayout.addWidget(self.fastWLevLabel, 2, 3, 1, 1)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.slowWLabel.setFont(font)
        self.slowWLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.slowWLabel.setObjectName("slowWLabel")
        self.tWGridLayout.addWidget(self.slowWLabel, 4, 1, 1, 1)
        self.tWRLevLabel.setMinimumSize(QtCore.QSize(75, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.tWRLevLabel.setFont(font)
        self.tWRLevLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.tWRLevLabel.setObjectName("tWRLevLabel")
        self.tWGridLayout.addWidget(self.tWRLevLabel, 0, 5, 1, 1)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.fastWLabel.setFont(font)
        self.fastWLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.fastWLabel.setObjectName("fastWLabel")
        self.tWGridLayout.addWidget(self.fastWLabel, 2, 1, 1, 1)
        self.tWLevLabel.setMinimumSize(QtCore.QSize(75, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.tWLevLabel.setFont(font)
        self.tWLevLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.tWLevLabel.setObjectName("tWLevLabel")
        self.tWGridLayout.addWidget(self.tWLevLabel, 0, 3, 1, 1)
        self.tWVLine1.setFrameShape(QtWidgets.QFrame.VLine)
        self.tWVLine1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.tWVLine1.setObjectName("tWVLine1")
        self.tWGridLayout.addWidget(self.tWVLine1, 2, 2, 5, 1)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.eqWLabel.setFont(font)
        self.eqWLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.eqWLabel.setObjectName("eqWLabel")
        self.tWGridLayout.addWidget(self.eqWLabel, 6, 1, 1, 1)
        self.tWHLine2.setFrameShape(QtWidgets.QFrame.VLine)
        self.tWHLine2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.tWHLine2.setObjectName("tWHLine2")
        self.tWGridLayout.addWidget(self.tWHLine2, 2, 4, 5, 1)
        self.tWVLine3.setFrameShape(QtWidgets.QFrame.VLine)
        self.tWVLine3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.tWVLine3.setObjectName("tWVLine3")
        self.tWGridLayout.addWidget(self.tWVLine3, 0, 2, 1, 1)
        self.tWVLine4.setFrameShape(QtWidgets.QFrame.VLine)
        self.tWVLine4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.tWVLine4.setObjectName("tWVLine4")
        self.tWGridLayout.addWidget(self.tWVLine4, 0, 4, 1, 1)
        self.weightingsGridLayout.addLayout(self.tWGridLayout, 3, 2, 1, 1)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.tW1kHzLabel.setFont(font)
        self.tW1kHzLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.tW1kHzLabel.setObjectName("tW1kHzLabel")
        self.weightingsGridLayout.addWidget(self.tW1kHzLabel, 2, 2, 1, 1)
        self.parentTabWidget.addTab(self.weightingsTab, "")
        self.linearityTab.setObjectName("linearityTab")
        self.linearityTab.setEnabled(False)
        self.linearityGridLayout.setObjectName("linearityGridLayout")
        self.linearityTableView.setObjectName("linearityTableView")
        self.linearityGridLayout.addWidget(self.linearityTableView, 0, 0, 1, 1)
        self.parentTabWidget.addTab(self.linearityTab, "")
        self.ambientConditionsTab.setObjectName("ambientConditionsTab")
        self.ambientConditionsTab.setEnabled(False)
        self.ambientGridLayout.setObjectName("ambientGridLayout")
        self.ambientTableView.setObjectName("ambientTableView")
        self.ambientGridLayout.addWidget(self.ambientTableView, 0, 0, 1, 1)
        self.parentTabWidget.addTab(self.ambientConditionsTab, "")
        self.gridCentralLayout.addWidget(self.parentTabWidget, 0, 0, 4, 1)
        self.setCentralWidget(self.centralWidget)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1320, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile.setObjectName("menuFile")
        self.menuCalibration.setObjectName("menuCalibration")
        self.menuTools.setObjectName("menuTools")
        self.setMenuBar(self.menubar)
        self.toolBar.setObjectName("toolBar")
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLoadCalibration.setIcon(icon)
        self.actionLoadCalibration.setObjectName("actionLoadCalibration")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSaveCalibration.setIcon(icon1)
        self.actionSaveCalibration.setObjectName("actionSaveCalibration")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/searchInstruments.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSearchStandards.setIcon(icon2)
        self.actionSearchStandards.setObjectName("actionSearchStandards")
        self.actionSearchStandards.setEnabled(False)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/test.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSelfTest.setIcon(icon3)
        self.actionSelfTest.setObjectName("actionSelfTest")
        self.actionSelfTest.setEnabled(False)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/certificate.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionEmitCertificate.setIcon(icon4)
        self.actionEmitCertificate.setObjectName("actionEmitCertificate")
        self.actionEmitCertificate.setEnabled(False)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionStart.setIcon(icon5)
        self.actionStart.setObjectName("actionStart")
        self.actionStart.setEnabled(False)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPause.setIcon(icon6)
        self.actionPause.setObjectName("actionPause")
        self.actionPause.setEnabled(False)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRestart.setIcon(icon7)
        self.actionRestart.setObjectName("actionRestart")
        self.actionRestart.setEnabled(False)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icons/next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNextPoint.setIcon(icon8)
        self.actionNextPoint.setObjectName("actionNextPoint")
        self.actionNextPoint.setEnabled(False)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/icons/back.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPreviousPoint.setIcon(icon9)
        self.actionPreviousPoint.setObjectName("actionPreviousPoint")
        self.actionPreviousPoint.setEnabled(False)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/icons/next_next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNextTest.setIcon(icon10)
        self.actionNextTest.setObjectName("actionNextTest")
        self.actionNextTest.setEnabled(False)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/icons/back_back.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPreviousTest.setIcon(icon11)
        self.actionPreviousTest.setObjectName("actionPreviousTest")
        self.actionPreviousTest.setEnabled(False)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/icons/goTo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionGoToTest.setIcon(icon12)
        self.actionGoToTest.setObjectName("actionGoToTest")
        self.actionGoToTest.setEnabled(False)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(":/icons/goTo_goTo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionGoToPoint.setIcon(icon13)
        self.actionGoToPoint.setObjectName("actionGoToPoint")
        self.actionGoToPoint.setEnabled(False)
        self.menuFile.addAction(self.actionLoadCalibration)
        self.menuFile.addAction(self.actionSaveCalibration)
        self.menuCalibration.addAction(self.actionStart)
        self.menuCalibration.addAction(self.actionPause)
        self.menuCalibration.addAction(self.actionRestart)
        self.menuCalibration.addAction(self.actionNextPoint)
        self.menuCalibration.addAction(self.actionPreviousPoint)
        self.menuCalibration.addAction(self.actionGoToPoint)
        self.menuCalibration.addAction(self.actionNextTest)
        self.menuCalibration.addAction(self.actionPreviousTest)
        self.menuCalibration.addAction(self.actionGoToTest)
        self.menuTools.addAction(self.actionSearchStandards)
        self.menuTools.addAction(self.actionSelfTest)
        self.menuTools.addAction(self.actionEmitCertificate)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuCalibration.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.toolBar.addAction(self.actionLoadCalibration)
        self.toolBar.addAction(self.actionSaveCalibration)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionSearchStandards)
        self.toolBar.addAction(self.actionSelfTest)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionPreviousTest)
        self.toolBar.addAction(self.actionPreviousPoint)
        self.toolBar.addAction(self.actionStart)
        self.toolBar.addAction(self.actionPause)
        self.toolBar.addAction(self.actionNextPoint)
        self.toolBar.addAction(self.actionNextTest)
        self.toolBar.addAction(self.actionGoToPoint)
        self.toolBar.addAction(self.actionGoToTest)
        self.toolBar.addAction(self.actionRestart)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionEmitCertificate)

        self.translate_ui()
        self.set_tap_order()
        self.parentTabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)

        # Connecting signals
        self.afgModelLineEdit.returnPressed.connect(self.enable_search_standards)
        self.afgModelLineEdit.editingFinished.connect(self.enable_search_standards)
        self.multimeterModelLineEdit.returnPressed.connect(self.enable_search_standards)
        self.multimeterModelLineEdit.editingFinished.connect(self.enable_search_standards)

    def set_tap_order(self) -> None:
        """
        This method sets up the tap order of the elements of the GUI.
        """
        self.setTabOrder(self.afgBrandLineEdit, self.afgModelLineEdit)
        self.setTabOrder(self.afgModelLineEdit, self.afgSerialNumberLineEdit)
        self.setTabOrder(self.afgSerialNumberLineEdit, self.afgIdentificationLineEdit)
        self.setTabOrder(self.afgIdentificationLineEdit, self.afgGPIBbusLineEdit)
        self.setTabOrder(self.afgGPIBbusLineEdit, self.afgGPIBChannelComboBox)
        self.setTabOrder(self.afgGPIBChannelComboBox, self.afgSelfTestCheckBox)
        self.setTabOrder(self.afgSelfTestCheckBox, self.decadeBoxBrandLineEdit)
        self.setTabOrder(self.decadeBoxBrandLineEdit, self.decadeBoxModelLineEdit)
        self.setTabOrder(self.decadeBoxModelLineEdit, self.decadeBoxSerialNumberLineEdit)
        self.setTabOrder(self.decadeBoxSerialNumberLineEdit, self.decadeBoxIdentificationLineEdit)
        self.setTabOrder(self.decadeBoxIdentificationLineEdit, self.multimeterBrandLineEdit)
        self.setTabOrder(self.multimeterBrandLineEdit, self.multimeterModelLineEdit)
        self.setTabOrder(self.multimeterModelLineEdit, self.multimeterSerialNumberLineEdit)
        self.setTabOrder(self.multimeterSerialNumberLineEdit, self.multimeterIdentificationLineEdit)
        self.setTabOrder(self.multimeterIdentificationLineEdit, self.multimeterGPIBBusLineEdit)
        self.setTabOrder(self.multimeterGPIBBusLineEdit, self.multimeterGPIBChannelComboBox)
        self.setTabOrder(self.multimeterGPIBChannelComboBox, self.multimeterSelfTestCheckBox)
        self.setTabOrder(self.multimeterSelfTestCheckBox, self.saveStandardsInfo)
        self.setTabOrder(self.saveStandardsInfo, self.streamingButton)
        self.setTabOrder(self.streamingButton, self.videoView)
        self.setTabOrder(self.videoView, self.nextTestToolButton)
        self.setTabOrder(self.nextTestToolButton, self.previousTestToolButton)
        self.setTabOrder(self.previousTestToolButton, self.parentTabWidget)
        self.setTabOrder(self.parentTabWidget, self.consecutiveLineEdit)
        self.setTabOrder(self.consecutiveLineEdit, self.dutBrandLineEdit)
        self.setTabOrder(self.dutBrandLineEdit, self.dutModelLineEdit)
        self.setTabOrder(self.dutModelLineEdit, self.dutSerialNumberLineEdit)
        self.setTabOrder(self.dutSerialNumberLineEdit, self.dutIdentificationLineEdit)
        self.setTabOrder(self.dutIdentificationLineEdit, self.dutClassComboBox)
        self.setTabOrder(self.dutClassComboBox, self.supplyULimitLineEdit)
        self.setTabOrder(self.supplyULimitLineEdit, self.supplyLLimitLineEdit)
        self.setTabOrder(self.supplyLLimitLineEdit, self.referenceLevelLineEdit)
        self.setTabOrder(self.referenceLevelLineEdit, self.lu1kHzLineEdit)
        self.setTabOrder(self.lu1kHzLineEdit, self.lu8kHzLineEdit)
        self.setTabOrder(self.lu8kHzLineEdit, self.li8kHzLineEdit)
        self.setTabOrder(self.li8kHzLineEdit, self.startPointLineEdit)
        self.setTabOrder(self.startPointLineEdit, self.screenRateLineEdit)
        self.setTabOrder(self.screenRateLineEdit, self.loadFreeFieldPushButton)
        self.setTabOrder(self.loadFreeFieldPushButton, self.preampBrandLineEdit)
        self.setTabOrder(self.preampBrandLineEdit, self.preampModelLineEdit)
        self.setTabOrder(self.preampModelLineEdit, self.preampSerialLineEdit)
        self.setTabOrder(self.preampSerialLineEdit, self.micBrandLineEdit)
        self.setTabOrder(self.micBrandLineEdit, self.micModelLineEdit)
        self.setTabOrder(self.micModelLineEdit, self.micSerialNumberLineEdit)
        self.setTabOrder(self.micSerialNumberLineEdit, self.customerNameLineEdit)
        self.setTabOrder(self.customerNameLineEdit, self.addressLineEdit)
        self.setTabOrder(self.addressLineEdit, self.cityLineEdit)
        self.setTabOrder(self.cityLineEdit, self.countryLineEdit)
        self.setTabOrder(self.countryLineEdit, self.postalCodeLineEdit)
        self.setTabOrder(self.postalCodeLineEdit, self.contactNumberLineEdit)
        self.setTabOrder(self.contactNumberLineEdit, self.saveDUTInfo)
        self.setTabOrder(self.saveDUTInfo, self.adjEdit)
        self.setTabOrder(self.adjEdit, self.adjTableView)
        self.setTabOrder(self.adjTableView, self.adjSaveButton)
        self.setTabOrder(self.adjSaveButton, self.viRefLineEdit)
        self.setTabOrder(self.viRefLineEdit, self.vuRefLineEdit)
        self.setTabOrder(self.vuRefLineEdit, self.vRefButton)
        self.setTabOrder(self.vRefButton, self.saveVRefButton)
        self.setTabOrder(self.saveVRefButton, self.aWTableView)
        self.setTabOrder(self.aWTableView, self.cWTableView)
        self.setTabOrder(self.cWTableView, self.zWTableView)
        self.setTabOrder(self.zWTableView, self.linearityTableView)
        self.setTabOrder(self.linearityTableView, self.ambientTableView)

    def translate_ui(self) -> None:
        """
        This method sets the text of all printable objects of the main window.
        """
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Calibración de sonómetros"))
        self.testLabel.setText(_translate("MainWindow", "PRUEBA"))
        self.previousTestToolButton.setText(_translate("MainWindow", "..."))
        self.nextTestToolButton.setText(_translate("MainWindow", "..."))
        self.measurementProgressLabel.setText(_translate("MainWindow", "Progreso de medición"))
        self.generalProgressLabel.setText(_translate("MainWindow", "Progreso general"))
        self.streamingButton.setText(_translate("MainWindow", "Iniciar streaming"))
        self.videoLabel.setText(_translate("MainWindow", "VÍDEO"))
        self.decadeBoxGroupBox.setTitle(_translate("MainWindow", "ATENUADOR PROGRAMABLE"))
        self.decadeBoxBrandLabel.setText(_translate("MainWindow", "Marca:"))
        self.decadeBoxBrandLineEdit.setText(_translate("MainWindow", "ACOEM"))
        self.decadeBoxModelLabel.setText(_translate("MainWindow", "Modelo:"))
        self.decadeBoxModelLineEdit.setText(_translate("MainWindow", "OUT-1694000"))
        self.decadeBoxSerialNumberLabel.setText(_translate("MainWindow", "Número de serie:"))
        self.decadeBoxSerialNumberLineEdit.setText(_translate("MainWindow", "16-05-205"))
        self.decadeBoxIdentificationLabel.setText(_translate("MainWindow", "Identificación:"))
        self.decadeBoxIdentificationLineEdit.setText(_translate("MainWindow", "1520161"))
        self.afgGroupBox.setTitle(_translate("MainWindow", "GENERADOR DE SEÑALES"))
        self.afgBrandLabel.setText(_translate("MainWindow", "Marca:"))
        self.afgModelLabel.setText(_translate("MainWindow", "Modelo:"))
        self.afgModelLineEdit.setText(_translate("MainWindow", "33511B"))
        self.afgSerialNumberLabel.setText(_translate("MainWindow", "Número de serie:"))
        self.afgIdentificationLabel.setText(_translate("MainWindow", "Identificación:"))
        self.afgIdentificationLineEdit.setText(_translate("MainWindow", "1520164"))
        self.afgGPIBbusLabel.setText(_translate("MainWindow", "Bus GPIB:"))
        self.afgGPIBChannelLabel.setText(_translate("MainWindow", "Canal GPIB:"))
        for i in range(22):
            self.afgGPIBChannelComboBox.setItemText(i + 1, _translate("MainWindow", str(i + 1)))
        self.afgSelfTestLabel.setText(_translate("MainWindow", "Auto-verificación"))
        self.multimeterGroupBox.setTitle(_translate("MainWindow", "MULTÍMETRO"))
        self.multimeterBrandLabel.setText(_translate("MainWindow", "Marca:"))
        self.multimeterModelLabel.setText(_translate("MainWindow", "Modelo:"))
        self.multimeterModelLineEdit.setText(_translate("MainWindow", "34461A"))
        self.multimeterSerialNumberLabel.setText(_translate("MainWindow", "Número de serie:"))
        self.multimeterIdentificationLabel.setText(_translate("MainWindow", "Identificación:"))
        self.multimeterIdentificationLineEdit.setText(_translate("MainWindow", "1520163"))
        self.multimeterGPIBbusLabel.setText(_translate("MainWindow", "Bus GPIB:"))
        self.multimeterGPIBChannelLabel.setText(_translate("MainWindow", "Canal GPIB:"))
        for i in range(22):
            self.multimeterGPIBChannelComboBox.setItemText(i + 1, _translate("MainWindow", str(i + 1)))
        self.multimeterSelfTestLabel.setText(_translate("MainWindow", "Auto-verificación"))
        self.saveStandardsInfo.setText(_translate("MainWindow", "Guardar"))
        self.parentTabWidget.setTabText(self.parentTabWidget.indexOf(self.standardsTab),
                                        _translate("MainWindow", "Patrones"))
        self.preampGroupBox.setTitle(_translate("MainWindow", "PREAMPLIFICADOR"))
        self.preampBrandLabel.setText(_translate("MainWindow", "Marca:"))
        self.preampModelLabel.setText(_translate("MainWindow", "Modelo:"))
        self.preampSerialLabel.setText(_translate("MainWindow", "Número de serie:"))
        self.customerGroupBox.setTitle(_translate("MainWindow", "CLIENTE"))
        self.customerNameLabel.setText(_translate("MainWindow", "Nombre:"))
        self.addressLabel.setText(_translate("MainWindow", "Dirección:"))
        self.cityLabel.setText(_translate("MainWindow", "Ciudad:"))
        self.countryLabel.setText(_translate("MainWindow", "País:"))
        self.postalCodeLabel.setText(_translate("MainWindow", "Código Postal:"))
        self.contactNumberLabel.setText(_translate("MainWindow", "Contacto:"))
        self.saveDUTInfo.setText(_translate("MainWindow", "Guardar"))
        self.dutGroupBox.setTitle(_translate("MainWindow", "ÍTEM DE CALIBRACIÓN"))
        self.consecutiveLabel.setText(_translate("MainWindow", "Consecutivo:"))
        self.dutBrandLabel.setText(_translate("MainWindow", "Marca:"))
        self.dutModelLabel.setText(_translate("MainWindow", "Modelo:"))
        self.dutSerialNumberLabel.setText(_translate("MainWindow", "Número de serie:"))
        self.dutIdentificationLabel.setText(_translate("MainWindow", "Identificación:"))
        self.dutClassLabel.setText(_translate("MainWindow", "Clase:"))
        self.dutClassComboBox.setCurrentText(_translate("MainWindow", "1"))
        self.dutClassComboBox.setItemText(0, _translate("MainWindow", "1"))
        self.dutClassComboBox.setItemText(1, _translate("MainWindow", "2"))
        self.supplyULimitLabel.setText(_translate("MainWindow", "Lu fuente alimentación:"))
        self.supplyLLimitLabel.setText(_translate("MainWindow", "Li fuente alimentación:"))
        self.referenceLevelLabel.setText(_translate("MainWindow", "Nivel de referencia:"))
        self.loadFreeFieldPushButton.setText(_translate("MainWindow", "Cargar correcciones de campo libre"))
        self.lu1kHzLabel.setText(_translate("MainWindow", "Lu 1 kHz:"))
        self.lu8kHzLabel.setText(_translate("MainWindow", "Lu 8 kHz:"))
        self.li8kHzLabel.setText(_translate("MainWindow", "Li 8  kHz:"))
        self.startPointLabel.setText(_translate("MainWindow", "Punto de inicio:"))
        self.screenRateLabel.setText(_translate("MainWindow", "Periodo de pantalla (ms):"))
        self.micGroupBox.setTitle(_translate("MainWindow", "MICRÓFONO"))
        self.micBrandLabel.setText(_translate("MainWindow", "Marca:"))
        self.micModelLabel.setText(_translate("MainWindow", "Modelo:"))
        self.micSerialNumberLabel.setText(_translate("MainWindow", "Número de serie:"))
        self.parentTabWidget.setTabText(self.parentTabWidget.indexOf(self.infoTab),
                                        _translate("MainWindow", "Información IBC"))
        self.supplyLabel.setText(_translate("MainWindow", "FUENTE DE ALIMENTACIÓN"))
        self.electricTestsLabel.setText(_translate("MainWindow", "ENSAYOS ELÉCTRICOS"))
        self.beforeLabel.setText(_translate("MainWindow", "ANTES"))
        self.afterLabel.setText(_translate("MainWindow", "DESPUÉS"))
        self.afterElecUnitsLabel.setText(_translate("MainWindow", "V"))
        self.beforeAcusUnitsLabel.setText(_translate("MainWindow", "V"))
        self.acousticTestsLabel.setText(_translate("MainWindow", "ENSAYOS ACÚSTICOS"))
        self.afterAcusUnitsLabel.setText(_translate("MainWindow", "V"))
        self.beforeElecUnitsLabel.setText(_translate("MainWindow", "V"))
        self.calIndLabel.setText(
            _translate("MainWindow", "INDICACIÓN A LA FRECUENCIA DE COMPROBACIÓN DE LA CALIBRACIÓN"))
        self.initAdjUnitsLabel.setText(_translate("MainWindow", "dB"))
        self.adjSaveButton.setText(_translate("MainWindow", "GUARDAR"))
        self.adjLabel.setText(_translate("MainWindow", "Ajuste"))
        self.beforeAdjLabel.setText(_translate("MainWindow", "Antes del ajuste"))
        self.afterAdjLabel.setText(_translate("MainWindow", "Después del ajuste"))
        self.initAdjLabel.setText(_translate("MainWindow", "Ajuste inicial"))
        self.repliesLabel.setText(_translate("MainWindow", "Réplicas [dB]"))
        self.vRefTitleLabel.setText(_translate("MainWindow", "VOLTAJE DE REFERENCIA"))
        self.vuRefLabel.setText(_translate("MainWindow", "Voltaje superior [V]"))
        self.vRefLabel.setText(_translate("MainWindow", "Voltaje medio [v]"))
        self.lvRefLabel.setText(_translate("MainWindow", "Nivel de voltaje medio [dBV]"))
        self.viRefLabel.setText(_translate("MainWindow", "Voltaje inferior [V]"))
        self.vRefButton.setText(_translate("MainWindow", "RECONOCER"))
        self.saveVRefButton.setText(_translate("MainWindow", "GUARDAR"))
        self.parentTabWidget.setTabText(self.parentTabWidget.indexOf(self.preTestsTab),
                                        _translate("MainWindow", "Pruebas preliminares"))
        self.zWeightLabel.setText(_translate("MainWindow", "PONDERACIÓN FRECUENCIAL Z"))
        self.cWeightLabel.setText(_translate("MainWindow", "PONDERACIÓN FRECUENCIAL C"))
        self.aWeightLabel.setText(_translate("MainWindow", "PONDERACIÓN FRECUENCIAL A"))
        self.aW1kHzLabel.setText(_translate("MainWindow", "A"))
        self.bW1kHzLabel.setText(_translate("MainWindow", "B"))
        self.cW1kHzLabel.setText(_translate("MainWindow", "C"))
        self.fWRLevLabel.setText(_translate("MainWindow", "Relativo [dB]"))
        self.fWLevLabel.setText(_translate("MainWindow", "Nivel [dB]"))
        self.fW1kHzLabel.setText(_translate("MainWindow", "FRECUENCIALES A 1 kHz"))
        self.slowWLabel.setText(_translate("MainWindow", "S"))
        self.tWRLevLabel.setText(_translate("MainWindow", "Relativo [dB]"))
        self.fastWLabel.setText(_translate("MainWindow", "F"))
        self.tWLevLabel.setText(_translate("MainWindow", "Nivel [dB]"))
        self.eqWLabel.setText(_translate("MainWindow", "eq"))
        self.tW1kHzLabel.setText(_translate("MainWindow", "TEMPORALES A 1 kHz"))
        self.parentTabWidget.setTabText(self.parentTabWidget.indexOf(self.weightingsTab),
                                        _translate("MainWindow", "Ponderaciones frecuenciales y temporales"))
        self.parentTabWidget.setTabText(self.parentTabWidget.indexOf(self.linearityTab),
                                        _translate("MainWindow", "Linealidad de nivel en el rango de referencia"))
        self.parentTabWidget.setTabText(self.parentTabWidget.indexOf(self.ambientConditionsTab),
                                        _translate("MainWindow", "Condiciones ambientales"))
        self.menuFile.setTitle(_translate("MainWindow", "Archivo"))
        self.menuCalibration.setTitle(_translate("MainWindow", "Calibración"))
        self.menuTools.setTitle(_translate("MainWindow", "Herramientas"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionLoadCalibration.setText(_translate("MainWindow", "Cargar calibración"))
        self.actionSaveCalibration.setText(_translate("MainWindow", "Guardar calibración"))
        self.actionSearchStandards.setText(_translate("MainWindow", "Buscar patrones"))
        self.actionSelfTest.setText(_translate("MainWindow", "Auto-verificar patrones"))
        self.actionEmitCertificate.setText(_translate("MainWindow", "Generar certificado de calibración"))
        self.actionStart.setText(_translate("MainWindow", "Iniciar"))
        self.actionPause.setText(_translate("MainWindow", "Pausar"))
        self.actionRestart.setText(_translate("MainWindow", "Reiniciar"))
        self.actionNextPoint.setText(_translate("MainWindow", "Avanzar punto"))
        self.actionPreviousPoint.setText(_translate("MainWindow", "Retroceder punto"))
        self.actionNextTest.setText(_translate("MainWindow", "Avanzar prueba"))
        self.actionPreviousTest.setText(_translate("MainWindow", "Retroceder prueba"))
        self.actionGoToTest.setText(_translate("MainWindow", "Ir a la prueba"))
        self.actionGoToPoint.setText(_translate("MainWindow", "Ir al punto"))

    def enable_search_standards(self):
        """
        Method for enabling the search standards action guarantying there is info to execute it.
        """
        if self.afgModelLineEdit.displayText() != "":
            self.actionSearchStandards.setEnabled(True)
        else:
            self.actionSearchStandards.setEnabled(False)


class GUIController(object):
    # Temporal preset sonometer
    __01dBFusionInfo = {'Brand': '01dB', 'Model': 'FUSION', 'S/N': '11428', 'ID': '12345', 'Class': '1',
                        'Power Supply Limits': ('8', '28'), 'Reference Level': '94', 'Lu 1 kHz': '138',
                        'Range 8 kHz': ('23', '138'), 'Linearity Start Point': '94', 'Screen Rate': '100'}
    __mic40CEInfo = {'Brand': 'GRAS', 'Model': '40CE', 'S/N': '34567154'}
    __pre22Info = {'Brand': '01dB', 'Model': 'PRE22', 'S/N': '11811'}
    __K2Customer = {'Name': 'K2 Ingeniería SAS', 'Address': 'Carrera 22A # 85A - 36', 'City': 'Bogotá',
                    'Country': 'Colombia', 'Postal Code': '111811', 'Contact': '601594354'}

    def __init__(self, gui: QtWidgets.QMainWindow):
        self._gui = gui
        self.fill_dut_info()  # Temporal calling for filling info on GUI
        self._TESTER = ac.SLMPeriodicTester()  # Instantiates the object for calibration of sound level meters (model)
        self.calibrationThread = QtCore.QThread()  # This is the thread that will run all the calibration tasks
        self.save_standards_state = 1  # Instance attribute flag to save the state of standards info saving button
        self.save_DUT_info_sate = 1  # Instance attribute flag to save the state of dut info saving button
        self.AFG_info = {}
        self.DecadeBox_info = {}
        self.DMM_info = {}
        self.self_test_passed = False  # Instance flag to save the results of self-test
        empty_array = np.empty((9, 6))
        empty_array[:] = np.nan
        self.electric_ff_corrections = pd.DataFrame(empty_array)

        self.instruction = QtWidgets.QMessageBox()

        self.searchStandardWorker = QtCore.QObject()  # This is the worker for searching standards
        self.searchStandardThread = QtCore.QThread()  # This is the parallel thread for searching standards
        self.selfTesterWorker = QtCore.QObject()  # This is the worker for self-testing
        self.selfTesterThread = QtCore.QThread()  # This is the parallel thread for self-testing
        self.cameraWorker = VideoObject()  # Object for video streaming in a parallel thread
        self.cameraThread = QtCore.QThread()  # Parallel thread for video capturing
        self.streaming_running = False  # Instance flag to save the state of the video streaming
        self.x1 = self.x2 = self.y1 = self.y2 = 0  # Coordinates for cropping the video frames
        self.timer_started = False  # Flag that indicates if the timer for frames capturing has started
        self.frames = []  # List for storing the frames of the current calibration point
        self.frames_queue = Queue()  # A queue for sharing the frames between the controller and the model. This enables
        # to store temporally the new frames while the previous frames are processed.
        self.imgProcessingThread = ImageProcessingThread(self.frames_queue, self._TESTER, self.cameraWorker)

        # self.videoSave = QtCore.QObject()
        # self.saveVideoThread = QtCore.QThread()

        self._connect_signals()

    def _connect_signals(self) -> None:
        self._gui.saveStandardsInfo.clicked.connect(self.save_standards_info)
        self._gui.actionSearchStandards.triggered.connect(self.search_standards)
        self._gui.actionSelfTest.triggered.connect(self.self_test)
        self._gui.saveDUTInfo.clicked.connect(self.save_dut_info)
        self._gui.loadFreeFieldPushButton.clicked.connect(self.read_elec_ff_corrections)
        self._gui.streamingButton.clicked.connect(self.streaming_control)
        self._gui.actionStart.triggered.connect(self.start)
        self._gui.actionPause.triggered.connect(self.pause)
        self._gui.adjSaveButton.clicked.connect(self.save_cal_ind_values)
        self._gui.saveVRefButton.clicked.connect(self.save_ref_volt)

        self._gui.vRefButton.clicked.connect(functools.partial(self.run_sequence, 5))  # TODO: temporal

        # Connect signals of the calibration worker and thread
        self._TESTER.moveToThread(self.calibrationThread)
        self.calibrationThread.started.connect(self._TESTER.run_main_sequence)

        self._TESTER.measurementProgress.connect(self._gui.measurementProgressBar.setValue)

        self._TESTER.calibrationProgress.connect(lambda x: self._gui.generalProgressBar.setValue(int(x / 9 * 100)))
        self._TESTER.calibrationProgress.connect(self.sequence_control)
        self._TESTER.calibrationProgress.connect(self._gui.lcdNumber.display)
        self._TESTER.calibrationProgress.connect(self.show_power_supply_values)
        self._TESTER.calibrationProgress.connect(self.calibrationThread.quit)

        self._TESTER.timerStarted.connect(self.capture_frames)
        # self._TESTER.realTimeValues.connect(self.update_real_time_values)

        # Connect signals of the camera worker and thread
        self.cameraWorker.moveToThread(self.cameraThread)
        self.cameraThread.started.connect(self.cameraWorker.run)
        self.cameraWorker.frameCaptured.connect(self.stream_frame)
        self.cameraWorker.cameraReleased.connect(self.cameraThread.quit)
        # self.cameraThread.finished.connect(self.cameraThread.deleteLater)
        # self.cameraWorker.cameraReleased.connect(self.cameraWorker.deleteLater)

    def fill_dut_info(self) -> None:
        """
        Temporal method for filling information of the sound level meter under test, its preamp, its mic, and the
        customer info.
        :return: None
        """
        self._gui.dutBrandLineEdit.setText(self.__01dBFusionInfo['Brand'])
        self._gui.dutModelLineEdit.setText(self.__01dBFusionInfo['Model'])
        self._gui.dutSerialNumberLineEdit.setText(self.__01dBFusionInfo['S/N'])
        self._gui.dutIdentificationLineEdit.setText(self.__01dBFusionInfo['ID'])
        self._gui.dutClassComboBox.setCurrentIndex(int(self.__01dBFusionInfo['Class']) - 1)
        self._gui.supplyULimitLineEdit.setText(self.__01dBFusionInfo['Power Supply Limits'][1])
        self._gui.supplyLLimitLineEdit.setText(self.__01dBFusionInfo['Power Supply Limits'][0])
        self._gui.referenceLevelLineEdit.setText(self.__01dBFusionInfo['Reference Level'])
        self._gui.lu1kHzLineEdit.setText(self.__01dBFusionInfo['Lu 1 kHz'])
        self._gui.lu8kHzLineEdit.setText(self.__01dBFusionInfo['Range 8 kHz'][1])
        self._gui.li8kHzLineEdit.setText(self.__01dBFusionInfo['Range 8 kHz'][0])
        self._gui.startPointLineEdit.setText(self.__01dBFusionInfo['Linearity Start Point'])
        self._gui.screenRateLineEdit.setText(self.__01dBFusionInfo['Screen Rate'])
        self._gui.preampBrandLineEdit.setText(self.__pre22Info['Brand'])
        self._gui.preampModelLineEdit.setText(self.__pre22Info['Model'])
        self._gui.preampSerialLineEdit.setText(self.__pre22Info['S/N'])
        self._gui.micBrandLineEdit.setText(self.__mic40CEInfo['Brand'])
        self._gui.micModelLineEdit.setText(self.__mic40CEInfo['Model'])
        self._gui.micSerialNumberLineEdit.setText(self.__mic40CEInfo['S/N'])
        self._gui.customerNameLineEdit.setText(self.__K2Customer['Name'])
        self._gui.addressLineEdit.setText(self.__K2Customer['Address'])
        self._gui.cityLineEdit.setText(self.__K2Customer['City'])
        self._gui.countryLineEdit.setText(self.__K2Customer['Country'])
        self._gui.postalCodeLineEdit.setText(self.__K2Customer['Postal Code'])
        self._gui.contactNumberLineEdit.setText(self.__K2Customer['Contact'])

    def save_standards_info(self) -> None:
        """
        Method that catch the standards information and save that in the TESTER object.
        Also enables and disables the corresponding objects and actions.
        """
        self.AFG_info = {'Brand': self._gui.afgBrandLineEdit.displayText(),
                         'Model': self._gui.afgModelLineEdit.displayText(),
                         'S/N': self._gui.afgSerialNumberLineEdit.displayText(),
                         'ID': self._gui.afgIdentificationLineEdit.displayText(),
                         'GPIB bus': self._gui.afgGPIBbusLineEdit.displayText(),
                         'GPIB channel': self._gui.afgGPIBChannelComboBox.currentText()}
        self.DecadeBox_info = {'Brand': self._gui.decadeBoxBrandLineEdit.displayText(),
                               'Model': self._gui.decadeBoxModelLineEdit.displayText(),
                               'S/N': self._gui.decadeBoxSerialNumberLineEdit.displayText(),
                               'ID': self._gui.decadeBoxIdentificationLineEdit.displayText()}
        self.DMM_info = {'Brand': self._gui.multimeterBrandLineEdit.displayText(),
                         'Model': self._gui.multimeterModelLineEdit.displayText(),
                         'S/N': self._gui.multimeterSerialNumberLineEdit.displayText(),
                         'ID': self._gui.multimeterIdentificationLineEdit.displayText(),
                         'GPIB bus': self._gui.multimeterGPIBBusLineEdit.displayText(),
                         'GPIB channel': self._gui.multimeterGPIBChannelComboBox.currentText()}
        # Dual function of the save button: 1 for save, 2 for edit
        if self.save_standards_state == 1:
            if ("" not in self.AFG_info.values()) * (
                    "" not in self.DecadeBox_info.values()) * (
                    "" not in self.DMM_info.values()):  # Checks complete info
                self._TESTER.set_standards(self.AFG_info, self.DMM_info)
                self._gui.saveStandardsInfo.setText('Editar')
                self._gui.afgGroupBox.setEnabled(False)
                self._gui.decadeBoxGroupBox.setEnabled(False)
                self._gui.multimeterGroupBox.setEnabled(False)
                self.save_standards_state = 2
                QtWidgets.QMessageBox.information(self._gui, 'Información', 'Información guardada correctamente.')
                self._gui.actionSelfTest.setEnabled(True)
            else:
                QtWidgets.QMessageBox.warning(self._gui, 'Advertencia',
                                              'La información de los patrones no está completa.')
        else:
            # TODO: Incluir control de edición cuando ya ha indicado la calibración
            self._gui.afgGroupBox.setEnabled(True)
            self._gui.decadeBoxGroupBox.setEnabled(True)
            self._gui.multimeterGroupBox.setEnabled(True)
            self.save_standards_state = 1
            self._gui.saveStandardsInfo.setText('Guardar')

    def read_elec_ff_corrections(self) -> None:
        """
        This method launches a file dialog for searching the csv file with the free field corrections used in the
        frequency weightings test with electric signals.
        :return: None
        """
        path, _ = QtWidgets.QFileDialog.getOpenFileName(parent=self._gui,
                                                        caption='Seleccione el archivo',
                                                        directory=os.getcwd(),
                                                        filter='Valores separados por coma (*.csv)')
        self.electric_ff_corrections = pd.read_csv(path, sep=';', header=0, index_col=0)

    def save_dut_info(self) -> None:
        """
        Method that catch the DUT and customer information and save that in the TESTER object.
        Also enables and disables the corresponding objects and actions.
        """
        dut_info = {'Consecutive': self._gui.consecutiveLineEdit.displayText(),
                    'Brand': self._gui.dutBrandLineEdit.displayText(),
                    'Model': self._gui.dutModelLineEdit.displayText(),
                    'S/N': self._gui.dutSerialNumberLineEdit.displayText(),
                    'ID': self._gui.dutIdentificationLineEdit.displayText(),
                    'Class': int(self._gui.dutClassComboBox.currentText()),
                    'Power Supply Limits': (float(self._gui.supplyULimitLineEdit.displayText()),
                                            float(self._gui.supplyLLimitLineEdit.displayText())),
                    'Reference Level': float(self._gui.referenceLevelLineEdit.displayText()),
                    'Lu 1 kHz': float(self._gui.lu1kHzLineEdit.displayText()),
                    'Range 8 kHz': (float(self._gui.li8kHzLineEdit.displayText()),
                                    float(self._gui.lu8kHzLineEdit.displayText())),
                    'Linearity Start Point': float(self._gui.startPointLineEdit.displayText()),
                    'Screen Rate': float(self._gui.screenRateLineEdit.displayText())}
        pre_info = {'Brand': self._gui.preampBrandLineEdit.displayText(),
                    'Model': self._gui.preampModelLineEdit.displayText(),
                    'S/N': self._gui.preampSerialLineEdit.displayText()}
        mic_info = {'Brand': self._gui.micBrandLineEdit.displayText(),
                    'Model': self._gui.micModelLineEdit.displayText(),
                    'S/N': self._gui.micSerialNumberLineEdit.displayText()}
        customer_info = {'Name': self._gui.customerNameLineEdit.displayText(),
                         'Address': self._gui.addressLineEdit.displayText(),
                         'City': self._gui.cityLineEdit.displayText(),
                         'Country': self._gui.consecutiveLineEdit.displayText(),
                         'Postal code': self._gui.postalCodeLineEdit.displayText(),
                         'Contact': self._gui.contactNumberLineEdit.displayText()}

        # Dual function of the save button: 1 for save, 2 for edit.
        if self.save_DUT_info_sate == 1:
            # Checks complete info
            if ("" not in dut_info.values()) * ("" not in mic_info.values()) * (
                    "" not in pre_info.values()) * ("" not in customer_info.values()) * (
                    not self.electric_ff_corrections.isnull().values.any()):
                dut = ac.SoundLevelMeter(slm_brand=dut_info['Brand'], slm_model=dut_info['Model'],
                                         slm_sn=dut_info['S/N'],
                                         slm_identification=dut_info['ID'], slm_cl=dut_info['Class'],
                                         power_supply_limits=dut_info['Power Supply Limits'],
                                         reference_level=dut_info['Reference Level'], lu_1kHz=dut_info['Lu 1 kHz'],
                                         range_8kHz=dut_info['Range 8 kHz'],
                                         lin_start_point=dut_info['Linearity Start Point'],
                                         screen_rate=dut_info['Screen Rate'],
                                         electrical_ff_corrections=self.electric_ff_corrections,
                                         mic_brand=mic_info['Brand'], mic_model=mic_info['Model'],
                                         mic_sn=mic_info['S/N'], pre_brand=pre_info['Brand'],
                                         pre_model=pre_info['Model'], pre_sn=pre_info['S/N'])
                self._TESTER.set_dut(dut)
                self._TESTER.set_consecutive(dut_info['Consecutive'])
                self._TESTER.set_customer_info(customer_info)
                self.save_DUT_info_sate = 2
                self._gui.saveDUTInfo.setText('Editar')
                self._gui.dutGroupBox.setEnabled(False)
                self._gui.customerGroupBox.setEnabled(False)
                self._gui.preampGroupBox.setEnabled(False)
                self._gui.micGroupBox.setEnabled(False)
                QtWidgets.QMessageBox.information(self._gui, 'Información',
                                                  'La información del IBC y del cliente se guardó correctamente')
                if self.self_test_passed and self.save_standards_state == 2:
                    self._gui.actionStart.setEnabled(True)
                    self._gui.preTestsTab.setEnabled(True)
            else:
                QtWidgets.QMessageBox.warning(self._gui, 'Advertencia',
                                              'La información del IBC o del cliente no está completa.')
        else:
            # TODO: Incluir control de edición cuando ya ha iniciado la calibración
            self._gui.dutGroupBox.setEnabled(True)
            self._gui.customerGroupBox.setEnabled(True)
            self._gui.preampGroupBox.setEnabled(True)
            self._gui.micGroupBox.setEnabled(True)
            self.save_DUT_info_sate = 1
            self._gui.saveDUTInfo.setText('Guardar')

    def search_standards(self) -> None:
        """
        This method search for the indicated model of signal generator in the available VISA resources.
        """
        self.searchStandardThread = QtCore.QThread()  # This is the parallel thread for searching standards
        resources = self._TESTER.resource_manager.list_resources()  # List all available resources
        self.searchStandardWorker = StandardsSearcher(AFG_model=self._gui.afgModelLineEdit.displayText(),
                                                      DMM_model=self._gui.multimeterModelLineEdit.displayText(),
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
        instrument and fill the information available
        :param data_found: Boolean that indicates if the generator was founded.
        :return: None.
        """
        if not data_found[0]:
            QtWidgets.QMessageBox.warning(self._gui, 'Advertencia', 'Generador no encontrado.')
        if not data_found[1]:
            QtWidgets.QMessageBox.warning(self._gui, 'Advertencia', 'Multímetro no encontrado.')
        if data_found[0] and data_found[1]:
            self._gui.afgBrandLineEdit.setText(self.searchStandardWorker.data['AFG']['Brand'])
            self._gui.afgSerialNumberLineEdit.setText(self.searchStandardWorker.data['AFG']['S/N'])
            self._gui.afgGPIBbusLineEdit.setText(self.searchStandardWorker.data['AFG']['GPIB bus'])
            self._gui.afgGPIBChannelComboBox.setCurrentIndex(
                int(self.searchStandardWorker.data['AFG']['GPIB channel']))
            self._gui.multimeterBrandLineEdit.setText(self.searchStandardWorker.data['DMM']['Brand'])
            self._gui.multimeterSerialNumberLineEdit.setText(self.searchStandardWorker.data['DMM']['S/N'])
            self._gui.multimeterGPIBBusLineEdit.setText(self.searchStandardWorker.data['DMM']['GPIB bus'])
            self._gui.multimeterGPIBChannelComboBox.setCurrentIndex(
                int(self.searchStandardWorker.data['DMM']['GPIB channel']))
        self._gui.measurementProgressLabel.setText('Progreso de medición')
        self._gui.measurementProgressBar.setValue(0)

    def self_test(self) -> None:
        """
        This method executes the self-test routine of generator in a parallel thread.
        """
        self.selfTesterThread = QtCore.QThread()  # Parallel thread for testing
        self.selfTesterWorker = SelfTester(self._TESTER.DMM, self._TESTER.AFG)  # Instantiates the worker object
        self.selfTesterWorker.moveToThread(self.selfTesterThread)
        self.selfTesterThread.started.connect(self.selfTesterWorker.self_test)
        self.selfTesterWorker.progress.connect(self._gui.measurementProgressBar.setValue)
        self.selfTesterWorker.finished.connect(self.show_self_test_results)
        self.selfTesterWorker.finished.connect(self.selfTesterThread.quit)
        self.selfTesterWorker.finished.connect(self.selfTesterWorker.deleteLater)
        self.selfTesterThread.finished.connect(self.selfTesterThread.deleteLater)
        self._gui.measurementProgressLabel.setText('Progreso de auto-verificación')
        self.selfTesterThread.start()

    def show_self_test_results(self, results: bool) -> None:
        """
        This method presents the result of self-test of generator on the corresponding checkbox.
        This is executed when the parallel thread finished
        :param results: Boolean that describe the result of test, passed or no.
        :return: None
        """
        self._gui.multimeterSelfTestCheckBox.setChecked(results[0])
        self._gui.afgSelfTestCheckBox.setChecked(results[1])
        self._gui.measurementProgressLabel.setText('Progreso de medición')
        self._gui.measurementProgressBar.setValue(0)
        self.self_test_passed = results[0] and results[1]
        if self.save_standards_state == 2 and self.save_DUT_info_sate == 2 and self.self_test_passed:
            self._gui.actionStart.setEnabled(True)
            self._gui.preTestsTab.setEnabled(True)

    def streaming_control(self) -> None:
        """
        This method controls the video streaming to the GUI View.
        :return:
        """
        if not self.streaming_running:
            self._gui.streamingButton.setText('Detener streaming')
            self.cameraWorker.run_flag = True
            self.cameraThread.start()
            self.streaming_running = True
            # self._gui.roi.rect().moveCenter(self._gui.videoPixmap.center())
        elif self.streaming_running:
            mutex.lock()
            self.cameraWorker.run_flag = False
            mutex.unlock()
            self.streaming_running = False
            self._gui.streamingButton.setText('Iniciar streaming')

    def stream_frame(self, frame: np.ndarray):
        """
        This method takes the frame emitted by the video object running on a parallel thread and shows it on the view
        :param frame: The frame captured by the video object
        :return: None
        """
        mutex.lock()
        if self.timer_started:
            self.frames.append(frame[self.y1:self.y2, self.x1:self.x2])
        mutex.unlock()
        qpixmap = self.img2qpixmap(cv.cvtColor(frame, cv.COLOR_BGR2RGB))  # Converts the frames to a QImage
        self._gui.videoPixmap.setPixmap(qpixmap)  # Updates the QPixmap item with the new frame
        self._gui.videoView.centerOn(self._gui.videoPixmap)  # Force centering on the View

    def capture_frames(self, timer_started: bool) -> None:
        if timer_started:
            mutex.lock()
            roi_top_left = self._gui.roi.rect().topLeft()
            roi_top_left_mapped = self._gui.roi.mapToItem(self._gui.videoPixmap, roi_top_left)
            roi_bottom_right = self._gui.roi.rect().bottomRight()
            roi_bottom_right_mapped = self._gui.roi.mapToItem(self._gui.videoPixmap, roi_bottom_right)
            self.x1 = int(roi_top_left_mapped.x())
            self.y1 = int(roi_top_left_mapped.y())
            self.x2 = int(roi_bottom_right_mapped.x())
            self.y2 = int(roi_bottom_right_mapped.y())
            self.frames = []
            self.timer_started = timer_started
            mutex.unlock()
        elif not timer_started:
            mutex.lock()
            self.timer_started = timer_started
            mutex.unlock()
            logging.info(f'Añadiendo {len(self.frames)} cuadros a la cola.')
            self.frames_queue.put(self.frames)
            del self.frames

            # video_writer = cv.VideoWriter('video_test.avi',
            #                               cv.VideoWriter_fourcc(*'DIVX'),
            #                               self.cameraWorker.fps,
            #                               (self.frames[0].shape[1], self.frames[0].shape[0]))
            # self.saveVideoThread = QtCore.QThread()
            # self.videoSave = VideoSaving(self.frames, video_writer)
            # self.videoSave.moveToThread(self.saveVideoThread)
            # self.saveVideoThread.started.connect(self.videoSave.save_video)
            # self.videoSave.videoSaved.connect(self.saveVideoThread.quit)
            # self.saveVideoThread.start()

    def start(self) -> None:
        """
        This method is launched when the start action is triggered.
        This starts or resumes the calibration sequence and controls the GUI buttons.
        """
        self._gui.actionStart.setEnabled(False)
        self._gui.actionPause.setEnabled(True)
        # If the sequence was paused, It doesn't show instructions again; just resumes the sequence
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

    def run_sequence(self, stage) -> None:
        """
        Temporal method that forces a stage of the sequence.
        """
        self._TESTER._calibration_stage = stage
        self.sequence_control()

    def sequence_control(self) -> None:
        """
        This is the controller method of the principal calibration sequence.
        This method  also shows the corresponding calibration instructions on every stage.
        For your reference consult the GRAFCET.
        """
        if self._TESTER.stage == 0:
            self._gui.measurementProgressLabel.setText('Entrenando clasificador')
            self.calibrationThread.start()
        elif any([self._TESTER.stage == stage for stage in [1, 3, 11]]):
            self._gui.measurementProgressLabel.setText('Progreso de medición')
            # Power supply checks
            instruction = InstructionDialog(self._gui,
                                            'Coloque las puntas de prueba del multímetro\n' +
                                            'en la salida de la fuente de alimentación.')
            self.eval_answer(instruction)
        elif self._TESTER.stage == 2:
            # Indication at the calibration check frequency
            QtWidgets.QMessageBox.information(self._gui, 'Instrucción',
                                              'Realice tres repeticiones de la prueba de\n' +
                                              'Indicación a la frecuencia de comprobación de\n' +
                                              'la calibración. Luego, haga clic en Guardar.')
        elif self._TESTER.stage == 4:
            # Reference voltage
            QtWidgets.QMessageBox.information(self._gui, 'Instrucción',
                                              'Encuentre el voltaje superior e inferior\n' +
                                              'del intervalo de voltajes que produce una\n' +
                                              'indicación del nivel de referencia. Luego,\n' +
                                              'haga clic en guardar.')
        elif any([self._TESTER.stage == stage for stage in range(5, 8)]):
            # Electrical signal tests of frequency weightings
            if not self.streaming_running:
                self.streaming_control()
            W = [*'ACZ']
            self.instruction = InstructionDialog(None,
                                                 '1. Ajuste el sonómetro para mostrar un nivel de' +
                                                 ' sonido con ponderación\ntemporal Fast y ponderación ' +
                                                 f'frecuencial {W[self._TESTER.stage - 5]}.\n' +
                                                 '2. Ajuste la región de interés en el área de vídeo' +
                                                 'de forma que abarque\n' +
                                                 'el valor numérico del nivel de sonido.\n' +
                                                 '3. Haga clic en Ok para iniciar la prueba.')
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/icons/slm_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.instruction.setWindowIcon(icon)
            self.instruction.setWindowModality(QtCore.Qt.WindowModal)
            self.instruction.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.instruction.show()
            self.instruction.finished.connect(self.parallel_dialog_response)

    def eval_answer(self, instruction) -> None:
        """
        This is a simple method for evaluate the user response to a given instruction
        :param instruction: Dialog object
        :return: None
        """
        if instruction.exec() == QtWidgets.QMessageBox.Ok:
            self.calibrationThread.start()
        else:
            self._gui.actionStart.setEnabled(True)
            self._gui.actionPause.setEnabled(False)

    def parallel_dialog_response(self, answer) -> None:
        """
        This is a simple method for evaluate the user response to a given instruction running without parent
        :param answer: The dialog answer
        :return: None
        """
        if answer == QtWidgets.QMessageBox.Ok:
            self.calibrationThread.start()
            if not self.imgProcessingThread.isRunning():
                self.imgProcessingThread.start()
        else:
            self._gui.actionStart.setEnabled(True)
            self._gui.actionPause.setEnabled(False)

    def show_power_supply_values(self) -> None:
        """
        This method is executed on every calibration progress signal and, depending on the calibration stage,
        it updates the corresponding GUI elements with the power supply values.
        :return: None
        """
        if self._TESTER.stage == 2:
            self._gui.beforeAcusValLabel.setText(str(round(self._TESTER.power_supply_results[0, 0], 4)))
        elif self._TESTER.stage == 4:
            self._gui.afterAcusValLabel.setText(str(round(self._TESTER.power_supply_results[0, 1], 4)))
            self._gui.beforeElecValLabel.setText(str(round(self._TESTER.power_supply_results[0, 1], 4)))
        elif self._TESTER.stage == 12:
            self._gui.afterElecValLabel.setText(str(round(self._TESTER.power_supply_results[1, 1], 4)))

    def save_cal_ind_values(self) -> None:
        """
        This method catches the values of the Indication at the calibration check frequency test and saves them
        in the SoundLevelMeter object. Then, continues the calibration sequence.
        :return: None
        """
        if not self._gui.adjTableModel.df.isin([""]).any(None) and self._gui.adjEdit.displayText():
            self._TESTER.dut.set_calibration_check_indications(float(self._gui.adjEdit.displayText()),
                                                               self._gui.adjTableModel.df)
            self.calibrationThread.start()
        else:
            QtWidgets.QMessageBox.warning(self._gui, 'Advertencia',
                                          'La prueba de indicación a la frecuencia de\n' +
                                          'comprobación de la calibración no está completa.\n' +
                                          'Complete la prueba antes de continuar.')

    def save_ref_volt(self):
        if self._gui.viRefLineEdit.displayText() and self._gui.vuRefLineEdit.displayText():
            reference_voltages = np.array([float(self._gui.viRefLineEdit.displayText()),
                                           float(self._gui.vuRefLineEdit.displayText())])
            self._TESTER.dut.set_reference_voltages_values(reference_voltages)
            self._gui.lvValueLabel.setText(
                str(round(self._TESTER.dut.calibration_results['Reference Voltage'].iloc[0, 2], 2)))
            self._gui.vRefValueLabel.setText(
                str(round(self._TESTER.dut.calibration_results['Reference Voltage'].iloc[0, 3], 2)))
            self.calibrationThread.start()
        else:
            QtWidgets.QMessageBox.warning(self._gui, 'Advertencia',
                                          'No han sido ingresados los dos voltajes\n' +
                                          'que producen una indicación de referencia.')

    @staticmethod
    def img2qpixmap(img: np.ndarray) -> QtGui.QPixmap:
        """
        This utility method converts a given frames to a QPixmap object
        :param img: ndarray that represents the frames pixels. It may be a color frames of 3 channels.
        :return: The QPixmap object.
        """
        h, w, ch = img.shape
        bytes_per_line = ch * w
        qt_image = QtGui.QImage(img.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        return QtGui.QPixmap.fromImage(qt_image)


class StandardsSearcher(QtCore.QObject):
    """
    QObject for searching standards running in a parallel thread.
    """
    finished = QtCore.pyqtSignal(tuple)
    progress = QtCore.pyqtSignal(int)

    def __init__(self, AFG_model: str, DMM_model: str, resources: tuple, resource_manager: ac.visa.ResourceManager):
        super().__init__()
        self.AFG_model = AFG_model
        self.DMM_model = DMM_model
        self.resources = resources
        self._resource_manager = resource_manager
        self.data = {'AFG': {'Brand': '',
                             'S/N': '',
                             'GPIB bus': '',
                             'GPIB channel': ''},
                     'DMM': {'Brand': '',
                             'S/N': '',
                             'GPIB bus': '',
                             'GPIB channel': ''}}

    def search(self) -> None:
        """
        Method for searching the given models between the available VISA resources.
        :return: None
        """
        i = 0
        generator_found = False
        multimeter_found = False
        for res in self.resources:  # Search for the Arbitrary Function Generator
            i += int(1 / len(self.resources) * 100)
            self.progress.emit(i)  # Signal for updating the progress bar
            try:
                instrument = self._resource_manager.open_resource(res)
                idn = instrument.query('*IDN?')
            except ac.visa.errors.VisaIOError:
                continue
            # Check if the current resource is the specified generator model
            if self.AFG_model in idn and 'GPIB' in res:
                idn_data = idn.split(',')
                self.data['AFG']['Brand'] = idn_data[0]
                self.data['AFG']['S/N'] = idn_data[2]
                res_data = res.split("::")
                self.data['AFG']['GPIB bus'] = res_data[0].replace("GPIB", "")
                self.data['AFG']['GPIB channel'] = res_data[1]
                generator_found = True
            # Check if the current resource is the specified multimeter model
            if self.DMM_model in idn and 'GPIB' in res:
                idn_data = idn.split(',')
                self.data['DMM']['Brand'] = idn_data[0]
                self.data['DMM']['S/N'] = idn_data[2]
                res_data = res.split("::")
                self.data['DMM']['GPIB bus'] = res_data[0].replace("GPIB", "")
                self.data['DMM']['GPIB channel'] = res_data[1]
                multimeter_found = True

        self.finished.emit((generator_found, multimeter_found))


class SelfTester(QtCore.QObject):
    """
    QObject for execute self-test routine of every instrument in a parallel thread.
    """
    finished = QtCore.pyqtSignal(tuple)
    progress = QtCore.pyqtSignal(int)

    def __init__(self, DMM: ac.visa.Resource, AFG: ac.visa.Resource):
        super().__init__()
        self._DMM = DMM
        self._AFG = AFG

    def self_test(self):
        dmm_pass = self._DMM.query('*TST?')  # Run self-test on multimeter
        dmm_pass = not bool(int(dmm_pass))
        self.progress.emit(50)
        afg_pass = self._AFG.query('*TST?', 8)  # Run self-test on multimeter
        afg_pass = not bool(int(afg_pass))
        self.progress.emit(100)
        self.finished.emit((dmm_pass, afg_pass))


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


class EditablePandasTableModel(QtCore.QAbstractTableModel):
    """
    This class is the implementation of a table model that enables the interactive editing from the View.
    The model is created from a Pandas DataFrame.
    """

    def __init__(self, df, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self.df = df

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if orientation == QtCore.Qt.Horizontal:
            try:
                return self.df.columns.tolist()[section]
            except (IndexError,):
                return QtCore.QVariant()
        elif orientation == QtCore.Qt.Vertical:
            try:
                # return self.df.index.tolist()
                return self.df.index.tolist()[section]
            except (IndexError,):
                return QtCore.QVariant()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if not index.isValid():
            return QtCore.QVariant()

        if role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(str(self.df.iat[index.row(), index.column()]))

        if role == QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignHCenter

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.df.index)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.df.columns)

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlags:
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable

    def setData(self, index: QtCore.QModelIndex, value, role: int = ...) -> bool:
        if role == QtCore.Qt.EditRole:
            self.df.iloc[index.row(), index.column()] = value
            return True


class VideoObject(QtCore.QObject):
    """
    This class is responsible for taking the video frames and transmit them in real time from a parallel thread to the
    Controller of the View.

    Attributes
    -----------
    run_flag: bool
        This flag controls the running of the camera. If it is set to True, the camera takes the frames.

    Methods
    -------
    run()
        Instantiates an OpenCV video capturer and begins the loop for capturing the frames.
    """
    frameCaptured = QtCore.pyqtSignal(np.ndarray)
    cameraReleased = QtCore.pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.run_flag = False
        self.fps = 50
        self.frame_size = (640, 480)

    def run(self) -> None:
        """
        This method starts the loop for capturing frame by frame from the video capturer.
        :return: None
        """
        camera = cv.VideoCapture(0, cv.CAP_MSMF)
        camera.set(cv.CAP_PROP_FPS, self.fps)
        self.fps = camera.get(cv.CAP_PROP_FPS)
        logging.info(f'FPS: {self.fps}')
        self.frame_size = (int(camera.get(cv.CAP_PROP_FRAME_WIDTH)), int(camera.get(cv.CAP_PROP_FRAME_HEIGHT)))
        while True:
            mutex.lock()
            if not self.run_flag:
                mutex.unlock()
                break
            mutex.unlock()
            ret, frame = camera.read()
            if ret:
                self.frameCaptured.emit(frame)
                # sleep(0.1)
        camera.release()
        self.cameraReleased.emit(True)


class VideoSaving(QtCore.QObject):
    """
    This is a class used as worker for saving a video in a parallel thread.

    Attributes
    -----------
    frames: list
        The list of the acquired video frames.
    video_writer: cv.VideoWriter
        The OpenCV video writer object

    Methods
    -------
    save_video()
        Method for saving the video frames in the hard disk.
    """
    videoSaved = QtCore.pyqtSignal(bool)

    def __init__(self, frames, video_writer: cv.VideoWriter):
        super().__init__()
        self.frames = frames
        self.video_writer = video_writer

    def save_video(self):
        logging.info('...Guardando vídeo...')
        for frame in self.frames:
            self.video_writer.write(frame)
        logging.info('...Video guardado...')
        self.video_writer.release()
        self.videoSaved.emit(True)


class ImageProcessingThread(QtCore.QThread):
    """
    This thread is intended to be used for process and recognize the frames acquired for some calibration point. Then,
    it constructs the stochastic model based on Markov chains. Finally, it estimates the measurement result as the
    expected value.

    Attributes
    ----------
    realTimeValues: pyqtSignal
        This signals shares the measurement value computed.
    _frames_queue: Queue
        This queue temporally stores the acquired videos, one video for each calibration point. This queue
        is intended to be used to secure the processing flow.
    _TESTER: ac.SLMPeriodicTester
        This is the model used for the periodic calibration of sound level meters.
    fps: int
        Frames per second of the camera object
    _stage: int
        The current stage of the calibration
    _current_f: int
        The current frequency under calibration
    _fweightings: list
        This is a list of strings representing the three frequency weightings: A, C and Z.
    _octave_frequencies: list
        This is a list of ints representing the nominal central frequency of octave bands.

    Methods
    _______
    run()
        This method executes the parallel processing and recognizing of the video frames. Also constructs the
        stochastic model.
    """
    realTimeValues = QtCore.pyqtSignal(float)

    def __init__(self, frames_queue: Queue, tester: ac.SLMPeriodicTester, camera: VideoObject):
        super(ImageProcessingThread, self).__init__()
        self._frames_queue = frames_queue
        self._TESTER = tester
        self._stage = 0
        self._current_f = 0
        self._fweightings = [*'ACZ']
        self._octave_frequencies = np.array([63, 125, 250, 500, 1e3, 2e3, 4e3, 8e3, 16e3])
        self.fps = camera.fps

    def run(self) -> None:
        """
        This method executes the parallel processing and recognizing of the video frames using the model's methods.
        This method also constructs the stochastic model based on Markov chains from the samples obtained of a
        downsampled sequence of images corresponding to the "real" samples of the sound level meter screen.
        :return: None
        """
        self._stage = self._TESTER.stage
        while self._stage < 8:
            if not self._frames_queue.empty():  # If there is any video in the queue
                logging.info(f'\n-----\nFrequency {int(self._octave_frequencies[self._current_f])} Hz process begins.')
                frames = self._frames_queue.get()
                frames = np.array([cv.cvtColor(frame, cv.COLOR_BGR2GRAY) for frame in frames])
                # Recognize first the frames taken while the stabilization time. This is for identifying the frame zero
                # and then computes downsampling in order to obtain the "true" samples from the screen.
                stab_frames = frames[:self._TESTER.elect_stab_time * self.fps, :, :]  # Samples until stabilization
                logging.info('--Recognizing stabilization frames--')
                stab_frames = np.array([self._TESTER.read_screen(frame) for frame in stab_frames])  # Recognize numbers
                changed_value_idx = np.where(stab_frames != stab_frames[0])[0][0]  # Frame 0 (first change identified)
                frames_down_sampled = frames[changed_value_idx:]  # From frame 0 onwards
                frames_down_sampled = frames_down_sampled[np.arange(0,  # Downsampling video signal
                                                                    frames_down_sampled.shape[0],
                                                                    self.fps // self._TESTER.dut.screen_rate + 2,
                                                                    dtype=int), :, :]
                stab_frame = int((self._TESTER.elect_stab_time - changed_value_idx / self.fps)
                                 * self._TESTER.dut.screen_rate)  # Frame in which the stabilization time has finished
                frames_down_sampled = frames_down_sampled[stab_frame:, :, :]  # Crops the stabilization time
                logging.info('--Recognizing measurement frames--')
                samples = np.array([self._TESTER.read_screen(frame) for frame in frames_down_sampled])
                del frames_down_sampled
                # Construction of the states transition matrix
                states = np.unique(samples)
                P = pd.DataFrame(data=np.zeros((states.shape[0], states.shape[0])), index=states, columns=states)
                for i in range(1, samples.shape[0]):
                    P.loc[samples[i - 1], samples[i]] += 1
                P = P.divide(samples.shape[0] - 1)
                # TODO: Probabilidad estacionaria y valor esperado

                if self._stage <= 8:  # Electric frequency weightings test
                    point_name = (f'{self._fweightings[self._stage - 5]}' +
                                  f'_{int(self._octave_frequencies[self._current_f])}')
                    path = ('CalibrationResults/ElectricalFrequencyWeightings/' + f'{point_name}Hz.pkl')
                    with open(path, "wb") as file:  # Saves the grayscale video in bare binary format
                        pickle.dump(frames, file)
                    del frames
                    self._TESTER.fweighting_results['Samples'][point_name] = samples
                    self._TESTER.fweighting_results['Transition Matrix'][point_name] = P
                    # TODO: Presentar resultado en la GUI
                # TODO: Pruebas restantes
                logging.info(f'Transition Matrix:\n{P}')
                logging.info(f'\nFrequency {int(self._octave_frequencies[self._current_f])} Hz process finish\n-----')
                del samples
                # Updates the current stage and frequency in process
                self._stage += self._current_f // 8
                self._current_f += (1 - 9 * (self._current_f // 8))

            else:
                sleep(1)
        with open('CalibrationResults/ElectricalFrequencyWeightings/DataFrame.pkl', 'wb') as file:
            pickle.dump(self._TESTER.fweighting_results, file)


class GraphicsRectItem(QtWidgets.QGraphicsRectItem):
    """
    This is the class for an interactive rectangle item used for controlling the region of interest.
    """
    handleTopLeft = 1
    handleTopMiddle = 2
    handleTopRight = 3
    handleMiddleLeft = 4
    handleMiddleRight = 5
    handleBottomLeft = 6
    handleBottomMiddle = 7
    handleBottomRight = 8

    handleSize = 5.0
    handleSpace = -4.0

    handleCursors = {
        handleTopLeft: QtCore.Qt.SizeFDiagCursor,
        handleTopMiddle: QtCore.Qt.SizeVerCursor,
        handleTopRight: QtCore.Qt.SizeBDiagCursor,
        handleMiddleLeft: QtCore.Qt.SizeHorCursor,
        handleMiddleRight: QtCore.Qt.SizeHorCursor,
        handleBottomLeft: QtCore.Qt.SizeBDiagCursor,
        handleBottomMiddle: QtCore.Qt.SizeVerCursor,
        handleBottomRight: QtCore.Qt.SizeFDiagCursor,
    }

    def __init__(self, *args):
        """
        Initialize the shape.
        """
        super().__init__(*args)
        self.handles = {}
        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None
        self.setAcceptHoverEvents(True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, True)
        self.updateHandlesPos()

    def handleAt(self, point):
        """
        Returns the resize handle below the given point.
        """
        for k, v, in self.handles.items():
            if v.contains(point):
                return k
        return None

    def hoverMoveEvent(self, moveEvent):
        """
        Executed when the mouse moves over the shape (NOT PRESSED).
        """
        if self.isSelected():
            handle = self.handleAt(moveEvent.pos())
            cursor = QtCore.Qt.ArrowCursor if handle is None else self.handleCursors[handle]
            self.setCursor(cursor)
        super().hoverMoveEvent(moveEvent)

    def hoverLeaveEvent(self, moveEvent):
        """
        Executed when the mouse leaves the shape (NOT PRESSED).
        """
        self.setCursor(QtCore.Qt.ArrowCursor)
        super().hoverLeaveEvent(moveEvent)

    def mousePressEvent(self, mouseEvent):
        """
        Executed when the mouse is pressed on the item.
        """
        self.handleSelected = self.handleAt(mouseEvent.pos())
        if self.handleSelected:
            self.mousePressPos = mouseEvent.pos()
            self.mousePressRect = self.boundingRect()
        super().mousePressEvent(mouseEvent)

    def mouseMoveEvent(self, mouseEvent):
        """
        Executed when the mouse is being moved over the item while being pressed.
        """
        if self.handleSelected is not None:
            self.interactiveResize(mouseEvent.pos())
        else:
            super().mouseMoveEvent(mouseEvent)

    def mouseReleaseEvent(self, mouseEvent):
        """
        Executed when the mouse is released from the item.
        """
        super().mouseReleaseEvent(mouseEvent)
        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None
        self.update()

    def boundingRect(self):
        """
        Returns the bounding rect of the shape (including the resize handles).
        """
        o = self.handleSize + self.handleSpace
        return self.rect().adjusted(-o, -o, o, o)

    def updateHandlesPos(self):
        """
        Update current resize handles according to the shape size and position.
        """
        s = self.handleSize
        b = self.boundingRect()
        self.handles[self.handleTopLeft] = QtCore.QRectF(b.left(), b.top(), s, s)
        self.handles[self.handleTopMiddle] = QtCore.QRectF(b.center().x() - s / 2, b.top(), s, s)
        self.handles[self.handleTopRight] = QtCore.QRectF(b.right() - s, b.top(), s, s)
        self.handles[self.handleMiddleLeft] = QtCore.QRectF(b.left(), b.center().y() - s / 2, s, s)
        self.handles[self.handleMiddleRight] = QtCore.QRectF(b.right() - s, b.center().y() - s / 2, s, s)
        self.handles[self.handleBottomLeft] = QtCore.QRectF(b.left(), b.bottom() - s, s, s)
        self.handles[self.handleBottomMiddle] = QtCore.QRectF(b.center().x() - s / 2, b.bottom() - s, s, s)
        self.handles[self.handleBottomRight] = QtCore.QRectF(b.right() - s, b.bottom() - s, s, s)

    def interactiveResize(self, mousePos):
        """
        Perform shape interactive resize.
        """
        offset = self.handleSize + self.handleSpace
        boundingRect = self.boundingRect()
        rect = self.rect()
        diff = QtCore.QPointF(0, 0)

        self.prepareGeometryChange()

        if self.handleSelected == self.handleTopLeft:

            fromX = self.mousePressRect.left()
            fromY = self.mousePressRect.top()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setLeft(toX)
            boundingRect.setTop(toY)
            rect.setLeft(boundingRect.left() + offset)
            rect.setTop(boundingRect.top() + offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleTopMiddle:

            fromY = self.mousePressRect.top()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setY(toY - fromY)
            boundingRect.setTop(toY)
            rect.setTop(boundingRect.top() + offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleTopRight:

            fromX = self.mousePressRect.right()
            fromY = self.mousePressRect.top()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setRight(toX)
            boundingRect.setTop(toY)
            rect.setRight(boundingRect.right() - offset)
            rect.setTop(boundingRect.top() + offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleMiddleLeft:

            fromX = self.mousePressRect.left()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            diff.setX(toX - fromX)
            boundingRect.setLeft(toX)
            rect.setLeft(boundingRect.left() + offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleMiddleRight:
            fromX = self.mousePressRect.right()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            diff.setX(toX - fromX)
            boundingRect.setRight(toX)
            rect.setRight(boundingRect.right() - offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleBottomLeft:

            fromX = self.mousePressRect.left()
            fromY = self.mousePressRect.bottom()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setLeft(toX)
            boundingRect.setBottom(toY)
            rect.setLeft(boundingRect.left() + offset)
            rect.setBottom(boundingRect.bottom() - offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleBottomMiddle:

            fromY = self.mousePressRect.bottom()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setY(toY - fromY)
            boundingRect.setBottom(toY)
            rect.setBottom(boundingRect.bottom() - offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleBottomRight:

            fromX = self.mousePressRect.right()
            fromY = self.mousePressRect.bottom()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setRight(toX)
            boundingRect.setBottom(toY)
            rect.setRight(boundingRect.right() - offset)
            rect.setBottom(boundingRect.bottom() - offset)
            self.setRect(rect)

        self.updateHandlesPos()

    def shape(self):
        """
        Returns the shape of this item as a QPainterPath in local coordinates.
        """
        path = QtGui.QPainterPath()
        path.addRect(self.rect())
        if self.isSelected():
            for shape in self.handles.values():
                path.addEllipse(shape)
        return path

    def paint(self, painter, option, widget=None):
        """
        Paint the node in the graphic view.
        """
        painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255, 0)))
        painter.setPen(QtGui.QPen(QtGui.QColor(127, 127, 127), 2.0, QtCore.Qt.DashLine))
        painter.drawRect(self.rect())

        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(81, 168, 220, 180)))
        painter.setPen(
            QtGui.QPen(QtGui.QColor(0, 0, 0, 255), 1.0, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        for handle, rect in self.handles.items():
            if self.handleSelected is None or handle == self.handleSelected:
                painter.drawRect(rect)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = SonometersCalibrationUI()
    Controller = GUIController(MainWindow)
    MainWindow.showMaximized()
    sys.exit(app.exec_())
