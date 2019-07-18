from Parser import *
from Struct import *
from Uefi import *
from ParserMicrocode import *
from ParserVersionFfs import *

class FirmwareVolumn(Parser):
  def __init__(self, Payload):
    Parser.__init__(self, Payload)
    self.__FirstFile = True

  def __FvHeader(self):
    Header = ParseStruct(EFI_FIRMWARE_VOLUME_HEADER, self._Payload[self._BegOffset:])
    Prefix = self._PrefixFormat(self._PrefixLevel)
    Relation = self._PrefixRelation(self._PrefixLevel)

    if self._PrefixLevel > 0:
      print (Relation)

    print ("%sEFI_FIRMWARE_VOLUME_HEADER:" % (Prefix), end='')
    print (" (Payload Offset = 0x%x)" % (self._CurOffset))
    print ("%s  FileSystemGuid  - %s" %(Prefix, self._FormatGuid(Header[16])))
    print ("%s  FvLength        - 0x%x" % (Prefix, Header[17]))
    print ("%s  Signature       - 0x%x (%s)" % (Prefix, Header[18], SIGNATURE_TO_STR(Header[18])))
    print ("%s  HeaderLength    - 0x%x" % (Prefix, Header[20]))
    print ("%s  Checksum        - 0x%x" % (Prefix, Header[21]))
    print ("%s  ExtHeaderOffset - 0x%x" % (Prefix, Header[22]))
    if Header[18] == EFI_FVH_SIGNATURE:
      self._CurOffset += StructLen(EFI_FIRMWARE_VOLUME_HEADER) + StructLen(EFI_FV_BLOCK_MAP_ENTRY)
    else:
      print ("EFI_SIGNATURE Error!!!")
      assert (False)

  def __FileHeader(self):
    Prefix = self._PrefixFormat(self._PrefixLevel)
    Relation = self._PrefixRelation(self._PrefixLevel)

    if self.__FirstFile:
      self.__FirstFile = False
      print ("%s" % (Relation))
    else:
      print ("%s" % (Prefix))

    Header = ParseStruct(EFI_FFS_FILE_HEADER, self._Payload[self._CurOffset:])
    print ("%sEFI_FFS_FILE_HEADER:" % (Prefix), end='')
    print (" (Payload Offset = 0x%x)" % (self._CurOffset))
    print ("%s  Name       - %s" % (Prefix, self._FormatGuid(Header[0])))
    print ("%s  Type       - 0x%x" % (Prefix, Header[2]))
    print ("%s  Attributes - 0x%x" % (Prefix, Header[3]))
    FileSize = Header[6] * 65536 + Header[5] * 256 + Header[4]
    print ("%s  Size       - 0x%x" % (Prefix, FileSize))
    print ("%s  State      - 0x%x" % (Prefix, Header[7]))
    print ("%s  Content    - Binary [0x%x~0x%x]" % (Prefix, self._CurOffset + StructLen(EFI_FFS_FILE_HEADER), self._CurOffset + FileSize))

    return [self._CurOffset + StructLen(EFI_FFS_FILE_HEADER), FileSize]

  def __Ffs(self):
    self.__FirstFile = True
    self._PrefixLevel += 1
    Index = 1
    while self._CurOffset + StructLen(EFI_FFS_FILE_HEADER) < len(self._Payload):
      #
      # Info = [Pos, Size]
      #
      Info = self.__FileHeader()
      self._CurOffset += Info[1]
      if Index == 1:
        obj = VersionFfs(self._Payload)
        obj.SetCurOffset(Info[0])
        obj.SetBegOffset(Info[0])
        obj.SetPrefixLevel(self._PrefixLevel+1)
        obj.Dump()
      elif Index == 2:
        pass
      elif Index == 3:
        obj = Microcode(self._Payload)
        obj.SetCurOffset(Info[0])
        obj.SetBegOffset(Info[0])
        obj.SetPrefixLevel(self._PrefixLevel+1)
        obj.DumpAll()
      else:
        assert(False)
      Index += 1
    self._PrefixLevel -= 1

  def IsValidFv(self):
    Header = ParseStruct(EFI_FIRMWARE_VOLUME_HEADER, self._Payload[self._BegOffset:])
    if Header[18] == EFI_FVH_SIGNATURE:
      return True
    else:
      return False

  def Dump(self):
    self._CurOffset += 4
    self._BegOffset += 4
    self.__FvHeader()
    self.__Ffs()