import json

def loadFile(fname):
    with open(fname, 'r', encoding="utf8") as fi:
        return json.load(fi)

def saveFile(fname, data):
    with open(fname, "w", encoding="utf8") as outfile:
        json.dump(data, outfile, default=str, sort_keys=True, indent=4)