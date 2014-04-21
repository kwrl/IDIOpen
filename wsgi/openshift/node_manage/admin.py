from django.contrib import admin

from .models import ExecutionNode

class NodeAdmin(admin.ModelAdmin):
    pass
    # list_display = ('title', 'url', 'start_date','end_date','publish_date')
    # search_fields = ('title', 'url',)
    # ordering = ('title',)


'''
Removed by: Kwrl 
'''
#admin.site.register(ExecutionNode, NodeAdmin)
# Register your models here.
