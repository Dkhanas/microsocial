# coding=utf-8
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.sites.models import Site
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.signing import Signer, TimestampSigner
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from django.utils import timezone
import hashlib
from django.utils.crypto import get_random_string
import os
from django.db.models import Q
import datetime
from django.dispatch import Signal
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render
# from django.contrib.auth.decorators import login_required

# @login_required
def get_ids_from_users(*users):
    #TODO: check this
    # try:
    return [user.pk if isinstance(user, User) else int(user) for user in users]
    # except SimpleLazyObject:
    #     return redirect('news')

class UserManger(BaseUserManager):
    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(email=email, is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class UserFriendShipManager(models.Manager):
    def are_friends(self, user1, user2):
        user1_id, user2_id = get_ids_from_users(user1, user2)
        return self.filter(pk=user1_id, friends__pk=user2_id).exists()

    def add(self, user1, user2):
        user1_id, user2_id = get_ids_from_users(user1, user2)
        if user1_id == user2_id:
            raise ValueError(_(u'Неможна самого себе додати в друзі'))
        if not self.are_friends(user1_id, user2_id):
            through_model = self.model.friends.through
            through_model.objects.bulk_create([
                through_model(from_user_id=user1_id, to_user_id=user2_id),
                through_model(from_user_id=user2_id, to_user_id=user1_id),
            ])
            FriendInvite.objects.filter(
                Q(from_user_id=user1_id, to_user_id=user2_id) | Q(from_user_id=user2_id, to_user_id=user1_id)
            ).delete()
            make_friends.send(self.model, user1_id=user1_id, user2_id=user2_id)
            return True

    def delete(self, user1, user2):
        user1_id, user2_id = get_ids_from_users(user1, user2)
        if self.are_friends(user1_id, user2_id):
            through_model = self.model.friends.through
            through_model.objects.filter(
                Q(from_user_id=user1_id, to_user_id=user2_id) | Q(from_user_id=user2_id, to_user_id=user1_id)
            ).delete()
            break_friends.send(self.model, user1_id=user1_id, user2_id=user2_id)
            return True


def get_avatar_fn(instance, filename):
    id_str = str(instance.pk)
    return 'avatars/{sub_dir}/{id}_{rand}{ext}'.format(
        sub_dir=id_str.zfill(2)[-2:],
        id=id_str,
        rand=get_random_string(8, 'abcdefghijklmnopqrstuvwxyz0123456789'),
        ext=os.path.splitext(filename)[1],
    )


class User(AbstractBaseUser, PermissionsMixin):
    SEX_NONE = 0
    SEX_MALE = 1
    SEX_FEMALE = 2
    SEX_CHOICES = (
        (SEX_NONE, _(u'------')),
        (SEX_MALE, _(u'чоловіча')),
        (SEX_FEMALE, _(u'жіноча')),
    )

    email = models.EmailField('email', unique=True)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    confirmed_registration = models.BooleanField(_('confirmed registration '), default=True)
    avatar = models.ImageField(_(u'avatar'), upload_to=get_avatar_fn, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    sex = models.SmallIntegerField(_(u'стать'), choices=SEX_CHOICES, default=SEX_NONE)
    birth_date = models.DateField(_(u'дата народження'), null=True, blank=True)
    city = models.CharField(_(u'місто'), max_length=50, blank=True)
    job = models.CharField(_(u'місце роботи'), max_length=200, blank=True)
    about_me = models.TextField(_(u'про себе'), max_length=1000, blank=True)
    interests = models.TextField(_(u'інтереси'), max_length=1000, blank=True)
    friends = models.ManyToManyField('self', verbose_name=_(u'друзі'), symmetrical=True, blank=True)

    objects = UserManger()
    friendship = UserFriendShipManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    # def send_registration_email(self):
    #     url = 'http://{}{}'.format(
    #         Site.objects.get_current().domain,
    #         reverse('registration_confirm', kwargs={'token': Signer(salt='registration-confirm').sign(self.pk)})
    #     )
    #     self.email_user(
    #         ugettext('Confirm registration on Microsocial'),
    #         ugettext('For confirmation please visit: {}'.format(url)),
    #     )

    def send_registration_email(self):
        url = 'http://{}{}'.format(
            Site.objects.get_current().domain,
            reverse('registration_confirm', kwargs={'token': Signer(salt='registration-confirm').sign(self.pk)})
        )
        subject = ugettext('Confirm registration on Microsocial')
        from_email = None
        to = [self.email]
        htmlemail = get_template("users/email_template/email_confirm_registration_template.html")
        textemail = get_template("users/email_template/email_confirm_registration_template.txt")
        context = Context({"url":url})
        text_content = textemail.render(context)
        html_content = htmlemail.render(context)
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        #
        # self.email_user(
        #     ugettext('Confirm registration on Microsocial'),
        #     ugettext('For confirmation please visit: {}'.format(url)),
        # )


    def get_last_login_hash(self):
        return hashlib.md5(self.last_login.strftime('%Y-%m-%d-%H-%M-%S-%f')).hexdigest()[:8]

    def send_password_recovery_mail(self):
        data = '{}:{}'.format(self.pk, self.get_last_login_hash())
        token = TimestampSigner(salt='password-recovery-confirm').sign(data)
        url = 'http://{}{}'.format(
            Site.objects.get_current().domain,
            reverse('password_recovery_confirm', kwargs={'token': token})
        )
        subject = ugettext('Confirm password recovery on Microsocial')
        from_email = None
        to = [self.email]
        htmlemail = get_template("users/email_template/email_confirm_registration_template.html")
        textemail = get_template("users/email_template/email_confirm_registration_template.txt")
        context = Context({"url":url})
        text_content = textemail.render(context)
        html_content = htmlemail.render(context)
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        # self.email_user(
        #     ugettext('Confirm password recovery on Microsocial'),
        #     ugettext('For confirmation please visit: {}'.format(url)),
        # )

    def get_age(self):
        if self.birth_date:
            return int((datetime.date.today() - self.birth_date).days / 365.2425)


class FriendInviteManager(models.Manager):
    def is_pending(self, from_user, to_user):
        from_user_id, to_user_id = get_ids_from_users(from_user, to_user)
        return self.filter(from_user_id=from_user_id, to_user_id=to_user_id).exists()

    def add(self, from_user, to_user):
        from_user_id, to_user_id = get_ids_from_users(from_user, to_user)
        if from_user_id == to_user_id:
            raise ValueError(_(u'Неможна самого себе додати в друзі'))
        if User.friendship.are_friends(from_user_id, to_user_id):
            raise ValueError(_(u'Ви вже друзі'))
        if self.is_pending(from_user_id, to_user_id):
            raise ValueError(_(u'Заявка вже створена і очікую розшляду'))
        if self.is_pending(to_user_id, from_user_id):
            User.friendship.add(from_user_id, to_user_id)
            return 2
        self.create(from_user_id=from_user_id, to_user_id=to_user_id)
        return 1

    def approve(self, from_user, to_user):
        from_user_id, to_user_id = get_ids_from_users(from_user, to_user)
        if not self.is_pending(from_user_id, to_user_id):
            raise ValueError(_(u'Заявки не існує'))
        User.friendship.add(from_user, to_user)

    def reject(self, from_user, to_user):
        from_user_id, to_user_id = get_ids_from_users(from_user, to_user)
        self.filter(from_user_id=from_user_id, to_user_id=to_user_id).delete()


class FriendInvite(models.Model):
    from_user = models.ForeignKey(User, related_name='out_friend_invites')
    to_user = models.ForeignKey(User, related_name='in_friend_invites')

    objects = FriendInviteManager()

    class Meta:
        unique_together = ('from_user', 'to_user')


class UserWallPost(models.Model):
    user = models.ForeignKey(User, verbose_name=_(u'власник стіни'), related_name='wall_posts')
    author = models.ForeignKey(User, verbose_name=_(u'author'), related_name='+')
    content = models.TextField(_(u'text'), max_length=5000)
    created = models.DateTimeField(_(u'date'), auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

make_friends = Signal(providing_args=['user1_id', 'user2_id'])
break_friends = Signal(providing_args=['user1_id', 'user2_id'])