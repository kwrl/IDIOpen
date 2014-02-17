from django.shortcuts import render

from openshift.article.models import Article
from openshift.contest.models import Contest
# Create your views here.

def index(request, url):
    article_list = Article.objects.all().filter(contest__url = url)
    contest = Contest.objects.get(url=url)
    context = {'article_list': article_list,
               'contest': contest,
               }
    return render(request, 'article/article_list.html', context)

def detail(request, url, article_id):
    article = Article.objects.get(id=article_id)
    context = {'article': article,
               'contest': article.contest,
               }
    return render(request, 'article/article.html', context)
