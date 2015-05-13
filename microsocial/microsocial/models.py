# coding=utf-8
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager, BaseUserManager
from django.core.mail import send_mail
from django.db import models
from  django.utils.translation import ugettext as _


class UserManager(BaseUserManager):
    def _create_user(self, email,first_name, password, is_staff, is_superuser,  second_name, sex, birth_date, locations, work, about_self, interests, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, is_staff=is_staff, is_active=True, is_superuser =is_superuser,
                          second_name=second_name, sex=sex,
                          birth_date=birth_date, locations=locations,
                          work=work, about_self=about_self,
                          interests=interests, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, first_name, password=None, **extra_fields):
        return self._create_user(email, first_name, password, False, False,
                                 **extra_fields)
    def create_superuser(self, email, first_name, password=None, **extra_fields):
        return self._create_user(email, first_name, password, True, True,
                                 **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    SEX_MALE = 0
    SEX_FEMALE = 1
    SEX_DEFAULT = 2
    SEX_CHOICES = (
        (SEX_MALE, u'чоловіча'),
        (SEX_FEMALE, u'жіноча'),
        (SEX_DEFAULT, u'------'),
    )

    email = models.EmailField(unique=True, verbose_name=u"Email")
    first_name = models.CharField(verbose_name=u"Ім'я", max_length='30')
    second_name = models.CharField(verbose_name=u"Фамілія", blank=True, max_length='40')
    sex = models.SmallIntegerField(verbose_name=u"Стать", choices=SEX_CHOICES, blank=True, default=2)
    birth_date = models.DateField(verbose_name=u"Дата народження", blank=True)
    locations = models.CharField(verbose_name=u"Місто", blank=True, max_length='20')
    work = models.CharField(verbose_name=u"Місце роботи", blank=True, max_length='20')
    about_self = models.CharField(verbose_name=u"Про себе", blank=True, max_length='500')
    interests = models.CharField(verbose_name=u"Інтереси", blank=True, max_length='250')

    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=False,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ('first_name','second_name','sex','birth_date','locations','work','about_self','interests',)

    objects = UserManager()

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.second_name)

    def get_short_name(self):
        return "{}".format(self.first_name)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)
