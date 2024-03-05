from typing import List, Tuple

import pyhdmap.proto.grpc.hdmapimpl_pb2 as hdmapimpl_pb2

def MapGirderDirection(num):
    if num == 1:
        return hdmapimpl_pb2.Vessel.GirderDirection.NORMAL
    elif num == 2:
        return hdmapimpl_pb2.Vessel.GirderDirection.REVERSE
    elif num == 3:
        return hdmapimpl_pb2.Vessel.GirderDirection.BOTH_EAST
    elif num == 4:
        return hdmapimpl_pb2.Vessel.GirderDirection.BOTH_WEST
    return hdmapimpl_pb2.Vessel.GirderDirection.NORMAL

class Vessel:
  def __init__(self) -> None:
    self._head_x = 0.0
    self._head_y = 0.0
    self._rear_x = 0.0
    self._rear_y = 0.0
    self._head_bridge = ""
    self._leave_bridge = ""
    self._east_area_direction = 0
    self._east_working_area_direction = 0
    self._west_working_area_direction = 0
    self._west_area_direction = 0
    
  def head_x(self):
    return self._head_x
  
  def set_head_x(self, head_x):
    self._head_x = head_x
    
  def head_y(self):
    return self._head_y
  
  def set_head_x(self, head_y):
    self._head_y = head_y
    
  def rear_x(self):
    return self._rear_x
  
  def set_rear_x(self, rear_x):
    self._rear_x = rear_x
    
  def rear_y(self):
    return self._rear_y
  
  def set_rear_y(self, rear_y):
    self._rear_y = rear_y
    
  def head_bridge(self):
    return self._head_bridge
  
  def set_head_x(self, head_bridge):
    self._head_bridge = head_bridge
    
  def leave_bridge(self):
    return self._leave_bridge
  
  def set_leave_bridge(self, leave_bridge):
    self._leave_bridge = leave_bridge
    
  def east_area_direction(self):
    return self._east_area_direction
  
  def set_east_area_direction(self, east_area_direction):
    self._east_area_direction = east_area_direction
    
  def east_working_area_direction(self):
    return self._east_working_area_direction
  
  def set_east_working_area_direction(self, east_working_area_direction):
    self._east_working_area_direction = east_working_area_direction
    
  def west_working_area_direction(self):
    return self._west_working_area_direction
  
  def set_west_working_area_direction(self, west_working_area_direction):
    self._west_working_area_direction = west_working_area_direction
    
  def west_area_direction(self):
    return self._west_area_direction
  
  def set_west_area_direction(self, west_area_direction):
    self._west_area_direction = west_area_direction
    
def build_vessel_status(vessels:List[Vessel]):
  vessel_status = hdmapimpl_pb2.VesselStatus()
  for vessel in vessels:
    one_vessel_status = vessel_status.vessels.add()
    one_vessel_status.head.x = vessel.head_x()
    one_vessel_status.head.y = vessel.head_y()
    one_vessel_status.rear.x = vessel.rear_x()
    one_vessel_status.rear.y = vessel.rear_y()
    one_vessel_status.head_bridge = vessel.head_bridge()
    one_vessel_status.leave_bridge = vessel.leave_bridge()
    one_vessel_status.east_area_girder_direction = MapGirderDirection(vessel.east_area_direction)
    one_vessel_status.east_working_area_girder_direction = MapGirderDirection(vessel.east_working_area_direction)
    one_vessel_status.west_working_area_girder_direction = MapGirderDirection(vessel.west_working_area_direction)
    one_vessel_status.west_area_girder_direction = MapGirderDirection(vessel.west_area_direction)
  return vessel_status