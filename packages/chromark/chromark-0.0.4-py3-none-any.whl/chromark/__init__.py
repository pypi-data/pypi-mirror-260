import sys

from chromark.main import read


def cli():
    bookmark_location = sys.argv[1]

    all_attrs = ["folders", "url", "datetime", "title", "netloc"]
    limited_attrs = [opt[2:] for opt in sys.argv if opt[2:] in all_attrs]

    for entry in read(bookmark_location):
        print(entry.to_json(*limited_attrs))
