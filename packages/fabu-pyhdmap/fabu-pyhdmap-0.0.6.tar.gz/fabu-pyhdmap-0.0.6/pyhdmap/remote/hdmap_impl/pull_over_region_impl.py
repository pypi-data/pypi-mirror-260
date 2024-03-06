from pyhdmap.externals.libhdmap import *
from pyhdmap.remote.hdmap_impl.relation_impl import RelationImpl

class PullOverRegionImpl:
  def __init__(self) -> None:
    self._id = 0
    self._pois:list[RelationImpl] = []
    self._lane_id = 0
    self._start_s = 0
    self._end_s = 0
    self._d = 0
    
  def id(self):
    return self._id
  
  def pois(self):
    return self._pois
  
  def lane(self):
    return self._lane_id
  
  def start_s(self):
    return self._start_s
  
  def end_s(self):
    return self._end_s
  
  def d(self):
    return self._d