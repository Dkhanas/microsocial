import datetime
from django.shortcuts import render
from videomain.models import VideoMainPage


def video_for_main(request):
    try:
        video = VideoMainPage.objects.get(checked=True)
    except VideoMainPage.MultipleObjectsReturned:
        video = VideoMainPage.objects.latest('last_active')
    except VideoMainPage.DoesNotExist:
        video.video_url =  "http://www.youtube.com/embed/UnBlst3T7bY"
        video.checked = True
        video.last_active = datetime.datetime.now().time()
        video.save()
    return render(request, 'video_for_main/video_for_main.html', {'video': video})

