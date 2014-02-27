from django.shortcuts import render

from openshift.article.models import Article
from openshift.contest.models import Contest
# Create your views here.
'''
Shows all articles for a contest
TODO: Add support for published date
'''
def index(request):
    # Get the current site url
    url = request.path.split('/')[1]
    # Get the articles with foreignkey to the given contest
    article_list = Article.objects.all().filter(contest__url = url)
    context = {'article_list': article_list,
               }
    return render(request, 'article/article_list.html', context)

'''
Shows the view for a single article
TODO: Add support for published date
'''
def detail(request, article_id):
    article = Article.objects.get(id=article_id)
    context = {'article': article,
               }
    return render(request, 'article/article.html', context)
