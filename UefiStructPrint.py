def GuidToString(GuidList):
  GuidString = "{"
  for index in range(len(GuidList)):
    GuidString = GuidString + str(hex(GuidList[index])) + ", "
    if index == 2:
      GuidString = GuidString + "{"
  return GuidString[:-2] + "}}"

def PrintEfiCapsuleHeader(Header):
  print ("     CapsuleGuid :",GuidToString(Header[0]))
  print ("      HeaderSize :",hex(Header[1]))
  print ("           Flags :",hex(Header[2]))
  print ("CapsuleImageSize :",hex(Header[3]))
  print ("")

def PrintEfiFirmwareManagementCapuleHeader(Header):
  print ("             Version :",Header[0])
  print ("EmbeddedDriverCount  :",Header[1])
  print ("    PayloadItemCount :",Header[2])
  print ("")