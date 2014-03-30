from django.shortcuts import render

def submission_view(request):
    context = {
                   # 'article_list' : article_list, 
               }    
    return render(request, 'submission_home.html', context)

# EOF