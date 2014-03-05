from django.shortcuts import render, get_object_or_404;
from django.utils import timezone;

from contest.models import Contest;
from article.models import Article

def index(request, contestURL):
    """ The main page for a contest
    """
    # Get the contest as pointed to by the URL
    # throw a 404 if it is not valid
    contest =  get_object_or_404( 
                    Contest.objects.exclude(
                        publish_date__gt=timezone.now()) \
                    .filter(
                        url=contestURL));

    # Get all articles for this contest, sort them
    article_list = Article.objects.all().filter(contest__url = contest.url) \
                                        .order_by("-created_at")
    context = {'article_list' : article_list, }    

    return render(request, 'contest/index.html', context)

# EOF
