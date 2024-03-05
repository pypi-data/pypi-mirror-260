from pyhdmap.externals.libhdmap import *
from pyhdmap.remote.hdmap_impl.relation_impl import RelationImpl
from pyhdmap.proto.hdmap_lib.proto import signal_pb2

class SignalImpl:
  def __init__(self) -> None:
    self._id = 0
    self._polygon = Polygon2d()
    self._stop_lines:list[RelationImpl] = []
    self._signal_type = signal_pb2.Signal.SignalType.UNKNOWN_SIGNAL
    self._combination_type = signal_pb2.Signal.CombinationType.UNKNOWN_COMNINATION
    self._signal_center = Vec2d()
    
  def id(self):
    return self._id
  
  def polygon(self):
    return self._polygon
  
  def stop_lines(self):
    return self._stop_lines
  
  def signal_type(self):
    return self._signal_type
  
  def combination_type(self):
    return self._combination_type
  
  def signal_center(self):
    return self._signal_center