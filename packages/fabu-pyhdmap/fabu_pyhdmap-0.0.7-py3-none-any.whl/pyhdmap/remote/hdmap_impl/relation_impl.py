from pyhdmap.proto.hdmap_lib.proto import relation_pb2
from pyhdmap.externals.libhdmap import *

class RelationImpl:
  def __init__(self) -> None:
    self._this_id = 0
    self._this_start_s = 0
    self._this_end_s = 0
    self._other_id = 0
    self._other_start_s = 0
    self._other_end_s = 0
    self._type = None
    
  def this_id(self):
    return self._this_id
  
  def this_lane_overlap_range(self):
    return Range(self._this_start_s, self._this_end_s)
  
  def other_id(self):
    return self._other_id
  
  def over_lane_overlap_range(self):
    return Range(self._other_start_s, self._other_end_s)