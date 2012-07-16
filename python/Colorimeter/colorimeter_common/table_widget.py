from PyQt4 import QtCore
from PyQt4 import QtGui

class ColorimeterTableWidget(QtGui.QTableWidget):

    def __init__(self,*args,**kwargs):
        super(ColorimeterTableWidget,self).__init__(self,*args,**kwargs)
