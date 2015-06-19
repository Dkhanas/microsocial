from django.conf.urls import url
from users import views

urlpatterns = [
    url(r'^profile/(?P<user_id>\d+)/$', views.ProfileViews.as_view(), name='user_profile'),
    url(r'^settings/$', views.UserSettingsView.as_view(), name='settings'),
    url(r'^friends/$', views.UserFriendsView.as_view(), name='friends'),
    url(r'^friends/incoming/$', views.UserIncomingView.as_view(), name='incoming'),
    url(r'^friends/outcoming/$', views.UserOutcomingView.as_view(), name='outcoming'),
    url(r'^api/friendship/$', views.FriendshipApiView.as_view(), name='friendship_api'),
    url(r'^search/$', views.SearchView.as_view(), name='search'),


]

