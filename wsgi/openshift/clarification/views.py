from django.shortcuts import render
from .forms import MessageForm
from .models import Message
from django.contrib import messages
from helpFunctions import views as helpView
from django.shortcuts import Http404

import pdb
# Create your views here.

def clarification(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        
        if not form.is_valid():
            messages.warning(request, "Something went wrong. Did you fill out all fields?")
        
        else: #e.g the form is valid
            '''
            Gets the data 
            '''
            subject = form.cleaned_data['subject'].strip()
            body    = form.cleaned_data['body'].strip()

            '''
            Inserts into the database
            '''
            Message.objects.create(subject=subject,
                                   body=body,
                                   sender=helpView.get_team(request),
                                   contest = helpView.get_current_contest(request)
                                   )
            
            messages.info(request, "You question has been submitted")
            
    else:
        form = MessageForm()
    
    context = {
               'clarification_form':form
               }
     
    return render(request, 'clarification.html', context)
    


def clarificationAnswers(request):
    # Raise 404 if contest hasn't begun or has ended, and if user is not member of team
    if not helpView.contest_begin(request) or not helpView.is_member_of_team(request):
        raise Http404
    
    answers = helpView.get_all_answers(request)
    print answers
    context = {
               'answers': answers
               }
    
    
    return render(request, 'clarificationAnswers.html', context)
