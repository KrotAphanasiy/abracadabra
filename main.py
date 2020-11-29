import sys
from JsonObjectParser import JParsers
import json
import os


if __name__ == "__main__":
    JParsers: JParsers = JParsers()
    d = JParsers.find(sys.argv[1], sys.argv[2])
    with open("data_file.json", "w") as write_file:
        json.dump(d, write_file, indent=4)
    print(os.path.dirname(os.path.abspath("data_file.json") + "\\data_file.json"))