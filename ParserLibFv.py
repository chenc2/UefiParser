from ParserLib import *

class FirmwareVolumn(ParserLib):
  def __init__(self, Payload):
    ParserLib.__init__(self, Payload)
    self.__IsFirstFv  = True
    self.__IsFirstFfs = True
    self.__EndOfFv    = 0
    self.__FileOffsetList = []

  def __FvHeader(self):
    Prefix = self.PrefixFormat()
    Header = ParseStruct(EFI_FIRMWARE_VOLUME_HEADER, self._Payload[self._CurOffset:])

    if self.__IsFirstFv:
      self.__IsFirstFv = False
    else:
      print ("%s" % (Prefix))

    print ("%sEFI_FIRMWARE_VOLUME_HEADER:" % (Prefix), end='')
    print (" (Payload Offset = 0x%x)"         % (self._CurOffset))
    print ("%s  FileSystemGuid  - %s"         % (Prefix, self._FormatGuid(Header[16])))
    print ("%s  FvLength        - 0x%x"       % (Prefix, Header[17]))
    print ("%s  Signature       - 0x%x (%s)"  % (Prefix, Header[18], EFI_SIGNATURE_TO_STR(Header[18])))
    print ("%s  HeaderLength    - 0x%x"       % (Prefix, Header[20]))
    print ("%s  Checksum        - 0x%x"       % (Prefix, Header[21]))
    print ("%s  ExtHeaderOffset - 0x%x"       % (Prefix, Header[22]))
    if Header[18] == EFI_FVH_SIGNATURE:
      self._CurOffset += StructLen(EFI_FIRMWARE_VOLUME_HEADER) + StructLen(EFI_FV_BLOCK_MAP_ENTRY)
    else:
      assert (False)

    self.__EndOfFv = self._BegOffset + Header[17]

  def __FileHeader(self):
    Prefix    = self.PrefixFormat()
    Relation  = self.PrefixRelation()

    Header = ParseStruct(EFI_FFS_FILE_HEADER, self._Payload[self._CurOffset:])

    if self.__IsFirstFfs:
      self.__IsFirstFfs = False
      print ("%s" % (Relation))
    else:
      print ("%s" % (Prefix))

    print ("%sEFI_FFS_FILE_HEADER:" % (Prefix), end='')
    print (" (Payload Offset = 0x%x)" % (self._CurOffset))
    print ("%s  Name       - %s" % (Prefix, self._FormatGuid(Header[0])))
    print ("%s  Type       - 0x%x" % (Prefix, Header[2]))
    print ("%s  Attributes - 0x%x" % (Prefix, Header[3]))
    FileSize = Header[6] * 65536 + Header[5] * 256 + Header[4]
    print ("%s  Size       - 0x%x" % (Prefix, FileSize))
    print ("%s  State      - 0x%x" % (Prefix, Header[7]))
    print ("%s  Content    - Binary [0x%x~0x%x]" % (Prefix, self._CurOffset + StructLen(EFI_FFS_FILE_HEADER), self._CurOffset + FileSize))
    self.__FileOffsetList.append(self._CurOffset + StructLen(EFI_FFS_FILE_HEADER))
    self._CurOffset += FileSize

  def __Ffs(self):
    self._PrefixLevel += 1
    self.__IsFirstFfs = True
    while self._CurOffset + StructLen(EFI_FFS_FILE_HEADER) < self.__EndOfFv:
      self.__FileHeader()
    self._PrefixLevel -= 1

  def SetFirstFv(self, First):
    self.__IsFirstFv = First

  def GetFileOffsetList(self):
    return self.__FileOffsetList

  def DumpOne(self):
    self._CurOffset = self._BegOffset
    self.__FvHeader()
    self.__Ffs()