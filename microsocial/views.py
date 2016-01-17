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
    return render(requests, 'main.html', {'video': video})
