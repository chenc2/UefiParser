from ParserLib import *

class FirmwareVolumn:
  def __init__(self, Payload):
    self.__Payload = Payload
    self.__IsConintue = False
    self.__FirstFile = True
    self.__Offset = 0
    self.__OutLvl = 0
  
  def __FvHeader(self):
    if self.__IsConintue:
      self.__IsConintue = False
      print ("%s" % (Relation[self.__OutLvl]))
  
    Header = ParseStruct(EFI_FIRMWARE_VOLUME_HEADER, self.__Payload[self.__Offset:])
    print ("%sEFI_FIRMWARE_VOLUME_HEADER:" % (Prefix[self.__OutLvl]), end='')
    print (" (Payload Offset = 0x%x)" % (self.__Offset))
    print ("%s  FileSystemGuid  - %s" %(Prefix[self.__OutLvl], FormatGuid(Header[16])))
    print ("%s  FvLength        - 0x%x" % (Prefix[self.__OutLvl], Header[17]))
    print ("%s  Signature       - 0x%x (%s)" % (Prefix[self.__OutLvl], Header[18], EFI_SIGNATURE_TO_STR(Header[18])))
    print ("%s  HeaderLength    - 0x%x" % (Prefix[self.__OutLvl], Header[20]))
    print ("%s  Checksum        - 0x%x" % (Prefix[self.__OutLvl], Header[21]))
    print ("%s  ExtHeaderOffset - 0x%x" % (Prefix[self.__OutLvl], Header[22]))
    if Header[18] == EFI_FVH_SIGNATURE:
      self.__Offset += StructLen(EFI_FIRMWARE_VOLUME_HEADER) + StructLen(EFI_FV_BLOCK_MAP_ENTRY)
    else:
      assert (False)
  
  def __FileHeader(self):
    if self.__FirstFile:
      self.__FirstFile = False
      print ("%s" % (Relation[self.__OutLvl]))
    else:
      print ("%s" % (Prefix[self.__OutLvl]))
    
    Header = ParseStruct(EFI_FFS_FILE_HEADER, self.__Payload[self.__Offset:])
    print ("%sEFI_FFS_FILE_HEADER:" % (Prefix[self.__OutLvl]), end='')
    print (" (Payload Offset = 0x%x)" % (self.__Offset))
    print ("%s  Name       - %s" % (Prefix[self.__OutLvl], FormatGuid(Header[0])))
    print ("%s  Type       - 0x%x" % (Prefix[self.__OutLvl], Header[2]))
    print ("%s  Attributes - 0x%x" % (Prefix[self.__OutLvl], Header[3]))
    FileSize = Header[6] * 65536 + Header[5] * 256 + Header[4]
    print ("%s  Size       - 0x%x" % (Prefix[self.__OutLvl], FileSize))
    print ("%s  State      - 0x%x" % (Prefix[self.__OutLvl], Header[7]))
    print ("%s  Content    - Binary [0x%x~0x%x]" % (Prefix[self.__OutLvl], self.__Offset + StructLen(EFI_FFS_FILE_HEADER), self.__Offset + FileSize))
    self.__Offset += FileSize
  
  def __Ffs(self):
    self.__FirstFile = True
    self.__OutLvl += 1
    while self.__Offset + StructLen(EFI_FFS_FILE_HEADER) < len(self.__Payload):
      self.__FileHeader()
  
  def SetIsContinue(self, Continue):
    self.__IsConintue = Continue
  
  def SetOffset(self, Offset):
    self.__Offset = Offset
  
  def SetOutputLevel(self, Level):
    self.__OutLvl = Level
    
  def Dump(self):
    self.__FvHeader()
    self.__Ffs()