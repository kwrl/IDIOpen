from django.db import models

class string_with_title(str):
    def __new__(cls, value, title):
        instance = str.__new__(cls, value)
        #pylint:disable=W0212
        instance._title = title
        return instance

    def title(self):
        return self._title

    __copy__ = lambda self: self
    __deepcopy__ = lambda self, memodict: self

class judge_view(models.Model):
    class Meta:
#       app_label = string_with_title("Judge_Supervisor", "Judge_Supervisor")
        managed = True #prevent from entering the DB
