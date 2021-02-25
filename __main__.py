from PyQt5 import QtWidgets, uic

from serial.tools import list_ports
import threading
import time
import sys

from zaber_motion.units import Units

from MotionControl import MotionControl

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
        self.home_x_button.clicked.connect(self.home_x_mp)
        self.home_y_button.clicked.connect(self.home_y_mp)
        self.home_z_button.clicked.connect(self.home_z_mp)
        self.set_z_level_button.clicked.connect(self.set_z_level)
        self.use_xy_button.clicked.connect(self.set_current_xy)
        self.run_test_button.clicked.connect(self.run_test_fire)
        # Populate list of serial devices by description and 
        # initalize MotionControl object.
        self.populate_serial_list()
        self.motion_controller = MotionControl()
        self.is_updating_positions = False
        

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
        if self.connect_controller_button.text() == "Connect":
            print(self.serial_port_combo.currentText())
            _serport = self.serial_port_combo.currentText().split('(')
            self.motion_controller.connect_controller(_serport[1][0:4].__str__())
            self.connect_controller_button.setText('Disconnect')
            self.ui_update_thread = threading.Thread(target=self.position_update_worker, daemon=True)
            self.ui_update_thread.start()
        
        elif self.connect_controller_button.text() == "Disconnect":
            self.is_updating_positions = False
            self.motion_controller.disconnect_controller()
            self.connect_controller_button.setText('Connect')
        return
    
    def set_z_level(self):
        print("z-level offset clicked")
        self.motion_controller.set_z_offset()
        self.z_offset_label.setText('{0:.2f}'.format(self.motion_controller.z_offset))
        return

    def set_current_xy(self):
        print("current xy clicked")
        _xpos = float(self.x_origin_le.text())
        _ypos = float(self.y_origin_le.text())
        self.motion_controller.move_x(_xpos)
        self.motion_controller.move_y(_ypos)
        return

    def run_test_fire(self):
        print("test fire clicked")
        return

    def home_x(self):
        print("home x")
        self.motion_controller.home_x()
        self.motion_controller.x_axis.wait_until_idle()
        if(self.motion_controller.x_axis.get_position() == 0.0):
            self.home_x_button.setText('Homed')
            self.home_x_button.setEnabled(False)
        return

    def home_x_mp(self):
        homing_thread = threading.Thread(target=self.home_x)
        homing_thread.start()
        return

    def home_y_mp(self):
        homing_thread = threading.Thread(target=self.home_y)
        homing_thread.start()
        return

    def home_z_mp(self):
        homing_thread = threading.Thread(target=self.home_z)
        homing_thread.start()
        return

    def home_y(self):
        print("home y")
        self.motion_controller.home_y()
        if(self.motion_controller.y_axis.get_position() == 0.0):
            self.home_y_button.setText('Homed')
            self.home_y_button.setEnabled(False)
        return

    def home_z(self):
        print("home z")
        self.motion_controller.home_z()
        self.motion_controller.z_axis.wait_until_idle()
        if(self.motion_controller.z_axis.get_position() == 0.0):
            self.home_z_button.setText('Homed')
            self.home_z_button.setEnabled(False)
        return

    def populate_serial_list(self):
        port_info = list_ports.comports()
        for x in range(0, port_info.__len__()):
            self.serial_port_combo.addItem(port_info[x][1])

    def position_update_worker(self):
        _interval = 0.250       # time to update UI in seconds
        self.is_updating_positions = True
        while self.is_updating_positions == True:
            self.x_position_label.setText('{0:.3f}'.format(
                self.motion_controller.x_axis.get_position(Units.LENGTH_MILLIMETRES)))
            self.y_position_label.setText('{0:.3f}'.format(
                self.motion_controller.y_axis.get_position(Units.LENGTH_MILLIMETRES)))
            self.z_position_label.setText('{0:.3f}'.format(
                self.motion_controller.z_axis.get_position(Units.LENGTH_MILLIMETRES)))
            time.sleep(_interval)
# Load the Ui and execute the application
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()
