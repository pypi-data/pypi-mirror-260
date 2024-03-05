import grpc
import time
from typing import List, Tuple

import proto.grpc.hdmapimpl_pb2 as hdmapimpl_pb2
from proto.grpc import hdmapimpl_pb2_grpc
from pyhdmap.utils.singleton import Singleton
from pyhdmap.utils.vessel import Vessel

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
  

@Singleton
class HDMapClient:

  def __init__(self):
    self._ip = "[::]"
    self._port = "50051"
    self._scene = ""
    self._uuid = " "
    self.channel = grpc.insecure_channel(f"{self._ip}:{self._port}")
    self.stub = hdmapimpl_pb2_grpc.HdmapImplStub(self.channel)
    print("grpc client init finish")

  def set_ip_and_port(self, ip, port):
    self._ip = ip
    self._port = port
    self.channel = grpc.insecure_channel(f"{self._ip}:{self._port}")
    self.stub = hdmapimpl_pb2_grpc.HdmapImplStub(self.channel)
  
  def set_business_scene(self, scene):
    self._scene = scene 
    
  ##hdmap interface
  
  async def LoadMap(self):
    request = hdmapimpl_pb2.LoadMapRequest()
    request.time_stamp = time.time()
    request.business_scene = self._scene
    response = await self.stub.LoadMap(request)
    if response.load_status == False:
      return False
    else:
      self._uuid = response.uuid
      return True
    
  async def ReleaseMap(self):
    request = hdmapimpl_pb2.ReleaseMapReply()
    request.time_stamp = time.time()
    request.uuid = self._uuid
    response = await self.stub.ReleaseMap(request)
    return response.status
    
  async def Reload(self, vessels):
    request = hdmapimpl_pb2.ReloadRequest()
    request.time_stamp = time.time()
    request.uuid = self._uuid
    vessel_status = build_vessel_status(vessels)
    request.vessel_status.CopyFrom(vessel_status)
    response = await self.stub.Reload(request)
    return response.reload_status
  
  async def GetMap(self):
    request = hdmapimpl_pb2.GetMapRequest()
    request.time_stamp = time.time()
    request.uuid = self._uuid
    response = await self.stub.GetMap(request)
    return response
      
  
  async def generate_get_element_by_id_request(self, ids, type):
    request = hdmapimpl_pb2.GetElementByIdRequest()
    request.time_stamp = time.time()
    request.business_scene = self._scene
    request.element_ids.extend(ids) 
    request.element_type = type
    return request
    
  async def get_elements_by_ids(self, ids, type):
    request = self.generate_get_element_by_id_request(ids, type)
    response = await self.stub.GetElementById(request)
    if response.status == False:
      pass #output error
    else:
      return response

  async def generate_get_elements_request(self, point, radius, type):
    request = hdmapimpl_pb2.GetElementsRequest()
    request.time_stamp = time.time()
    request.business_scene = self._scene
    request.x = point.x()
    request.y = point.y()
    request.element_type = type
    request.radius = radius
    return request
  
  async def get_elements(self, point, radius, type):
    request = self.generate_get_elements_request(point, radius, type)
    response = await self.stub.GetElements(request)
    if response.status == False:
      pass
    else:
      return response
    
  ## lane interface
  async def get_lane_projection(self, lane_id, x, y):
    request = hdmapimpl_pb2.GetProjectionRequest()
    request.time_stamp = time.time()
    request.business_scene = self._scene
    request.lane_id = lane_id
    request.x = x
    request.y = y
    response = await self.stub.Getprojection(request)
    if response.status == False:
      pass
    else:
      return response
    
  async def get_lane_point(self, lane_id, s, d):
    request = hdmapimpl_pb2.GetPointRequest()
    request.time_stamp = time.time()
    request.business_scene = self._scene
    request.lane_id = lane_id
    request.s = s
    request.d = d
    response = await self.stub.GetPoint(request)
    if response.status == False:
      pass
    else:
      return response
    
  async def get_lane_heading(self, lane_id, s):
    request = hdmapimpl_pb2.GetHeadingRequest()
    request.time_stamp = time.time()
    request.business_scene = self._scene
    request.lane_id = lane_id
    request.s = s
    response = await self.stub.GetHeading(request)
    if response.status == False:
      pass
    else:
      return response
    
  async def get_lane_width(self, lane_id, s):
    request = hdmapimpl_pb2.GetWidthRequest()
    request.time_stamp = time.time()
    request.business_scene = self._scene
    request.lane_id = lane_id
    request.s = s
    response = await self.stub.GetWidth(request)
    if response.status == False:
      pass
    else:
      return response
    
  async def get_lane_road_width(self, lane_id, s):
    request = hdmapimpl_pb2.GetWidthRequest()
    request.time_stamp = time.time()
    request.business_scene = self._scene
    request.lane_id = lane_id
    request.s = s
    response = await self.stub.GetRoadWidth(request)
    if response.status == False:
      pass
    else:
      return response
    
  async def get_lane_relative_width(self, lane_id, x, y, heading):
    request = hdmapimpl_pb2.GetRelativeWidthRequest()
    request.time_stamp = time.time()
    request.business_scene = self._scene
    request.lane_id = lane_id
    request.x = x
    request.y = y
    request.heading = heading
    response = await self.stub.GetRelativeWidth(request)
    if response.status == False:
      pass
    else:
      return response