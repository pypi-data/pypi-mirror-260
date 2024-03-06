from pyhdmap.externals.libhdmap import *
from pyhdmap.remote.hdmap_impl.relation_impl import RelationImpl
from pyhdmap.remote.hdmap_impl.geometry import CurveImpl

class StopLineImpl:
  def __init__(self) -> None:
    self._id = 0
    self._curve = CurveImpl()
    self._lanes:list[RelationImpl] = []
    self._signals:list[RelationImpl] = []
    
  def id(self):
    return self._id

  def curve(self):
    return self._curve
  
  def lanes(self):
    return self._lanes
  
  def signals(self):
    return self._signals