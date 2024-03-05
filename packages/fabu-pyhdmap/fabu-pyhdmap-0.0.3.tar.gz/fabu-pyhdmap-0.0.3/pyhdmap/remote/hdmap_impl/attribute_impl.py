class AttributesImpl:
  def __init__(self) -> None:
    self._attributes:dict[str, str] = {}
    
  def attributes(self):
    return self._attributes
  
  def SetAttribute(self, key, value):
    self._attributes[str(key)] = str(value)
    return
  
  def GetAttribute(self, key):
    if key not in self._attributes.keys():
      return None
    return self._attributes[key]