import grpc
import time
from typing import List, Tuple

import pyhdmap.proto.grpc.hdmapimpl_pb2 as hdmapimpl_pb2
from pyhdmap.proto.grpc import hdmapimpl_pb2_grpc
from pyhdmap.utils.singleton import Singleton
from pyhdmap.utils.vessel import *

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
  
  def LoadMap(self):
    print("11")
    request = hdmapimpl_pb2.LoadMapRequest()
    request.time_stamp = time.time()
    request.business_scene = self._scene
    response = self.stub.LoadMap(request)
    print("111")
    if response.load_status == False:
      return False
    else:
      self._uuid = response.uuid
      return True
    
  def ReleaseMap(self):
    request = hdmapimpl_pb2.ReleaseMapRequest()
    request.time_stamp = time.time()
    request.uuid = self._uuid
    response = self.stub.ReleaseMap(request)
    return response.status
    
  def Reload(self, vessels):
    request = hdmapimpl_pb2.ReloadRequest()
    request.time_stamp = time.time()
    request.uuid = self._uuid
    vessel_status = build_vessel_status(vessels)
    request.vessel_status.CopyFrom(vessel_status)
    response = self.stub.Reload(request)
    return response.reload_status
  
  def GetMap(self):
    request = hdmapimpl_pb2.GetMapRequest()
    request.time_stamp = time.time()
    request.uuid = self._uuid
    response = self.stub.GetMap(request)
    return response
      
  
  def generate_get_element_by_id_request(self, ids, type):
    request = hdmapimpl_pb2.GetElementByIdRequest()
    request.time_stamp = time.time()
    request.business_scene = self._scene
    request.element_ids.extend(ids) 
    request.element_type = type
    return request
    
  def get_elements_by_ids(self, ids, type):
    request = self.generate_get_element_by_id_request(ids, type)
    response = self.stub.GetElementById(request)
    if response.status == False:
      pass #output error
    else:
      return response

  def generate_get_elements_request(self, point, radius, type):
    request = hdmapimpl_pb2.GetElementsRequest()
    request.time_stamp = time.time()
    request.business_scene = self._scene
    request.x = point.x()
    request.y = point.y()
    request.element_type = type
    request.radius = radius
    return request
  
  def get_elements(self, point, radius, type):
    request = self.generate_get_elements_request(point, radius, type)
    response = self.stub.GetElements(request)
    if response.status == False:
      pass
    else:
      return response
    
  ## lane interface
  def get_lane_projection(self, lane_id, x, y):
    request = hdmapimpl_pb2.GetProjectionRequest()
    request.time_stamp = time.time()
    request.business_scene = self._scene
    request.lane_id = lane_id
    request.x = x
    request.y = y
    response = self.stub.Getprojection(request)
    if response.status == False:
      pass
    else:
      return response
    
  def get_lane_point(self, lane_id, s, d):
    request = hdmapimpl_pb2.GetPointRequest()
    request.time_stamp = time.time()
    request.business_scene = self._scene
    request.lane_id = lane_id
    request.s = s
    request.d = d
    response = self.stub.GetPoint(request)
    if response.status == False:
      pass
    else:
      return response
    
  def get_lane_heading(self, lane_id, s):
    request = hdmapimpl_pb2.GetHeadingRequest()
    request.time_stamp = time.time()
    request.business_scene = self._scene
    request.lane_id = lane_id
    request.s = s
    response = self.stub.GetHeading(request)
    if response.status == False:
      pass
    else:
      return response
    
  def get_lane_width(self, lane_id, s):
    request = hdmapimpl_pb2.GetWidthRequest()
    request.time_stamp = time.time()
    request.business_scene = self._scene
    request.lane_id = lane_id
    request.s = s
    response = self.stub.GetWidth(request)
    if response.status == False:
      pass
    else:
      return response
    
  def get_lane_road_width(self, lane_id, s):
    request = hdmapimpl_pb2.GetWidthRequest()
    request.time_stamp = time.time()
    request.business_scene = self._scene
    request.lane_id = lane_id
    request.s = s
    response = self.stub.GetRoadWidth(request)
    if response.status == False:
      pass
    else:
      return response
    
  def get_lane_relative_width(self, lane_id, x, y, heading):
    request = hdmapimpl_pb2.GetRelativeWidthRequest()
    request.time_stamp = time.time()
    request.business_scene = self._scene
    request.lane_id = lane_id
    request.x = x
    request.y = y
    request.heading = heading
    response = self.stub.GetRelativeWidth(request)
    if response.status == False:
      pass
    else:
      return response