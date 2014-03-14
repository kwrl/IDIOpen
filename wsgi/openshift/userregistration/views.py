from django import forms
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse;
from django.shortcuts import redirect, render_to_response;
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.sites.models import RequestSite, Site
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from contest.models import Invite
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _

from userregistration.forms import *
from userregistration import signals

import ipdb;

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from openshift.userregistration.models import CustomUser as User

class _RequestPassingFormView(FormView):
    """
    A version of FormView which passes extra arguments to certain
    methods, notably passing the HTTP request nearly everywhere, to
    enable finer-grained processing.    
    """
    
    def get(self, request, *args, **kwargs):
        # Pass request to get_form_class and get_form for per-request
        # form control.
        form_class = self.get_form_class(request)
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        # Pass request to get_form_class and get_form for per-request
        # form control.
        form_class = self.get_form_class(request)
        form = self.get_form(form_class)
        if form.is_valid():
            # Pass request to form_valid.
            return self.form_valid(request, form)
        else:
            return self.form_invalid(form)

    def get_form_class(self, request=None):
        return super(_RequestPassingFormView, self).get_form_class()

    def get_form_kwargs(self, request=None, form_class=None):
        return super(_RequestPassingFormView, self).get_form_kwargs()

    def get_initial(self, request=None):
        return super(_RequestPassingFormView, self).get_initial()

    def get_success_url(self, request=None, user=None):
        # We need to be able to use the request and the new user when
        # constructing success_url.
        return super(_RequestPassingFormView, self).get_success_url()

    def form_valid(self, form, request=None):
        return super(_RequestPassingFormView, self).form_valid(form)

    def form_invalid(self, form, request=None):
        return super(_RequestPassingFormView, self).form_invalid(form)


class RegistrationView(_RequestPassingFormView):
    """
    Base class for user registration views.
    admin/userregistration/cadmin/userregistration/customuser/ustomuser/
    """
    disallowed_url = 'registration_disallowed'
    form_class = RegistrationForm
    http_method_names = ['get', 'post', 'head', 'options', 'trace']
    success_url = None
    template_name = 'registration/registration_form.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Check that user signup is allowed before even bothering to
        dispatch or do other processing.
        
        """
        if not self.registration_allowed(request):
            return redirect(self.disallowed_url)
        return super(RegistrationView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, request, form):
        new_user = self.register(request, **form.cleaned_data)
        #success_url = self.get_success_url(request, new_user)
        
        # success_url may be a simple string, or a tuple providing the
        # full argument set for redirect(). Attempting to unpack it
        # tells us which one it is.
        #try:
        #    to, args, kwargs = success_url
        #    return redirect(to, *args, **kwargs)
        #except ValueError:
        #    return redirect(success_url)
        url = request.path.split('/')[1]
        return HttpResponseRedirect(reverse('registration_complete', args=(url,)))

    def registration_allowed(self, request):
        """
        Override this to enable/disable user registration, either
        globally or on a per-request basis.
        
        """
        return True

    def register(self, request, **cleaned_data):
        url = request.path.split('/')[1]
        print url
        email, first_name = cleaned_data['email'], cleaned_data['first_name'] 
        last_name, password = cleaned_data['last_name'], cleaned_data['password1']
        site = RequestSite(request)
        new_user = User.objects.create_inactive_user(email, first_name, last_name, password, site, url)
        signals.user_registered.send(sender=self.__class__, user=new_user, request=request)
        return new_user
    
# TODO: This needs to return with contest url first
    def get_success_url(self, request, user):
        """
        Return the name of the URL to redirect to after successful
        user registration.
        
        """
        url = request.path.split('/')[1]
        print url
        return ('registration_complete', (), {'contest':url})
    
class ActivationView(TemplateView):
    """
    Base class for user activation views.
    
    """
    http_method_names = ['get']
    template_name = 'registration/activate.html'

    def get(self, request, *args, **kwargs):
        activated_user = self.activate(request, *args, **kwargs)
        if activated_user:
            signals.user_activated.send(sender=self.__class__,
                                        user=activated_user,
                                        request=request)
            '''
            success_url = self.get_success_url(request, activated_user)
            try:
                to, args, kwargs = success_url
                return redirect(to, *args, **kwargs)
            except ValueError:
                return redirect(success_url)
                '''
            url = request.path.split('/')[1]
            return HttpResponseRedirect(reverse('registration_activation_complete', args=(url,)))
            
        return super(ActivationView, self).get(request, *args, **kwargs)

    def activate(self, request, activation_key):
        """
        Given an an activation key, look up and activate the user
        account corresponding to that key (if possible).

        After successful activation, the signal
        ``registration.signals.user_activated`` will be sent, with the
        newly activated ``User`` as the keyword argument ``user`` and
        the class of this backend as the sender.
        
        """
        activated_user = User.objects.activate_user(activation_key)
        if activated_user:
            signals.user_activated.send(sender=self.__class__,
                                        user=activated_user,
                                        request=request)
        return activated_user
# TODO: Fix so it will redirect with contest url as root
    def get_success_url(self, request, user):
        url = request.path.split('/')[1]
        return ('registration_activation_complete', (), {'contest':url})

@login_required
def updateProfilePw(request):
    form = None;
    if request.method == 'POST':
        form = PasswordForm(data=request.POST, instance=request.user);
        if form.is_valid():
            form.save();
    else:
        form = PasswordForm(instance=request.user);
    
    return retProfile(request, UserProfile(request,
                                            pw=form));

@login_required
def updateProfileEmail(request):
    form = None;
    if request.method == 'POST':
        form = EmailForm(data=request.POST, instance=request.user);
        if form.is_valid():
            form.save();
    else:
        form = EmailForm(instance=request.user);
    
    return retProfile(request, UserProfile(request,
                                           email=form));

@login_required
def updateProfilePI(request):
    form = None;
    if request.method == 'POST':
        form = PIForm(data=request.POST, instance=request.user);
        if form.is_valid():
            form.save();
    else:
        form = PIForm(instance=request.user);
    
    return retProfile(request, UserProfile(request, pi=form));

@login_required
def user_profile(request):
    email = request.user.email
    messages = []
    if request.method == 'POST':
        form = Invites_Form(request.POST)
        submit = form.data['submit']
        id = form.data['id']
        if id.isdigit():
            try:
                try:
                    invite = Invite.objects.filter(email=email).filter(is_member=False).get(pk=id)
                except ObjectDoesNotExist:
                    messages.append({'text':'Invalid invite','error':'alert-danger'})
                    raise Exception
                
                if submit == 'accept':
                    try:
                        invite.team.members.add(User.objects.get(email=email))
                        invite.is_member = True
                    except ObjectDoesNotExist:
                        raise forms.ValidationError(_("The form did not validate"))
                    invite.save()
                    messages.append({'text':'Invite accepted','error':'alert-success'})
                    
                elif submit == 'decline':
                    invite.delete()
                    messages.append({'text':'Invite declined','error':'alert-info'})
                else:
                    messages.append({'text':'Validation failed','error':'alert-danger'})
            except:
                pass
        else:
            messages.append({'text':'Validation failed','error':'alert-danger'})
    
    email = request.user.email;
    messages = [];
    invites = Invite.objects.filter(email=email).filter(is_member = False)
    context = {'invites' : invites,
               'messages':messages
               }
    context.update(UserProfile(request).getDict());
    return render(request, 'userregistration/profile.html', context)

class UserProfile(object):
    def __init__(self, request, pw=None, pi=None, email=None):
        self.pwForm = pw or PasswordForm(instance=request.user);
        self.piForm = pi or PIForm(instance=request.user);
        self.email = email or EmailForm(instance=request.user);
        self.forms = [self.pwForm, self.piForm, self.email];
        
    def getDict(self):
        a = {};
        for form in self.forms:
            a[form.contextName] = form;
        return a;

def retProfile(request, userProfile):
    email = request.user.email;
    messages = [];
    invites = Invite.objects.filter(email=email).filter(is_member = False)
    context = {'invites' : invites,
               'messages':messages
               }

    context.update(userProfile.getDict());

    #return HttpResponse(notification_list[0].confirmed)
    return render(request, 'userregistration/profile.html', context);
    return HttpResponseRedirect(reverse('profile', args={request.path.split('/')[1]:''}));
    return redirect('user_profile', data=request, name='profile');
    return redirect('userregistration/profile.html');

# EOF
