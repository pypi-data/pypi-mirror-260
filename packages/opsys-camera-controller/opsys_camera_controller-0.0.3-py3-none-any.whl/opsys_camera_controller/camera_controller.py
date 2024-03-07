import os
from .camera_abstract import CameraAbstract
from .configs import CameraTypes


class CameraController(CameraAbstract):
    """
    Camera controller interface
    """

    def __init__(self, camera_type, frame_handler=None):
        """
        Initialize parameters

        Args:
            camera_type (str): camera model name
            frame_handler (function, optional): frame handler function.
                                                Defaults to None.
        """
        self.camera_type = camera_type

        if self.camera_type == CameraTypes.ALLIED:
            from .vimba.allied_camera import AlliedCamera

            self.camera = AlliedCamera()

        elif self.camera_type == CameraTypes.IDS:
            from .ids.ids_camera import IdsCamera

            self.camera = IdsCamera()
            
        elif self.camera_type == CameraTypes.IDS_PEAK:
            from .ids.ids_peak_camera import IdsPeakCamera

            self.camera = IdsPeakCamera()

        self.camera.frame_handler_selected = frame_handler  # set frame handler

    def connect(self):
        """
        Connect to camera
        """
        self.camera.connect()
        
    def disconnect(self):
        """
        Disconnect from camera
        """
        if self.camera_type == CameraTypes.ALLIED:
            # runs in context manager - disconnects at exit
            print('Allied camera disconnected!')

        elif self.camera_type == CameraTypes.IDS:
            self.camera.free_memory()
            
        elif self.camera_type == CameraTypes.IDS_PEAK:
            self.camera.disconnect()

    def save_configurations(self, configs_filepath=None, to_eeprom=None):
        """
        Save configurations from camera to configurations file

        Args:
            configs_filepath (str, optional): configurations file path. Defaults to None.
            to_eeprom (bool, optional): Save to EEPROM. Defaults to False.
        """
        self.camera.save_configurations(
            configs_filepath=configs_filepath, to_eeprom=to_eeprom)

    def load_configurations(self, configs_filepath=None, from_eeprom=None):
        """
        Load configurations from configurations file to camera

        Args:
            configs_filepath (str, optional): configurations file path. Defaults to None.
            from_eeprom (bool, optional): Load from EEPROM. Defaults to False.
        """
        self.camera.load_configurations(
            configs_filepath=configs_filepath, from_eeprom=from_eeprom)

    def get_parameter(self, parameter_name):
        """
        Get camera parameter value

        Args:
            parameter_name (str): paramater name

        Returns:
            object: parameter value
        """
        return self.camera.get_parameter(parameter_name)

    def set_parameter(self, parameter_name, parameter_value=None, parameter_state=None):
        """
        Set camera parameter state and/or value

        Args:
            parameter_name (str): paramater name
            parameter_value (int/float, optional): parameter value. Defaults to None.
            parameter_state (str, optional): According to device API. Defaults to None.
        """
        self.camera.set_parameter(
            parameter_name, parameter_value, parameter_state)

    def get_image(self):
        """
        Get frame from camera

        Returns:
            numpy.array: image pixels 2D numpy array
        """
        return self.camera.get_image()

    def save_image(self, path=f'{os.getcwd()}/frame.jpg'):
        """
        Save image 2D array to jpg file

        Args:
            path (str, optional): path to save the image at.
                                  Defaults to f'{os.getcwd()}/frame.jpg'.
        """
        self.camera.save_image(path=path)

    def record(self, record_time=0):
        """
        Live frames streaming

        Args:
            record_time (int, optional): streaming time duration. 
                                         Defaults to 0.
        """
        self.camera.record(record_time)
