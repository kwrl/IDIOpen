from django.http import Http404
from django.shortcuts import render
from django.views.generic.base import TemplateView

from .models import ChangeEmail

class ChangeEmailView(TemplateView):
    """ Render the site that a user can activate a new email address
    """
    def get(self, request,  *args, **kwargs):
        """ Default is that the activation key is passed in the URL as HTTP GET
        """
        url = request.path.split('/')[1] # To get the contest
        user = request.user
        # Note: verifying both that the user and activation key is correct.
        # That way, you can't activate emails for other users
        instance = ChangeEmail.objects.get_instance(user, 
                                                    kwargs['activation_key'])
        context = {
                    'contest': url
            }

        # Not a valid activation key!
        if not instance:
            context['msg'] = "No such activation key, or you are not logged in" \
                             " with the right account before updating emails."
            return render(request, 'changeemail/change_complete.html', context)

        instance.updateUser() # See ChangeEmail()
        instance.delete() # The activation key is deleted and no longer valid

        context['msg'] = "Your email is now changed to %s" % \
                          (instance.new_email)

        return render(request, 'changeemail/change_complete.html', context)
# EOF
