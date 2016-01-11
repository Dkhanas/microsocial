import datetime
from django.utils import timezone
from django.db import models


class VideoMainPage(models.Model):
    video_url = models.URLField()
    checked = models.BooleanField(default=False)
    last_active = models.DateTimeField(default=timezone.now, blank=True)
