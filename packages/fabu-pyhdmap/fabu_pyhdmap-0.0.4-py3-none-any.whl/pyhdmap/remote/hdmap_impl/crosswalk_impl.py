from pyhdmap.externals.libhdmap import *
from pyhdmap.remote.hdmap_impl.relation_impl import RelationImpl
from pyhdmap.remote.hdmap_impl.geometry import CurveImpl
from pyhdmap.remote.hdmap_impl.attribute_impl import AttributesImpl

class CrosswalkImpl:
  def __init__(self) -> None:
    self._id = 0
    self._left_boundary = CurveImpl()
    self._right_boundary = CurveImpl()
    self._polygon = Polygon2d()
    self._attributes = AttributesImpl()
    self._lanes:list[RelationImpl] = []
    
  def id(self):
    return self._id
  
  def left_boundary(self):
    return self._left_boundary
  
  def right_boundary(self):
    return self._right_boundary
  
  def polygon(self):
    return self._polygon
  
  def attributes(self):
    return self._attributes
  
  def lanes(self):
    return self._lanes