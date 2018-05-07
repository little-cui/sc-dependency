#!/usr/bin/env python
# coding=utf-8

import io
import json
import sys
import urlparse
from collections import OrderedDict

import os


def load_json_file(file_name):
    with open(file_name, 'rb') as ifp:
        content = json.loads(ifp.read(), object_pairs_hook=OrderedDict)
        return content


if __name__ == "__main__":
    if len(sys.argv) < 3 or not sys.argv[1] or not sys.argv[2]:
        print "Usage: python build.py <manifest file> <output script file>"
        sys.exit(1)
    fileName = sys.argv[1]
    scriptName = sys.argv[2]
    obj = load_json_file(fileName)

    tempFileName = scriptName + ".temp"
    with io.open(tempFileName, 'wb') as f:
        f.write("#!/usr/bin/env bash\n\n")
        for dep in obj.get("dependencies"):
            f.write("gvt fetch -precaire -no-recurse ")
            if dep.get("branch") != "master":
                f.write("-revision ")
                f.write(dep.get("revision"))
                f.write(" ")
            repo = urlparse.urlparse(dep.get("repository"))
            f.write(repo.netloc)
            f.write(repo.path)
            path =dep.get("path")
            if path:
                if path[0] != "/":
                    f.write("/")
                f.write(path)
            f.write("\n")
    if os.path.exists(scriptName):
        os.remove(scriptName)
    os.rename(tempFileName, scriptName)
    os.chmod(scriptName, 0700)
