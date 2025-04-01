from django.http.response import Http404
from django.shortcuts import render
import json
import requests

from courses.models import OneTimeVideoToken
from smartfit.settings import VIDEO_SERVICE_SECRET_KEY


def video(request, uuid):
    token = OneTimeVideoToken.objects.filter(id=uuid).first()

    if not token or token.is_used:
        raise Http404()

    lesson = token.lesson

    token.is_used = True
    token.save()

    payload_str = json.dumps({
        "ttl": 300,
        "whitelisthref": "smart-fit.uz"
    })

    headers = {
        'Authorization': f"Apisecret {VIDEO_SERVICE_SECRET_KEY}",
        'Content-Type': "application/json",
        'Accept': "application/json"
    }

    response = requests.post(
        url=f"https://dev.vdocipher.com/api/videos/{lesson.video_service_id}/otp",
        headers=headers,
        data=payload_str
    )

    if response.status_code != 200:
        raise Http404()

    json_response = response.json()

    video_url = f"https://player.vdocipher.com/v2/?otp={json_response.get('otp')}&playbackInfo={json_response.get('playbackInfo')}"

    return render(
        request,
        "video.html",
        {
            "title": lesson.title,
            "token": token,
            "user": token.user,
            "video_url": video_url,
        },
    )
