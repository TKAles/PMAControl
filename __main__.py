from PyQt5 import QtWidgets, uic

import sys

class Ui(QtWidgets.QMainWindow):
    '''
    Ui: Class to load the Ui and provide callback functions
    '''
    def __init__(self):
        super(Ui,self).__init__()
        uic.loadUi('PMAControlUI.ui', self)
        self.show()


# Load the Ui and execute the application
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()
