# coding=utf-8
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager, BaseUserManager
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.core.signing import Signer
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from django.utils import timezone


class UserManager(BaseUserManager):
    def _create_user(self, email, first_name, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, is_staff=is_staff,
                          is_active=True, is_superuser=is_superuser,
                          last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, first_name, password=None, **extra_fields):
        return self._create_user(email, first_name, password, False, False, **extra_fields)

    def create_superuser(self, email, first_name, password=None, **extra_fields):
        return self._create_user(email, first_name, password, True, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    SEX_MALE = 0
    SEX_FEMALE = 1
    SEX_DEFAULT = 2
    SEX_CHOICES = (
        (SEX_MALE, _('чоловіча')),
        (SEX_FEMALE, _('жіноча')),
        (SEX_DEFAULT, _('---------')),
    )

    email = models.EmailField(_('email'), unique=True)
    first_name = models.CharField(_('name'), max_length='30')

    confirmed_registration = models.BooleanField(_('confirmed registration'), default=True)
    last_name = models.CharField(_('last_name'), blank=True, max_length='40')
    sex = models.SmallIntegerField(_('sex'), choices=SEX_CHOICES, blank=True, default=2)
    birth_date = models.DateField(_('birth date'), null=True, blank=True)
    city = models.CharField(_('city'), blank=True, max_length='20')
    work = models.CharField(_('work'), blank=True, max_length='20')
    about_self = models.CharField(_('about self'), blank=True, max_length='500')
    interests = models.CharField(_('interests'), blank=True, max_length='250')
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=False,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name']

    objects = UserManager()

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_short_name(self):
        return "{}".format(self.first_name)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def send_registration_email(self):
        url = 'http://{}{}'.format(
            Site.objects.get_current().domain,
            reverse('confirm_registration', kwargs={'token': Signer(salt='registration_confirm').sign(self.pk)})
        )
        self.email_user(
            ugettext('Confirm registration on Microsocial'),
            ugettext('For confirmation please visit: {}'.format(url)),
        )
