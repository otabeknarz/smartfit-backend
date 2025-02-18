from django.db import models
from django.contrib.auth.models import AbstractUser
import random


def get_random_id():
    return str(random.randint(1000000000, 9999999999))


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MA = "MALE", "Erkak"
        FE = "FEMALE", "Ayol"

    id = models.CharField(max_length=40, primary_key=True, unique=True, default=get_random_id)
    name = models.CharField(max_length=255, unique=False, null=True, blank=True)
    email = models.EmailField(unique=False, null=True, blank=True)
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True, choices=GenderChoices.choices)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk and not self.username:
            self.username = self.id
        super(User, self).save(*args, **kwargs)


class CustomSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name="custom_sessions")
    token = models.CharField(max_length=64, unique=True, null=False, blank=False)
    ip_address = models.CharField(max_length=64, null=True, blank=True)
    device_info = models.CharField(max_length=512, null=True, blank=True)
    last_online = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.device_info}"
