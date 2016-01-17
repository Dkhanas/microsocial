# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.core.exceptions import MultipleObjectsReturned


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
        videos_checked = VideoMainPage.objects.all()
        for video_checked in videos_checked:
            if video_checked != video:
                video_checked.checked = False
                video_checked.save()
    return render(requests, 'main.html', {'video': video})
