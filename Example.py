import os
import sys

from ParserLibCapsule import *
from ParserLibuCode import *
from ParserLibFv import *

def FileParser(Payload, Offset, PrefixLv):
  uCode = Microcode(Payload)
  uCode.SetBegOffset(Offset)
  uCode.SetFirstOutput(True)
  uCode.SetPrefixLevel(PrefixLv)
  uCode.DumpOne()

def CapBinParser(Payload, Offset, PrefixLv):
  Fv = FirmwareVolumn(Payload)
  Fv.SetBegOffset(Offset)
  Fv.SetFirstFv(True)
  Fv.SetPrefixLevel(PrefixLv)
  Fv.SetFileParserCb(FileParser)
  Fv.DumpOne()

if __name__ == "__main__":
  fd = open("uCodeBgup.cap", "rb")
  data = fd.read()
  fd.close()

  #
  # Dump Capsule Header
  #
  obj = Capsule(data)
  obj.SetBinParserCb(CapBinParser)
  obj.Dump()
  
  #
  # Dump Capsule Body
  #
  '''
  Fv = FirmwareVolumn(data)
  Fv.SetFirstFv(True)
  print ("")
  for Addr in obj.GetPayloadOffsetList():
    Fv.SetBegOffset(Addr)
    Fv.DumpOne()
  
  #
  # If want to dump uCodeBgup.cap or uCode.cap
  # Should parse Fv before dump uCode payload
  #
  
  #
  # Dump File
  #
  uCode = Microcode(data)
  uCode.SetFirstOutput(True)
  print ("")
  for Addr in Fv.GetFileOffsetList():
    uCode.SetBegOffset(Addr)
    uCode.DumpOne()
  '''