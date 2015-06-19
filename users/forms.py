# coding=utf-8
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.core import validators
from django.utils.translation import ugettext as _
from microsocial.forms import BootstrapFormMixin
from users.models import User, UserWallPost


class SettingsForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = User
        fields = ('avatar', 'first_name', 'last_name', 'sex', 'birth_date', 'city', 'job', 'about_me', 'interests',)

    def __init__(self, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        BootstrapFormMixin.__init__(self)
        self.fields['birth_date'].widget.attrs['placeholder'] = _(u'Enter birth date in format YYYY-MM-DD')


class UserPasswordChangeForm(PasswordChangeForm, BootstrapFormMixin):
    def __init__(self, *args, **kwargs):
        super(UserPasswordChangeForm, self).__init__(*args, **kwargs)
        BootstrapFormMixin.__init__(self)
        for field_name in ('old_password', 'new_password1', 'new_password2'):
            self.fields[field_name] = self.fields.pop(field_name)
            if field_name != 'old_password':
                self.fields[field_name].validators.extend([validators.MinLengthValidator(6),
                                                           validators.MaxLengthValidator(40)])


class UserEmailChangeForm(forms.Form, BootstrapFormMixin):
    new_email = forms.EmailField(max_length=75, label=_(u'New email'))
    password = forms.CharField(label=_(u'Password'), widget=forms.PasswordInput())

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UserEmailChangeForm, self).__init__(*args, **kwargs)
        BootstrapFormMixin.__init__(self)

    def clean_new_email(self):
        new_email = self.cleaned_data['new_email'].strip()
        if User.objects.filter(email=new_email).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError(_(u'User with this email already exist'))
        return new_email

    def clean_password(self):
        password = self.cleaned_data['password']
        if not self.user.check_password(password):
            raise forms.ValidationError(_(u'Incorrect password.'))
        return password

    def save(self, commit=True):
        self.user.email = self.cleaned_data['new_email']
        if commit:
            self.user.save()
        return self.user


class UserWallPostForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = UserWallPost
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': _(u'write on the wall...')})
        }

    def __init__(self, *args, **kwargs):
        super(UserWallPostForm, self).__init__(*args, **kwargs)
        BootstrapFormMixin.__init__(self)

    def clean_content(self):
        return self.cleaned_data['content'].strip()


class SearchForm(forms.Form, BootstrapFormMixin):
    name = forms.CharField(label=_(u'Імя Фамілія'), required=False)
    sex = forms.TypedChoiceField(label=_(u'Стать'), required=False,
                                 choices=((0, _(u'Усі')),) + User.SEX_CHOICES[1:],
                                 coerce=lambda val: int(val))
    by_from = forms.IntegerField(label=_(u'Рік народження від'), required=False,
                                 widget=forms.NumberInput(attrs={'placeholder': _(u'від')}))
    to_from = forms.IntegerField(label=_(u'Рік народження до'), required=False,
                                 widget=forms.NumberInput(attrs={'placeholder': _(u'до')}))
    city = forms.CharField(label=_(u'Місто'), required=False)
    job = forms.CharField(label=_(u'Робота'), required=False)
    about_me = forms.CharField(label=_(u'Про мене'), required=False)
    interests = forms.CharField(label=_(u'Інтереси'), required=False)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        BootstrapFormMixin.__init__(self)

    def get_values_list(self, field_name):
        val = self.cleaned_data.get(field_name)
        if isinstance(val, basestring):
            val = val.strip().split()
        return val or []
