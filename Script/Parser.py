class Parser:
  def __init__(self, Payload):
    self._Payload     = Payload
    self._BegOffset   = 0
    self._CurOffset   = 0
    self._PrefixLevel = 0
    self._ChildParse  = False
    self._CapType     = ""

  #
  # Public interface
  #
  def SetBegOffset(self, Offset):
    self._BegOffset = Offset

  def GetBegOffset(self):
    return self._BegOffset

  def SetCurOffset(self, Offset):
    self._CurOffset = Offset

  def GetCurOffset(self):
    return self._CurOffset

  def SetPrefixLevel(self, Level):
    self._PrefixLevel = Level

  def SetChildParse(self, Flag):
    self._ChildParse = Flag

  def SetCapType(self,Type):
    Type = Type.lower()
    if Type not in ["full","slot","bgup"]:
      print ("UnSupported Type:",Type)
      assert(False)
    self._CapType = Type

  #
  # Private interface
  #
  def _PrefixFormat(self, Level):
    str = "|"
    if Level > 0:
      str = str + " " + " " * (Level - 1) * 2 + "|"
    return str

  def _PrefixRelation(self, Level):
    str = "|"
    if Level > 0:
      str = str + " " * (Level - 1) * 2 + "\ "
    return str

  def _FormatGuid(self, GuidList):
    GuidString = "{"
    for index in range(len(GuidList)):
      GuidString = GuidString + str(hex(GuidList[index])) + ", "
      if index == 2:
        GuidString = GuidString + "{"
    return GuidString[:-2] + "}}"