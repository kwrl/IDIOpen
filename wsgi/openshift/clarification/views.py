from django.shortcuts import render
from .forms import MessageForm

# Create your views here.

def clarification(request):
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
    else:
        form = MessageForm()
    
    context = {
               'clarification_form':form
               }
     
    return render(request, 'clarification.html', context)
    
    
    