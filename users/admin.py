from django.contrib import admin
from users.models import User, UserWallPost, FriendInvite

admin.site.register(User)
admin.site.register(UserWallPost)
admin.site.register(FriendInvite)
