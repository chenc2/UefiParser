import os
import sys

from UefiStruct import ParseStruct
from UefiStruct import StructLen

from UefiBaseType import EFI_CAPSULE_HEADER
from UefiBaseType import EFI_FIRMWARE_MANAGEMENT_CAPSULE_HEADER

from UefiStructPrint import PrintEfiCapsuleHeader
from UefiStructPrint import PrintEfiFirmwareManagementCapuleHeader

if __name__ == "__main__":
  fd = open("Red.cap", "rb")
  data = fd.read()
  fd.close()
  
  Offset = 0
  
  PrintEfiCapsuleHeader(ParseStruct(EFI_CAPSULE_HEADER, data[Offset:]))
  Offset = Offset + StructLen(EFI_CAPSULE_HEADER)
  
  PrintEfiFirmwareManagementCapuleHeader(ParseStruct(EFI_FIRMWARE_MANAGEMENT_CAPSULE_HEADER, data[Offset:]))