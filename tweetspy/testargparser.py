"""Argument parser test script to see how things work.

Not for user use.  Just for debugging and exploring functionality.

"""
import sys

args = sys.argv
print(args)

for a in args:
    print(a, type(a))