#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import Tk
import inspect
import os
import tkSimpleDialog
import sys
import re


def pwd():
    dir = os.getcwd()
    return dir.replace("\\", "/")


def cd():
    path = sys.argv[0]
    dir = os.path.dirname(path + "/..")
    return dir.replace("\\", "/") + "/.."


DEFAULT_NAMESPACE = 'Model\Tables'
BASE_MODEL_DIR = pwd() + "/app/services/model/"


def check_project_root():
    directory = cd() + "/app/config/"
    if not os.path.exists(directory):
        print >> sys.stderr, "not a nette project"
        sys.exit(1)


def to_camelcase(s):
    return re.sub(r'(?!^)_([a-zA-Z])', lambda m: m.group(1).upper(), s)


def to_namespace(s):
    parts = s.split("/")
    corrected = []
    for i, part in enumerate(parts):
        if len(part) > 0:
            corrected.append(to_camelcase(part.capitalize()))
    return "\\".join(corrected)


def get_class_from_namespace(namespace):
    parts = namespace.split("\\")
    return parts[-1]


def get_prefix_from_namespace(namespace):
    parts = namespace.split("\\")
    return "\\".join(parts[:-1])


def write(input_filename, output_filename, name):
    with open(input_filename, "r") as myfile:
        data = transform(myfile.read(), name)
    with open(output_filename, "w") as myfile:
        myfile.write(data)


def transform(data, name):
    namespace = to_namespace(name)
    classname = get_class_from_namespace(to_namespace(name))
    prefix = get_prefix_from_namespace(namespace)
    if prefix != "":
        prefix = "\\" + prefix
    data = data.replace("{#NAME}", classname)
    data = data.replace("{#DEFAULT_NAMESPACE}", DEFAULT_NAMESPACE)
    data = data.replace("{#PREFIX}", prefix)
    return data


if __name__ == "__main__":
    check_project_root()
    root = Tk()
    root.withdraw()

    name = tkSimpleDialog.askstring('Novy model', 'Zadejte nazev modelu.\nformat: [prefix/]nazev')

    if name is None or len(name) == 0:
        sys.exit()

    namespace = to_namespace(name)
    classname = get_class_from_namespace(to_namespace(name))
    nprefix = pprefix = get_prefix_from_namespace(namespace)
    if nprefix != "":
        pprefix += "/"
        nprefix += "\\"

    output_filename_prefix = BASE_MODEL_DIR + pprefix + classname + "/" + classname

    directory = os.path.dirname(output_filename_prefix)
    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        print >> sys.stderr, "directory '%s' already exists" % directory
        sys.exit(1)

    write(cd() + "/templates/Entity.php", output_filename_prefix + ".php", name)
    write(cd() + "/templates/Repository.php", output_filename_prefix + "Repository.php", name)
    with open("./app/config/config.model.neon", "a") as myfile:
        myfile.write("\n    - " + DEFAULT_NAMESPACE + "\\" + nprefix + classname + "Repository")







