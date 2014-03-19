from django.shortcuts import render
from django.views.generic.base import TemplateView

from .models import ChangeEmail;


class ChangeEmailView(TemplateView):
    def get(self, request,  *args, **kwargs):
        '''
        TODO: Swap email
        '''
        
        #activated_user = self.activate(request, *args, **kwargs)
        #activated_user = ChangeEmail(request.user, "penis").activate_email(*args);
        activated_user = ChangeEmail.objects.get_instance(kwargs['activation_key']);
        activated_user.new_email = "poop";
        activated_user.save();

        return render(request);
        
    def activate(self, request, activation_key):
        """
        Given an an activation key, look up and activate the user
        account corresponding to that key (if possible).

        After successful activation, the signal
        ``registration.signals.user_activated`` will be sent, with the
        newly activated ``User`` as the keyword argument ``user`` and
        the class of this backend as the sender.
        """
        
        return activated_user
        
# EOF
