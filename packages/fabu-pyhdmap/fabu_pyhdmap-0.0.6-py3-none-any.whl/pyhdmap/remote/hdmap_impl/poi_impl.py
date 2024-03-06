from pyhdmap.externals.libhdmap import *
from pyhdmap.remote.hdmap_impl.relation_impl import RelationImpl
from pyhdmap.proto.hdmap_lib.proto import poi_pb2

class PoiImpl:
  def __init__(self) -> None:
    self._id = 0
    self._type = poi_pb2.Poi.PoiType.POI_QUEUE_REGION
    self._name = ""
    self._coordinate = Vec2d()
    self._lanes:list[RelationImpl] = []
    self._pull_over_regions:list[RelationImpl] = []
    self._parking_spaces:list[RelationImpl] = []
    
  def id(self):
    return self._id
  
  def type(self):
    return self._type
  
  def name(self):
    return self._name
  
  def coordinate(self):
    return self._coordinate
  
  def lanes(self):
    return self._lanes
  
  def pull_over_regions(self):
    return self._pull_over_regions
  
  def parking_spaces(self):
    return self._parking_spaces