#!/usr/bin/python3
import sys
import nethunter

if '-v' in sys.argv:
    nethunter.start(useverbose=True)
else:
    nethunter.start()