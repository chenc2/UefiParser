UINT8   = "UINT8"
UINT16  = "UINT16"
UINT32  = "UINT32"
UINT64  = "UINT64"

INT8    = "INT8"
INT16   = "INT16"
INT32   = "INT32"
INT64   = "INT64"

BOOLEAN = "BOOLEAN"

CHAR8   = "CHAR8"
CHAR16  = "CHAR16"

PADDING = "PADDING"

UEFI_TYPE_MAPPING = {
  UINT8   : "B",
  UINT16  : "H",
  UINT32  : "I",
  UINT64  : "Q",

  INT8    : "b",
  INT16   : "h",
  INT32   : "i",
  INT64   : "q",

  BOOLEAN : "?",

  CHAR8   : "c",
  CHAR16  : "H",

  PADDING : "x"
}

EFI_GUID = [UINT32, UINT16, UINT16, UINT8, UINT8, UINT8, UINT8, UINT8, UINT8, UINT8, UINT8]

def EFI_SIGNATURE_16(A,B):
  return A | (B << 8)

def EFI_SIGNATURE_32(A,B,C,D):
  return EFI_SIGNATURE_16(A,B) | (EFI_SIGNATURE_16(C,D) << 16)

def EFI_SIGNATURE_64(A,B,C,D,E,F,G,H):
  return EFI_SIGNATURE_32(A,B,C,D)  | (EFI_SIGNATURE_32(E,F,G,H) << 32)

def EFI_SIGNATURE_TO_STR(SigValue):
  str = ""
  while SigValue != 0:
    str = str + chr(SigValue & 0xFF)
    SigValue = SigValue >> 8
  return str