from enum import Enum
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from pyhdmap.remote.remote_manager import RemoteManager
from pyhdmap.local.local_manager import LocalManager
from pyhdmap.utils.singleton import Singleton

class Mode(Enum):
  LOCAL = 1
  REMOTE = 2
  
class Point:
  def __init__(self, x:float, y:float) -> None:
    self._x = x
    self._y = y
    
  def x(self):
    return self._x
  
  def y(self):
    return self._y

@Singleton
class PyHDMap(object):
  def __init__(self) -> None:
    self._mode = None
    self._remote_manager = RemoteManager()
    self._local_manager = LocalManager()
    print("pyhdmap init finish")
    
  def set_mode(self, mode:Mode):
    self._mode = mode
    
  def get_remote_manager(self):
    return self._remote_manager
  
  def get_local_manager(self):
    return self._local_manager

  