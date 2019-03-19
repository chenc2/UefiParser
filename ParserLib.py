import os

from UefiStruct import *
from TypeFv import *
from TypeCap import *
from TypeuCode import *

Prefix    = ["|", "| |", "|   |", "|     |", "|       |"]
Relation  = ["|", "|\ ", "|  \ ", "|    \ ", "|      \ "]

def FormatGuid(GuidList):
  GuidString = "{"
  for index in range(len(GuidList)):
    GuidString = GuidString + str(hex(GuidList[index])) + ", "
    if index == 2:
      GuidString = GuidString + "{"
  return GuidString[:-2] + "}}"