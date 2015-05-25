from django.contrib import messages
from django.contrib.auth.views import login, logout
from django.core.signing import Signer, BadSignature
from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView, RedirectView
from auths.forms import RegistrationForm
from microsocial import settings
from users.models import User


def login_view(request):
    if request.user.is_authenticated():
        return redirect('main')
    response = login(request, 'auths/login.html')
    if request.user.is_authenticated():
        if 'remember_me' not in request.POST:
            request.session.set_expiry(0)
    return response


def logout_view(request):
    return logout(request, next_page='login')


class RegistrationView(TemplateView):
    template_name = 'auths/registration.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('main')
        self.form = RegistrationForm(request.POST or None)
        return super(RegistrationView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RegistrationView, self).get_context_data(**kwargs)
        context['form'] = self.form
        if 'registered_user_id' in self.request.session:
            context['registered_user'] = User.objects.get(pk=self.request.session.pop('registered_user_id'))
        return context

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            user = self.form.save()
            user.send_registration_email()
            request.session['registered_user_id'] = user.pk
            return redirect(request.path)
        return self.get(request, *args, **kwargs)


class RegistrationConfirm(RedirectView):
    url = reverse_lazy(settings.LOGIN_URL)
    permanent = False

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            raise Http404
        try:
            user_id = Signer(salt='registration-confirm').unsign(kwargs['token'])
        except BadSignature:
            raise Http404
        user = User.objects.get(pk=user_id)
        if user.confirmed_registration:
            raise Http404
        user.confirmed_registration = True
        user.save(update_fields=('confirmed_registration',))
        messages.success(request, _('Successfully confirmed your registration. Can enter'))
        return super(RegistrationConfirm, self).dispatch(request, *args, **kwargs)


class PasswordRecovery(TemplateView):
    template_name = "auths/password_recovery.html"