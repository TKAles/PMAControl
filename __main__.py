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
        # Wire up the signals to the Ui
        self.x_origin_le.editingFinished.connect(self.x_origin_changed)
        self.y_origin_le.editingFinished.connect(self.y_origin_changed)
        self.test_length_le.editingFinished.connect(self.test_length_changed)
        self.prefire_le.editingFinished.connect(self.prefire_length_changed)
        self.postfire_le.editingFinished.connect(self.postfire_length_changed)
        self.serial_port_combo.currentIndexChanged.connect(self.selected_port_changed)
        self.connect_controller_button.clicked.connect(self.toggle_controller)
        self.home_x_button.clicked.connect(self.home_x)
        self.home_y_button.clicked.connect(self.home_y)
        self.home_z_button.clicked.connect(self.home_z)
        self.set_z_level_button.clicked.connect(self.set_z_level)
        self.use_xy_button.clicked.connect(self.set_current_xy)
        self.run_test_button.clicked.connect(self.run_test_fire)

    def x_origin_changed(self):
        print("editingFinished event caught on x_origin_le")
        return

    def y_origin_changed(self):
        print("editingFinished event caught on y_origin_le")
        return

    def test_length_changed(self):
        print("editingFinished event caught on test_length_le")
        return

    def prefire_length_changed(self):
        print("editingFinished event caught on prefire_le")
        return

    def postfire_length_changed(self):
        print("editingFinished on postfire_le")
        return

    def selected_port_changed(self):
        print("comport combobox changed")
        return

    def toggle_controller(self):
        print("controller toggled")
        return
    
    def set_z_level(self):
        print("z-level offset clicked")
        return

    def set_current_xy(self):
        print("current xy clicked")
        return

    def run_test_fire(self):
        print("test fire clicked")
        return

    def home_x(self):
        print("home x")
        return

    def home_y(self):
        print("home y")
        return

    def home_z(self):
        print("home z")
        return


# Load the Ui and execute the application
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()
