# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'colorimeter_gui.ui'
#
# Created: Tue Feb  7 11:43:23 2012
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(651, 441)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.widget_2 = QtGui.QWidget(self.centralwidget)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame = QtGui.QFrame(self.widget_2)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.transmissionGroupBox = QtGui.QGroupBox(self.frame)
        self.transmissionGroupBox.setObjectName("transmissionGroupBox")
        self.verticalLayout = QtGui.QVBoxLayout(self.transmissionGroupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.transmissionTextEdit = QtGui.QTextEdit(self.transmissionGroupBox)
        self.transmissionTextEdit.setObjectName("transmissionTextEdit")
        self.verticalLayout.addWidget(self.transmissionTextEdit)
        self.verticalLayout_2.addWidget(self.transmissionGroupBox)
        self.horizontalLayout_2.addWidget(self.frame)
        self.frame_2 = QtGui.QFrame(self.widget_2)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.frame_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.absorbanceGroupBox = QtGui.QGroupBox(self.frame_2)
        self.absorbanceGroupBox.setObjectName("absorbanceGroupBox")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.absorbanceGroupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.absorbanceTextEdit = QtGui.QTextEdit(self.absorbanceGroupBox)
        self.absorbanceTextEdit.setObjectName("absorbanceTextEdit")
        self.verticalLayout_3.addWidget(self.absorbanceTextEdit)
        self.verticalLayout_4.addWidget(self.absorbanceGroupBox)
        self.horizontalLayout_2.addWidget(self.frame_2)
        self.verticalLayout_5.addWidget(self.widget_2)
        self.widget_3 = QtGui.QWidget(self.centralwidget)
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.widget_3)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtGui.QLabel(self.widget_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.samplesLineEdit = QtGui.QLineEdit(self.widget_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.samplesLineEdit.sizePolicy().hasHeightForWidth())
        self.samplesLineEdit.setSizePolicy(sizePolicy)
        self.samplesLineEdit.setMaximumSize(QtCore.QSize(100, 16777215))
        self.samplesLineEdit.setObjectName("samplesLineEdit")
        self.horizontalLayout_3.addWidget(self.samplesLineEdit)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.redCheckBox = QtGui.QCheckBox(self.widget_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.redCheckBox.sizePolicy().hasHeightForWidth())
        self.redCheckBox.setSizePolicy(sizePolicy)
        self.redCheckBox.setMaximumSize(QtCore.QSize(65, 16777215))
        self.redCheckBox.setChecked(True)
        self.redCheckBox.setObjectName("redCheckBox")
        self.horizontalLayout_3.addWidget(self.redCheckBox)
        self.greenCheckBox = QtGui.QCheckBox(self.widget_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.greenCheckBox.sizePolicy().hasHeightForWidth())
        self.greenCheckBox.setSizePolicy(sizePolicy)
        self.greenCheckBox.setMaximumSize(QtCore.QSize(65, 16777215))
        self.greenCheckBox.setChecked(True)
        self.greenCheckBox.setObjectName("greenCheckBox")
        self.horizontalLayout_3.addWidget(self.greenCheckBox)
        self.blueCheckBox = QtGui.QCheckBox(self.widget_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.blueCheckBox.sizePolicy().hasHeightForWidth())
        self.blueCheckBox.setSizePolicy(sizePolicy)
        self.blueCheckBox.setMaximumSize(QtCore.QSize(65, 16777215))
        self.blueCheckBox.setChecked(True)
        self.blueCheckBox.setObjectName("blueCheckBox")
        self.horizontalLayout_3.addWidget(self.blueCheckBox)
        self.whiteCheckBox = QtGui.QCheckBox(self.widget_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.whiteCheckBox.sizePolicy().hasHeightForWidth())
        self.whiteCheckBox.setSizePolicy(sizePolicy)
        self.whiteCheckBox.setMaximumSize(QtCore.QSize(65, 16777215))
        self.whiteCheckBox.setChecked(True)
        self.whiteCheckBox.setObjectName("whiteCheckBox")
        self.horizontalLayout_3.addWidget(self.whiteCheckBox)
        self.verticalLayout_5.addWidget(self.widget_3)
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_5.addWidget(self.line)
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
        self.portLineEdit.setObjectName("portLineEdit")
        self.horizontalLayout.addWidget(self.portLineEdit)
        self.connectPushButton = QtGui.QPushButton(self.widget)
        self.connectPushButton.setObjectName("connectPushButton")
        self.horizontalLayout.addWidget(self.connectPushButton)
        spacerItem1 = QtGui.QSpacerItem(322, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.calibratePushButton = QtGui.QPushButton(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.calibratePushButton.sizePolicy().hasHeightForWidth())
        self.calibratePushButton.setSizePolicy(sizePolicy)
        self.calibratePushButton.setObjectName("calibratePushButton")
        self.horizontalLayout.addWidget(self.calibratePushButton)
        self.measurePushButton = QtGui.QPushButton(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.measurePushButton.sizePolicy().hasHeightForWidth())
        self.measurePushButton.setSizePolicy(sizePolicy)
        self.measurePushButton.setObjectName("measurePushButton")
        self.horizontalLayout.addWidget(self.measurePushButton)
        self.verticalLayout_5.addWidget(self.widget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 651, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Colorimeter", None, QtGui.QApplication.UnicodeUTF8))
        self.transmissionGroupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Transmission", None, QtGui.QApplication.UnicodeUTF8))
        self.absorbanceGroupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Absorbance", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Samples   ", None, QtGui.QApplication.UnicodeUTF8))
        self.redCheckBox.setText(QtGui.QApplication.translate("MainWindow", "red", None, QtGui.QApplication.UnicodeUTF8))
        self.greenCheckBox.setText(QtGui.QApplication.translate("MainWindow", "green", None, QtGui.QApplication.UnicodeUTF8))
        self.blueCheckBox.setText(QtGui.QApplication.translate("MainWindow", "blue", None, QtGui.QApplication.UnicodeUTF8))
        self.whiteCheckBox.setText(QtGui.QApplication.translate("MainWindow", "white", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Serail Port", None, QtGui.QApplication.UnicodeUTF8))
        self.connectPushButton.setText(QtGui.QApplication.translate("MainWindow", "Connect", None, QtGui.QApplication.UnicodeUTF8))
        self.calibratePushButton.setText(QtGui.QApplication.translate("MainWindow", "Calibrate", None, QtGui.QApplication.UnicodeUTF8))
        self.measurePushButton.setText(QtGui.QApplication.translate("MainWindow", "Measure", None, QtGui.QApplication.UnicodeUTF8))
