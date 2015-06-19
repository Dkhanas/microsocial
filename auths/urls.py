from django.conf.urls import url
from django.contrib.auth.views import logout
from auths import views
from microsocial import settings

urlpatterns = [
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', logout, {'next_page': settings.LOGIN_URL}, name='logout'),
    url(r'^registration/$', views.RegistrationView.as_view(), name='registration'),
    url(r'^registration/(?P<token>.+)/$', views.RegistrationConfirm.as_view(), name='registration_confirm'),
    url(r'^password-recovery/$', views.PasswordRecovery.as_view(), name='password_recovery'),
    url(r'^password-recovery/(?P<token>.+)/$', views.PasswordRecoveryConfirm.as_view(), name='password_recovery_confirm'),
]
