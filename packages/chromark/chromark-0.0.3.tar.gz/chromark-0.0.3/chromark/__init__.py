import sys
from chromark.main import read

def cli():
    bookmark_location = sys.argv[1]
    for entry in read(bookmark_location):
        print(entry)