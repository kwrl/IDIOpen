#/usr/bin/python
# -*- encoding:utf-8

from fabric.api import *

import logging

if __name__ == "__main__":
    logging.basicConfig(filename="test.log", level=logging.INFO)

    f = open("./passfile.py", mode='r')
    password = f.read().split('\n')[0]

    env.user = 'andesil'
    env.hosts = ['localhost']

# EOF
