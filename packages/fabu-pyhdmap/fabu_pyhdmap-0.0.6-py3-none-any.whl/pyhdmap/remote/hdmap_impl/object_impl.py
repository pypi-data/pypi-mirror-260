from pyhdmap.proto.hdmap_lib.proto import object_pb2
from pyhdmap.externals.libhdmap import *
from pyhdmap.remote.hdmap_impl.relation_impl import RelationImpl
from pyhdmap.remote.hdmap_impl.attribute_impl import AttributesImpl

class ObjectImpl:
  def __init__(self) -> None:
    self._id = 0
    self._type = object_pb2.Object.Type.NONE
    self._polygon = Polygon2d()
    self._height = 0
    self._lanes:list[RelationImpl] = [] 
    self._attributes = AttributesImpl()
  
  def id(self):
    return self._id
  
  def type(self):
    return self._type
  
  def polygon(self):
    return self._polygon
  
  def height(self):
    return self._height
  
  def lanes(self):
    return self._lanes
  
  def attibutes(self):
    return self._attributes