from django.contrib import admin
from openshift.article.models import Article


# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    
    def save_model(self, request, obj, form, change):
        obj.author = request.user()
        obj.save()
    
    class Media:
        # Include javascript for wysiwyg editor
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/openshift/js/tinymce_setup.js',
        ]
    
        


# Add article to admin page
admin.site.register(Article, ArticleAdmin)