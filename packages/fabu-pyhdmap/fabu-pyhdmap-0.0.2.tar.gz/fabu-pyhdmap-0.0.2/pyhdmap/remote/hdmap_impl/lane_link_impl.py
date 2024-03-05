class LaneLinkImpl:
  def __init__(self) -> None:
    self._from_lane_id = 0
    self._from_s = 0.0
    self._to_lane_id = 0
    self._to_s = 0.0
    
  def from_lane_id(self):
    return self._from_lane_id
  
  def from_s(self):
    return self._from_s
  
  def to_lane_id(self):
    return self._to_lane_id
  
  def to_s(self):
    return self._to_s