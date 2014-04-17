from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=200,
                             help_text = "Title of the Article, will be in a header 1 html tag")
    created_at = models.DateTimeField(auto_now_add=True)
    contest = models.ForeignKey('contest.Contest',
                                help_text = "The contest this article should be published in")
    text = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null = True, blank = True, editable = False)
# I don't use User as a foreignkey here, so an article isn't directly linked to an User model
    #author = models.CharField(max_length=200, null = True, blank = True, editable = False)
    visible_article_list = models.BooleanField(default=True, help_text = 
                           'If this is set the article will appear in the article list. (/article/list/)')
    url = models.CharField(null = True, blank=True, max_length=200, unique=True,
                           help_text = 'Set the url to access this page. Do only set if you want the article to be visible outside of the front page (exluding article/list). If set, the article can be view on: \'/pages/[url]/\'. Make sure you first have created a url you can put the article. You can do this in links. Create a /pages/[url] there first' )
    
    is_urgent = models.BooleanField(default = False,
                                    help_text = 'If set, this article will be at the top.\
                                    Please remark that if you mark as is urgent, it will come before other articles. \
                                    ')
    
    
    def __unicode__(self):      #Default return string
        return self.title
    
