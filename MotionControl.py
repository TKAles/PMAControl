'''
    MotionControl Object Version 0.0.1
    Thomas Ales | Iowa State University
    Feb-24-2021
'''
from zaber_motion.ascii import Connection, Device, Axis
from zaber_motion.units import Units
from zaber_motion import Library

class MotionControl():
    '''
    MotionControl: Object that represents the Zaber gantry
                   configuration used by the microarc system.
    '''
    def __init__(self):
        # Initalize object parameters
        self.serial_connection = []
        self.xy_controller = []
        self.z_controller = []
        self.x_axis = []
        self.y_axis = []
        self.z_axis = []
        self.positions = [0.0, 0.0, 0.0]
        self.velocity_target = 0.00
        self.z_offset = 0.00
        # Subprocess semaphores
        self.is_polling = False
        
    def connect_controller(self, _comport):
        '''
        connect_controller(self, _comport): Opens the serial
            connection on the specific COMport (COMx - Windows, 
            /dev/usbTTYx) on Linux/macOS. Assigns controllers and
            axes.
        '''
        # Enable DB store allows for device lookup so real world
        # units can be used. Requires internet connection
        Library.enable_device_db_store()
        # Open serial connection, assign controllers, 
        # identify models attached to controller, assign axes
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
        '''
        disconnect_controller(): Closes the serial connection to the
            XCB-2 controller.
        '''
        self.serial_connection.close()
        return

    def home_x(self):
        '''
        home_x(): Homes the x-axis of the system.
        '''
        self.x_axis.home()
        return

    def home_y(self):
        '''
        home_y(): Homes the y-axis of the system.
        '''
        self.y_axis.home()
        return

    def home_z(self):
        '''
        home_z(): Homes the z-axis of the system.
        '''
        self.z_axis.home()
        return

    def set_z_offset(self):
        '''
        set_z_offset(): Takes the current position of the z-stage
        and uses that as the 0.0 height for other calculations.
        '''
        self.z_offset = self.z_axis.get_position(Units.LENGTH_MILLIMETRES)
        return

    def move_x(self, _position):
        '''
        move_x(_position): Perform a move of the x axis to an
            absolute position. Expects millimeters
        '''
        self.x_axis.move_absolute(_position, Units.LENGTH_MILLIMETRES)
        self.x_axis.wait_until_idle()
        return
    
    def move_y(self, _position):
        '''
        move_y(_position): Perform a move of the y axis to an
            absolute position. Expects millimeters
        '''
        self.y_axis.move_absolute(_position, Units.LENGTH_MILLIMETRES)
        self.y_axis.wait_until_idle()
        return

    def move_z(self, _position):
        '''
        move_z(_position): Perform a move of the z axis to an
            absolute position. Expects millimeters
        '''
        # TODO: Add error check for if z-offset is set and requested
        # z position ends up below the plate.
        self.z_axis.move_absolute(_position, Units.LENGTH_MILLIMETRES)
        self.z_axis.wait_until_idle()
        return

    def toggle_feed(self, _state):
        '''
        toggle_feed(_state): Toggles the digital output (DO1) to
            enable the wire-feed system and start feeding wire.
        '''
        self.xy_controller.io.set_digital_output(1, _state)
        return

    def toggle_torch(self, _state):
        '''
        toggle_torch(_state): Toggles the digital output (DO2) to
            close the torch activate circuit. Will start the plasma
            process. Dual Arc MUST BE CONFIGURED PRIOR TO ACTIVATION.
            NO SOFTWARE CONTROL
        '''
        self.xy_controller.io.set_digital_output(2, _state)
        return

    def set_default_velocities(self):
        self.x_axis.settings.set('maxspeed', 100.0, Units.VELOCITY_MILLIMETRES_PER_SECOND)
        self.y_axis.settings.set('maxspeed', 100.0, Units.VELOCITY_MILLIMETRES_PER_SECOND)
        self.z_axis.settings.set('maxspeed', 100.0, Units.VELOCITY_MILLIMETRES_PER_SECOND)
        return