from Parser import *
from Uefi import *
from Struct import *
from ParserFv import *

class Capsule(Parser):
  def __init__(self, Payload):
    Parser.__init__(self, Payload)
    self.__BinaryOffsetList = []

  def __CapsuleHeader(self):
    Header = ParseStruct(EFI_CAPSULE_HEADER, self._Payload[self._BegOffset:])
    Prefix = self._PrefixFormat(self._PrefixLevel)

    print ("%sEFI_CAPSULE_HEADER:"        % (Prefix), end='')
    print (" (Payload Offset = 0x%x)"     % (self._BegOffset))
    print ("%s  CapsuleGuid      - %s"    % (Prefix, self._FormatGuid(Header[0])))
    print ("%s  HeaderSize       - 0x%x"  % (Prefix, Header[1]))
    print ("%s  Flags            - 0x%x"  % (Prefix, Header[2]))
    print ("%s  CapsuleImageSize - 0x%x"  % (Prefix, Header[3]))
    self._CurOffset = self._BegOffset + Header[1]

  def __ParseEfiFrimwareImageAuthentication(self):
    self._PrefixLevel += 1
    Prefix    = self._PrefixFormat(self._PrefixLevel)
    Relation  = self._PrefixRelation(self._PrefixLevel)

    print ("%s" % (Relation))
    print ("%sEFI_FIRMWARE_IMAGE_AUTHENTICATION:" % (Prefix), end='')
    print (" (Payload Offset = 0x%x)" % (self._CurOffset))
    print ("%s  MonotonicCount - 0x%x" % (Prefix, ParseBaseType(UINT64, self._Payload[self._CurOffset:])))
    print ("%s  dwLength       - 0x%x" % (Prefix, ParseBaseType(UINT32, self._Payload[self._CurOffset + BaseTypeLen(UINT64):])))

    self._PrefixLevel -= 1
    self._CurOffset += (BaseTypeLen(UINT64) + ParseBaseType(UINT32, self._Payload[self._CurOffset + BaseTypeLen(UINT64):]))

  def __ParseFmpPayloadHeader(self):
    self._PrefixLevel += 1
    Prefix    = self._PrefixFormat(self._PrefixLevel)
    Relation  = self._PrefixRelation(self._PrefixLevel)

    Header = ParseStruct(FMP_PAYLOAD_HEADER, self._Payload[self._CurOffset:])

    print ("%s" % (Prefix))
    print ("%sFMP_PAYLOAD_HEADER:" % (Prefix), end='')
    print (" (Payload Offset = 0x%x)" % (self._CurOffset))
    print ("%s  Signature              - 0x%x" % (Prefix, Header[0]))
    print ("%s  HeaderSize             - 0x%x" % (Prefix, Header[1]))
    print ("%s  FwVersion              - 0x%x" % (Prefix, Header[2]))
    print ("%s  LowestSupportedVersion - 0x%x" % (Prefix, Header[3]))

    self._PrefixLevel -= 1
    self._CurOffset += StructLen(FMP_PAYLOAD_HEADER)

  def __ParseRealBinary(self):
    self._PrefixLevel += 1
    Prefix    = self._PrefixFormat(self._PrefixLevel)
    Relation  = self._PrefixRelation(self._PrefixLevel)

    print ("%s" % (Prefix))
    print ("%sBinary:" % (Prefix), end = "")
    print (" (Payload Offset = 0x%x)" % (self._CurOffset))
    print ("%s  Full: [XDR + Fv(FvHeader + Version.ffs + Padding.ffs + uCodeArray.ffs)]" % (Prefix))
    print ("%s  Slot: [XDR + Fv(XDR + XDR + Version.ffs + XDR + uCodeArray.ffs)]" % (Prefix))
    print ("%s  Bgup: [XDR + Fv(FvHeader + Version.ffs + Padding.ffs + uCodeArray.ffs) + XDR + Bgup]" % (Prefix))

    #
    # Parse child part Automatically recursively
    #
    if self._ChildParse:
      obj = FirmwareVolumn(self._Payload)
      obj.SetBegOffset(self._CurOffset)
      obj.SetCurOffset(self._CurOffset)
      obj.SetPrefixLevel(self._PrefixLevel+1)
      obj.SetChildParse(self._ChildParse)
      obj.SetCapType(self._CapType)
      obj.Dump()

    self._PrefixLevel -= 1
    self.__BinaryOffsetList.append(self._CurOffset)

  def __CapsulePayload(self, Index):
    self._PrefixLevel += 1
    Prefix    = self._PrefixFormat(self._PrefixLevel)
    Relation  = self._PrefixRelation(self._PrefixLevel)

    Header = ParseStruct(EFI_FIRMWARE_MANAGEMENT_CAPSULE_IMAGE_HEADER, self._Payload[self._CurOffset:])

    print ("%s" % (Relation))
    print ("%sPayloadItem[%d] EFI_FIRMWARE_MANAGEMENT_CAPSULE_IMAGE_HEADER:" % (Prefix, Index), end='')
    print (" (Payload Offset = 0x%x)" % (self._CurOffset))
    print ("%s  Version                - 0x%x"  % (Prefix, Header[0]))
    print ("%s  UpdateImageTypeId      - %s"    % (Prefix, self._FormatGuid(Header[1])))
    print ("%s  UpdateImageIndex       - 0x%x"  % (Prefix, Header[2]))
    print ("%s  UpdateImageSize        - 0x%x"  % (Prefix, Header[6]))
    print ("%s  UpdateVendorCodeSize   - 0x%x"  % (Prefix, Header[7]))

    #
    # If the EFI_FIRMWARE_MANAGEMENT_CAPSULE_IMAGE_HEADER is version 1,
    # Header should exclude UpdateHardwareInstance field
    #
    if Header[0] >= 0x2:
      print ("%s  UpdateHardwareInstance - 0x%x" % (Prefix, Header[8]))
      self._CurOffset += StructLen(EFI_FIRMWARE_MANAGEMENT_CAPSULE_IMAGE_HEADER)
    else:
      self._CurOffset += StructLen(EFI_FIRMWARE_MANAGEMENT_CAPSULE_IMAGE_HEADER) - BaseTypeLen(UINT64)

    #
    # Auth, FMP, Binary
    #
    self.__ParseEfiFrimwareImageAuthentication()
    self.__ParseFmpPayloadHeader()
    self.__ParseRealBinary()

    self._PrefixLevel -= 1

  def __CapsuleBody(self):
    self._PrefixLevel += 1

    Header    = ParseStruct(EFI_FIRMWARE_MANAGEMENT_CAPSULE_HEADER, self._Payload[self._CurOffset:])
    Prefix    = self._PrefixFormat(self._PrefixLevel)
    Relation  = self._PrefixRelation(self._PrefixLevel)

    print ("%s" % (Relation))
    print ("%sEFI_FIRMWARE_MANAGEMENT_CAPSULE_IMAGE_HEADER:"  % (Prefix), end='')
    print (" (Payload Offset = 0x%x)"                         % (self._CurOffset))
    print ("%s  Version             - 0x%x"                   % (Prefix, Header[0]))
    print ("%s  EmbeddedDriverCount - 0x%x"                   % (Prefix, Header[1]))
    print ("%s  PayloadItemCount    - 0x%x"                   % (Prefix, Header[2]))

    PayloadOffsetList = []
    for index in range(Header[2]):
      OffsetValue = ParseBaseType(UINT64, self._Payload[self._CurOffset + (index+1) * BaseTypeLen(UINT64):])
      print ("%s  PayloadItem[%d]      - 0x%x" % (Prefix, index, OffsetValue))
      PayloadOffsetList.append(self._CurOffset + OffsetValue)

    for index in range(len(PayloadOffsetList)):
      self._CurOffset = PayloadOffsetList[index]
      self.__CapsulePayload(index)

    self._PrefixLevel -= 1

  def GetBinaryOffsetList(self):
    return self.__BinaryOffsetList

  def Dump(self):
    self.__CapsuleHeader()
    self.__CapsuleBody()