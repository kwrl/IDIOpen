from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import AdminTextInputWidget
from .models import Article


# Register your models here.
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        widgets = {
                  'url' : AdminTextInputWidget(attrs={'placeholder' : 'E.g The appended {url} you want = /{url}/'})
        }
        
    def clean_url(self):
        return self.cleaned_data['url'] or None


class ArticleAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'contest','visible_article_list', 'url', 'is_urgent', 'text'),
        }),
    )
    
    form = ArticleForm
    list_display = ('title', 'created_at','contest','author','visible_article_list','url', 'is_urgent')
    search_fields = ('title', 'text','author',)
    ordering = ('created_at',)
    
    # Set author, to the user/admin who created the article
    def save_model(self, request, obj, form, change):
        # Only update author if author = None
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()        
    class Media:
        # Include javascript for wysiwyg editor
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/openshift/js/tinymce_setup.js',
        ]
    
# Add article to admin pageus
admin.site.register(Article, ArticleAdmin)
