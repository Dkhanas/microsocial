from django.contrib.auth.views import login
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView


def login_view(request):
    if request.user.is_authenticated():
        return redirect('profile', user_id=request.user.pk, permanent=False)
    response = login(request, 'auths/login.html')
    if request.user.is_authenticated():
        if _(u'remember_me') not in request.POST:
            request.session.set_expiry(0)
    return response


class RegistrationView(TemplateView):
    template_name = 'auths/registration.html'


class PasswordRecoveryView(TemplateView):
    template_name = 'auths/password-recovery.html'
