from abc import ABCMeta, abstractmethod


class Logger(object, metaclass=ABCMeta):
    
    @abstractmethod
    def __init__(self):
      return
        
    @abstractmethod
    def log(self, message):
        return

class Console(Logger):
    def __init__(self):
      return

    def log(self, message):
        print(message)
