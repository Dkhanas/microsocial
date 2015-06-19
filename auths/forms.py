# coding=utf-8
from django import forms
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.core import validators
from django.utils.translation import ugettext_lazy as _, ugettext
from users.models import User
from microsocial.forms import BootstrapFormMixin


class RegistrationForm(forms.ModelForm, BootstrapFormMixin):
    password1 = forms.CharField(label=_(u'пароль'), min_length=6, max_length=40, widget=forms.PasswordInput)
    password2 = forms.CharField(label=_(u'повтор паролю'), min_length=6, max_length=40, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'email')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        BootstrapFormMixin.__init__(self)

    def clean(self):
        data = super(RegistrationForm, self).clean()
        if 'password1' not in self.errors and 'password2' not in self.errors:
            if data['password1'] != data['password2']:
                self.add_error('password1', _('Passwords do not match'))

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('User with that email already exist.'))
        return email

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.confirmed_registration = False
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm, BootstrapFormMixin):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        BootstrapFormMixin.__init__(self)

    def clean(self):
        has_error = False
        try:
            super(LoginForm, self).clean()
        except forms.ValidationError:
            has_error = True
        if has_error or self.errors or (self.user_cache and not self.user_cache.confirmed_registration):
            self._errors.clear()
            raise forms.ValidationError(ugettext(u'Incorrect email or password'))


class PasswordRecoveryForm(forms.Form, BootstrapFormMixin):
    email = forms.EmailField(label=(u'email'))

    def __init__(self, *args, **kwargs):
        super(PasswordRecoveryForm, self).__init__(*args, **kwargs)
        BootstrapFormMixin.__init__(self)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            self._user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError(ugettext(u'User does not exist'))
        return email

    def get_user(self):
        return self._user


class NewPasswordForm(SetPasswordForm, BootstrapFormMixin):
    def __init__(self, *args, **kwargs):
        super(NewPasswordForm, self).__init__(*args, **kwargs)
        BootstrapFormMixin.__init__(self)
        for field_name in ('new_password1', 'new_password2'):
            self.fields[field_name].validators.extend([validators.MinLengthValidator(6),
                                                      validators.MaxLengthValidator(40)])

