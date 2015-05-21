from django.conf.urls import include, url
from django.contrib import admin
from microsocial import views

urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('auths.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^profile/(?P<user_id>\d+)/$', views.ProfileView.as_view(), name='profile'),

    url(r'', include('django.contrib.flatpages.urls'))
]