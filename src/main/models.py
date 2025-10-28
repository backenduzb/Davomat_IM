from django.contrib.auth.models import User
from django.db import models

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telegram_id = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = "Admin "
        verbose_name_plural = "Adminlar "