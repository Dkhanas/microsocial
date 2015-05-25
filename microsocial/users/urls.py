from django.conf.urls import url
from users import views

urlpatterns = [
    url(r'^profile/(?P<user_id>\d+)/$', views.ProfileViews.as_view(), name='user_profile'),
]