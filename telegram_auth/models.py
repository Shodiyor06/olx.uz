import random

from django.conf import settings
from django.db import models
from django.utils import timezone


class TelegramLoginCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=5)

    def generate_code(self):
        self.code = str(random.randint(100000, 999999))
        self.save()