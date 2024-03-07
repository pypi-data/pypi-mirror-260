import time
import copy
import cv2
import ids_peak.ids_peak as ids_peak
import ids_peak_ipl.ids_peak_ipl as ids_peak_ipl
import ids_peak.ids_peak_ipl_extension as ids_peak_ipl_extension
from ..camera_abstract import CameraAbstract
from ..configs import CameraParameters


class IdsPeakCamera(CameraAbstract):
    """
    IDS Peak camera controller interface
    """
    fps_limit = 30
    image_buffer_size = 5000

    def __init__(self):
        """
        Initialize parameters
        """
        ids_peak.Library.Initialize()
        self.camera = None
        self.frame_handler_selected = None
        self.__acquisition_running = False

    def connect(self):
        """
        Connect to camera
        """
        self._init_camera_parameters()
        self._memory_allocation()
        self.__start_acquisition()

    def _init_camera_parameters(self):
        """
        Camera required settings before image/video grab
        """
        # Create instance of the device manager
        device_manager = ids_peak.DeviceManager.Instance()

        # Update the device manager
        device_manager.Update()

        # Return if no device was found
        if device_manager.Devices().empty():
            raise Exception("Error, No device found!")

        # Open the first openable device in the managers device list
        for device in device_manager.Devices():
            if device.IsOpenable():
                self.__device = device.OpenDevice(ids_peak.DeviceAccessType_Control)
                break

        # Return if no device could be opened
        if self.__device is None:
            raise Exception('Error, Device could not be opened!')

        # Open standard data stream
        datastreams = self.__device.DataStreams()
        if datastreams.empty():
            self.__device = None
            raise Exception('Error, Device has no DataStream!')

        self.__datastream = datastreams[0].OpenDataStream()

        # Get nodemap of the remote device for all accesses to the genicam nodemap tree
        self.__nodemap_remote_device = self.__device.RemoteDevice().NodeMaps()[0]

        # To prepare for untriggered continuous image acquisition,
        # load the default user set if available and
        # wait until execution is finished
        try:
            self.__nodemap_remote_device.FindNode("UserSetSelector").SetCurrentEntry("Default")
            self.__nodemap_remote_device.FindNode("UserSetLoad").Execute()
            self.__nodemap_remote_device.FindNode("UserSetLoad").WaitUntilDone()
        except ids_peak.Exception:
            raise Exception('Userset is not available')

    def save_configurations(self, configs_filepath=None, to_eeprom=False):
        """
        Save configurations from camera to configurations file

        Args:
            configs_filepath (str, optional): configurations file path. Defaults to None.
            to_eeprom (bool, optional): Save to EEPROM. Defaults to False.
        """
        if configs_filepath is not None:
            try:
                # Save to file
                self.__nodemap_remote_device.StoreToFile(configs_filepath)
            except Exception as e:
                print(f'Exception saving to file:{e}')
                
        if to_eeprom:
            try:
                # Set selector to "UserSet0"
                self.__nodemap_remote_device.FindNode("UserSetSelector").SetCurrentEntry("UserSet0")
                # Save user set
                self.__nodemap_remote_device.FindNode("UserSetSave").Execute()
                # Wait until the UserSetSave command has been finished
                self.__nodemap_remote_device.FindNode("UserSetSave").WaitUntilDone()
            except Exception as e:
                print(f'Exception saving to camera:{e}')

    def load_configurations(self, configs_filepath=None, from_eeprom=False):
        """
        Load configurations from configurations file to camera

        Args:
            configs_filepath (str, optional): configurations file path. Defaults to None.
            from_eeprom (bool, optional): Load from EEPROM. Defaults to False.
        """
        if configs_filepath is not None:
            try:
                # Load from file
                self.__nodemap_remote_device.LoadFromFile(configs_filepath)
            except Exception as e:
                print(f'Exception loading from file:{e}')
        
        if from_eeprom:
            # Load the default user set
            try:
                # Set selector to "Default"
                self.__nodemap_remote_device.FindNode("UserSetSelector").SetCurrentEntry("Default")
                # Load user set
                self.__nodemap_remote_device.FindNode("UserSetLoad").Execute()
                # Wait until the UserSetLoad command has been finished
                self.__nodemap_remote_device.FindNode("UserSetLoad").WaitUntilDone()
            except Exception as e:
                print(f'Exception loading from camera:{e}')
    
    def _memory_allocation(self):
        """
        Memory allocation for used data types
        """
        # Get the payload size for correct buffer allocation
        payload_size = self.__nodemap_remote_device.FindNode("PayloadSize").Value()

        # Get minimum number of buffers that must be announced
        buffer_count_max = self.__datastream.NumBuffersAnnouncedMinRequired()

        # Allocate and announce image buffers and queue them
        for _ in range(buffer_count_max):
            buffer = self.__datastream.AllocAndAnnounceBuffer(payload_size)
            self.__datastream.QueueBuffer(buffer)

    def get_parameter(self, parameter_name):
        """
        Get camera parameter value

        Args:
            parameter_name (str): paramater name

        Returns:
            object: parameter value
        """
        if parameter_name == CameraParameters.GAMMA:
            gamma = self.__nodemap_remote_device.FindNode("Gamma").Value()

            return gamma

        elif parameter_name == CameraParameters.BLACK_LEVEL:
            black_level = self.__nodemap_remote_device.FindNode("BlackLevel").Value()

            return black_level

        elif parameter_name == CameraParameters.EXPOSURE_TIME:
            exposure_time = self.__nodemap_remote_device.FindNode("ExposureTime").Value()

            return exposure_time

        elif parameter_name == CameraParameters.GAIN:
            gain = self.__nodemap_remote_device.FindNode("Gain").Value()

            return gain

        elif parameter_name == CameraParameters.FPS:
            fps = self.__nodemap_remote_device.FindNode("AcquisitionFrameRate").Value()

            return fps

        elif parameter_name == CameraParameters.DLL_VERSION:
            # not required

            return None

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

        try:
            if parameter_name == CameraParameters.GAMMA:
                if parameter_state is not None:
                    print("Not Implemented")
                else:
                    self.__nodemap_remote_device.FindNode("Gamma").SetValue(parameter_value)
                    
            elif parameter_name == CameraParameters.BLACK_LEVEL:
                if parameter_state is not None:
                    self.__nodemap_remote_device.FindNode("BlackLevelAuto").SetCurrentEntry("Off" if state else "Continuous")
                else:
                    self.__nodemap_remote_device.FindNode("BlackLevel").SetValue(parameter_value)

            elif parameter_name == CameraParameters.EXPOSURE_TIME:
                if parameter_state is not None:
                    self.__nodemap_remote_device.FindNode("ExposureAuto").SetCurrentEntry("Off" if state else "Continuous")
                else:
                    if self.__nodemap_remote_device.FindNode("ExposureTime").HasConstantIncrement():
                        inc_exposure_time = self.__nodemap_remote_device.FindNode("ExposureTime").Increment()
                    else:
                        # If there is no increment, it might be useful to choose a suitable 
                        # increment for a GUI control element (e.g. a slider)
                        inc_exposure_time = parameter_value
                    
                    self.__nodemap_remote_device.FindNode("ExposureTime").SetValue(inc_exposure_time)

            elif parameter_name == CameraParameters.GAIN:
                if parameter_state is not None:
                    self.__nodemap_remote_device.FindNode("GainAuto").SetCurrentEntry("Off" if state else "Continuous")
                else:
                    if self.__nodemap_remote_device.FindNode("Gain").HasConstantIncrement():
                        inc_gain = self.__nodemap_remote_device.FindNode("Gain").Increment()
                    else:
                        inc_gain = parameter_value
                    
                    self.__nodemap_remote_device.FindNode("Gain").SetValue(inc_gain)

            elif parameter_name == CameraParameters.FPS:
                if parameter_state is not None:
                    self.__nodemap_remote_device.FindNode("AcquisitionMode").SetCurrentEntry("Off" if state else "Continuous")
                else:
                    if self.__nodemap_remote_device.FindNode("AcquisitionFrameRate").HasConstantIncrement():
                        inc_frame_rate = self.__nodemap_remote_device.FindNode("AcquisitionFrameRate").Increment()
                    else:
                        # If there is no increment, it might be useful to choose a suitable
                        # increment for a GUI control element (e.g. a slider)
                        inc_frame_rate = parameter_value
                    
                    self.__nodemap_remote_device.FindNode("AcquisitionFrameRate").SetValue(inc_frame_rate)

        except:
            print(f"Set {parameter_name} to {parameter_value} failed!")

    def get_image(self):
        """
        Get frame from camera

        Returns:
            array: image pixels 2D numpy array
        """
        buffer = self.__datastream.WaitForFinishedBuffer(self.image_buffer_size)

        # Create IDS peak IPL image for debayering and convert it to RGBa8 format
        ipl_image = ids_peak_ipl_extension.BufferToImage(buffer)
        converted_ipl_image = ipl_image.ConvertTo(ids_peak_ipl.PixelFormatName_Mono8)

        # Queue buffer so that it can be used again
        self.__datastream.QueueBuffer(buffer)

        # Get raw image data from converted image and construct a QImage from it
        image_np_array = converted_ipl_image.get_numpy_2D()
        
        return copy.deepcopy(image_np_array)

    def save_image(self, path):
        """
        Save image 2D array to jpg file

        Args:
            path (str): path to save the image at
        """
        image_np_array = self.get_image()
        cv2.imwrite(path, image_np_array) 

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
    
    def __start_acquisition(self):
        """
        Start Acquisition on camera and start the acquisition timer to receive and display images

        Returns: 
            bool: True/False if acquisition start was successful
        """
        # Check that a device is opened and that the acquisition is NOT running. If not, return.
        if self.__device is None:
            return False
        if self.__acquisition_running is True:
            return True

        # Get the maximum framerate possible, limit it to the configured fps limit. If the limit can't be reached, set
        # acquisition interval to the maximum possible framerate
        try:
            max_fps = self.__nodemap_remote_device.FindNode("AcquisitionFrameRate").Maximum()
            target_fps = min(max_fps, self.fps_limit)
            self.__nodemap_remote_device.FindNode("AcquisitionFrameRate").SetValue(target_fps)
        except ids_peak.Exception:
            print("Warning", "Unable to limit fps, since the AcquisitionFrameRate Node is"
                  " not supported by the connected camera. Program will continue without limit.")

        try:
            # Lock critical features to prevent them from changing during acquisition
            self.__nodemap_remote_device.FindNode("TLParamsLocked").SetValue(1)

            # Start acquisition on camera
            self.__datastream.StartAcquisition()
            self.__nodemap_remote_device.FindNode("AcquisitionStart").Execute()
            self.__nodemap_remote_device.FindNode("AcquisitionStart").WaitUntilDone()
        except Exception as e:
            print("Exception: " + str(e))
            return False

        self.__acquisition_running = True

        return True
    
    def __stop_acquisition(self):
        """
        Stop acquisition timer and stop acquisition on camera
        """
        # Check that a device is opened and that the acquisition is running.
        # If not, return.
        if self.__device is None or self.__acquisition_running is False:
            return

        # Otherwise try to stop acquisition
        try:
            remote_nodemap = self.__device.RemoteDevice().NodeMaps()[0]
            remote_nodemap.FindNode("AcquisitionStop").Execute()

            # Stop and flush datastream
            self.__datastream.KillWait()
            self.__datastream.StopAcquisition(ids_peak.AcquisitionStopMode_Default)
            self.__datastream.Flush(ids_peak.DataStreamFlushMode_DiscardAll)

            self.__acquisition_running = False

            # Unlock parameters after acquisition stop
            if self.__nodemap_remote_device is not None:
                try:
                    self.__nodemap_remote_device.FindNode("TLParamsLocked").SetValue(0)
                except Exception as e:
                    print(f'Exception, {e}')

        except Exception as e:
            print(f'Exception, {str(e)}')

    def disconnect(self):
        """
        Stop acquisition if still running and close datastream and nodemap of the device
        """
        self.__stop_acquisition()

        # If a datastream has been opened, try to revoke its image buffers
        if self.__datastream is not None:
            try:
                for buffer in self.__datastream.AnnouncedBuffers():
                    self.__datastream.RevokeBuffer(buffer)
            except Exception as e:
                print(f'Exception: {e}')
                
        ids_peak.Library.Close()
