from os import walk

import sys
from random import randint


ALL_SUBS = [(path, lol, file) for path, lol, file in walk("./subfiles")][0][2]
FILETYPES = [".java", ".cpp", "c"]
FILES_PREFIX = "./subfiles/"
def get_files(extension, fileList=ALL_SUBS):

    return [open(FILES_PREFIX + filename, 'r') for filename in ALL_SUBS \
                                        if extension in filename]

JAVA_FILES = get_files("java", ALL_SUBS)
C_FILES = get_files(".java")
CPP_FILES = get_files(".java")
files = JAVA_FILES
print files

print files


