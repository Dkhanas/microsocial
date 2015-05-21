from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic import TemplateView


@login_required
def main(request):
    return redirect('profile', user_id=request.user.pk, permanent=False)


class ProfileView(TemplateView):
    template_name = 'profile.html'


