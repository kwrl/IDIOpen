from django.contib.auth.decorators import login_required;
from userregistration import models as reg_models;
#from usermanagent import models as man_models;
from contest import models as con_models;
from django.shortcuts import render;

# Create your views here.
@login_required
def user_dashboard(request):
    invites = con_models.Invite.get(pk=request.user.id)
    return HttpResponse("Liten tiss")


@login_required
def user_edit(request):
    return HttpResponse("Enorm pikk")

