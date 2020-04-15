from src.common.singleton import Singleton


class LoggingService(metaclass=Singleton):
    def __init__(self):
        pass

    def info(self, message: str):
        pass

    def warn(self, message: str):
        pass

    def error(self, message: str):
        pass
