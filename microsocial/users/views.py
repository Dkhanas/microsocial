from django.views.generic import TemplateView


class ProfileViews(TemplateView):
    template_name = 'users/profile.html'