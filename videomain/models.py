from django.db import models


class VideoMainPage(models.Model):
    video_url = models.URLField()
    checked = models.BooleanField(default=False)