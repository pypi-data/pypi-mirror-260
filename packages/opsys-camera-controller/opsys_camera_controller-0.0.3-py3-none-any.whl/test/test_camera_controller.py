import unittest
from unittest.mock import patch, MagicMock
from camera_controller_wrapper import CameraControllerWrapper


class Test(unittest.TestCase):
    @ classmethod
    def setUp(self):
        pass

    @ classmethod
    def setUpClass(cls):
        pass

    @ classmethod
    def tearDownClass(cls):
        pass

    @ patch.object(CameraControllerWrapper, 'connect')
    def test_connect(self, camera_mock: MagicMock):
        camera_type = 'IDS'
        camera = CameraControllerWrapper(camera_type)
        camera.connect()
        camera_mock.assert_called_once_with()
        
    @ patch.object(CameraControllerWrapper, 'disconnect')
    def test_disconnect(self, camera_mock: MagicMock):
        camera_type = 'IDS'
        camera = CameraControllerWrapper(camera_type)
        camera.disconnect()
        camera_mock.assert_called_once_with()

    @ patch.object(CameraControllerWrapper, 'get_image')
    def test_get_image(self, camera_mock: MagicMock):
        camera_type = 'IDS'
        camera = CameraControllerWrapper(camera_type)
        camera.get_image()
        camera_mock.assert_called_once_with()

    @ patch.object(CameraControllerWrapper, 'save_configurations')
    def test_save_configurations(self, camera_mock: MagicMock):
        camera_type = 'IDS'
        camera = CameraControllerWrapper(camera_type)
        filepath = None
        to_eeprom = False
        camera.save_configurations(
            configs_filepath=filepath, to_eeprom=to_eeprom)
        camera_mock.assert_called_once_with(
            configs_filepath=None, to_eeprom=False)

    @ patch.object(CameraControllerWrapper, 'load_configurations')
    def test_load_configurations(self, camera_mock: MagicMock):
        camera_type = 'IDS'
        camera = CameraControllerWrapper(camera_type)
        filepath = None
        from_eeprom = False
        camera.load_configurations(
            configs_filepath=filepath, from_eeprom=from_eeprom)
        camera_mock.assert_called_once_with(
            configs_filepath=None, from_eeprom=False)

    @ patch.object(CameraControllerWrapper, 'save_image')
    def test_save_image(self, camera_mock: MagicMock):
        camera_type = 'IDS'
        camera = CameraControllerWrapper(camera_type)
        camera.save_image()
        camera_mock.assert_called_once_with()

    @ patch.object(CameraControllerWrapper, 'get_parameter')
    def test_get_parameter(self, camera_mock: MagicMock):
        camera_type = 'IDS'
        camera = CameraControllerWrapper(camera_type)
        camera.get_parameter('gamma')
        camera_mock.assert_called_once_with('gamma')

    @ patch.object(CameraControllerWrapper, 'set_parameter')
    def test_set_parameter(self, camera_mock: MagicMock):
        camera_type = 'IDS'
        camera = CameraControllerWrapper(camera_type)
        camera.set_parameter('gamma', 94)
        camera_mock.assert_called_once_with('gamma', 94)

    @ patch.object(CameraControllerWrapper, 'record')
    def test_record(self, camera_mock: MagicMock):
        camera_type = 'IDS'
        camera = CameraControllerWrapper(camera_type)
        record_time = 20
        camera.record(record_time=record_time)
        camera_mock.assert_called_once_with(record_time=20)


if __name__ == '__main__':
    unittest.main()
