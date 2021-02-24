from typing import NoReturn
from zaber_motion.ascii import Connection, Device, Axis
from zaber_motion.units import Units
from zaber_motion import Library

class MotionControl():

    def __init__(self):
        self.serial_connection = []
        self.xy_controller = []
        self.z_controller = []
        self.x_axis = []
        self.y_axis = []
        self.z_axis = []
        self.velocity_target = 0.00
        self.z_offset = 0.00
        
    def connect_controller(self, _comport):
        Library.enable_device_db_store()
        self.serial_connection = Connection.open_serial_port(_comport)
        self.xy_controller = self.serial_connection.get_device(1)
        self.z_controller = self.serial_connection.get_device(2)
        self.xy_controller.identify()
        self.z_controller.identify()
        self.x_axis = self.xy_controller.get_axis(1)
        self.y_axis = self.xy_controller.get_axis(2)
        self.z_axis = self.z_controller.get_axis(1)
        return

    def disconnect_controller(self):
        self.serial_connection.close()
        return

    def home_x(self):
        self.x_axis.home()
        return

    def home_y(self):
        self.y_axis.home()
        return

    def home_z(self):
        self.z_axis.home()
        return

    def set_z_offset(self):
        self.z_offset = self.z_axis.get_position()
        return

    def move_x(self, _position):
        self.x_axis.move_absolute(_position, Units.LENGTH_MILLIMETRES)
        self.x_axis.wait_until_idle()
        return
    
    def move_y(self, _position):
        self.y_axis.move_absolute(_position, Units.LENGTH_MILLIMETRES)
        self.y_axis.wait_until_idle()
        return

    def move_z(self, _position):
        self.z_axis.move_absolute(_position, Units.LENGTH_MILLIMETRES)
        self.z_axis.wait_until_idle()
        return

    def toggle_feed(self, _state):
        if _state == True:
            self.xy_controller.io.set_digital_output(1, True)
            return
        elif _state == False:
            self.xy_controller.io.set_digital_output(1, False)
            return
        
        return

    def toggle_torch(self, _state):
        if _state == True:
            self.xy_controller.io.set_digital_output(2, True)
            return
        elif _state == False:
            self.xy_controller.io.set_digital_output(2, False)
            return

        return

        return