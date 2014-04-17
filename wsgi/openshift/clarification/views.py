from django.shortcuts import render
from .forms import MessageForm
from django.contrib import messages

# Create your views here.

def clarification(request):
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "You question has been submitted. ")
        else:
            messages.warning(request, "Form invalid. ")
    else:
        form = MessageForm()
    
    context = {
               'clarification_form':form
               }
     
    return render(request, 'clarification.html', context)
    
    
    