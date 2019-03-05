import os
import sys

from UefiParser import DumpCapsule
from UefiParser import DumpMicrocode

if __name__ == "__main__":
  DumpCapsule("Red.cap")