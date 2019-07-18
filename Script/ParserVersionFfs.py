from Parser import *
from Struct import *
from Uefi import *

class VersionFfs(Parser):
  def __init__(self, Payload):
    Parser.__init__(self, Payload)

  def Dump(self):
    Prefix = self._PrefixFormat(self._PrefixLevel)
    Relation = self._PrefixRelation(self._PrefixLevel)

    Data = self._Payload[self._BegOffset:]
    VersionFfs = ParseStruct(INTEL_MICROCODE_VERSION_FFS_DATA, Data)
    string = Data[8:8+Data[8:].find(b'\x00\x00')].replace(b'\x00',b'').decode()
    print ("%s" % (Relation))
    print ("%sVersion.Ffs: (Payload Offset = 0x%x)" % (Prefix, self._BegOffset))
    print ("%s  fw-version     - 0x%x" % (Prefix, int(VersionFfs[0])))
    print ("%s  lsv            - 0x%x" % (Prefix, int(VersionFfs[1])))
    print ("%s  version-string - \"%s\"" % (Prefix, string))