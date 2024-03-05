from externals.libhdmap import *
from pyhdmap.utils.singleton import Singleton
from pyhdmap.remote.grpc_client import HDMapClient
from pyhdmap.remote.hdmap_impl.geometry import LineStringDataImpl
from pyhdmap.remote.hdmap_impl.lane_impl import LaneImpl
from pyhdmap.remote.hdmap_impl.road_impl import RoadImpl
from pyhdmap.remote.hdmap_impl.junction_impl import JunctionImpl
from pyhdmap.remote.hdmap_impl.object_impl import ObjectImpl
from pyhdmap.remote.hdmap_impl.poi_impl import PoiImpl
from pyhdmap.remote.hdmap_impl.parking_space_impl import ParkingSpaceImpl
from pyhdmap.remote.hdmap_impl.pull_over_region_impl import PullOverRegionImpl
from pyhdmap.remote.hdmap_impl.stop_line_impl import StopLineImpl
from pyhdmap.remote.hdmap_impl.crosswalk_impl import CrosswalkImpl
from pyhdmap.remote.hdmap_impl.signal_impl import SignalImpl
from pyhdmap.remote.builder import Builder

@Singleton
class ImplCache:
  def __init__(self) -> None:
    self._line_impl_cache:dict[int, LineStringDataImpl] = {}
    self._lane_impl_cache:dict[int, LaneImpl] = {}
    self._road_impl_cache:dict[int, RoadImpl] = {}
    self._junction_impl_cache:dict[int, JunctionImpl] = {}
    self._object_impl_cache:dict[int, ObjectImpl] = {}
    self._poi_impl_cache:dict[int, PoiImpl] = {}
    self._parking_space_impl_cache:dict[int, ParkingSpaceImpl] = {}
    self._pull_over_region_impl_cache:dict[int, PullOverRegionImpl] = {}
    self._stop_line_impl_cache:dict[int, StopLineImpl] = {}
    self._crosswalk_impl_cache:dict[int, CrosswalkImpl] = {}
    self._signal_impl_cache:dict[int, SignalImpl] = {}
    
    self.hdmap_client = HDMapClient()
    print("impl cache init finish")
    
  def set_config(self, ip, port, scene):
    self.hdmap_client.set_business_scene(scene)
    self.hdmap_client.set_ip_and_port(ip, port)
    
  def build_impls_from_getmap_response(self, grpc_response):
    for lane_proto in grpc_response.lane_proto:
      if lane_proto.id.id in self._lane_impl_cache:
        continue
      impl, line_impls = Builder.build_lane_impl(lane_proto, grpc_response.lines, grpc_response.relations, grpc_response.lane_links)
      self._lane_impl_cache[impl.id()] = impl
      for line_impl in line_impls:
        self._line_impl_cache[line_impl.id()] = line_impl
    for road_proto in grpc_response.road_proto:
      if road_proto.id.id in self._road_impl_cache:
        continue
      impl = Builder.build_road_impl(road_proto, grpc_response.lines)
      self._road_impl_cache[impl.id()] = impl
    for junction_proto in grpc_response.junction_proto:
      if junction_proto.id.id in self._junction_impl_cache:
        continue
      impl = Builder.build_junction_impl(junction_proto, grpc_response.lines, grpc_response.relations)
      self._junction_impl_cache[impl.id()] = impl
    for object_proto in grpc_response.object_proto:
      if object_proto.id.id in self._object_impl_cache:
        continue
      impl = Builder.build_object_impl(object_proto, grpc_response.lines, grpc_response.relations)
      self._object_impl_cache[impl.id()] = impl
    for crosswalk_proto in grpc_response.crosswalk_proto:
      if crosswalk_proto.id.id in self._crosswalk_impl_cache:
        continue
      impl, line_impls = Builder.build_crosswalk_impl(crosswalk_proto, grpc_response.lines, grpc_response.relations)
      self._crosswalk_impl_cache[impl.id()] = impl
      for line_impl in line_impls:
        self._line_impl_cache[line_impl.id()] = line_impl
    for parking_space_proto in grpc_response.parking_space_proto:
      if parking_space_proto.id.id in self._parking_space_impl_cache:
        continue
      impl, line_impls = Builder.build_parking_space_impl(parking_space_proto, grpc_response.lines, grpc_response.relations)
      self._parking_space_impl_cache[impl.id()] = impl
      for line_impl in line_impls:
        self._line_impl_cache[line_impl.id()] = line_impl
    for poi_proto in grpc_response.poi_proto:
      if poi_proto.id.id in self._poi_impl_cache:
        continue
      impl = Builder.build_poi_impl(poi_proto, grpc_response.relations)
      self._poi_impl_cache[impl.id()] = impl
    for pull_over_region_proto in grpc_response.pull_over_region_proto:
      if pull_over_region_proto.id.id in self._pull_over_region_impl_cache:
        continue
      impl = Builder.build_pull_over_region_impl(pull_over_region_proto, grpc_response.relations)
      self._pull_over_region_impl_cache[impl.id()] = impl
    for signal_proto in grpc_response.signal_proto:
      if signal_proto.id.id in self._signal_impl_cache:
        continue
      impl = Builder.build_signal_impl(signal_proto, grpc_response.lines, grpc_response.relations)
      self._signal_impl_cache[impl.id()] = impl
    for stop_line_proto in grpc_response.stop_line_proto:
      if stop_line_proto.id.id in self._stop_line_impl_cache:
        continue
      impl, line_impls = Builder.build_stop_line_impl(stop_line_proto, grpc_response.lines, grpc_response.relations)
      self._stop_line_impl_cache[impl.id()] = impl
      for line_impl in line_impls:
        self._line_impl_cache[line_impl.id()] = line_impl
    
    return 
        
      
  def build_impls_from_proto(self, grpc_response, type):
    impls = []
    total_line_impls = []
    if type == "lane":
      for element in grpc_response.element_proto:
        impl, line_impls = Builder.build_lane_impl(element.lane_proto, grpc_response.lines, grpc_response.relations, grpc_response.lane_links)
        impls.append(impl)
        total_line_impls.append(line_impls)
    elif type == "road":
      for element in grpc_response.element_proto:
        impl = Builder.build_road_impl(element.road_proto, grpc_response.lines)
        impls.append(impl)
    elif type == "junction":
      for element in grpc_response.element_proto:
        impl = Builder.build_junction_impl(element.junction_proto, grpc_response.lines, grpc_response.relations)
        impls.append(impl)
    elif type == "object":
      for element in grpc_response.element_proto:
        impl = Builder.build_object_impl(element.object_proto, grpc_response.lines, grpc_response.relations)
        impls.append(impl)
    elif type == "crosswalk":
      for element in grpc_response.element_proto:
        impl, line_impls = Builder.build_crosswalk_impl(element.crosswalk_proto, grpc_response.lines, grpc_response.relations)
        impls.append(impl)
        total_line_impls.append(line_impls)
    elif type == "parking_space":
      for element in grpc_response.element_proto:
        impl, line_impls = Builder.build_parking_space_impl(element.parking_space_proto, grpc_response.lines, grpc_response.relations)
        impls.append(impl)
        total_line_impls.append(line_impls)
    elif type == "poi":
      for element in grpc_response.element_proto:
        impl = Builder.build_poi_impl(element.poi_proto, grpc_response.relations)
        impls.append(impl)
    elif type == "pull_over_region":
      for element in grpc_response.element_proto:
        impl = Builder.build_pull_over_region_impl(element.pull_over_region_proto, grpc_response.relations)
        impls.append(impl)
    elif type == "signal":
      for element in grpc_response.element_proto:
        impl = Builder.build_signal_impl(element.signal_proto, grpc_response.lines, grpc_response.relations)
        impls.append(impl)
    elif type == "stop_line":
      for element in grpc_response.element_proto:
        impl, line_impls = Builder.build_stop_line_impl(element.stop_line_proto, grpc_response.lines, grpc_response.relations)
        impls.append(impl)
        total_line_impls.append(line_impls)
        
    return impls, total_line_impls
      
    
  def get_impl_by_ids(self, type, ids):
    if type == "lane":
      impl_cache = self._lane_impl_cache
    elif type == "line":  
      impl_cache = self._line_impl_cache
    elif type == "road":
      impl_cache = self._road_impl_cache
    elif type == "junction":
      impl_cache = self._junction_impl_cache
    elif type == "object":
      impl_cache = self._object_impl_cache
    elif type == "crosswalk":
      impl_cache = self._crosswalk_impl_cache
    elif type == "parking_space":
      impl_cache = self._parking_space_impl_cache
    elif type == "poi":
      impl_cache = self._poi_impl_cache
    elif type == "pull_over_region":
      impl_cache = self._pull_over_region_impl_cache
    elif type == "signal":
      impl_cache = self._signal_impl_cache
    elif type == "stop_line":
      impl_cache = self._stop_line_impl_cache
    
    res = []
    query_ids = []
    if isinstance(ids, list):
      for id in ids:
        if id in impl_cache.keys():
          res.append(impl_cache[id])
        else:
          query_ids.append(id)
    else:
      if ids in impl_cache.keys():
        res.append(impl_cache[ids])
      else:
        query_ids.append(ids)
        
    if len(query_ids) == 0:
      return res
    
    response = self.hdmap_client.get_elements_by_ids(query_ids, type)
    if response == None:
      pass
    
    impls, total_line_impls = self.build_impls_from_proto(response, type)

    if len(total_line_impls) != 0:
      for line_impl in total_line_impls:
        self._line_impl_cache[line_impl.id()] = line_impl

    for impl in impls:
      impl_cache[impl.id()] = impl 
    res.append(impls)
    return res
  
if __name__ == "__main__":
  impl_cache = ImplCache()
  print(impl_cache.get_impl_by_id("lane", 1))
    
  