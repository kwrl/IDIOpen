#pylint:disable=C0103
from __future__ import absolute_import

from .celeryapp import app

@app.task(ignore_result=True)
def add(x, y):
    return x + y

if __name__ == '__main__':
    app.start()

# EOF
