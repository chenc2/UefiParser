from struct import unpack
from struct import calcsize

from TypeBase import UEFI_TYPE_MAPPING

def BaseTypeLen(BaseType):
  return calcsize(UEFI_TYPE_MAPPING[BaseType])

def StructLen(StructType):
  Len = 0
  for Type in StructType:
    if isinstance(Type, list):
      Len = Len + StructLen(Type)
    else:
      Len = Len + BaseTypeLen(Type)
  return Len

def ParseBaseType(BaseType, Content):
  return unpack(UEFI_TYPE_MAPPING[BaseType], Content[:BaseTypeLen(BaseType)])[0]

def ParseStruct(StructType, Content):
  Result = []
  Offset = 0

  for Type in StructType:
    if isinstance(Type, list):
      Result.append(ParseStruct(Type, Content[Offset:]))
      Offset = Offset + StructLen(Type)
    else:
      Result.append(ParseBaseType(Type, Content[Offset:]))
      Offset = Offset + BaseTypeLen(Type)

  return Result