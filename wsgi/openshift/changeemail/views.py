from django.shortcuts import render
from django.views.generic.base import TemplateView

from .models import ChangeEmail;


class ChangeEmailView(TemplateView):
    def get(self, request,  *args, **kwargs):
        instance = ChangeEmail.objects.get_instance(kwargs['activation_key']);
        instance.updateUser();
        instance.delete();

        return render(request);
# EOF
