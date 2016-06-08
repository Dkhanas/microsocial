# coding=utf-8
import datetime
from django.shortcuts import render


from videomain.models import VideoMainPage

# @login_required
def main(requests):
    """
    Take checked video. If checked more one then check last active
    and show it.
    """
    try:
        video = VideoMainPage.objects.get(checked=True)
    except VideoMainPage.MultipleObjectsReturned:
        video = VideoMainPage.objects.latest('last_active')
        videos_checked = VideoMainPage.objects.filter(checked=True)
        for video_checked in videos_checked:
            if video_checked != video:
                video_checked.checked = False
                video_checked.save()
    except VideoMainPage.DoesNotExist:
        video = VideoMainPage.objects.create(
            video_url="https://www.youtube.com/embed/2OD3oeodNms",
            checked=True,
        )
    return render(requests, 'main.html', {'video': video})
