# Generated by Django 5.1.6 on 2025-04-01 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0005_onetimevideotoken_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="thumbnail",
            field=models.ImageField(
                blank=True, null=True, upload_to="images/course_thumbnails/"
            ),
        ),
    ]
