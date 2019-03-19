from ParserLib import *

class Capsule:
  def __init__(self, Payload):
    self.__Payload = Payload

    self.__CapsuleHeaderOffset = 0
    self.__CapsuleBodyOffset = 0

    self.__PayloadOffsetList = []
    self.__PayloadAddressList = []

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

  def __CapsuleHeader(self):
    Header = ParseStruct(EFI_CAPSULE_HEADER, self.__Payload)
    print ("%sEFI_CAPSULE_HEADER:" % (self.__Prefix["L1"]), end='')
    print (" (Payload Offset = 0x%x)" % (self.__CapsuleHeaderOffset))
    print ("%s  CapsuleGuid      - %s" %(self.__Prefix["L1"], FormatGuid(Header[0])))
    print ("%s  HeaderSize       - 0x%x" % (self.__Prefix["L1"], Header[1]))
    print ("%s  Flags            - 0x%x" % (self.__Prefix["L1"], Header[2]))
    print ("%s  CapsuleImageSize - 0x%x" % (self.__Prefix["L1"], Header[3]))
    self.__CapsuleBodyOffset = self.__CapsuleHeaderOffset + Header[1]

  def __CapsuleBody(self):
    print ("%s" % (self.__Relation["L1"]))
    Header = ParseStruct(EFI_FIRMWARE_MANAGEMENT_CAPSULE_HEADER, self.__Payload[self.__CapsuleBodyOffset:])
    print ("%sEFI_FIRMWARE_MANAGEMENT_CAPSULE_IMAGE_HEADER:" % (self.__Prefix["L1"]), end='')
    print (" (Payload Offset = 0x%x)" % (self.__CapsuleBodyOffset))
    print ("%s  Version             - 0x%x" % (self.__Prefix["L1"], Header[0]))
    print ("%s  EmbeddedDriverCount - 0x%x" % (self.__Prefix["L1"], Header[1]))
    print ("%s  PayloadItemCount    - 0x%x" % (self.__Prefix["L1"], Header[2]))

    for index in range(Header[1]):
      pass

    for index in range(Header[2]):
      OffsetValue = ParseBaseType(UINT64, self.__Payload[self.__CapsuleBodyOffset + (index+1) * BaseTypeLen(UINT64):])
      print ("%s  PayloadItem[%d]      - 0x%x" % (self.__Prefix["L1"], index, OffsetValue))
      self.__PayloadOffsetList.append(self.__CapsuleBodyOffset + OffsetValue)

    index = 0
    for Offset in self.__PayloadOffsetList:
      print ("%s" % (self.__Relation["L2"]))
      print ("%sPayloadItem[%d] EFI_FIRMWARE_MANAGEMENT_CAPSULE_IMAGE_HEADER:" % (self.__Prefix["L2"], index), end='')
      print (" (Payload Offset = 0x%x)" % (Offset))
      self.__ParsePayload(Offset)
      index += 1

  def __ParsePayload(self, Offset):
    Header = ParseStruct(EFI_FIRMWARE_MANAGEMENT_CAPSULE_IMAGE_HEADER, self.__Payload[Offset:])
    print ("%s  Version                - 0x%x" % (self.__Prefix["L2"], Header[0]))
    print ("%s  UpdateImageTypeId      - %s" % (self.__Prefix["L2"], FormatGuid(Header[1])))
    print ("%s  UpdateImageIndex       - 0x%x" % (self.__Prefix["L2"], Header[2]))
    print ("%s  UpdateImageSize        - 0x%x" % (self.__Prefix["L2"], Header[6]))
    print ("%s  UpdateVendorCodeSize   - 0x%x" % (self.__Prefix["L2"], Header[7]))
    #
    # If the EFI_FIRMWARE_MANAGEMENT_CAPSULE_IMAGE_HEADER is version 1,
    # Header should exclude UpdateHardwareInstance field
    #
    if Header[0] >= 0x2:
      print ("%s  UpdateHardwareInstance - 0x%x" % (self.__Prefix["L2"], Header[8]))
      Offset = Offset + StructLen(EFI_FIRMWARE_MANAGEMENT_CAPSULE_IMAGE_HEADER)
    else:
      Offset = Offset + StructLen(EFI_FIRMWARE_MANAGEMENT_CAPSULE_IMAGE_HEADER) - BaseTypeLen(UINT64)

    #
    # Auth
    #
    Offset += self.__ParseEfiFrimwareImageAuthentication(Offset)

    #
    # FMP payload
    #
    Offset += self.__ParseFmpPayloadHeader(Offset)

    #
    # Real binary payload
    #
    self.__ParseRealBinary(Offset)

  def __ParseEfiFrimwareImageAuthentication(self, Offset):
    print ("%s" % (self.__Relation["L3"]))
    print ("%sEFI_FIRMWARE_IMAGE_AUTHENTICATION:" % (self.__Prefix["L3"]), end='')
    print (" (Payload Offset = 0x%x)" % (Offset))
    print ("%s  MonotonicCount - 0x%x" % (self.__Prefix["L3"], ParseBaseType(UINT64, self.__Payload[Offset:])))
    print ("%s  dwLength       - 0x%x" % (self.__Prefix["L3"], ParseBaseType(UINT32, self.__Payload[Offset + BaseTypeLen(UINT64):])))
    return BaseTypeLen(UINT64) + ParseBaseType(UINT32, self.__Payload[Offset + BaseTypeLen(UINT64):])

  def __ParseFmpPayloadHeader(self, Offset):
    Header = ParseStruct(FMP_PAYLOAD_HEADER, self.__Payload[Offset:])
    print ("%s" % (self.__Prefix["L3"]))
    print ("%sFMP_PAYLOAD_HEADER:" % (self.__Prefix["L3"]), end='')
    print (" (Payload Offset = 0x%x)" % (Offset))
    print ("%s  Signature              - 0x%x" % (self.__Prefix["L3"], Header[0]))
    print ("%s  HeaderSize             - 0x%x" % (self.__Prefix["L3"], Header[1]))
    print ("%s  FwVersion              - 0x%x" % (self.__Prefix["L3"], Header[2]))
    print ("%s  LowestSupportedVersion - 0x%x" % (self.__Prefix["L3"], Header[3]))
    return StructLen(FMP_PAYLOAD_HEADER)

  def __ParseRealBinary(self, Offset):
    print ("%s" % (self.__Prefix["L3"]))
    print ("%sBinary:" % (self.__Prefix["L3"]), end = "")
    print (" (Payload Offset = 0x%x)" % (Offset))
    print ("%s  Option1, uCode     payload" % (self.__Prefix["L3"]))
    print ("%s  Option2, uCodeBgup Payload, [FV + BgupHeader + script.bin + CertHeader + SignedData]" % (self.__Prefix["L3"]))
    print ("%s  Others" % (self.__Prefix["L3"]))
    self.__PayloadAddressList.append(Offset)

  def Dump(self):
    self.__CapsuleHeader()
    self.__CapsuleBody()

  def GetPayloadAddrList(self):
    return self.__PayloadAddressList