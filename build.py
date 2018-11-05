#!/usr/bin/env python3

import os, errno, subprocess

try:
    os.makedirs("build")
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

for directory in next(os.walk('.'))[1]:
    if (directory.startswith(".")) or directory == "build":
        continue
    subprocess.run([
        "pdflatex", "-output-directory=build", directory + "/" + directory + ".tex"
    ])

subprocess.run(["rm build/*.log"], shell=True)
subprocess.run(["rm build/*.aux"], shell=True)
