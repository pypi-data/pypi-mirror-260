from abc import ABC, abstractmethod


class CameraAbstract(ABC):  
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def get_image(self):
        pass
    
    @abstractmethod
    def save_image(self, path: str):
        pass
    
    @abstractmethod
    def record(self, record_time: int):
        pass