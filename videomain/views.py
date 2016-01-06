from django.shortcuts import render, render_to_response
from django.template import Context
from videomain.models import VideoMainPage


def video_for_main(request):
    video = VideoMainPage.objects.get(checked=True)
    return render(request, 'video_for_main/video_for_main.html', {'video': video})

