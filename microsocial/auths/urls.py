from django.conf.urls import url
from auths import views

urlpatterns = [
    url(r'^login/$', views.login_view, name='login'),
    url(r'^registration/$', views.RegistrationView.as_view(), name='registration'),
    url(r'^registration/(?P<token>.+)/$', views.RegistrationConfirm.as_view(), name='registration_confirm'),
    url(r'^password-recovery/$', views.PasswordRecovery.as_view(), name='password_recovery'),
]
