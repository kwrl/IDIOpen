from django.shortcuts import render, get_object_or_404;

import datetime;

from contest.models import Contest;
from article.models import Article


import ipdb;

def index(request, contestURL):
    contest =  get_object_or_404( 
                    Contest.objects.exclude(
                        publish_date__gt=datetime.datetime.now()) \
                    .filter(
                        url=contestURL));

    article_list = Article.objects.all().filter(contest__url = contest.url) \
                                        .order_by("-created_at")
    context = {'article_list' : article_list, }    

    return render(request, 'contest/index.html', context)

