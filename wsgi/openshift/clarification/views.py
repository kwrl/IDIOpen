from django.shortcuts import render, redirect
from .forms import QuestionForm
from .models import Question
from django.contrib import messages
from openshift.helpFunctions import views as helpView
from django.shortcuts import Http404
from openshift.helpFunctions.views import get_current_contest

# Create your views here.

'''
This is for clarification post a question
'''
def clarification(request):
    
    if not helpView.contest_begin(request): 
        messages.info(request, "contest has not yet begun")
        return redirect("clarificationAnswersPage", get_current_contest(request).url)
    
    elif not request.user.is_authenticated():
        messages.info(request, "You are not logged in")
        return clarificationAnswers(request)
        
    elif not helpView.is_member_of_team(request):
        messages.info(request, "You are not on a team")
        return clarificationAnswers(request)
    
    if request.method == 'POST':
        
        form = QuestionForm(request.POST)
        
        if not form.is_valid():
            messages.warning(request, "Something went wrong. Did you fill out all fields?")

        else: #e.g the form is valid
            
            # Gets the data 
            data = {
                'sender'    :helpView.get_team(request),
                'contest'   :helpView.get_current_contest(request),
                }
            form.save(data)

            messages.info(request, "Your question has been submitted successfully")
            form = QuestionForm()
            
    else:
        form = QuestionForm()
    
    context = {
               'clarification_form':form
               }
     
    return render(request, 'clarification.html', context)
    


def clarificationAnswers(request):
    '''
    Everybody should be able to view clarifications at all time
    '''
    answers = helpView.get_all_answers(request)
    context = {
               'answers': answers
               }
    return render(request, 'clarificationAnswers.html', context)
