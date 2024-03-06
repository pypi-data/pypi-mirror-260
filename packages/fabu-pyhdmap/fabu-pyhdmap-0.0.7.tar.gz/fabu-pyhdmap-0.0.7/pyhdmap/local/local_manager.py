import os
from typing import List, Tuple

import pyhdmap.proto.grpc.hdmapimpl_pb2 as hdmapimpl_pb2
from pyhdmap.config.config import ConfigManager
from pyhdmap.externals import libhdmap
from pyhdmap.externals.libhdmap import *
from pyhdmap.utils.vessel import *
from pyhdmap.utils.singleton import Singleton
from pyhdmap.utils.exception import except_output

current_file_path = os.path.abspath(__file__)
config_path = os.path.dirname(os.path.dirname(current_file_path))
ConfigManager().init_config(config_path)
runtime_flags = ConfigManager()._get_runtime_flags()
libhdmap.SetRuntimeFlags(runtime_flags)

@Singleton
class LocalManager:
  def __init__(self) -> None:
    self._map_bin_path = ""
    self._business_scene = ""
    self._hdmap = HDMap()
    
    
  def set_bin_path_and_scene(self, bin_path, scene):
    self._map_bin_path = bin_path
    self._business_scene = scene
    
  def LoadMap(self, bridge_mode = {}):
    hdmap_bridge_modes = []
    for bridge_name, mode in bridge_mode.items():
      hdmap_bridge_mode = BridgeMode()
      hdmap_bridge_mode.bridge_name = bridge_name
      hdmap_bridge_mode.mode = mode
      hdmap_bridge_modes.append(hdmap_bridge_mode)
    res = self._hdmap.LoadMapWithMode(self._map_bin_path, self._business_scene, hdmap_bridge_modes)
    return res
  
  ## basic method    
  @except_output
  def Reload(self, vessels:List[Vessel]):
    vessel_status = build_vessel_status(vessels)
    return self._hdmap.Reload(vessel_status.SerializeToString())
  
  @except_output
  def GetMap(self):
    return self._hdmap.GetMap()
  
  @except_output
  def GetLaneById(self, id:int):
    return self._hdmap.GetLaneById(IdInfo(id))
  
  @except_output
  def GetRoadById(self, id:int):
    return self._hdmap.GetRoadById(IdInfo(id))
    
  @except_output
  def GetJunctionById(self, id:int):
    return self._hdmap.GetJunctionById(IdInfo(id))
  
  @except_output
  def GetObjectById(self, id:int):
    return self._hdmap.GetObjectById(IdInfo(id))  
    
  @except_output
  def GetCrosswalkById(self, id:int):
    return self._hdmap.GetCrosswalkById(IdInfo(id))

  @except_output
  def GetParkingSpaceById(self, id:int):
    return self._hdmap.GetParkingSpaceById(IdInfo(id))
  
  @except_output
  def GetPoiById(self, id:int):
    return self._hdmap.GetPoiById(IdInfo(id))
  
  @except_output
  def GetPullOverRegionById(self, id:int):
    return self._hdmap.GetPullOverRegionById(IdInfo(id))
  
  @except_output
  def GetSignalById(self, id:int):
    return self._hdmap.GetSignalById(IdInfo(id))
  
  @except_output
  def GetStopLineById(self, id:int):
    return self._hdmap.GetStopLineById(IdInfo(id))
  
  @except_output
  def GetLanes(self, point, distance):
    return self._hdmap.GetLanes(Vec2d(point.x(), point.y()), distance)
    
  @except_output
  def GetJunctions(self, point, distance):
    return self._hdmap.GetJunctions(Vec2d(point.x(), point.y()), distance)
    
  @except_output
  def GetObjects(self, point, distance):
    return self._hdmap.GetObjects(Vec2d(point.x(), point.y()), distance)
    
  @except_output
  def GetCrosswalks(self, point, distance):
    return self._hdmap.GetCrosswalks(Vec2d(point.x(), point.y()), distance)
    
  @except_output
  def GetParkingSpaces(self, point, distance):
    return self._hdmap.GetParkingSpaces(Vec2d(point.x(), point.y()), distance)