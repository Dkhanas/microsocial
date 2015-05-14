from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.flatpages.views import flatpage

from microsocial import views

urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^about/$', flatpage, {'url':'/about/'},name='about_page'),
    url(r'^help/$', flatpage, {'url':'/help/'},name='help_page'),
    url(r'^advertising/$', flatpage, {'url':'/advertising/'}, name='advertising_page'),
    url(r'^developers/$', flatpage, {'url':'/developers/'}, name='developers_page'),
    url(r'^vacancies/$', flatpage, {'url':'/vacancies/'}, name='vacancies_page'),

]