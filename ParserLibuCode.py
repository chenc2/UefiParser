from ParserLib import *

class Microcode:
  def __init__(self, Payload):
    self.__Payload = Payload
    self.__FirstuCode = False
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

  def __Sum32(self, Data, Len):
    if Len % 4 != 0:
      assert (False)
    Sum32 = 0
    for Offset in range(0,Len,4):
      Sum32 += ParseBaseType(UINT32, Data[Offset:Offset+4])
      if Sum32 > 4294967295:
        Sum32 -= 4294967296
    return Sum32

  def __IsMicrocodeValid(self, Data):
    if len(Data) < 48:
      return False

    Header = ParseStruct(CPU_MICROCODE_HEADER, Data)

    if Header[0] != 1:
      return False

    if Header[5] != 1:
      return False

    if Header[8] % 4 != 0 and len(Data) < Header[8]:
      return False

    if self.__Sum32(Data, int(Header[8])) != 0:
      return False

    if Header[7] != 0 and Header[8] < 48:
      return False

    if Header[7] % 4 != 0:
      return False

    return True

  def __ParseMircrocode(self, Offset):
    if not self.__IsMicrocodeValid(self.__Payload[Offset:]):
      return None

    #
    # Main Header
    #
    self.__ParseMainHeader(Offset)

    Header = ParseStruct(CPU_MICROCODE_HEADER, self.__Payload[Offset:])
    #
    # No more data for Extended part.
    #
    if 48 + Header[7] == Header[8]:
      return
    else:
      Offset += StructLen(CPU_MICROCODE_HEADER) + Header[7]

    #
    # Extended Table Header
    #
    Count = self.__ParseExtendedTableHeader(Offset)
    Offset += StructLen(CPU_MICROCODE_EXTENDED_TABLE_HEADER)

    #
    # Extended Table Entry
    #
    self.__ParseExtendedTableEntry(Offset, Count)

  def __ParseMainHeader(self, Offset):
    if self.__FirstuCode:
      self.__FirstuCode = False
    else:
      print ("%s" % (self.__Relation["L1"]))

    Header = ParseStruct(CPU_MICROCODE_HEADER, self.__Payload[Offset:])
    print ("%sMicrocode Header:" % (self.__Prefix["L1"]), end = "")
    print (" (Payload Offset = 0x%x)" % (Offset))
    print ("%s  HeaderVersion      - 0x%x" % (self.__Prefix["L1"], Header[0]))
    print ("%s  UpdateRevision     - 0x%x" % (self.__Prefix["L1"], Header[1]))
    print ("%s  ProcessorSignature - 0x%x" % (self.__Prefix["L1"], Header[3]))
    print ("%s  Checksum           - 0x%x" % (self.__Prefix["L1"], Header[4]))
    print ("%s  LoaderRevision     - 0x%x" % (self.__Prefix["L1"], Header[5]))
    print ("%s  ProcessorFlags     - 0x%x" % (self.__Prefix["L1"], Header[6]))
    print ("%s  DataSize           - 0x%x" % (self.__Prefix["L1"], Header[7]))
    print ("%s  TotalSize          - 0x%x" % (self.__Prefix["L1"], Header[8]))

  def __ParseExtendedTableHeader(self, Offset):
    print ("%s" % (self.__Relation["L2"]))
    Header = ParseStruct(CPU_MICROCODE_EXTENDED_TABLE_HEADER, self.__Payload[Offset:])
    print ("%sMicrocode Extended Table Header:" % (self.__Prefix["L2"]), end = "")
    print (" (Payload Offset = 0x%x)" % (Offset))
    print ("%s  ExtendedSignatureCount - 0x%x" % (self.__Prefix["L2"], Header[0]))
    print ("%s  ExtendedChecksum       - 0x%x" % (self.__Prefix["L2"], Header[1]))
    return Header[0]

  def __ParseExtendedTableEntry(self, Offset, Count):
    print ("%s" % (self.__Relation["L3"]))
    for index in range(Count):
      if index > 0:
        print ("%s" % (self.__Prefix["L3"]))
      Table = ParseStruct(CPU_MICROCODE_EXTENDED_TABLE, self.__Payload[Offset:])
      print ("%sMicrocode Extended Table:" % (self.__Prefix["L3"]), end = "")
      print (" (Payload Offset = 0x%x)" % (Offset))
      print ("%s  ProcessorSignature - 0x%x" % (self.__Prefix["L3"], Table[0]))
      print ("%s  ProcessorFlags     - 0x%x" % (self.__Prefix["L3"], Table[1]))
      print ("%s  Checksum           - 0x%x" % (self.__Prefix["L3"], Table[2]))
      Offset = Offset + StructLen(CPU_MICROCODE_EXTENDED_TABLE)

  def Dump(self):
    Offset = 0
    self.__FirstuCode = True
    while Offset < len(self.__Payload):
      Ret = self.__ParseMircrocode(Offset)
      if Ret == None:
        Offset += 1024
      else:
        Offset += Ret