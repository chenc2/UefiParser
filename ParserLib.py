from UefiStruct import *
from TypeFv     import *
from TypeCap    import *
from TypeuCode  import *

Prefix    = ["|", "| |", "|   |", "|     |", "|       |"]
Relation  = ["|", "|\ ", "|  \ ", "|    \ ", "|      \ "]

def FormatGuid(GuidList):
  GuidString = "{"
  for index in range(len(GuidList)):
    GuidString = GuidString + str(hex(GuidList[index])) + ", "
    if index == 2:
      GuidString = GuidString + "{"
  return GuidString[:-2] + "}}"

class ParserLib:
  def __init__(self, Payload):
    self._Payload      = Payload

    self._BegOffset    = 0
    self._CurOffset    = 0

    self._PrefixLevel  = 0

  def SetBegOffset(self, Offset):
    self._BegOffset = Offset

  def GetBegOffset(self):
    return self._BegOffset

  def GetCurOffset(self):
    return self._CurOffset

  def SetPrefixLevel(self, Level):
    self._PrefixLevel = Level

  def _PrefixFormat(self, Level):
    if Level == 0:
      return "|"
    else:
      return "|" + " " + " " * (Level - 1) * 2 + "|"

  def _PrefixRelation(self, Level):
    if Level == 0:
      return "|"
    else:
      return "|" + " " * (Level - 1) * 2 + "\ "

  def _FormatGuid(self, GuidList):
    GuidString = "{"
    for index in range(len(GuidList)):
      GuidString = GuidString + str(hex(GuidList[index])) + ", "
      if index == 2:
        GuidString = GuidString + "{"
    return GuidString[:-2] + "}}"