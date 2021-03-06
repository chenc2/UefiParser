#
# Build up data structure relationship between C and Python
#

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

TYPE_MAPPING = {
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