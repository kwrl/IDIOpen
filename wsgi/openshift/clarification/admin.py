from django.contrib import admin
from .models import MessageAnswer, Message
# Register your models here.

class AnswerInline(admin.TabularInline):
    model = MessageAnswer
    # Don't show any extra MessageAnswer's on default
    extra = 1
    fields = ('subject', 'body',)
        
class MessageAdmin(admin.ModelAdmin):
    inlines = (AnswerInline,)
    list_display = ('subject', 'sender', 'sent_at', 'answered')
    list_filter = ('sent_at',)
    date_hierarchy = 'sent_at'
    search_fields = ('sender',)
    
    ordering = ('-sent_at', '-answered')
    readonly_fields = ('subject', 'body', 'sender', 'contest', 'answered')
    
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.answered_by = request.user
            instance.contest = instance.message.contest
            instance.save()
        formset.save_m2m()
        
    def save_model(self, request, obj, form, change):
        if change:
            obj.answered = True
        obj.save()
        
admin.site.register(Message, MessageAdmin)
admin.site.register(MessageAnswer)