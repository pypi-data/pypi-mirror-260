from pyhdmap.externals.libhdmap import *
from pyhdmap.remote.hdmap_impl.relation_impl import RelationImpl
from pyhdmap.remote.hdmap_impl.geometry import CurveImpl

class LanePoint:
  def __init__(self, lane_id, s) -> None:
    self._lane_id = lane_id
    self._s = s
    
  def lane_id(self):
    return self._lane_id
  
  def s(self):
    return self._s

class ParkingSpaceImpl:
  def __init__(self) -> None:
    self._id = 0
    self._left_boundary = CurveImpl()
    self._right_boundary = CurveImpl()
    self._central_line:list[Vec2d] = []
    self._reference_line = None
    self._polygon = Polygon2d()
    self._in_lanes:list[LanePoint] = []
    self._out_lanes:list[LanePoint] = []
    self._pois:list[RelationImpl] = []
    
  def id(self):
    return self._id
  
  def left_boundary(self):
    return self._left_boundary
  
  def right_boundary(self):
    return self._right_boundary
  
  def reference_line(self):
    if self._reference_line == None:
      Utils.BuildReferenceLineFromPoints(self._central_line, self._reference_line)
    return self._reference_line
  
  def polygon(self):
    return self._polygon
  
  def in_lanes(self):
    return self._in_lanes
  
  def out_lanes(self):
    return self._out_lanes
  
  def pois(self):
    return self._pois
