from pyhdmap.proto.hdmap_lib.proto import road_pb2
from pyhdmap.externals.libhdmap import *
from pyhdmap.remote.hdmap_impl.attribute_impl import AttributesImpl

class LaneSectionImpl:
  def __init__(self) -> None:
    self._lane_ids = []
    self._index = -1
    self._road_id = 0
    
  def lanes(self):
    return self._lane_ids
  
  def index(self):
    return self._index
  
  def road_id(self):
    return self._road_id

class RoadImpl:
  def __init__(self) -> None:
    self._id = 0
    self._lane_sections = []
    self._junction_id = 0
    self._next_road_ids = []
    self._prev_road_ids = []
    self._prev_junction_id = 0
    self._next_junction_id = 0
    self._polygon = Polygon2d()
    self._attributes = AttributesImpl()
    self._name = ""
    self._type = road_pb2.Road.RoadType.UNKNOWN_ROAD
    self._road_struct = None
    self._schedule_poi_id = 0
    
  def id(self):
    return self._id
    
  def lane_sections(self):
    return self._lane_sections
  
  def junction(self):
    return self._junction_id
  
  def IsInJunction(self):
    return self._junction_id != 0
  
  def next_roads(self):
    return self._next_road_ids
  
  def prev_roads(self):
    return self._prev_road_ids
  
  def next_junction(self):
    return self._next_junction_id
  
  def prev_junction(self):
    return self._prev_junction_id
  
  def polygon(self):
    return self._polygon
  
  def attributes(self):
    return self._attributes
  
  def name(self):
    return self._name
  
  def type(self):
    return self._type
  
  def road_struct(self):
    return self._road_struct
  
  def poi(self):
    return self._schedule_poi_id