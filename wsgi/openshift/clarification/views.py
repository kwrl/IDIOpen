from django.shortcuts import render
from .forms import QuestionForm
from .models import Question
from django.contrib import messages
from openshift.helpFunctions import views as helpView
from django.shortcuts import Http404

# Create your views here.

'''
This is for clarification post a question
'''
def clarification(request):
	'''
	This view handles sending Questions/clarifications.
	In order to get access to the clarifications you need to
	be logged in, on a team, and the contest needs to have started.
	'''
    if not helpView.contest_begin(request): 
        messages.info(request, "contest has not yet begun")
        return clarificationAnswers(request)
    
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
	This view displays the answers to a question. 
	Access to this view is not restricted in any way.
    '''
    answers = helpView.get_all_answers(request)
    context = {
               'answers': answers
               }
    return render(request, 'clarificationAnswers.html', context)
