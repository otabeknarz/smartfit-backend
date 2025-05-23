# Generated by Django 5.1.6 on 2025-05-15 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0005_alter_payment_order"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="cancel_time",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="payment",
            name="reason",
            field=models.IntegerField(
                blank=True,
                choices=[
                    (1, "Recipient not found or inactive"),
                    (2, "Debit operation error"),
                    (3, "Transaction error"),
                    (4, "Transaction cancelled (timeout)"),
                    (5, "Refund"),
                    (10, "Unknown error"),
                ],
                null=True,
            ),
        ),
    ]
