# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'colorimeter_measurement.ui'
#
# Created: Fri Jul  6 17:47:08 2012
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(589, 537)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtGui.QWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.portLineEdit = QtGui.QLineEdit(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.portLineEdit.sizePolicy().hasHeightForWidth())
        self.portLineEdit.setSizePolicy(sizePolicy)
        self.portLineEdit.setMaximumSize(QtCore.QSize(140, 16777215))
        self.portLineEdit.setObjectName("portLineEdit")
        self.horizontalLayout.addWidget(self.portLineEdit)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.connectPushButton = QtGui.QPushButton(self.widget)
        self.connectPushButton.setObjectName("connectPushButton")
        self.horizontalLayout.addWidget(self.connectPushButton)
        self.verticalLayout.addWidget(self.widget)
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.testSolutionWidget = QtGui.QWidget(self.centralwidget)
        self.testSolutionWidget.setObjectName("testSolutionWidget")
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.testSolutionWidget)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_4 = QtGui.QLabel(self.testSolutionWidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_5.addWidget(self.label_4)
        self.testSolutionComboBox = QtGui.QComboBox(self.testSolutionWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.testSolutionComboBox.sizePolicy().hasHeightForWidth())
        self.testSolutionComboBox.setSizePolicy(sizePolicy)
        self.testSolutionComboBox.setMinimumSize(QtCore.QSize(200, 0))
        self.testSolutionComboBox.setObjectName("testSolutionComboBox")
        self.horizontalLayout_5.addWidget(self.testSolutionComboBox)
        spacerItem1 = QtGui.QSpacerItem(461, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.verticalLayout.addWidget(self.testSolutionWidget)
        self.line_2 = QtGui.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.coeffLEDWidget = QtGui.QWidget(self.centralwidget)
        self.coeffLEDWidget.setObjectName("coeffLEDWidget")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.coeffLEDWidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtGui.QLabel(self.coeffLEDWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.coefficientLineEdit = QtGui.QLineEdit(self.coeffLEDWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.coefficientLineEdit.sizePolicy().hasHeightForWidth())
        self.coefficientLineEdit.setSizePolicy(sizePolicy)
        self.coefficientLineEdit.setMaximumSize(QtCore.QSize(120, 16777215))
        self.coefficientLineEdit.setObjectName("coefficientLineEdit")
        self.horizontalLayout_2.addWidget(self.coefficientLineEdit)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.label_3 = QtGui.QLabel(self.coeffLEDWidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.redRadioButton = QtGui.QRadioButton(self.coeffLEDWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.redRadioButton.sizePolicy().hasHeightForWidth())
        self.redRadioButton.setSizePolicy(sizePolicy)
        self.redRadioButton.setObjectName("redRadioButton")
        self.horizontalLayout_2.addWidget(self.redRadioButton)
        self.greenRadioButton = QtGui.QRadioButton(self.coeffLEDWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.greenRadioButton.sizePolicy().hasHeightForWidth())
        self.greenRadioButton.setSizePolicy(sizePolicy)
        self.greenRadioButton.setObjectName("greenRadioButton")
        self.horizontalLayout_2.addWidget(self.greenRadioButton)
        self.blueRadioButton = QtGui.QRadioButton(self.coeffLEDWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.blueRadioButton.sizePolicy().hasHeightForWidth())
        self.blueRadioButton.setSizePolicy(sizePolicy)
        self.blueRadioButton.setObjectName("blueRadioButton")
        self.horizontalLayout_2.addWidget(self.blueRadioButton)
        self.whiteRadioButton = QtGui.QRadioButton(self.coeffLEDWidget)
        self.whiteRadioButton.setObjectName("whiteRadioButton")
        self.horizontalLayout_2.addWidget(self.whiteRadioButton)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout.addWidget(self.coeffLEDWidget)
        self.line_3 = QtGui.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout.addWidget(self.line_3)
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.tableWidget = QtGui.QTableWidget(self.frame)
        self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.AnyKeyPressed|QtGui.QAbstractItemView.DoubleClicked|QtGui.QAbstractItemView.SelectedClicked)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.ContiguousSelection)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.horizontalLayout_4.addWidget(self.tableWidget)
        self.verticalLayout.addWidget(self.frame)
        self.widget_3 = QtGui.QWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.widget_3.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.widget_3)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.calibratePushButton = QtGui.QPushButton(self.widget_3)
        self.calibratePushButton.setObjectName("calibratePushButton")
        self.horizontalLayout_3.addWidget(self.calibratePushButton)
        self.clearPushButton = QtGui.QPushButton(self.widget_3)
        self.clearPushButton.setObjectName("clearPushButton")
        self.horizontalLayout_3.addWidget(self.clearPushButton)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.measurePushButton = QtGui.QPushButton(self.widget_3)
        self.measurePushButton.setObjectName("measurePushButton")
        self.horizontalLayout_3.addWidget(self.measurePushButton)
        self.plotPushButton = QtGui.QPushButton(self.widget_3)
        self.plotPushButton.setObjectName("plotPushButton")
        self.horizontalLayout_3.addWidget(self.plotPushButton)
        self.verticalLayout.addWidget(self.widget_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 589, 23))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuOptions = QtGui.QMenu(self.menubar)
        self.menuOptions.setObjectName("menuOptions")
        self.menuInclude = QtGui.QMenu(self.menuOptions)
        self.menuInclude.setObjectName("menuInclude")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionReloadTestSolutions = QtGui.QAction(MainWindow)
        self.actionReloadTestSolutions.setObjectName("actionReloadTestSolutions")
        self.actionEditTestSolutions = QtGui.QAction(MainWindow)
        self.actionEditTestSolutions.setObjectName("actionEditTestSolutions")
        self.actionIncludeUserTestSolutions = QtGui.QAction(MainWindow)
        self.actionIncludeUserTestSolutions.setCheckable(True)
        self.actionIncludeUserTestSolutions.setObjectName("actionIncludeUserTestSolutions")
        self.actionIncludeDefaultTestSolutions = QtGui.QAction(MainWindow)
        self.actionIncludeDefaultTestSolutions.setCheckable(True)
        self.actionIncludeDefaultTestSolutions.setObjectName("actionIncludeDefaultTestSolutions")
        self.actionLoad = QtGui.QAction(MainWindow)
        self.actionLoad.setObjectName("actionLoad")
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionLoad)
        self.menuInclude.addAction(self.actionIncludeUserTestSolutions)
        self.menuInclude.addAction(self.actionIncludeDefaultTestSolutions)
        self.menuOptions.addAction(self.menuInclude.menuAction())
        self.menuOptions.addAction(self.actionReloadTestSolutions)
        self.menuOptions.addAction(self.actionEditTestSolutions)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuOptions.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Colorimeter Measurement", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Serial Port", None, QtGui.QApplication.UnicodeUTF8))
        self.connectPushButton.setText(QtGui.QApplication.translate("MainWindow", "Connect", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "Test Solution", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Coefficient: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "LED", None, QtGui.QApplication.UnicodeUTF8))
        self.redRadioButton.setText(QtGui.QApplication.translate("MainWindow", "red", None, QtGui.QApplication.UnicodeUTF8))
        self.greenRadioButton.setText(QtGui.QApplication.translate("MainWindow", "green", None, QtGui.QApplication.UnicodeUTF8))
        self.blueRadioButton.setText(QtGui.QApplication.translate("MainWindow", "blue", None, QtGui.QApplication.UnicodeUTF8))
        self.whiteRadioButton.setText(QtGui.QApplication.translate("MainWindow", "white", None, QtGui.QApplication.UnicodeUTF8))
        self.calibratePushButton.setText(QtGui.QApplication.translate("MainWindow", "Calibrate", None, QtGui.QApplication.UnicodeUTF8))
        self.clearPushButton.setText(QtGui.QApplication.translate("MainWindow", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.measurePushButton.setText(QtGui.QApplication.translate("MainWindow", "Measure", None, QtGui.QApplication.UnicodeUTF8))
        self.plotPushButton.setText(QtGui.QApplication.translate("MainWindow", "Plot", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuOptions.setTitle(QtGui.QApplication.translate("MainWindow", "Options", None, QtGui.QApplication.UnicodeUTF8))
        self.menuInclude.setTitle(QtGui.QApplication.translate("MainWindow", "Include", None, QtGui.QApplication.UnicodeUTF8))
        self.actionReloadTestSolutions.setText(QtGui.QApplication.translate("MainWindow", "Reload Test Solutions", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEditTestSolutions.setText(QtGui.QApplication.translate("MainWindow", "Edit Test Solutions", None, QtGui.QApplication.UnicodeUTF8))
        self.actionIncludeUserTestSolutions.setText(QtGui.QApplication.translate("MainWindow", "User Test Solutions", None, QtGui.QApplication.UnicodeUTF8))
        self.actionIncludeDefaultTestSolutions.setText(QtGui.QApplication.translate("MainWindow", "Default Test Solutions", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoad.setText(QtGui.QApplication.translate("MainWindow", "&Load", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("MainWindow", "&Save", None, QtGui.QApplication.UnicodeUTF8))

