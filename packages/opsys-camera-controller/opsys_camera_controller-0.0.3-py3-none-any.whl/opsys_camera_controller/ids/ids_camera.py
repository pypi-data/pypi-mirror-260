import numpy as np
import time
import cv2
from pyueye import ueye
from ..camera_abstract import CameraAbstract
from ..configs import CameraParameters


class IdsCamera(CameraAbstract):
    """
    IDS camera controller interface
    """

    def __init__(self):
        """
        Initialize parameters
        """
        self.camera = None
        self.frame_handler_selected = None

    def connect(self):
        """
        Connect to camera
        """
        self.camera = ueye.HIDS(
            0)  # 0: first available camera;  1-254: The camera with the specified camera ID
        self._sensor_info = ueye.SENSORINFO()
        self._cam_info = ueye.CAMINFO()
        self._pc_image_memory = ueye.c_mem_p()
        self._mem_id = ueye.int()
        self._rect_aoi = ueye.IS_RECT()
        self._pitch = ueye.INT()
        # 24: bits per pixel for color mode; take 8 bits per pixel for monochrome
        self._n_bits_per_pixel = ueye.INT(24)
        # 3: channels for color mode(RGB); take 1 channel for monochrome
        self._channels = 3
        self._m_n_color_mode = ueye.INT()		# Y8/RGB16/RGB24/REG32
        self._bytes_per_pixel = int(self._n_bits_per_pixel / 8)
        # other camera configurations
        self._init_camera_parameters()
        self._memory_allocation()

    def _init_camera_parameters(self):
        """
        Camera required settings before image/video grab
        """
        # Starts the driver and establishes the connection to the camera
        n_ret = ueye.is_InitCamera(self.camera, None)
        if n_ret != ueye.IS_SUCCESS:
            print("is_InitCamera ERROR")

        # Reads out the data hard-coded in the non-volatile camera memory and
        # writes it to the data structure that cInfo points to
        n_ret = ueye.is_GetCameraInfo(self.camera, self._cam_info)
        if n_ret != ueye.IS_SUCCESS:
            print("is_GetCameraInfo ERROR")

        # You can query additional information about the sensor type used in the camera
        n_ret = ueye.is_GetSensorInfo(self.camera, self._sensor_info)
        if n_ret != ueye.IS_SUCCESS:
            print("is_GetSensorInfo ERROR")

        n_ret = ueye.is_ResetToDefault(self.camera)
        if n_ret != ueye.IS_SUCCESS:
            print("is_ResetToDefault ERROR")

        # Set display mode to DIB
        n_ret = ueye.is_SetDisplayMode(self.camera, ueye.IS_SET_DM_DIB)

        # Set the right color mode
        if int.from_bytes(self._sensor_info.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_BAYER:
            # setup the color depth to the current windows setting
            ueye.is_GetColorDepth(
                self.camera, self._n_bits_per_pixel, self._m_n_color_mode)
            self._bytes_per_pixel = int(self._n_bits_per_pixel / 8)
            print("IS_COLORMODE_BAYER: ", self._m_n_color_mode)

        elif int.from_bytes(self._sensor_info.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_CBYCRY:
            # for color camera models use RGB32 mode
            self._m_n_color_mode = ueye.IS_CM_BGRA8_PACKED
            self._n_bits_per_pixel = ueye.INT(32)
            self._bytes_per_pixel = int(self._n_bits_per_pixel / 8)
            print("IS_COLORMODE_CBYCRY: ", self._m_n_color_mode)

        elif int.from_bytes(self._sensor_info.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_MONOCHROME:
            # for color camera models use RGB32 mode
            self._m_n_color_mode = ueye.IS_CM_MONO8
            self._n_bits_per_pixel = ueye.INT(8)
            self._bytes_per_pixel = int(self._n_bits_per_pixel / 8)
            print("IS_COLORMODE_MONOCHROME: ", self._m_n_color_mode)

        else:
            # for monochrome camera models use Y8 mode
            self._m_n_color_mode = ueye.IS_CM_MONO8
            self._n_bits_per_pixel = ueye.INT(8)
            self._bytes_per_pixel = int(self._n_bits_per_pixel / 8)

        # Can be used to set the size and position of an "area of interest"(AOI) within an image
        n_ret = ueye.is_AOI(self.camera, ueye.IS_AOI_IMAGE_GET_AOI,
                           self._rect_aoi, ueye.sizeof(self._rect_aoi))
        
        if n_ret != ueye.IS_SUCCESS:
            print("is_AOI ERROR")

        self._width = self._rect_aoi.s32Width
        self._height = self._rect_aoi.s32Height

        # Prints out some information about the sensor
        print("Maximum image width:\t", self._width)
        print("Maximum image height:\t", self._height)

    def save_configurations(self, configs_filepath=None, to_eeprom=False):
        """
        Save configurations from camera to configurations file

        Args:
            configs_filepath (str, optional): configurations file path. Defaults to None.
            to_eeprom (bool, optional): Save to EEPROM. Defaults to False.
        """
        config_file = ueye.wchar_p()  # allocate variable memory
        config_file.value = configs_filepath

        n_ret = ueye.is_ParameterSet(
            self.camera, ueye.IS_PARAMETERSET_CMD_SAVE_FILE, config_file, 0)

        if n_ret != ueye.IS_SUCCESS:
            print("is_ParameterSet 'SAVE to file' ERROR")

        if to_eeprom:
            n_ret = ueye.is_ParameterSet(
                self.camera, ueye.IS_PARAMETERSET_CMD_SAVE_EEPROM, config_file, 0)

            if n_ret != ueye.IS_SUCCESS:
                print("is_ParameterSet 'SAVE to EEPROM' ERROR")

    def load_configurations(self, configs_filepath=None, from_eeprom=False):
        """
        Load configurations from configurations file to camera

        Args:
            configs_filepath (str, optional): configurations file path. Defaults to None.
            from_eeprom (bool, optional): Load from EEPROM. Defaults to False.
        """
        config_file = ueye.wchar_p()  # allocate variable memory
        config_file.value = configs_filepath

        n_ret = ueye.is_ParameterSet(
            self.camera, ueye.IS_PARAMETERSET_CMD_LOAD_FILE, config_file, 0)

        if n_ret != ueye.IS_SUCCESS:
            print("is_ParameterSet 'LOAD from file' ERROR")

        if from_eeprom:
            n_ret = ueye.is_ParameterSet(
                self.camera, ueye.IS_PARAMETERSET_CMD_LOAD_EEPROM, config_file, 0)

            if n_ret != ueye.IS_SUCCESS:
                print("is_ParameterSet 'LOAD from EEPROM' ERROR")

    def _memory_allocation(self):
        """
        Memory allocation for used data types
        """
        # Allocates an image memory for an image having its dimensions defined by 
        # width and height and its color depth defined by nBitsPerPixel
        n_ret = ueye.is_AllocImageMem(self.camera, self._width, self._height,
                                     self._n_bits_per_pixel, self._pc_image_memory, self._mem_id)
        if n_ret != ueye.IS_SUCCESS:
            print("is_AllocImageMem ERROR")
            
        else:
            # Makes the specified image memory the active memory
            n_ret = ueye.is_SetImageMem(
                self.camera, self._pc_image_memory, self._mem_id)
            
            if n_ret != ueye.IS_SUCCESS:
                print("is_SetImageMem ERROR")
                
            else:
                # Set the desired color mode
                n_ret = ueye.is_SetColorMode(self.camera, self._m_n_color_mode)

        # Activates the camera's live video mode (free run mode)
        n_ret = ueye.is_CaptureVideo(self.camera, ueye.IS_DONT_WAIT)
        if n_ret != ueye.IS_SUCCESS:
            print("is_CaptureVideo ERROR")

        # Enables the queue mode for existing image memory sequences
        n_ret = ueye.is_InquireImageMem(self.camera, self._pc_image_memory, self._mem_id,
                                       self._width, self._height, self._n_bits_per_pixel, self._pitch)

        if n_ret != ueye.IS_SUCCESS:
            print("is_InquireImageMem ERROR")
        else:
            pass

    def get_parameter(self, parameter_name):
        """
        Get camera parameter value

        Args:
            parameter_name (str): paramater name

        Returns:
            object: parameter value
        """
        if parameter_name == CameraParameters.GAMMA:
            gamma = ueye.c_int()  # allocate variable memory

            n_ret = ueye.is_Gamma(
                self.camera, ueye.IS_GAMMA_CMD_GET, gamma, ueye.sizeof(gamma))

            if n_ret != ueye.IS_SUCCESS:
                print(f"Get {parameter_name} failed!")

            return gamma.value

        elif parameter_name == CameraParameters.BLACK_LEVEL:
            offset = ueye.c_int()

            n_ret = ueye.is_Blacklevel(
                self.camera, ueye.IS_BLACKLEVEL_CMD_GET_OFFSET, offset, ueye.sizeof(offset))

            if n_ret != ueye.IS_SUCCESS:
                print(f"Get {parameter_name} failed!")

            return offset.value

        elif parameter_name == CameraParameters.EXPOSURE_TIME:
            exposure_time = ueye.c_double()

            n_ret = ueye.is_Exposure(
                self.camera, ueye.IS_EXPOSURE_CMD_GET_EXPOSURE, exposure_time, ueye.sizeof(exposure_time))

            if n_ret != ueye.IS_SUCCESS:
                print(f"Get {parameter_name} failed!")

            return exposure_time.value

        elif parameter_name == CameraParameters.GAIN:
            red_gain, green_gain, blue_gain = ueye.c_int(), ueye.c_int(), ueye.c_int()

            n_ret = ueye.is_SetHardwareGain(
                self.camera, ueye.IS_GET_MASTER_GAIN, red_gain, green_gain, blue_gain)

            return n_ret

        elif parameter_name == CameraParameters.FPS:
            fps = ueye.c_double()

            n_ret = ueye.is_GetFramesPerSecond(self.camera, fps)

            if n_ret != ueye.IS_SUCCESS:
                print(f"Get {parameter_name} failed!")

            return fps.value

        elif parameter_name == CameraParameters.DLL_VERSION:
            dll_version = ueye.is_GetDLLVersion()

            build = dll_version & 0xFFFF
            dll_version = dll_version >> 16
            minor = dll_version & 0xFF
            dll_version = dll_version >> 8
            major = dll_version & 0xFF

            return f'{major}.{minor}.{build}'

    def set_parameter(self, parameter_name, parameter_value, parameter_state):
        """
        Set camera parameter state and/or value

        Args:
            parameter_name (str): paramater name
            parameter_value (int/float): parameter value
            parameter_state (str): According to device API
        """
        if parameter_state is not None:
            state = 1 if parameter_state in ['on', 'auto'] else 0

        if parameter_name == CameraParameters.GAMMA:
            if parameter_state is not None:
                mode = ueye.IS_SET_HW_GAMMA_ON if state == 1 else ueye.IS_SET_HW_GAMMA_OFF
                n_ret = ueye.is_SetHardwareGamma(self.camera, mode)
            else:
                gamma = ueye.c_int()
                gamma.value = parameter_value

                n_ret = ueye.is_Gamma(
                    self.camera, ueye.IS_GAMMA_CMD_SET, gamma, ueye.sizeof(gamma))

        elif parameter_name == CameraParameters.BLACK_LEVEL:
            if parameter_state is not None:
                mode = ueye.c_int()
                mode.value = ueye.IS_AUTO_BLACKLEVEL_ON if state == 1 else ueye.IS_AUTO_BLACKLEVEL_OFF
                n_ret = ueye.is_Blacklevel(
                    self.camera, ueye.IS_BLACKLEVEL_CMD_SET_MODE, mode, ueye.sizeof(mode))
            else:
                offset = ueye.c_int()
                offset.value = parameter_value

                n_ret = ueye.is_Blacklevel(
                    self.camera, ueye.IS_BLACKLEVEL_CMD_SET_OFFSET, offset, ueye.sizeof(offset))

        elif parameter_name == CameraParameters.EXPOSURE_TIME:
            if parameter_state is not None:
                state_value = ueye.c_double()
                state_value.value = state
                n_ret = ueye.is_SetAutoParameter(
                    self.camera, ueye.IS_SET_ENABLE_AUTO_SHUTTER, state_value, ueye.c_double(0))
            else:
                exposure_time = ueye.c_double()
                exposure_time.value = parameter_value

                n_ret = ueye.is_Exposure(
                    self.camera, ueye.IS_EXPOSURE_CMD_SET_EXPOSURE, exposure_time, ueye.sizeof(exposure_time))

        elif parameter_name == CameraParameters.GAIN:
            if parameter_state is not None:
                state_value = ueye.c_double()
                state_value.value = state
                n_ret = ueye.is_SetAutoParameter(
                    self.camera, ueye.IS_SET_ENABLE_AUTO_GAIN, state_value, ueye.c_double(0))
            else:
                gain = ueye.c_int()
                # convert ranges: [0:100] to [100:400]
                gain.value = int(
                    ((int(parameter_value) - 0) / (100 - 0)) * (400 - 100) + 100)

                max_gain_value = ueye.is_SetHWGainFactor(
                    self.camera, ueye.IS_INQUIRE_MASTER_GAIN_FACTOR, ueye.c_int(100))

                if gain.value > max_gain_value or gain.value < 100:
                    print(
                        f'Gain value is out of range. Valid range: 100 to {max_gain_value}')
                    n_ret = -1  # fail status
                else:
                    n_ret = ueye.is_SetHWGainFactor(
                        self.camera, ueye.IS_SET_MASTER_GAIN_FACTOR, gain)

                    if n_ret - 2 < gain.value < n_ret + 2:
                        n_ret = 0

        elif parameter_name == CameraParameters.FPS:
            if parameter_state is not None:
                state_value = ueye.c_double()
                state_value.value = state
                # enable auto shutter
                ueye.is_SetAutoParameter(
                    self.camera, ueye.IS_SET_ENABLE_AUTO_SHUTTER, state_value, ueye.c_double(0))

                n_ret = ueye.is_SetAutoParameter(
                    self.camera, ueye.IS_SET_ENABLE_AUTO_FRAMERATE, state_value, ueye.c_double(0))
            else:
                fps = ueye.c_double()
                fps.value = parameter_value

                new_fps = ueye.c_double()

                n_ret = ueye.is_SetFrameRate(self.camera, fps, new_fps)

        # check status
        if n_ret != ueye.IS_SUCCESS:
            if parameter_state is not None:
                print(f"Set {parameter_name} to <{parameter_state}> failed!")
            else:
                print(f"Set {parameter_name} to {parameter_value} failed!")

    def get_image(self):
        """
        Get frame from camera

        Returns:
            array: image pixels 2D numpy array
        """
        # In order to display the image in an OpenCV window we need to
        # extract the data of our image memory
        array = ueye.get_data(self._pc_image_memory, self._width,
                              self._height, self._n_bits_per_pixel, self._pitch, copy=False)

        # reshape it in an numpy array
        image = np.reshape(
            array, (self._height.value, self._width.value, self._bytes_per_pixel))

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
        Record frames

        Args:
            record_time (int): streaming time duration
        """
        start = time.time()

        while True:
            image = self.get_image()
            cv2.imshow("IDS Frame", image)

            end = time.time()

            if cv2.waitKey(1) & int((end - start) > record_time):
                break

    def free_memory(self):
        """
        Free previously allocated for data types memory
        """
        # Releases an image memory that was allocated using is_AllocImageMem()
        # and removes it from the driver management
        ueye.is_FreeImageMem(self.camera, self._pc_image_memory, self._mem_id)
        # Disables the hCam camera handle and releases the data structures 
        # and memory areas taken up by the uEye camera
        ueye.is_ExitCamera(self.camera)
