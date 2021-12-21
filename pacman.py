#!/usr/bin/env python3
import fileinput
import sys
import json


def getProjects(data: dict):
    """Extract the project from the status"""
    return data["DONE"], data["DOING"], data["TODO"], data["PENDING"]


def updateData(data: dict, todo: dict):
    """Safely update data from todo"""
    output = data.copy()
    updating = todo.copy()
    for k, v in updating.items():
        output["TODO"][k] = v
        output["PENDING"].pop(k, None)
    return output


def pacmain(data: dict):
    """Main function, updates data if compilation is needed"""
    done, doing, todo, pending = getProjects(data)
    for key, project in pending.items():
        # filter pending dependencies
        # dont care about external dependencies
        pending_dependencies = [i for i in project.get("dependencies")
                                if i in pending.keys()
                                or i in doing.keys()
                                or i in todo.keys()]
        if len(pending_dependencies) == 0:
            todo[key] = project.copy()

    return updateData(data, todo)


if __name__ == '__main__':
    # Read file or stdin
    # https://stackoverflow.com/questions/1744989/read-from-file-or-stdin
    INPUT_FILE = ""
    for line in fileinput.input(sys.argv[1:]):
        INPUT_FILE += str(line)
    INPUT_DATA = json.loads(INPUT_FILE)
    OUTPUT_DATA = pacmain(INPUT_DATA)
    print(json.dumps(OUTPUT_DATA))
