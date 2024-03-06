from pyhdmap.proto.hdmap_lib.proto import lane_pb2
from pyhdmap.externals.libhdmap import *
from pyhdmap.remote.hdmap_impl.relation_impl import RelationImpl
from pyhdmap.remote.grpc_client import HDMapClient
from pyhdmap.remote.hdmap_impl.geometry import CurveImpl
from pyhdmap.remote.hdmap_impl.attribute_impl import AttributesImpl

hdmap_client = HDMapClient()

class LaneImpl:
  
  def __init__(self) -> None:
    self._id = 0
    self._type = lane_pb2.Lane.Type.NONE
    self._turn_type = lane_pb2.Lane.TurnType.NO_TURN
    self._speed_info = None
    self._junction_id = 0
    self._left_boundary = CurveImpl()
    self._right_boundary = CurveImpl()
    self._central_line:list[Vec2d] = []
    self._reference_line:ReferenceLine = None
    self._successor_lane_links = []
    self._predecessor_lane_links = []
    self._left_neighbor_forward_id = 0
    self._left_neighbor_forward_driving_id = 0
    self._right_neighbor_forward_id = 0
    self._right_neighbor_forward_driving_id = 0
    self._left_neighbor_reverse_ids = []
    self._right_neighbor_reverse_ids = []
    self._polygon = Polygon2d()
    self._attrbutes = AttributesImpl()
    self._lane_section = None
    self._road = None
    self._lane_priority = 0
    self._rank = 0
    self._bi_direction_lane_id = 0
    
    # relations
    self._lanes:list[RelationImpl] = []
    self._stop_lines:list[RelationImpl] = []
    self._cross_walks:list[RelationImpl] = []
    self._pois:list[RelationImpl] = []
    self._parking_spaces:list[RelationImpl] = []
    self._objects:list[RelationImpl] = []
    self._clear_areas:list[RelationImpl] = []
    self._junctions:list[RelationImpl] = []
  
  def id(self):
    return self._id
  
  def type(self):
    return self._type
  
  def turn_type(self):
    return self._turn_type
  
  def max_speed(self):
    return self._speed_info.max
  
  def min_speed(self):
    return self._speed_info.min
  
  def junction_id(self):
    return self._junction_id
  
  def IsInJunction(self):
    return self._junction_id == 0
  
  def left_boundary(self):
    return self._left_boundary
  
  def right_boundary(self):
    return self._right_boundary
  
  def central_line(self):
    return self._central_line

  def reference_line(self):
    if self._reference_line == None:
      Utils.BuildReferenceLineFromPoints(self._central_line, self._reference_line)
    return self._reference_line  
  
  def length(self):
    if self._reference_line == None:
      Utils.BuildReferenceLineFromPoints(self._central_line, self._reference_line)
    return self._reference_line.length()  
  
  def lane_section(self):
    return self._lane_section
  
  def road(self):
    return self._road
  
  def successor_lane_links(self):
    return self._successor_lane_links
  
  def predecessor_lane_links(self):
    return self._predecessor_lane_links
  
  def left_neighbor_forward_lane(self):
    return self._left_neighbor_forward_id
  
  def left_neighbor_forward_driving_lane(self):
    return self._left_neighbor_forward_driving_id
  
  def right_neighbor_forward_lane(self):
    return self._right_neighbor_forward_id
  
  def right_neighbor_forward_driving_lane(self):
    return self._right_neighbor_forward_driving_id
  
  def left_neighbor_reverse_lane_ids(self):
    return self._left_neighbor_reverse_ids
  
  def right_neighbor_reverse_lane_ids(self):
    return self._right_neighbor_reverse_ids
  
  def lanes(self):
    return self._lanes
  
  def stop_lines(self):
    return self._stop_lines
  
  def cross_walks(self):
    return self._cross_walks
  
  def pois(self):
    return self._pois
  
  def pull_over_regions(self):
    return self._pull_over_regions
  
  def parking_spaces(self):
    return self._parking_spaces
  
  def objects(self):
    return self._objects
  
  def junctions(self):
    return self._junctions  
  
  def GetProjection(self, point:Vec2d):
    res = hdmap_client.get_lane_projection(self._id, point.x(), point.y())
    return res.s, res.d
  
  def GetPoint(self, s, d):
    res = hdmap_client.get_lane_point(self._id, s, d)
    return Vec2d(res.x, res.y)
  
  def GetHeading(self, s):
    res = hdmap_client.get_lane_heading(self._id, s)
    return res.heading
  
  def GetWidth(self, s):
    res = hdmap_client.get_lane_width(self._id, s)
    return res.left_width, res.right_width
  
  def GetRoadWidth(self, s):
    res = hdmap_client.get_lane_road_width(self._id, s)
    return res.left_width, res.right_width
  
  def GetRelativeWidth(self, point:Vec2d, heading):
    res = hdmap_client.get_lane_relative_width(self._id, point.x(), point.y(), heading)
    return res.left_relative_width, res.right_relative_width
    
    