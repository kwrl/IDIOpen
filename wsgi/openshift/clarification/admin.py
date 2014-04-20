from django.contrib import admin
from .models import QuestionAnswer, Question
# Register your models here.

class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ('subject', 'answered_by', 'answered_at', 'question', )
    fields = ('subject', 'body', 'contest', 'question', )
    
    def save_model(self, request, obj, form, change):
        import ipdb; ipdb.set_trace()
        if getattr(obj, 'answered_by', None) is None:
            obj.answered_by = request.user
        obj.save()
        
class AnswerInline(admin.TabularInline):
    model = QuestionAnswer
    # Don't show any extra MessageAnswer's on default
    extra = 0
    fields = ('subject', 'body', 'answered_by',)
    readonly_fields = ('answered_by',)
    
        
class QuestionAdmin(admin.ModelAdmin):
    inlines = (AnswerInline,)
    list_display = ('subject', 'sender', 'sent_at', 'answered',)
    list_filter = ('sent_at',)
    date_hierarchy = 'sent_at'
    ordering = ('-sent_at', '-answered')
    fields = ('subject', 'body', 'sender', 'contest', 'answered',)
    readonly_fields = ('subject', 'body', 'sender', 'contest',)
    
    def has_add_permission(self, request):
        return False
    
    # Set answered_by and contest fields for the MessageAnswers before saving them
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.answered_by = request.user
            instance.contest = instance.question.contest
            instance.save()
        formset.save_m2m()
    
    # Set Message.answered = True, when saving.     
    def save_model(self, request, obj, form, change):
        # Check if 'answered' field has been set manually
        if 'answered' in form.changed_data: 
            obj.save()
        # Set answered to True, if not specified by the admin
        else:
            obj.answered = True
        obj.save()
        
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionAnswer, QuestionAnswerAdmin)