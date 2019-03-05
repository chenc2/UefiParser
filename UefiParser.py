import os

from UefiStruct import ParseBaseType
from UefiStruct import ParseStruct
from UefiStruct import BaseTypeLen
from UefiStruct import StructLen

from UefiBaseType import UINT64

from UefiBaseType import EFI_CAPSULE_HEADER
from UefiBaseType import EFI_FIRMWARE_MANAGEMENT_CAPSULE_HEADER
from UefiBaseType import EFI_FIRMWARE_MANAGEMENT_CAPSULE_IMAGE_HEADER

from UefiBaseType import CPU_MICROCODE_HEADER
from UefiBaseType import CPU_MICROCODE_EXTENDED_TABLE_HEADER
from UefiBaseType import CPU_MICROCODE_EXTENDED_TABLE

def Read(File):
  if not os.path.isfile(File):
    assert(False)

  fd = open(File, "rb")
  data = fd.read()
  fd.close()

  return data

def GuidToString(GuidList):
  GuidString = "{"
  for index in range(len(GuidList)):
    GuidString = GuidString + str(hex(GuidList[index])) + ", "
    if index == 2:
      GuidString = GuidString + "{"
  return GuidString[:-2] + "}}"

def DumpCapsule(CapFile):
  data = Read(CapFile)
  Offset = 0

  Header = ParseStruct(EFI_CAPSULE_HEADER, data[Offset:])
  print ("")
  print ("FmpCapsule:", end='')
  print (" (Payload Offset = 0x%x)" % (Offset))
  print ("  CapsuleGuid      - %s" %(GuidToString(Header[0])))
  print ("  HeaderSize       - 0x%x" % (Header[1]))
  print ("  Flags            - 0x%x" % (Header[2]))
  print ("  CapsuleImageSize - 0x%x" % (Header[3]))
  print ("")
  Offset = Offset + Header[1]

  Header = ParseStruct(EFI_FIRMWARE_MANAGEMENT_CAPSULE_HEADER, data[Offset:])
  print ("FmpCapsule:", end='')
  print (" (Payload Offset = 0x%x)" % (Offset))
  print ("  Version             - 0x%x" % (Header[0]))
  print ("  EmbeddedDriverCount - 0x%x" % (Header[1]))
  print ("  PayloadItemCount    - 0x%x" % (Header[2]))
  Offset = Offset + StructLen(EFI_FIRMWARE_MANAGEMENT_CAPSULE_HEADER)

  for index in range(Header[1]):
    pass

  for index in range(Header[2]):
    print ("  PayloadItem[%d]      - 0x%x" % (index, ParseBaseType(UINT64, data[Offset:])))
    Offset = Offset + BaseTypeLen(UINT64)

  print ("")

  for index in range(Header[1]):
    pass

  for index in range(Header[2]):
    print ("PayloadItem[%d] ImageHeader:" % (index), end='')
    print (" (Payload Offset = 0x%x)" % (Offset))
    Header = ParseStruct(EFI_FIRMWARE_MANAGEMENT_CAPSULE_IMAGE_HEADER, data[Offset:])
    print ("  Version")
    print ("  UpdateImageTypeId      - 0x%x" % (Header[0]))
    print ("  UpdateImageIndex       - %s" % (GuidToString(Header[1])))
    print ("  UpdateImageSize        - 0x%x" % (Header[2]))
    print ("  UpdateVendorCodeSize   - 0x%x" % (Header[3]))
    if Header[0] >= 0x2:
      print ("  UpdateHardwareInstance - 0x%x" % (Header[4]))
    Offset = Offset + StructLen(EFI_FIRMWARE_MANAGEMENT_CAPSULE_IMAGE_HEADER)

def DumpMicrocode(uCodeFile):
  data = Read(uCodeFile)
  Offset = 0

  Header = ParseStruct(CPU_MICROCODE_HEADER, data[Offset:])
  print ("")
  print ("Microcode Header:", end = "")
  print (" (Payload Offset = 0x%x)" % (Offset))
  print ("  HeaderVersion      - 0x%x" % (Header[0]))
  print ("  UpdateRevision     - 0x%x" % (Header[1]))
  print ("  ProcessorSignature - 0x%x" % (Header[3]))
  print ("  Checksum           - 0x%x" % (Header[4]))
  print ("  LoaderRevision     - 0x%x" % (Header[5]))
  print ("  ProcessorFlags     - 0x%x" % (Header[6]))
  print ("  DataSize           - 0x%x" % (Header[7]))
  print ("  TotalSize          - 0x%x" % (Header[8]))
  print ("")
  Offset = Offset + StructLen(CPU_MICROCODE_HEADER) + Header[7]

  if Offset == len(data):
    return

  Header = ParseStruct(CPU_MICROCODE_EXTENDED_TABLE_HEADER, data[Offset:])
  print ("Microcode Extended Table Header:", end = "")
  print (" (Payload Offset = 0x%x)" % (Offset))
  print ("  ExtendedSignatureCount - 0x%x" % (Header[0]))
  print ("  ExtendedChecksum       - 0x%x" % (Header[1]))
  print ("")
  Offset = Offset + StructLen(CPU_MICROCODE_EXTENDED_TABLE_HEADER)

  for index in range(Header[0]):
    Table = ParseStruct(CPU_MICROCODE_EXTENDED_TABLE, data[Offset:])
    print ("Microcode Extended Table:", end = "")
    print (" (Payload Offset = 0x%x)" % (Offset))
    print ("  ProcessorSignature - 0x%x" % (Table[0]))
    print ("  ProcessorFlags     - 0x%x" % (Table[1]))
    print ("  Checksum           - 0x%x" % (Table[2]))
    print ("")
    Offset = Offset + StructLen(CPU_MICROCODE_EXTENDED_TABLE)