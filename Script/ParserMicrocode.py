from Parser import *
from Struct import *
from Uefi import *

class Microcode(Parser):
  def __init__(self, Payload):
    Parser.__init__(self, Payload)
    self.__IsFirstOutput = True

  def __Sum32(self, Len):
    if Len%4 != 0:
      return -1
    Sum32 = 0
    for Offset in range(0, Len, 4):
      Sum32 += ParseBaseType(UINT32, self._Payload[self._CurOffset + Offset : self._CurOffset + Offset + 4])
      if Sum32 > 4294967295:
        Sum32 -= 4294967296
    return Sum32

  def __IsHeaderValid(self):
    if len(self._Payload[self._CurOffset:]) < 48:
      return False

    Header = ParseStruct(CPU_MICROCODE_HEADER, self._Payload[self._CurOffset:])

    if Header[0] != 1:
      return False

    if Header[5] != 1:
      return False

    if Header[8] % 4 != 0 and len(self._Payload[self._CurOffset:]) < Header[8]:
      return False

    if self.__Sum32(Header[8]) != 0:
      return False

    if Header[7] != 0 and Header[8] < 48:
      return False

    if Header[7] % 4 != 0:
      return False

    return True

  def __MainHeader(self):
    Header    = ParseStruct(CPU_MICROCODE_HEADER, self._Payload[self._CurOffset:])
    Prefix    = self._PrefixFormat(self._PrefixLevel)
    Relation  = self._PrefixRelation(self._PrefixLevel)

    if self.__IsFirstOutput:
      self.__IsFirstOutput = False
      if self._PrefixLevel > 0:
        print (Relation)
    else:
      print ("%s" % (Prefix))

    print ("%sMicrocode Header:" % (Prefix), end = "")
    print (" (Payload Offset = 0x%x)" % (self._CurOffset))
    print ("%s  HeaderVersion      - 0x%x" % (Prefix, Header[0]))
    print ("%s  UpdateRevision     - 0x%x" % (Prefix, Header[1]))
    print ("%s  ProcessorSignature - 0x%x" % (Prefix, Header[3]))
    print ("%s  Checksum           - 0x%x" % (Prefix, Header[4]))
    print ("%s  LoaderRevision     - 0x%x" % (Prefix, Header[5]))
    print ("%s  ProcessorFlags     - 0x%x" % (Prefix, Header[6]))
    print ("%s  DataSize           - 0x%x" % (Prefix, Header[7]))
    print ("%s  TotalSize          - 0x%x" % (Prefix, Header[8]))
    self._CurOffset += StructLen(CPU_MICROCODE_HEADER)
    self._CurOffset += Header[7]

    if 48 + Header[7] == Header[8]:
      return False
    else:
      return True

  def __ExtendedTableEntry(self, Index):
    self._PrefixLevel += 1
    Prefix    = self._PrefixFormat(self._PrefixLevel)
    Relation  = self._PrefixRelation(self._PrefixLevel)

    if Index == 0:
      print ("%s" % (Relation))
    else:
      print ("%s" % (Prefix))

    Table = ParseStruct(CPU_MICROCODE_EXTENDED_TABLE, self._Payload[self._CurOffset:])
    print ("%sMicrocode Extended Table:"    % (Prefix), end = "")
    print (" (Payload Offset = 0x%x)"       % (self._CurOffset))
    print ("%s  ProcessorSignature - 0x%x"  % (Prefix, Table[0]))
    print ("%s  ProcessorFlags     - 0x%x"  % (Prefix, Table[1]))
    print ("%s  Checksum           - 0x%x"  % (Prefix, Table[2]))
    self._CurOffset += StructLen(CPU_MICROCODE_EXTENDED_TABLE)

    self._PrefixLevel -= 1

  def __Extended(self):
    self._PrefixLevel += 1
    Prefix    = self._PrefixFormat(self._PrefixLevel)
    Relation  = self._PrefixRelation(self._PrefixLevel)

    Header = ParseStruct(CPU_MICROCODE_EXTENDED_TABLE_HEADER, self._Payload[self._CurOffset:])

    print ("%s" % (Relation))
    print ("%sMicrocode Extended Table Header:" % (Prefix), end = "")
    print (" (Payload Offset = 0x%x)"           % (self._CurOffset))
    print ("%s  ExtendedSignatureCount - 0x%x"  % (Prefix, Header[0]))
    print ("%s  ExtendedChecksum       - 0x%x"  % (Prefix, Header[1]))

    self._CurOffset += StructLen(CPU_MICROCODE_EXTENDED_TABLE_HEADER)

    for index in range(Header[0]):
      self.__ExtendedTableEntry(index)

    self._PrefixLevel -= 1

  def __Mircrocode(self):
    if not self.__IsHeaderValid():
      return False

    if self.__MainHeader():
      self.__Extended()
    return True

  def SetFirstOutput(self, First):
    self.__IsFirstOutput = First

  def DumpOne(self):
    self._CurOffset = self._BegOffset
    self.__Mircrocode()

  def DumpAll(self):
    self._CurOffset = self._BegOffset
    while self._CurOffset < len(self._Payload):
      if not self.__Mircrocode():
        self._CurOffset += 1024