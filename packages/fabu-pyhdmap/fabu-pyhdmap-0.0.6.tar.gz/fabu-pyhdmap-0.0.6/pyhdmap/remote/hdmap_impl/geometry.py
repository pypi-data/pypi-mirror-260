from pyhdmap.externals.libhdmap import *
from pyhdmap.proto.hdmap_lib.proto import geometry_pb2

class LineStringDataImpl:
  def __init__(self) -> None:
    self._id = 0
    self._points:list[Vec2d] = []
    self._type = geometry_pb2.LineStringData.Type.NONE
    self._color = geometry_pb2.LineStringData.Color.WHITE
    
  def id(self):
    return self._id
  
  def points(self):
    return self._points
  
  def type(self):
    return self._type
  
  def color(self):
    return self._color
  
class LineStringImpl:
  def __init__(self) -> None:
    self._id = 0
    self._is_reverse = False
    
  def id(self):
    return self._id
  
  def id_reverse(self):
    return self._is_reverse
  

class CurveImpl:
  def __init__(self) -> None:
    self._lines:list[LineStringImpl] = []
    
  def lines(self):
    return self._lines 