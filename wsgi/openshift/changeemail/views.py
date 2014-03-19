from django.shortcuts import render
from django.views.generic.base import TemplateView

from .models import ChangeEmail;


class ChangeEmailView(TemplateView):
    def get(self, request,  *args, **kwargs):
        '''
        TODO: Swap email
        '''
        
        activated_user = self.activate(request, *args, **kwargs)
        if(activated_user):
            pass
        
    def activate(self, request, activation_key):
        """
        Given an an activation key, look up and activate the user
        account corresponding to that key (if possible).

        After successful activation, the signal
        ``registration.signals.user_activated`` will be sent, with the
        newly activated ``User`` as the keyword argument ``user`` and
        the class of this backend as the sender.
        """
        
        activated_user = self.activate_new_email(request ,activation_key)
        #if activated_user:
            #signals.user_activated.send(sender=self.__class__,
                                        #user=activated_user,
                                        #request=request)
        return activated_user

    def activate_new_email(self, request, activation_key):
        #j = ChangeEmail(None, None);
        #e.activate_email(activation_key)
        user = ChangeEmail(request.user, "penis").activate_email(activation_key);
        #if activated_user:
            #signals.user_activated.send(sender=self.__class__,
                                        #user=activated_user,
                                        #request=request);
        #return activated_user;
    
    