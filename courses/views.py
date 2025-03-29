from django.http.response import Http404
from django.shortcuts import render

from courses.models import OneTimeVideoToken, Lesson


def video(request, uuid):
    token = OneTimeVideoToken.objects.filter(id=uuid).first()

    if not token or token.is_used:
        raise Http404()

    lesson = token.lesson

    token.is_used = True
    token.save()

    return render(
        request,
        "video.html",
        {
            "title": lesson.title,
            "token": token,
            "video_url": lesson.video_url,
        }
    )
