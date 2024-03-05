from pyhdmap.proto.hdmap_lib.proto import junction_pb2
from pyhdmap.externals.libhdmap import *
from pyhdmap.remote.hdmap_impl.relation_impl import RelationImpl
from pyhdmap.remote.hdmap_impl.geometry import CurveImpl
from pyhdmap.remote.hdmap_impl.attribute_impl import AttributesImpl

class JunctionImpl:
  def __init__(self) -> None:
    self._id = 0
    self._polygon = Polygon2d()
    self._type = junction_pb2.Junction.Type.UNKNOWN
    self._name = ""
    self._is_virtual_junction = False
    self._road_ids = []
    self._road_links = []
    self._lanes:list[RelationImpl] = []
    self._attributes = AttributesImpl()
    
  def id(self):
    return self._id
  
  def polygon(self):
    return self._polygon
  
  def type(self):
    return self._type
  
  def name(self):
    return self._name
  
  def is_virtual_junction(self):
    return self._is_virtual_junction
  
  def roads(self):
    return self._road_ids
  
  def road_links(self):
    return self._road_links
  
  def attributes(self):
    return self._attributes
  
  def lanes(self):
    return self._lanes