__version__ = "0.3.0"

"""
Search the file system for the path to a Julia executable or install Julia if none is found.
"""
from ._find import find, find_or_install
