from UefiStruct import *
from TypeFv     import *
from TypeCap    import *
from TypeuCode  import *

class ParserLib:
  def __init__(self, Payload):
    self._Payload      = Payload

    self._BegOffset    = 0
    self._CurOffset    = 0

    self._PrefixLevel  = 0
    self._MostDepthLv  = 0

  def SetBegOffset(self, Offset):
    self._BegOffset = Offset

  def GetBegOffset(self):
    return self._BegOffset

  def GetCurOffset(self):
    return self._CurOffset

  def SetPrefixLevel(self, Level):
    self._PrefixLevel = Level

  def GetPrefixLevel(self):
    return self._PrefixLevel

  def GetMostDepthLv(self):
    return self._MostDepthLv

  def _UpPrefixLv(self):
    self._PrefixLevel += 1
    if self._PrefixLevel > self._MostDepthLv:
      self._MostDepthLv = self._PrefixLevel

  def PrefixFormat(self):
    if self._PrefixLevel == 0:
      return "|"
    else:
      return "|" + " " + " " * (self._PrefixLevel - 1) * 2 + "|"

  def PrefixRelation(self):
    if self._PrefixLevel == 0:
      return "|"
    else:
      return "|" + " " * (self._PrefixLevel - 1) * 2 + "\ "

  def _FormatGuid(self, GuidList):
    GuidString = "{"
    for index in range(len(GuidList)):
      GuidString = GuidString + str(hex(GuidList[index])) + ", "
      if index == 2:
        GuidString = GuidString + "{"
    return GuidString[:-2] + "}}"