from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import random


def get_random_id():
    return str(random.randint(1000000000, 9999999999))


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MA = "MALE", "Erkak"
        FE = "FEMALE", "Ayol"

    id = models.CharField(
        max_length=40, primary_key=True, unique=True, default=get_random_id
    )
    name = models.CharField(max_length=255, unique=False, null=True, blank=True)
    picture = models.ImageField(upload_to="images/users/", null=True, blank=True)
    email = models.EmailField(unique=False, null=True, blank=True)
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    gender = models.CharField(
        max_length=10, null=True, blank=True, choices=GenderChoices.choices
    )
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk and not self.username:
            self.username = self.id
        super(User, self).save(*args, **kwargs)


class CustomSession(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="custom_sessions",
    )
    token = models.CharField(max_length=64, unique=True, null=False, blank=False)
    ip_address = models.CharField(max_length=64, null=True, blank=True)
    device_info = models.CharField(max_length=512, null=True, blank=True)
    last_online = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.device_info}"


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ("CARD", "Credit/Debit Card"),
        ("PAYME", "Payme"),
        ("PAYNET", "Paynet"),
        ("CLICK", "Click"),
        ("UZUM", "UZUM"),
        ("STRIPE", "Stripe"),
        ("BANK", "Bank Transfer"),
        ("CASH", "Cash"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("COMPLETED", "Completed"),
        ("FAILED", "Failed"),
        ("REFUNDED", "Refunded"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="UZS")
    method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(
        max_length=10, choices=PAYMENT_STATUS_CHOICES, default="PENDING"
    )
    transaction_id = models.CharField(
        max_length=100, unique=True, null=True, blank=True
    )
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def mark_completed(self, transaction_id):
        self.status = "COMPLETED"
        self.transaction_id = transaction_id
        self.save()

    def mark_failed(self):
        self.status = "FAILED"
        self.save()

    def __str__(self):
        return f"{self.user} - {self.amount} {self.currency} - {self.status}"
