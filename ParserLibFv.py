from ParserLib import *

class FirmwareVolumn:
  def __init__(self, Payload):
    self.__Payload = Payload
    self.__FirstFile = True
    self.__Offset = 0
    self.__Prefix = {
      "L1":"|",
      "L2":"| |",
      "L3":"|   |",
    }
    self.__Relation = {
      "L1":"|",
      "L2":"|\ ",
      "L3":"|  \ ",
    }
  
  def __FvHeader(self):
    Header = ParseStruct(EFI_FIRMWARE_VOLUME_HEADER, self.__Payload[self.__Offset:])
    print ("%sEFI_FIRMWARE_VOLUME_HEADER:" % (self.__Prefix["L1"]), end='')
    print (" (Payload Offset = 0x%x)" % (self.__Offset))
    print ("%s  FileSystemGuid  - %s" %(self.__Prefix["L1"], FormatGuid(Header[16])))
    print ("%s  FvLength        - 0x%x" % (self.__Prefix["L1"], Header[17]))
    print ("%s  Signature       - 0x%x (%s)" % (self.__Prefix["L1"], Header[18], EFI_SIGNATURE_TO_STR(Header[18])))
    print ("%s  HeaderLength    - 0x%x" % (self.__Prefix["L1"], Header[20]))
    print ("%s  Checksum        - 0x%x" % (self.__Prefix["L1"], Header[21]))
    print ("%s  ExtHeaderOffset - 0x%x" % (self.__Prefix["L1"], Header[22]))
    
    if Header[18] == EFI_FVH_SIGNATURE:
      self.__Offset += StructLen(EFI_FIRMWARE_VOLUME_HEADER) + StructLen(EFI_FV_BLOCK_MAP_ENTRY)
    else:
      assert (False)
  
  def __FileHeader(self):
    if self.__FirstFile:
      self.__FirstFile = False
      print ("%s" % (self.__Relation["L2"]))
    else:
      print ("%s" % (self.__Prefix["L2"]))
    
    Header = ParseStruct(EFI_FFS_FILE_HEADER, self.__Payload[self.__Offset:])
    print ("%sEFI_FFS_FILE_HEADER:" % (self.__Prefix["L2"]), end='')
    print (" (Payload Offset = 0x%x)" % (self.__Offset))
    print ("%s  Name       - %s" % (self.__Prefix["L2"], FormatGuid(Header[0])))
    print ("%s  Type       - 0x%x" % (self.__Prefix["L2"], Header[2]))
    print ("%s  Attributes - 0x%x" % (self.__Prefix["L2"], Header[3]))
    FileSize = Header[6] * 65536 + Header[5] * 256 + Header[4]
    print ("%s  Size       - 0x%x" % (self.__Prefix["L2"], FileSize))
    print ("%s  State      - 0x%x" % (self.__Prefix["L2"], Header[7]))
    print ("%s  Content    - Binary (Payload Offset = 0x%x)" % (self.__Prefix["L2"], self.__Offset + StructLen(EFI_FFS_FILE_HEADER)))
    self.__Offset += FileSize
  
  def __Ffs(self):
    self.__FirstFile = True
    while self.__Offset + StructLen(EFI_FFS_FILE_HEADER) < len(self.__Payload):
      self.__FileHeader()  
  
  def SetOffset(self, Offset):
    self.__Offset = Offset
    
  def Dump(self):
    self.__FvHeader()
    self.__Ffs()