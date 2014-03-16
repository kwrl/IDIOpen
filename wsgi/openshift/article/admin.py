from django.contrib import admin
from article.models import Article


# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    
    list_display = ('title', 'created_at','author','contest','visible_article_list','url',)
    search_fields = ('title', 'text','author',)
    ordering = ('title',)
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