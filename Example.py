import os
import sys

from ParserLibCapsule import *
from ParserLibuCode import *

if __name__ == "__main__":
  fd = open("uCode.cap", "rb")
  data = fd.read()
  fd.close()

  #
  # Dump Capsule Header
  #
  obj = Capsule(data)
  obj.Dump()

  #
  # Dump Capsule Body
  #
  for Addr in obj.GetPayloadAddrList():
    print ("")
    uCode = Microcode(data[Addr:])
    uCode.Dump()