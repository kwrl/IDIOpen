from django.contrib import admin
from .models import Message
# Register your models here.
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender', 'sent_at', 'answared_by', 'answared_at')
    list_filter = ('sent_at',)
    date_hierarchy = 'sent_at'
    search_fields = ('sender',)
    change_form_template = 'index.html'
    
admin.site.register(Message, MessageAdmin)



