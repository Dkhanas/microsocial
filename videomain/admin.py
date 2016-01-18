from django.contrib import admin
from models import VideoMainPage


class VideoAdmin(admin.ModelAdmin):
    list_display = ('video_url', 'checked', 'last_active',)


admin.site.register(VideoMainPage, VideoAdmin)
