# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'colorimeter_plot_gui.ui'
#
# Created: Tue Jun 12 17:31:01 2012
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(487, 618)
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Colorimeter Plot Slammer", None, QtGui.QApplication.UnicodeUTF8))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget = QtGui.QWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Serial Port", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.portLineEdit = QtGui.QLineEdit(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.portLineEdit.sizePolicy().hasHeightForWidth())
        self.portLineEdit.setSizePolicy(sizePolicy)
        self.portLineEdit.setMaximumSize(QtCore.QSize(140, 16777215))
        self.portLineEdit.setObjectName(_fromUtf8("portLineEdit"))
        self.horizontalLayout.addWidget(self.portLineEdit)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.connectPushButton = QtGui.QPushButton(self.widget)
        self.connectPushButton.setText(QtGui.QApplication.translate("MainWindow", "Connect", None, QtGui.QApplication.UnicodeUTF8))
        self.connectPushButton.setObjectName(_fromUtf8("connectPushButton"))
        self.horizontalLayout.addWidget(self.connectPushButton)
        self.verticalLayout.addWidget(self.widget)
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.widget_2 = QtGui.QWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.redRadioButton = QtGui.QRadioButton(self.widget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.redRadioButton.sizePolicy().hasHeightForWidth())
        self.redRadioButton.setSizePolicy(sizePolicy)
        self.redRadioButton.setText(QtGui.QApplication.translate("MainWindow", "red", None, QtGui.QApplication.UnicodeUTF8))
        self.redRadioButton.setObjectName(_fromUtf8("redRadioButton"))
        self.horizontalLayout_2.addWidget(self.redRadioButton)
        self.greenRadioButton = QtGui.QRadioButton(self.widget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.greenRadioButton.sizePolicy().hasHeightForWidth())
        self.greenRadioButton.setSizePolicy(sizePolicy)
        self.greenRadioButton.setText(QtGui.QApplication.translate("MainWindow", "green", None, QtGui.QApplication.UnicodeUTF8))
        self.greenRadioButton.setObjectName(_fromUtf8("greenRadioButton"))
        self.horizontalLayout_2.addWidget(self.greenRadioButton)
        self.blueRadioButton = QtGui.QRadioButton(self.widget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.blueRadioButton.sizePolicy().hasHeightForWidth())
        self.blueRadioButton.setSizePolicy(sizePolicy)
        self.blueRadioButton.setText(QtGui.QApplication.translate("MainWindow", "blue", None, QtGui.QApplication.UnicodeUTF8))
        self.blueRadioButton.setObjectName(_fromUtf8("blueRadioButton"))
        self.horizontalLayout_2.addWidget(self.blueRadioButton)
        self.whiteRadioButton = QtGui.QRadioButton(self.widget_2)
        self.whiteRadioButton.setText(QtGui.QApplication.translate("MainWindow", "white", None, QtGui.QApplication.UnicodeUTF8))
        self.whiteRadioButton.setObjectName(_fromUtf8("whiteRadioButton"))
        self.horizontalLayout_2.addWidget(self.whiteRadioButton)
        spacerItem1 = QtGui.QSpacerItem(134, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addWidget(self.widget_2)
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.tableWidget = QtGui.QTableWidget(self.frame)
        self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.AnyKeyPressed|QtGui.QAbstractItemView.DoubleClicked|QtGui.QAbstractItemView.SelectedClicked)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.horizontalLayout_4.addWidget(self.tableWidget)
        self.verticalLayout.addWidget(self.frame)
        self.widget_3 = QtGui.QWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.widget_3.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.widget_3.setObjectName(_fromUtf8("widget_3"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.widget_3)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.calibratePushButton = QtGui.QPushButton(self.widget_3)
        self.calibratePushButton.setText(QtGui.QApplication.translate("MainWindow", "Calibrate", None, QtGui.QApplication.UnicodeUTF8))
        self.calibratePushButton.setObjectName(_fromUtf8("calibratePushButton"))
        self.horizontalLayout_3.addWidget(self.calibratePushButton)
        self.clearPushButton = QtGui.QPushButton(self.widget_3)
        self.clearPushButton.setText(QtGui.QApplication.translate("MainWindow", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.clearPushButton.setObjectName(_fromUtf8("clearPushButton"))
        self.horizontalLayout_3.addWidget(self.clearPushButton)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.measurePushButton = QtGui.QPushButton(self.widget_3)
        self.measurePushButton.setText(QtGui.QApplication.translate("MainWindow", "Measure", None, QtGui.QApplication.UnicodeUTF8))
        self.measurePushButton.setObjectName(_fromUtf8("measurePushButton"))
        self.horizontalLayout_3.addWidget(self.measurePushButton)
        self.plotPushButton = QtGui.QPushButton(self.widget_3)
        self.plotPushButton.setText(QtGui.QApplication.translate("MainWindow", "Plot", None, QtGui.QApplication.UnicodeUTF8))
        self.plotPushButton.setObjectName(_fromUtf8("plotPushButton"))
        self.horizontalLayout_3.addWidget(self.plotPushButton)
        self.verticalLayout.addWidget(self.widget_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 487, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuAbout = QtGui.QMenu(self.menubar)
        self.menuAbout.setTitle(QtGui.QApplication.translate("MainWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAbout.setObjectName(_fromUtf8("menuAbout"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.action_Save = QtGui.QAction(MainWindow)
        self.action_Save.setText(QtGui.QApplication.translate("MainWindow", "&Save...", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Save.setObjectName(_fromUtf8("action_Save"))
        self.action_About = QtGui.QAction(MainWindow)
        self.action_About.setText(QtGui.QApplication.translate("MainWindow", "About...", None, QtGui.QApplication.UnicodeUTF8))
        self.action_About.setObjectName(_fromUtf8("action_About"))
        self.menuFile.addAction(self.action_Save)
        self.menuAbout.addAction(self.action_About)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        pass

