from django.contrib import admin
from openshift.article.models import Article
from django_summernote.admin import SummernoteModelAdmin


# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/openshift/js/tinymce_setup.js',
        ]
    
admin.site.register(Article, ArticleAdmin)