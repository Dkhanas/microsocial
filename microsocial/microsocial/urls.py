from django.conf.urls import patterns, include, url
from django.contrib import admin
from microsocial import views

urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^admin/', include(admin.site.urls)),
]