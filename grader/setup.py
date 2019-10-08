#!/usr/bin/env python3

"""
Generates some user specific values and saves them in config.yaml
"""
import yaml

_USERNAMES = ["Camisa", "Evan", "Fisher", "Jared", "Josh", "Jude", "Kaitlynne", "Logan", "Nicholas", "Parichit", "Sub", "Teresa", "Greg", "Ye", "Yuchen"]
_CLONES = ["ssh", "https"]

def setup():
    f = "config.yaml"
    with open(f, "w+") as c:
        data = yaml.safe_load(c) or {} #handle case where file doesn't exist/ have data


    while data.get("username", "") not in _USERNAMES:
        data["username"] = getChoice(_USERNAMES, "Enter the number corresponding to your name: ")

    while data.get("clonetype", "") not in _CLONES:
        data["clonetype"] = getChoice(_CLONES, "Choose the number corresponding to the clone method you prefer (if you don't have ssh keys setup already, you probably want 'https'): ")

    with open(f, 'w') as c:
        yaml.dump(data, c)
    print("------------")
    print("All set up. Now run 'getRepos.py' to start grading")

def getChoice(xList, inputString):
    for i, name in enumerate(xList):
        print("{}. {}".format(i, name))
    index = input(inputString)
    if not index.isdigit():
        return ""
    index = int(index)

    if 0 <= index < len(xList):
        return xList[index]
    return ""


if __name__=="__main__":
    setup()
