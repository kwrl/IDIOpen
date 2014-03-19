from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import Http404;

from .models import ChangeEmail;


class ChangeEmailView(TemplateView):
    def get(self, request,  *args, **kwargs):
        url = request.path.split('/')[1] # To get the contest

        instance = ChangeEmail.objects.get_instance(kwargs['activation_key']);
        if not instance:
            raise Http404; # Could we render a message saying invalid id?

        instance.updateUser(); # See ChangeEmail()
        instance.delete();

        return render(request, 'changeemail/change_complete.html', {'contest':url});
# EOF
