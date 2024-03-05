from externals.libhdmap import *
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
from pyhdmap.remote.hdmap_impl.geometry import *
from proto.hdmap_lib.proto import relation_pb2, geometry_pb2

def build_curve(lines, line_string_datas:dict):
  curve = CurveImpl()
  line_string_data_impls = []
  for line in lines:
    line_string_impl = LineStringImpl()
    line_string_impl._id = line.id.id
    line_string_impl._is_reverse = line.is_reverse
    curve._lines.append(line_string_impl)
    line_string_data_impl = LineStringDataImpl()
    line_string_data_impl._id  = line.id.id
    line_string_data = line_string_datas[line.id.id]
    for point in line_string_data.points:
      line_string_data_impl._points.append(Vec2d(point.x, point.y))
    line_string_data_impls.append(line_string_data_impl)
    
  return curve, line_string_data_impls

def build_attributes(attribute_proto):
  attribute_impl = AttributesImpl()
  for attribute in attribute_proto:
    attribute_impl.SetAttribute(attribute.key, attribute.value)
    
  return attribute_impl
  
def build_lane_link(lane_link_proto):
  lane_link_impl = LaneLinkImpl()
  lane_link_impl._from_lane_id = lane_link_proto.from_lane.id
  lane_link_impl._from_s = lane_link_proto.from_s
  lane_link_impl._to_lane_id = lane_link_proto.to_lane.id
  lane_link_impl._to_s = lane_link_proto.to_s
  return lane_link_impl

def build_polygon(polygon_proto, lines:dict):
  polygon_points = []
  for line in polygon_proto.lines:
    line_string_data = lines[line.id.id]
    for point in line_string_data.points:
      polygon_points.append(Vec2d(point.x, point.y))
  
  return Polygon2d(polygon_points)
  

def build_lane_section(lane_section_proto, road_id, index):
  lane_section_impl = LaneSectionImpl()
  lane_section_impl._index = index
  lane_section_impl._road_id = road_id
  for lane_id in lane_section_proto.lane_ids:
    lane_section_impl._lane_ids.append(lane_id.id)
  return lane_section_impl


def build_lane_lane_relation(relation_proto, this_id):
  relation_impl = RelationImpl()
  relation_impl._type = relation_proto.type
  relation_impl._this_id = this_id
  relation_impl._other_id = relation_proto.lane_lane_overlap_info.one_lane.id.id \
                  if relation_proto.lane_lane_overlap_info.another_lane.id.id == this_id \
                  else relation_proto.lane_lane_overlap_info.another_lane.id.id
  return relation_impl

def build_lane_crosswalk_relation(relation_proto, this_id):
  relation_impl = RelationImpl()
  relation_impl._type = relation_proto.type
  relation_impl._this_id = this_id
  relation_impl._other_id = relation_proto.lane_crosswalk_overlap_info.lane.id.id \
                  if relation_proto.lane_crosswalk_overlap_info.crosswalk.id.id == this_id \
                  else relation_proto.lane_crosswalk_overlap_info.crosswalk.id.id
  return relation_impl

def build_lane_stop_line_relation(relation_proto, this_id):
  relation_impl = RelationImpl()
  relation_impl._type = relation_proto.type
  relation_impl._this_id = this_id
  relation_impl._other_id = relation_proto.lane_stop_line_overlap_info.one_lane.id.id \
                  if relation_proto.lane_stop_line_overlap_info.stop_line.id.id == this_id \
                  else relation_proto.lane_stop_line_overlap_info.stop_line.id.id
  return relation_impl

def build_lane_poi_relation(relation_proto, this_id):
  relation_impl = RelationImpl()
  relation_impl._type = relation_proto.type
  relation_impl._this_id = this_id
  relation_impl._other_id = relation_proto.lane_poi_relation_info.lane.id.id \
                  if relation_proto.lane_poi_relation_info.poi.id.id == this_id \
                  else relation_proto.lane_poi_relation_info.poi.id.id
  return relation_impl

def build_lane_object_relation(relation_proto, this_id):
  relation_impl = RelationImpl()
  relation_impl._type = relation_proto.type
  relation_impl._this_id = this_id
  relation_impl._other_id = relation_proto.lane_object_overlap_info.lane.id.id \
                  if relation_proto.lane_object_overlap_info.object.id.id == this_id \
                  else relation_proto.lane_object_overlap_info.object.id.id
  return relation_impl

def build_lane_junction_relation(relation_proto, this_id):
  relation_impl = RelationImpl()
  relation_impl._type = relation_proto.type
  relation_impl._this_id = this_id
  relation_impl._other_id = relation_proto.lane_junction_overlap_info.lane.id.id \
                  if relation_proto.lane_junction_overlap_info.junction.id.id == this_id \
                  else relation_proto.lane_junction_overlap_info.junction.id.id
  return relation_impl

def build_poi_parking_space_relation(relation_proto, this_id):
  relation_impl = RelationImpl()
  relation_impl._type = relation_proto.type
  relation_impl._this_id = this_id
  relation_impl._other_id = relation_proto.poi_parking_space_relation_info.poi.id.id \
                  if relation_proto.poi_parking_space_relation_info.parking_space.id.id == this_id \
                  else relation_proto.poi_parking_space_relation_info.parking_space.id.id
  return relation_impl

def build_poi_pull_over_region_relation(relation_proto, this_id):
  relation_impl = RelationImpl()
  relation_impl._type = relation_proto.type
  relation_impl._this_id = this_id
  relation_impl._other_id = relation_proto.poi_pull_over_region_relation_info.poi.id.id \
                  if relation_proto.poi_pull_over_region_relation_info.pull_over_region.id.id == this_id \
                  else relation_proto.poi_pull_over_region_relation_info.pull_over_region.id.id
  return relation_impl

def build_signal_stop_line_relation(relation_proto, this_id):
  relation_impl = RelationImpl()
  relation_impl._type = relation_proto.type
  relation_impl._this_id = this_id
  relation_impl._other_id = relation_proto.traffic_light_overlap_info.traffic_light.id.id \
                  if relation_proto.traffic_light_overlap_info.stop_line.id.id == this_id \
                  else relation_proto.traffic_light_overlap_info.stop_line.id.id
  return relation_impl

class Builder:

  @staticmethod
  def build_lane_impl(lane_proto, lines, relations, lane_links):
    lane_impl = LaneImpl()
    line_string_data_impls = []
    lane_impl._id = lane_proto.id.id
    lane_impl._type = lane_proto.type
    lane_impl._turn_type = lane_proto.turn_type
    lane_impl._speed_info = lane_proto.speed_info
    lane_impl._junction_id = lane_proto.junction_id
    
    central_line_data = lines[lane_proto.central_line]
    for point in central_line_data.points:
      lane_impl._central_line.append(Vec2d(point.x, point.y))
    
    lane_impl._left_boundary, left_line_data_impls = \
      build_curve(lane_proto.left_lane_marking.lines, lines)
    lane_impl._right_boundary, right_line_data_impls = \
      build_curve(lane_proto.right_lane_marking.lines, lines)
    line_string_data_impls.extend(left_line_data_impls)
    line_string_data_impls.extend(right_line_data_impls)
      
    for id in lane_proto.successor_lane_ids:
      lane_impl._successor_lane_ids.append(id.id)
      
    for id in lane_proto.predecessor_lane_ids:
      lane_impl._predecessor_lane_ids.append(id.id)
      
    lane_impl._left_neighbor_forward_id = lane_proto.left_neighbor_forward_lane_id.id
    lane_impl._right_neighbor_forward_id = lane_proto.right_neighbor_forward_lane_id.id
    lane_impl._left_neighbor_forward_driving_id = lane_proto.left_neighbor_forward_driving_lane_id.id
    lane_impl._right_neighbor_forward_driving_id = lane_proto.right_neighbor_forward_driving_lane_id.id
    
    for id in lane_proto.left_neighbor_reverse_lane_ids:
      lane_impl._left_neighbor_reverse_ids.append(id.id)
      
    for id in lane_proto.right_neighbor_reverse_lane_ids:
      lane_impl._right_neighbor_reverse_ids.append(id.id)
    lane_impl._lane_priority = lane_proto.priority
    lane_impl._rank = lane_proto.rank
    lane_impl._road = lane_proto.road_id
    lane_impl._lane_section = lane_proto.lane_section_index
    lane_impl._attrbutes = build_attributes(lane_proto.attributes)
    
    lane_impl._polygon = build_polygon(lane_proto.polygon, lines)
    
    for lane_link_proto in lane_links:
      lane_link_impl = build_lane_link(lane_link_proto)
      if lane_link_impl.from_lane_id() == lane_impl._id:
        lane_impl._successor_lane_links.append(lane_link_impl)
      else:
        lane_impl._predecessor_lane_links.append(lane_link_impl)
        
    for relation_proto in relations:
      if relation_proto.type == relation_pb2.Relation.RelationType.RELATION_LANE_LANE:
        relation_impl = build_lane_lane_relation(relation_proto, lane_impl._id)
        lane_impl._lanes.append(relation_impl)
      elif relation_proto.type == relation_pb2.Relation.RelationType.RELATION_LANE_CROSSWALK:
        relation_impl = build_lane_crosswalk_relation(relation_proto, lane_impl._id)
        lane_impl._cross_walks.append(relation_impl)
      elif relation_proto.type == relation_pb2.Relation.RelationType.RELATION_LANE_STOP_LINE:
        relation_impl = build_lane_stop_line_relation(relation_proto, lane_impl._id)
        lane_impl._stop_lines.append(relation_impl)
      elif relation_proto.type == relation_pb2.Relation.RelationType.RELATION_LANE_POI:
        relation_impl = build_lane_poi_relation(relation_proto, lane_impl._id)
        lane_impl._poi.append(relation_impl)
      elif relation_proto.type == relation_pb2.Relation.RelationType.RELATION_LANE_OBJECT:
        relation_impl = build_lane_object_relation(relation_proto, lane_impl._id)
        lane_impl._objects.append(relation_impl)
      elif relation_proto.type == relation_pb2.Relation.RelationType.RELATION_LANE_JUNCTION:
        relation_impl = build_lane_junction_relation(relation_proto, lane_impl._id)
        lane_impl._junctions.append(relation_impl)
    
    return lane_impl, line_string_data_impls
    
    
  @staticmethod
  def build_road_impl(road_proto, lines):
    road_impl = RoadImpl()
    road_impl._id = road_proto.id.id
    
    lane_section_index = 0
    for lane_section_proto in road_proto.lane_sections:
      lane_section_impl = build_lane_section(lane_section_proto, road_proto.id.id, lane_section_index)
      road_impl._lane_sections.append(lane_section_impl)
      lane_section_index += 1
    
    road_impl._junction_id = road_proto.junction_id.id
    road_impl._prev_junction_id = road_proto.prev_junction_id.id
    road_impl._next_junction_id = road_proto.next_junction_id.id
    for prev_road_id in road_proto.prev_road_ids:
      road_impl._prev_road_ids.append(prev_road_id.id)
    for next_road_id in road_proto.next_road_ids:
      road_impl._next_road_ids.append(next_road_id.id)
      
    road_impl._polygon = build_polygon(road_proto.polygon, lines)
    road_impl._attributes = build_attributes(road_proto.attributes)
    road_impl._name = road_proto.name
    road_impl._type = road_proto.type
    
    return road_impl
  
  @staticmethod
  def build_junction_impl(junction_proto, lines, relations):
    junction_impl = JunctionImpl()
    junction_impl._id = junction_proto.id.id
    junction_impl._polygon = build_polygon(junction_proto.polygon, lines)
    junction_impl._name = junction_proto.name
    junction_impl._is_virtual_junction = junction_proto.is_virtual_junction
    for road_id in junction_proto.road_ids:
      junction_impl._road_ids.append(road_id.id)
    
    for relation_proto in relations:  
      if relation_proto.type == relation_pb2.Relation.RelationType.RELATION_LANE_JUNCTION:
          relation_impl = build_lane_junction_relation(relation_proto, junction_impl._id)
          junction_impl._lanes.append(relation_impl)
          
    junction_impl._attributes = build_attributes(junction_proto.attributes)
    
    return junction_impl
  
  @staticmethod
  def build_object_impl(object_proto, lines, relations):
    object_impl = ObjectImpl()
    object_impl._id = object_proto.id.id
    object_impl._type = object_proto.type
    object_impl._polygon = build_polygon(object_proto.polygon, lines)
    object_impl._height = object_proto.height
    
    for relation_proto in relations:
      if relation_proto.type == relation_pb2.Relation.RelationType.RELATION_LANE_OBJECT:
        relation_impl = build_lane_object_relation(relation_proto, object_impl._id)
        object_impl._lanes.append(relation_impl)
    return object_impl
  
  @staticmethod
  def build_crosswalk_impl(crosswalk_proto, lines, relations):
    crosswalk_impl = CrosswalkImpl()
    line_string_data_impls = []
    crosswalk_impl._id = crosswalk_proto.id.id
    crosswalk_impl._left_boundary, left_line_data_impls = \
      build_curve(crosswalk_proto.left_boundary.lines, lines)
    crosswalk_impl._right_boundary, right_line_data_impls = \
      build_curve(crosswalk_proto.right_boundary.lines, lines)
    line_string_data_impls.extend(left_line_data_impls)
    line_string_data_impls.extend(right_line_data_impls)
    crosswalk_impl._polygon = build_polygon(crosswalk_proto.polygon, lines)
    crosswalk_impl._attributes = build_attributes(crosswalk_proto.attributes)
    
    for relation_proto in relations:
      if relation_proto.type == relation_pb2.Relation.RelationType.RELATION_LANE_CROSSWALK:
        relation_impl = build_lane_crosswalk_relation(relation_proto, crosswalk_impl._id)
        crosswalk_impl._lanes.append(relation_impl)
    return crosswalk_impl, line_string_data_impls
  
  @staticmethod
  def build_parking_space_impl(parking_space_proto, lines, relations):
    parking_space_impl = ParkingSpaceImpl()
    line_string_data_impls = []
    parking_space_impl._id = parking_space_proto.id.id
    parking_space_impl._left_boundary, left_line_data_impls = \
      build_curve(parking_space_proto.left_boundary.lines, lines)
    parking_space_impl._right_boundary, right_line_data_impls = \
      build_curve(parking_space_proto.right_boundary.lines, lines)
    line_string_data_impls.extend(left_line_data_impls)
    line_string_data_impls.extend(right_line_data_impls)
    
    central_line_data = lines[parking_space_proto.central_line]
    for point in central_line_data.points:
      parking_space_impl._central_line.append(Vec2d(point.x, point.y))
    
    parking_space_impl._polygon = build_polygon(parking_space_proto.polygon, lines)
    
    for in_lane in parking_space_proto.in_lanes:
      parking_space_impl._in_lanes.append(LanePoint(in_lane.id.id, in_lane.s))
      
    for out_lane in parking_space_proto.out_lanes:
      parking_space_impl._out_lanes.append(LanePoint(out_lane.id.id, out_lane.s))
      
    for relation_proto in relations:
      if relation_proto.type == relation_pb2.Relation.RelationType.RELATION_POI_PARKING_SPACE:
          relation_impl = build_poi_parking_space_relation(relation_proto, parking_space_impl._id)
          parking_space_impl._pois.append(relation_impl)
    
    return parking_space_impl, line_string_data_impls
  
  @staticmethod
  def build_poi_impl(poi_proto, relations):
    poi_impl = PoiImpl()
    poi_impl._id = poi_proto.id.id
    poi_impl._type = poi_proto.type
    poi_impl._name = poi_proto.name
    poi_impl._coordinate = Vec2d(poi_proto.coordinate.x, poi_proto.coordinate.y)
    
    for relation_proto in relations:
      if relation_proto.type == relation_pb2.Relation.RelationType.RELATION_LANE_POI:
        relation_impl = build_lane_poi_relation(relation_proto, poi_impl._id)
        poi_impl._lanes.append(relation_impl)
      elif relation_proto.type == relation_pb2.Relation.RelationType.RELATION_POI_PARKING_SPACE:
        relation_impl = build_poi_parking_space_relation(relation_proto, poi_impl._id)
        poi_impl._parking_spaces.append(relation_impl)
      elif relation_proto.type == relation_pb2.Relation.RelationType.RELATION_POI_PULL_OVER_REGION:
        relation_impl = build_poi_pull_over_region_relation(relation_proto, poi_impl._id)
        poi_impl._pull_over_regions.append(relation_impl)
    
    return poi_impl
  
  @staticmethod
  def build_pull_over_region_impl(pull_over_region_proto, relations):
    pull_over_region_impl = PullOverRegionImpl()
    pull_over_region_impl._id = pull_over_region_proto.id.id
    pull_over_region_impl._lane_id = pull_over_region_proto.lane_id.id
    pull_over_region_impl._start_s = pull_over_region_proto.start_s
    pull_over_region_impl._end_s = pull_over_region_proto.end_s
    pull_over_region_impl._d = pull_over_region_proto.d
    
    for relation_proto in relations:
      if relation_proto.type == relation_pb2.Relation.RelationType.RELATION_POI_PULL_OVER_REGION:
        relation_impl = build_poi_pull_over_region_relation(relation_proto, pull_over_region_impl._id)
        pull_over_region_impl._pois.append(relation_impl)
    return pull_over_region_impl
  
  @staticmethod
  def build_signal_impl(signal_proto, lines, relations):
    signal_impl = SignalImpl()
    signal_impl._id = signal_proto.id.id
    signal_impl._polygon = build_polygon(signal_proto.boundary, lines)
    signal_impl._signal_type = signal_proto.signal_type
    signal_impl._combination_type = signal_proto.combination_type
    signal_impl._signal_center = Vec2d(signal_proto.coordinate.x, signal_proto.coordinate.y)
    
    for relation_proto in relations:
      if relation_proto.type == relation_pb2.Relation.RelationType.RELATION_TRAFFIC_LIGHT_STOP_LINE:
        relation_impl = build_signal_stop_line_relation(relation_proto, signal_impl._id)
        signal_impl._stop_lines.append(relation_impl)
        
    return signal_impl
  
  @staticmethod
  def build_stop_line_impl(stop_line_proto, lines, relations):
    stop_line_impl = StopLineImpl()
    line_string_data_impls = []
    stop_line_impl._id = stop_line_proto.id.id
    stop_line_impl._curve, line_string_datas = build_curve(stop_line_proto.curve, lines)
    line_string_data_impls.extend(line_string_datas)
    
    for relation_proto in relations:
      if relation_proto.type == relation_pb2.Relation.RelationType.RELATION_TRAFFIC_LIGHT_STOP_LINE:
        relation_impl = build_signal_stop_line_relation(relation_proto, stop_line_impl._id)
        stop_line_impl._signals.append(relation_impl)
    
    return stop_line_impl, line_string_data_impls