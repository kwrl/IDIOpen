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

user = 'aaa@aaa.com'
loginDict = {
'username': user,
'password': 'password',
}

submission_json = {
'compileProfile' : {'1'},
'compileProfile' : {'2'},
'compileProfile' : {'3'},
}

file_type_list = [(3, JAVA_FILES), (2, C_FILES), (1, CPP_FILES)]

#submission_json = {
#        'compileProfile': {'1'},
#        }

compiler, files = file_type_list[randint(1, 3) -1]
#print compiler, files
# random_filetype = file_type_list[randint(1, 3)]

file_upload = files[randint(0, len(files))-1]

# file_upload = random_filetype[randint(0, len(filetype[])- 1]

file_json = {
'submission' : file_upload,
}

problem = 2

print compiler
print file_upload
