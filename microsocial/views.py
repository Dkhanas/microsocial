# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render



from videomain.models import VideoMainPage

# @login_required
def main(requests):
    #TODO: 1:"Check last active"
    # return redirect('user_profile', user_id=requests.user.pk, permanent=False)
    video = VideoMainPage.objects.get(checked=True)
    return render(requests, 'main.html', {'video': video})
