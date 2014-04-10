from __future__ import absolute_import
from testWork.tasks import add

from time import sleep
import ipdb


def main():
    res = add.apply_async((1, 2))
    while not res.ready():
        sleep(1)
    print res.get()



main()

