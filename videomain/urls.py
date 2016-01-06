from django.conf.urls import url
from videomain import views

urlpatterns = [
    url(r'^video$', views.video_for_main, name='video'),
]
