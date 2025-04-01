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


# class OnboardingAnswers(models.Model):
#     class GoalsChoices(models.TextChoices):
#         WEIGHT_LOSS = "weight_loss", "Weight Loss"
#         MUSCLE_GAIN = "muscle_gain", "Muscle Gain"
#         ENDURANCE = "endurance", "Improve Endurance"
#         STRENGTH = "strength", "Increase Strength"
#         MAINTENANCE = "maintenance", "Maintain Fitness"
#
#     class TimelineChoices(models.TextChoices):
#         ONE_MONTH = "one_month", "One Month"
#         TWO_THREE_MONTHS = "two_three_months", "Two Three Months"
#         LONG_TERM = "long_term", "Long Term"
#
#     class ExperienceLevelChoices(models.TextChoices):
#         BEGINNER = "beginner", "Beginner"
#         INTERMEDIATE = "intermediate", "Intermediate"
#         ADVANCED = "advanced", "Advanced"
#
#     class TrainingFrequencyChoices(models.TextChoices):
#         TWICE = "twice", "Twice"
#         THREE_TO_FOUR = "three_to_four", "Three to four"
#         FIVE_PLUS = "five_plus", "Five Plus"
#
#     class ConsultationChoices(models.TextChoices):
#         YES = "yes", "Yes"
#         NO = "no", "No"
#
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="onboarding_answers")
#     goal = models.CharField(max_length=20, choices=GoalsChoices.choices, null=True, blank=True)
#     timeline = models.CharField(max_length=20, choices=TimelineChoices.choices, null=True, blank=True)
#     experience_level = models.CharField(max_length=20, choices=ExperienceLevelChoices.choices, null=True, blank=True)
#     training_frequency = models.CharField(max_length=20, choices=TrainingFrequencyChoices.choices, null=True, blank=True)
#     consultation = models.CharField(max_length=20, choices=ConsultationChoices.choices, null=True, blank=True)
#
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return f"{self.user.username} - {self.goal} - {self.timeline} - {self.experience_level}"
