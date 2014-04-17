from django.contrib import admin
from article.models import Article


# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'contest','visible_article_list', 'url', 'is_urgent'),
            'description': "You can here create a new article. Please note that if is_urgent is set, those articles will come before all other articles"
        }),
    )
    
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