from pyhdmap.remote.impl_cache import ImplCache
from pyhdmap.remote.hdmap_impl.lane_impl import LaneImpl
from pyhdmap.remote.hdmap_impl.road_impl import RoadImpl, LaneSectionImpl
from pyhdmap.remote.hdmap_impl.junction_impl import JunctionImpl
from pyhdmap.remote.hdmap_impl.object_impl import ObjectImpl
from pyhdmap.remote.hdmap_impl.crosswalk_impl import CrosswalkImpl
from pyhdmap.remote.hdmap_impl.parking_space_impl import ParkingSpaceImpl, LanePoint
from pyhdmap.remote.hdmap_impl.poi_impl import PoiImpl
from pyhdmap.remote.hdmap_impl.pull_over_region_impl import PullOverRegionImpl
from pyhdmap.remote.hdmap_impl.signal_impl import SignalImpl
from pyhdmap.remote.hdmap_impl.stop_line_impl import StopLineImpl
from pyhdmap.remote.hdmap_impl.lane_link_impl import LaneLinkImpl
from pyhdmap.remote.hdmap_impl.relation_impl import RelationImpl
from pyhdmap.remote.hdmap_impl.attribute_impl import AttributesImpl
from externals.libhdmap import *

impl_cache = ImplCache()

def ToInfo(impls, type):
  target_impls = []
  info_list = []
  if isinstance(impls, list) == False:
    target_impls.append(impls)
  else:
    target_impls = impls
    
  if type == "lane":
    info_list.extend([LaneInfo(impl) for impl in target_impls])
  elif type == "lane_section":
    info_list.extend([LaneSectionInfo(impl) for impl in target_impls])
  
  return info_list
class LaneInfo:
  def __init__(self, lane_impl:LaneImpl) -> None:
    self._impl = lane_impl
    
  def id(self):
    return self._impl.id()
  
  def type(self):
    return self._impl.type()
  
  def turn_type(self):
    return self._impl.turn_type()
  
  def max_speed(self):
    return self._impl.max_speed()
  
  def min_speed(self):
    return self._impl.min_speed()
  
  def junction_id(self):
    return self._impl.junction_id()
  
  def IsInJunction(self):
    return self._impl.IsInJunction()
  
  def left_boundary(self):
    return self._impl.left_boundary()
  
  def right_boundary(self):
    return self._impl.right_boundary()
  
  def central_line(self):
    return self._impl.central_line()

  def reference_line(self):
    return self._impl.reference_line()
  
  def length(self):
    return self._impl.length() 
  
  def lane_section(self):
    road_impl = impl_cache.get_impl_by_ids("road", self._impl.road())
    if len(road_impl) == 0:
      pass
    for lane_section_impl in road_impl.lane_sections():
      for lane_id in lane_section_impl.lanes():
        if lane_id == self.id():
          return ToInfo(lane_section_impl, "lane_section")[0]
    return None
  
  def road(self):
    road_impl = impl_cache.get_impl_by_ids("road", self._impl.road())
    if len(road_impl) == 0:
      pass
    return ToInfo(road_impl, "road")[0]
    
  def successor_lane_links(self):
    return ToInfo(self._impl.successor_lane_links(), "lane_link") 
  
  def predecessor_lane_links(self):
    return ToInfo(self._impl.predecessor_lane_links(), "lane_link") 
  
  def left_neighbor_forward_lane(self):
    impls = impl_cache.get_impl_by_ids("lane", self._impl.left_neighbor_forward_lane())
    return ToInfo(impls, "lane")[0]
  
  def left_neighbor_forward_driving_lane(self):
    impls = impl_cache.get_impl_by_ids("lane", self._impl.left_neighbor_forward_driving_lane())
    return ToInfo(impls, "lane")[0]
  
  def right_neighbor_forward_lane(self):
    impls = impl_cache.get_impl_by_ids("lane", self._impl.right_neighbor_forward_lane())
    return ToInfo(impls, "lane")[0]
  
  def right_neighbor_forward_driving_lane(self):
    impls = impl_cache.get_impl_by_ids("lane", self._impl.right_neighbor_forward_driving_lane())
    return ToInfo(impls, "lane")[0]
  
  def left_neighbor_reverse_lane_ids(self):
    impls = impl_cache.get_impl_by_ids("lane", self._impl.left_neighbor_reverse_lane_ids())
    return ToInfo(impls, "lane")
  
  def right_neighbor_reverse_lane_ids(self):
    impls = impl_cache.get_impl_by_ids("lane", self._impl.right_neighbor_reverse_lane_ids())
    return ToInfo(impls, "lane")
  
  def lanes(self):
    return self._impl.lanes()
  
  def stop_lines(self):
    return self._impl.stop_lines()
  
  def cross_walks(self):
    return self._impl.cross_walks()
  
  def pois(self):
    return self._impl.pois()
  
  def pull_over_regions(self):
    return self._impl.pull_over_regions()
  
  def parking_spaces(self):
    return self._impl.parking_spaces()
  
  def objects(self):
    return self._impl.objects()
  
  def junctions(self):
    return self._impl.junctions()  
  
  def GetProjection(self, point:Vec2d):
    return self._impl.GetProjection(point)
  
  def GetPoint(self, s, d):
    return self._impl.GetProjection(s, d)
  
  def GetHeading(self, s):
    return self._impl.GetProjection(s)
  
  def GetWidth(self, s):
    return self._impl.GetProjection(s)
  
  def GetRoadWidth(self, s):
    return self._impl.GetProjection(s)
  
  def GetRelativeWidth(self, point:Vec2d, heading):
    return self._impl.GetProjection(point, heading)
  
class LanelinkInfo:
  def __init__(self, lane_link_impl:LaneLinkImpl) -> None:
    self._impl = lane_link_impl
    
  def from_lane(self):
    lane_impl = impl_cache.get_impl_by_ids("lane", self._impl.from_lane_id())
    return ToInfo(lane_impl, "lane")
  
  def from_s(self):
    return self._impl.from_s()
  
  def to_lane(self):
    lane_impl = impl_cache.get_impl_by_ids("lane", self._impl.to_lane_id())
    return ToInfo(lane_impl, "lane")
  
  def to_s(self):
    return self._impl.to_s()
  
class LaneSectionInfo:
  def __init__(self, lane_section_impl:LaneSectionImpl) -> None:
    self._impl = lane_section_impl
    
  def lanes(self):
    lane_impls = impl_cache.get_impl_by_ids("lane", self._impl.lanes())
    return ToInfo(lane_impls, "lane")
  
  def road(self):
    road_impl = impl_cache.get_impl_by_ids("road", self._impl.road_id())[0]
    return ToInfo([road_impl], "road")[0]
  
  def prev_lane_section(self):
    road_impl = impl_cache.get_impl_by_ids("road", self._impl.road_id())[0]
    for lane_section_impl in road_impl.lane_sections():
      if lane_section_impl.index == self._impl.index() - 1:
        return ToInfo(lane_section_impl, "lane_section")
    return None
  
  def next_lane_section(self):
    road_impl = impl_cache.get_impl_by_ids("road", self._impl.road_id())[0]
    for lane_section_impl in road_impl.lane_sections():
      if lane_section_impl.index == self._impl.index() + 1:
        return ToInfo(lane_section_impl, "lane_section")
    return None
       
   
class RoadInfo:
  def __init__(self, road_impl:RoadImpl) -> None:
    self._impl = road_impl
    self._lane_section_infos = ToInfo(road_impl.lane_sections())
    
  def id(self):
    return self._impl.id()
  
  def lane_sections(self):
    return self._lane_section_infos
  
  def junction_id(self):
    return self._impl.junction()
  
  def junction(self):
    junction_impl = impl_cache.get_impl_by_ids("junction", self._impl.junction())[0]
    return ToInfo(junction_impl, "junction")
  
  def IsInJunction(self):
    return self._impl.IsInJunction()
  
  def prev_roads(self):
    road_impls = impl_cache.get_impl_by_ids("road", self._impl.prev_roads())
    return ToInfo(road_impls, "road")
  
  def next_roads(self):
    road_impls = impl_cache.get_impl_by_ids("road", self._impl.next_roads())
    return ToInfo(road_impls, "road")
  
  def prev_junction(self):
    junction_impl = impl_cache.get_impl_by_ids("junction", self._impl.prev_junction())
    return ToInfo(junction_impl, "junction")
  
  def next_junction(self):
    junction_impl = impl_cache.get_impl_by_ids("junction", self._impl.next_junction())
    return ToInfo(junction_impl, "junction")
  
  def polygon(self):
    return self._impl.polygon()
  
  def attributes(self):
    return self._impl.attributes()
  
  def name(self):
    return self._impl.name()
  
  def type(self):
    return self._impl.type()
  
  # road struct and schedule poi todo
  
class JunctionInfo:
  def __init__(self, junction_impl:JunctionImpl) -> None:
    self._impl = junction_impl
    
  def id(self):
    return self._impl.id()
  
  def polygon(self):
    return self._impl.polygon()
  
  def type(self):
    return self._impl.type()
  
  def name(self):
    return self._impl.name()
  
  def is_virtual_junction(self):
    return self._impl.is_virtual_junction()
  
  def roads(self):
    road_impls = impl_cache.get_impl_by_ids("road", self._impl.roads())
    return ToInfo(road_impls, "road")
  
  def attributes(self):
    return self._impl.attributes()
  
  def lanes(self):
    return self._impl.lanes()
    
class ObjectInfo:
  def __init__(self, object_impl:ObjectImpl) -> None:
    self._impl = object_impl
  
  def id(self):
    return self._impl.id()    
  
  def type(self):
    return self._impl.type()
  
  def polygon(self):
    return self._impl.polygon()
  
  def height(self):
    return self._impl.height()
  
  def lanes(self):
    return self._impl.lanes()
  
  def attributes(self):
    return self._impl.attibutes()
  
class CrosswalkInfo:
  def __init__(self, crosswalk_impl:CrosswalkImpl) -> None:
    self._impl = crosswalk_impl
    
  def id(self):
    return self._impl.id()
  
  def left_boundary(self):
    return self._impl.left_boundary()
  
  def right_boundary(self):
    return self._impl.right_boundary()
  
  def polygon(self):
    return self._impl.polygon()
  
  def attributes(self):
    return self._impl.attributes()
  
  def lanes(self):
    return self._impl.lanes()
  
class ParkingSpaceInfo:
  def __init__(self, parking_space_impl:ParkingSpaceImpl) -> None:
    self._impl = parking_space_impl
    
  def id(self):
    return self._impl.id()
  
  def left_boundary(self):
    return self._impl.left_boundary()
  
  def right_boundary(self):
    return self._impl.right_boundary()
  
  def reference_line(self):
    return self._impl.reference_line()
  
  def polygon(self):
    return self._impl.polygon()
  
  def in_lanes(self):
    return self._impl.in_lanes()
  
  def out_lanes(self):
    return self._impl.out_lanes()
  
  def pois(self):
    return self._impl.pois()
  
class PoiInfo:
  def __init__(self, poi_impl:PoiImpl) -> None:
    self._impl = poi_impl
    
  def id(self):
    return self._impl.id()
  
  def type(self):
    return self._impl.type()
  
  def name(self):
    return self._impl.name()
  
  def coordinate(self):
    return self._impl.coordinate()
  
  def lanes(self):
    return self._impl.lanes()
  
  def pull_over_regions(self):
    return self._impl.pull_over_regions()
  
  def parking_spaces(self):
    return self._impl.parking_spaces()
  
class PullOverRegionInfo:
  def __init__(self, pull_over_region_impl:PullOverRegionImpl) -> None:
    self._impl = pull_over_region_impl
    
  def id(self):
    return self._impl.id()
  
  def pois(self):
    return self._impl.pois()
  
  def lane(self):
    lane_impl = impl_cache.get_impl_by_ids("lane", self._impl.lane())
    return ToInfo(lane_impl, "lane")
  
  def start_s(self):
    return self._impl.start_s()
  
  def end_s(self):
    return self._impl.end_s()
  
  def d(self):
    return self._impl.d()
  
class SignalInfo:
  def __init__(self, signal_impl:SignalImpl) -> None:
    self._impl = signal_impl
    
  def id(self):
    return self._impl.id()
  
  def polygon(self):
    return self._impl.polygon()
  
  def stop_lines(self):
    return self._impl.stop_lines()
  
  def signal_type(self):
    return self._impl.signal_type()
  
  def combination_type(self):
    return self._impl.combination_type()
  
  def signal_center(self):
    return self._impl.signal_center()
  
class StopLineInfo:
  def __init__(self, stop_line_impl:StopLineImpl) -> None:
    self._impl = stop_line_impl
    
  def id(self):
    return self._impl.id()
  
  def curve(self):
    return self.curve()
  
  def lanes(self):
    return self.lanes()
  
  def signals(self):
    return self.signals()
  
  
  
    
    
  