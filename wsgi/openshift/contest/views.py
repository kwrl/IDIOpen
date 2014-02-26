from django.shortcuts import render
from openshift.contest.models import Contest
from openshift.article.models import Article
# Create your views here.

def index(request):
    url = request.path.split('/')[1]
    article_list = Article.objects.all().filter(contest__url = url).order_by("-created_at")
    context = {'article_list' : article_list, 
               }    
    return render(request, 'contest/index.html', context)

