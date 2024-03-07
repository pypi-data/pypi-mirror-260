from opsys_camera_controller.camera_controller import CameraController


class CameraControllerWrapper(CameraController):
    """
    Interface wrapper
    """
    def __init__(self, camera_type):    
        super(CameraController, self)
            
        self.camera_type = camera_type
        self.camera = CameraController
