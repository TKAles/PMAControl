import zaber_motion

class MotionControl(self):

    def __init__(self):
        self.xy_controller = []
        self.z_controller = []
        self.x_axis = []
        self.y_axis = []
        self.z_axis = []
        self.velocity_target = 0.00
        self.z_offset = 0.00
        
    