from django.shortcuts import render, render_to_response
from django.template import Context
from videomain.models import VideoMainPage
from django.core.exceptions import MultipleObjectsReturned


def video_for_main(request):
    try:
        video = VideoMainPage.objects.get(checked=True)
    except VideoMainPage.MultipleObjectsReturned:
        video = VideoMainPage.objects.latest('last_active')
    return render(request, 'video_for_main/video_for_main.html', {'video': video})

