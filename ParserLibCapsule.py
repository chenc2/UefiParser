from ParserLib import *

class Capsule(ParserLib):
  def __init__(self, Payload):
    ParserLib.__init__(self, Payload)
    self.__PayloadOffsetList = []
    self.__BinParserCallBack = None

  def __CapsuleHeader(self):
    Prefix = self.PrefixFormat()
    Header = ParseStruct(EFI_CAPSULE_HEADER, self._Payload[self._CurOffset:])

    self._PrintTitle("EFI_CAPSULE_HEADER", Prefix)
    print ("%s  CapsuleGuid      - %s"    % (Prefix, self._FormatGuid(Header[0])))
    print ("%s  HeaderSize       - 0x%x"  % (Prefix, Header[1]))
    print ("%s  Flags            - 0x%x"  % (Prefix, Header[2]))
    print ("%s  CapsuleImageSize - 0x%x"  % (Prefix, Header[3]))
    self._CurOffset = self._CurOffset + Header[1]

  def __ParseEfiFrimwareImageAuthentication(self):
    Prefix    = self.PrefixFormat()
    Relation  = self.PrefixRelation()

    self._PrintTitle("EFI_FIRMWARE_IMAGE_AUTHENTICATION", Prefix, Relation)
    print ("%s  MonotonicCount - 0x%x" % (Prefix, ParseBaseType(UINT64, self._Payload[self._CurOffset:])))
    print ("%s  dwLength       - 0x%x" % (Prefix, ParseBaseType(UINT32, self._Payload[self._CurOffset + BaseTypeLen(UINT64):])))

    return BaseTypeLen(UINT64) + ParseBaseType(UINT32, self._Payload[self._CurOffset + BaseTypeLen(UINT64):])

  def __ParseFmpPayloadHeader(self):
    Prefix = self.PrefixFormat()
    Header = ParseStruct(FMP_PAYLOAD_HEADER, self._Payload[self._CurOffset:])

    self._PrintTitle("FMP_PAYLOAD_HEADER", Prefix, Prefix)
    print ("%s  Signature              - 0x%x" % (Prefix, Header[0]))
    print ("%s  HeaderSize             - 0x%x" % (Prefix, Header[1]))
    print ("%s  FwVersion              - 0x%x" % (Prefix, Header[2]))
    print ("%s  LowestSupportedVersion - 0x%x" % (Prefix, Header[3]))

    return StructLen(FMP_PAYLOAD_HEADER)

  def __ParseRealBinary(self):
    Prefix = self.PrefixFormat()
    self._PrintTitle("Binary", Prefix, Prefix)

    if self.__BinParserCallBack == None:
      print ("%s  Option1, [uCode]" % (Prefix))
      print ("%s  Option2, [FvHeader + uCode] + [BgupHeader + script.bin + CertHeader + SignedData]" % (Prefix))
      print ("%s  Option3, [FvHeader + uCode]" % (Prefix))
    else:
      self.__BinParserCallBack(self._Payload, self._CurOffset, self._MostDepthLv + 1)

    return 0

  def __CapsulePayload(self, Index):
    self._UpPrefixLv()

    Prefix    = self.PrefixFormat()
    Relation  = self.PrefixRelation()
    Header    = ParseStruct(EFI_FIRMWARE_MANAGEMENT_CAPSULE_IMAGE_HEADER, self._Payload[self._CurOffset:])

    str = "PayloadItem[%d] EFI_FIRMWARE_MANAGEMENT_CAPSULE_IMAGE_HEADER" % Index
    self._PrintTitle(str, Prefix, Relation)
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
    self._UpPrefixLv()
    self._CurOffset += self.__ParseEfiFrimwareImageAuthentication()
    self._CurOffset += self.__ParseFmpPayloadHeader()
    self._CurOffset += self.__ParseRealBinary()
    self._DePrefixLv()

    self._DePrefixLv()

  def __CapsuleBody(self):
    self._UpPrefixLv()

    Prefix = self.PrefixFormat()
    Relation  = self.PrefixRelation()
    Header    = ParseStruct(EFI_FIRMWARE_MANAGEMENT_CAPSULE_HEADER, self._Payload[self._CurOffset:])

    self._PrintTitle("EFI_FIRMWARE_MANAGEMENT_CAPSULE_IMAGE_HEADER", Prefix, Relation)
    print ("%s  Version             - 0x%x"                   % (Prefix, Header[0]))
    print ("%s  EmbeddedDriverCount - 0x%x"                   % (Prefix, Header[1]))
    print ("%s  PayloadItemCount    - 0x%x"                   % (Prefix, Header[2]))

    self.__PayloadOffsetList = []
    for index in range(Header[2]):
      OffsetValue = ParseBaseType(UINT64, self._Payload[self._CurOffset + (index+1) * BaseTypeLen(UINT64):])
      print ("%s  PayloadItem[%d]      - 0x%x" % (Prefix, index, OffsetValue))
      self.__PayloadOffsetList.append(self._CurOffset + OffsetValue)

    for Offset in self.__PayloadOffsetList:
      self._CurOffset = Offset
      self.__CapsulePayload(index)

    self._DePrefixLv()

  def GetPayloadOffsetList(self):
    return self.__PayloadOffsetList

  def SetBinParserCb(self, Cb):
    self.__BinParserCallBack = Cb

  def Dump(self):
    self.__CapsuleHeader()
    self.__CapsuleBody()