from django.contrib import admin
from .models import MessageAnswer, Message
# Register your models here.

class AnswerInline(admin.TabularInline):
    model = MessageAnswer
    # Don't show any extra MessageAnswer's on default
    extra = 0

class MessageAdmin(admin.ModelAdmin):
    inlines = (AnswerInline,)
    list_display = ('subject', 'sender', 'sent_at', 'answared_by', 'answared_at')
    list_filter = ('sent_at',)
    date_hierarchy = 'sent_at'
    search_fields = ('sender',)
    ordering = ('-sent_at',)
    

admin.site.register(Message, MessageAdmin)



