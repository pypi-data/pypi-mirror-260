import os
from typing import List, Tuple

from externals import libhdmap
from externals.libhdmap import *
from pyhdmap.utils.singleton import Singleton
from pyhdmap.utils.exception import except_output
from pyhdmap.utils.vessel import Vessel
from pyhdmap.remote.grpc_client import HDMapClient
from pyhdmap.remote.impl_cache import ImplCache
from pyhdmap.remote.common import *

@Singleton
class RemoteManager:
  
  def __init__(self):
    self._remote_ip = "[::]"
    self._remote_port = "50051"
    self._business_scene = ""
    self._map_impls = ImplCache()
    self._hdmap_client = HDMapClient()
    print("remote manager init finish")
    
  def set_config(self, ip, port, scene):
    self._remote_ip = ip
    self._remote_port = port
    self._business_scene = scene
    self._map_impls.set_config(ip, port, scene)
    
  ## basic method
  @except_output()
  def LoadMap(self):
    return self._hdmap_client.LoadMap()
  
  @except_output()
  def ReleaseMap(self):
    return self._hdmap_client.ReleaseMap()
    
  @except_output
  def Reload(self, vessels:List[Vessel]):
    return self._hdmap_client.Reload(vessels)
  
  @except_output
  def GetMap(self):
    response = self._hdmap_client.GetMap()
    self._map_impls.build_impls_from_getmap_response(response)
    return True
  
  @except_output
  def GetLaneById(self, id:int):
    return ToInfo(self._map_impls.get_impl_by_ids("lane", id))
  
  @except_output
  def GetRoadById(self, id:int):
    return ToInfo(self._map_impls.get_impl_by_ids("road", id))
    
  @except_output
  def GetJunctionById(self, id:int):
    return ToInfo(self._map_impls.get_impl_by_ids("junction", id))
  
  @except_output
  def GetObjectById(self, id:int):
    return ToInfo(self._map_impls.get_impl_by_ids("object", id))    
    
  @except_output
  def GetCrosswalkById(self, id:int):
    return ToInfo(self._map_impls.get_impl_by_ids("crosswalk", id))

  @except_output
  def GetParkingSpaceById(self, id:int):
    return ToInfo(self._map_impls.get_impl_by_ids("parking_space", id))
  
  @except_output
  def GetPoiById(self, id:int):
    return ToInfo(self._map_impls.get_impl_by_ids("poi", id))
  
  @except_output
  def GetPullOverRegionById(self, id:int):
    return ToInfo(self._map_impls.get_impl_by_ids("pull_over_region", id))
  
  @except_output
  def GetSignalById(self, id:int):
    return ToInfo(self._map_impls.get_impl_by_ids("signal", id))
  
  @except_output
  def GetStopLineById(self, id:int):
    return ToInfo(self._map_impls.get_impl_by_ids("stop_line", id))
  
  @except_output
  def GetLanes(self, point, distance):
    response = self._hdmap_client.get_elements(point, distance, "lane")
    if response.status == False:
      pass
    else:
      self._map_impls.build_impls_from_proto(response, "lane")
      return True
    
  @except_output
  def GetJunctions(self, point, distance):
    response = self._hdmap_client.get_elements(point, distance, "junction")
    if response.status == False:
      pass
    else:
      self._map_impls.build_impls_from_proto(response, "junction")
      return True
    
  @except_output
  def GetObjects(self, point, distance):
    response = self._hdmap_client.get_elements(point, distance, "object")
    if response.status == False:
      pass
    else:
      self._map_impls.build_impls_from_proto(response, "object")
      return True
    
  @except_output
  def GetCrosswalks(self, point, distance):
    response = self._hdmap_client.get_elements(point, distance, "crosswalk")
    if response.status == False:
      pass
    else:
      self._map_impls.build_impls_from_proto(response, "crosswalk")
      return True
    
  @except_output
  def GetParkingSpaces(self, point, distance):
    response = self._hdmap_client.get_elements(point, distance, "parking_space")
    if response.status == False:
      pass
    else:
      self._map_impls.build_impls_from_proto(response, "parking_space")
      return True
    
  