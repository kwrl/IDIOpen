from django.shortcuts import render
from .forms import MessageForm
from django.contrib import messages

# Create your views here.

def clarification(request):
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        messages.info(request, "You question has been submitted. ")
        
    
    else:
        form = MessageForm()
    
    context = {
               'clarification_form':form
               }
     
    return render(request, 'clarification.html', context)
    
    
    