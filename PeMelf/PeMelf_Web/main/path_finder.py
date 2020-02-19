#!/usr/bin/env python3

import subprocess
import os


def find_path(file):

    command = "find"
    directory = "."
    flag = "-iname"
    args = [command, directory, flag, file]
    process = subprocess.run(args, stdout=subprocess.PIPE)
    path = process.stdout.decode().strip("\n")
    return path
