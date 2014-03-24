
from django import template

register = template.Library()

@register.filter
def commalist(objects):
    l = len(objects);
    if l==1:
        return u"%s" % objects[0]
    else:
        return ", ".join(unicode(obj) for obj in objects[:l-1]) \
                + " and " + unicode(objects[l-1])

# EOF
