from ..camera_abstract import CameraAbstract
import cv2
import time
import threading
from . import vimba, error, camera
from .frame import PixelFormat, FrameStatus
from ..configs import CameraParameters


ENTER_KEY_CODE = 13  # keyboard code


class AlliedCamera(CameraAbstract):
    """
    Allied camera controller interface
    """

    def __init__(self):
        """
        Initialize parameters
        """
        self.camera = None
        self._user_set = None
        # image acquisition event handler
        self.shutdown_event = threading.Event()
        self.frame_handler_selected = None

    def connect(self):
        """
        Connect to camera
        """
        with vimba.Vimba.get_instance() as cam:  # call vimba API
            cams = cam.get_all_cameras()

        self.camera = cams[0]

    def _get_active_user_set(self):
        """
        Get user set ID
        """
        with vimba.Vimba.get_instance():  # call vimba API
            with self.camera as cam:
                try:
                    self._user_set = cam.get_feature_by_name(
                        'UserSetSelector').get()

                except error.VimbaFeatureError:
                    print('Failed to get user set id')

    def save_configurations(self, configs_filepath=None, to_eeprom=False):
        """
        Save configurations from camera to configurations file

        Args:
            configs_filepath (str, optional): configurations file path. Defaults to None.
            to_eeprom (bool, optional): Save to EEPROM. Defaults to False.
        """
        if self._user_set is None:
            self._get_active_user_set()

        with vimba.Vimba.get_instance():  # call vimba API
            with self.camera as cam:
                # Save camera settings to file
                cam.save_settings(configs_filepath, camera.PersistType.All)

                if to_eeprom:
                    try:
                        cam.get_feature_by_name(
                            'UserSetSelector').set(self._user_set)

                    except error.VimbaFeatureError as e:
                        print(e)

                    try:
                        cmd = cam.get_feature_by_name('UserSetSave')
                        cmd.run()

                        while not cmd.is_done():
                            pass

                    except error.VimbaFeatureError as e:
                        print(e)

    def load_configurations(self, configs_filepath=None, from_eeprom=False):
        """
        Load configurations from configurations file to camera

        Args:
            configs_filepath (str, optional): configurations file path. Defaults to None.
            from_eeprom (bool, optional): Load from EEPROM. Defaults to False.
        """
        if self._user_set is None:
            self._get_active_user_set()

        with vimba.Vimba.get_instance():  # call vimba API
            with self.camera as cam:
                try:
                    cam.get_feature_by_name(
                        'UserSetSelector').set(self._user_set)

                except error.VimbaFeatureError as e:
                    print(e)

                try:
                    cmd = cam.get_feature_by_name('UserSetLoad')
                    cmd.run()

                    while not cmd.is_done():
                        pass

                except error.VimbaFeatureError as e:
                    print(e)

                print(
                    f'Loaded user set {self._user_set} loaded from flash successfully')

                if from_eeprom:
                    # Load camera settings from file
                    cam.load_settings(configs_filepath, camera.PersistType.All)

    def get_parameter(self, parameter_name):
        """
        Get camera parameter value

        Args:
            parameter_name (str): paramater name
        """
        with vimba.Vimba.get_instance():  # call vimba API
            with self.camera as cam:
                if parameter_name == CameraParameters.GAMMA:
                    return cam.Gamma.get()

                elif parameter_name == CameraParameters.BLACK_LEVEL:
                    return cam.BlackLevel.get()

                elif parameter_name == CameraParameters.EXPOSURE_TIME:
                    return cam.ExposureTime.get()

                elif parameter_name == CameraParameters.GAIN:
                    return cam.Gain.get()

                elif parameter_name == CameraParameters.FPS:
                    return cam.AcquisitionFrameRate.get()

    def set_parameter(self, parameter_name, parameter_value, parameter_state):
        """
        Set camera parameter state and/or value

        Args:
            parameter_name (str): paramater name
            parameter_value (int/float): parameter value
            parameter_state (str): According to device API
        """
        with vimba.Vimba.get_instance():  # call vimba API
            with self.camera as cam:
                if parameter_name == CameraParameters.GAMMA:
                    if parameter_state is not None:
                        print(
                            f'No <{parameter_state}> option for parameter {parameter_name} available!')
                    else:
                        try:
                            cam.Gamma.set(parameter_value)
                        except Exception as e:
                            print(e)

                elif parameter_name == CameraParameters.BLACK_LEVEL:
                    if parameter_state is not None:
                        print(
                            f'No <{parameter_state}> option for parameter {parameter_name} available!')
                    else:
                        try:
                            cam.BlackLevel.set(parameter_value)
                        except Exception as e:
                            print(e)

                elif parameter_name == CameraParameters.EXPOSURE_TIME:
                    if parameter_state is not None and parameter_state in ['Off', 'Once', 'Continuous']:
                        cam.ExposureAuto.set(parameter_state)
                    else:
                        try:
                            cam.ExposureTime.set(parameter_value)
                        except Exception as e:
                            print(e)

                elif parameter_name == CameraParameters.GAIN:
                    if parameter_state is not None and parameter_state in ['Off', 'Once', 'Continuous']:
                        cam.GainAuto.set(parameter_state)
                    else:
                        try:
                            cam.Gain.set(parameter_value)
                        except Exception as e:
                            print(e)

                elif parameter_name == CameraParameters.FPS:
                    if parameter_state is not None and parameter_state == 'Basic':
                        cam.AcquisitionFrameRateMode = parameter_state
                    else:
                        cam.AcquisitionFrameRateEnable.set(
                            True)  # enable write
                        
                        try:
                            cam.AcquisitionFrameRate.set(parameter_value)
                        except Exception as e:
                            print(e)
                            
                        cam.AcquisitionFrameRateEnable.set(False)

    def get_image(self):
        """
        Get frame from camera

        Returns:
            numpy.array: image pixels 2D numpy array
        """
        with vimba.Vimba.get_instance():  # call vimba API
            with self.camera as cam:
                frame = cam.get_frame()
                frame.convert_pixel_format(PixelFormat.Mono8)
                image = frame.as_opencv_image()  # convert to array

        return image

    def save_image(self, path):
        """
        Save image 2D array to jpg file

        Args:
            path (str): path to save the image at
        """
        image = self.get_image()
        cv2.imwrite(path, image)

    def record(self, record_time):
        """
        Record frames within specified duration or forever

        Args:
            record_time (int): Streaming time duration
        """
        if self.frame_handler_selected is None:
            self.frame_handler_selected = self.frame_handler

        with vimba.Vimba.get_instance():  # call vimba API
            with self.camera:
                self.camera.start_streaming(self.frame_handler_selected)

                if record_time == 0:
                    while not self.shutdown_event.wait():
                        pass
                else:
                    time.sleep(record_time)

    def frame_handler(self, cam, frame):
        """
        Frame recording handler

        Args:
            cam (object): camera object
            frame (object): frame object
        """
        key = cv2.waitKey(1)

        if key == ENTER_KEY_CODE:
            self.shutdown_event.set()
            return

        elif frame.get_status() == FrameStatus.Complete:
            print(f'Frame acquired: {frame}', flush=True)

            msg = 'Press <Enter> to stop stream'
            image = frame.as_opencv_image()

            cv2.imshow(msg, image)

            cv2.resizeWindow(
                msg, int(image.shape[1] / 3), int(image.shape[0] / 3))

        cam.queue_frame(frame)
