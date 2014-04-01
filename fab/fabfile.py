#/usr/bin/python
# -*- encoding:utf-8
# pylint:disable=E0602
""" File to deploy and launch init script
"""


from fabric.api import run, env, put
from fabric.contrib.files import append

env.user = 'andesil'
env.hosts = ['localhost']
env.keys = ['~/.ssh/id_rsa']

F = open("./passfile.py", mode='r')
env.password = F.read().split('\n')[0]

def test_file():
    rsa_key = open("/home/andesil/.ssh/id_rsa.pub", mode='r')
    append("~/test", rsa_key.read(), use_sudo = False, shell=False)

