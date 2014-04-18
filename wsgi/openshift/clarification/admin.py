from django.contrib import admin
from .models import MessageAnswer, Message
# Register your models here.

class CommentInline(admin.TabularInline):
    model = MessageAnswer

class MessageAdmin(admin.ModelAdmin):
    inlines = [CommentInline,]
    list_display = ('subject', 'sender', 'sent_at')
    list_filter = ('sent_at',)
    date_hierarchy = 'sent_at'
    search_fields = ('sender',)
    ordering = ('-sent_at',)
    

admin.site.register(Message, MessageAdmin)



