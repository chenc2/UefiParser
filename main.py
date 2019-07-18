import os
import sys

sys.path.append(os.path.join(os.getcwd(),"Script"))
from ParserCapsule import *
from ParserFv import *
from ParserMicrocode import *
from ParserVersionFfs import *

def Read(File):
  fd = open(File, "rb")
  data = fd.read()
  fd.close()
  return data

def DumpCapsule(FilePath, Offset, PrintLevel = 0):
  obj = Capsule(Read(FilePath)[Offset:])
  obj.SetPrefixLevel(PrintLevel)
  obj.Dump()
  return obj

def DumpFv(FilePath, Offset, PrintLevel = 0):
  obj = FirmwareVolumn(Read(FilePath)[Offset:])
  obj.SetPrefixLevel(PrintLevel)
  obj.Dump()
  return obj

def DumpVersionFfs(FilePath, Offset, PrintLevel = 0):
  obj = VersionFfs(Read(FilePath)[Offset:])
  obj.SetPrefixLevel(PrintLevel)
  obj.Dump()
  return obj

def DumpMicrocodeArray(FilePath, Offset, PrintLevel = 0):
  obj = Microcode(Read(FilePath)[Offset:])
  obj.SetPrefixLevel(PrintLevel)
  obj.DumpAll()
  return obj

if __name__ == "__main__":
  Len = len(sys.argv)
  if Len != 5:
    print ("Usage: python",sys.argv[0],"<Capsule|Fv|VersionFfs|uCodeArray|all> <FilePath> <Offset> <Full|Slot|Bgup>")
    print ("")
    print ("   Capsule:", "Dump capsule structure")
    print ("        Fv:", "Dump Fv structure")
    print ("VersionFfs:", "Dump version information in Ffs")
    print ("uCodeArray:", "Dump Microcode patch")
    print ("  FilePath:", "Indicate the location of capsule file")
    print ("    Offset:", "Will dump information with the Offset bytes at the beginning of the file")
    print ("      Full:", "Full range mode")
    print ("      Slot:", "Slot mode")
    print ("      Bgup:", "Full range with BGUP")
    quit()

  Type = sys.argv[1].lower()
  File = sys.argv[2]
  if sys.argv[3][:2].lower() == "0x":
    Offset = int(sys.argv[3],16)
  else:
    Offset = int(sys.argv[3])
  Mode = sys.argv[4].lower()

  if Type == "capsule":
    DumpCapsule(File,Offset)
  elif Type == "fv":
    if Mode == "slot":
      print ("UnSupported Mode!")
      quit()
    DumpFv(File,Offset)
  elif Type == "versionffs":
    DumpVersionFfs(File, Offset)
  elif Type == "ucodearray":
    DumpMicrocodeArray(File,Offset)
  elif Type == "all":
    obj = Capsule(Read(File))
    obj.SetChildParse(True)
    obj.SetCapType(Mode)
    obj.Dump()
  else:
    print ("Invalid Input!")
    quit()