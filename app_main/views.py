import os
import time
import datetime
import subprocess
import json
from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .models import VideoModel


def index(request):
    all = VideoModel.objects.order_by('-id')
    ctx = {
        "title": "動画一覧",
        "lst": all,
        "num": len(all),
    }

    return render(request, "index.html", context=ctx)


def rank(request):
    all = VideoModel.objects.order_by('-rank')
    ctx = {
        "title": "動画一覧 ランク順",
        "lst": all,
        "num": len(all),
    }

    return render(request, "index.html", context=ctx)


def radom(request):
    all = VideoModel.objects.order_by('?')
    ctx = {
        "title": "動画一覧 ランダム",
        "lst": all,
        "num": len(all),
    }

    return render(request, "index.html", context=ctx)


@ensure_csrf_cookie
def rank_update(request):
    if request.method == 'POST':
        # JSON文字列
        data = json.loads(request.body)
        obj = VideoModel.objects.filter(name=data['name']).first()
        obj.rank = int(data['select'])
        obj.save()
        return JsonResponse({'ok': 1})

    return JsonResponse({'ok': 0})


@ensure_csrf_cookie
def del_update(request):
    if request.method == 'POST':
        # JSON文字列
        data = json.loads(request.body)
        # ファイル削除
        os.remove(f"{settings.MY_VIDEO_PATH}{data['name']}.mp4")
        subprocess.Popen("python sync_mtdb.py", shell=True)
        return JsonResponse({'ok': 1})

    return JsonResponse({'ok': 0})


def upload(request):
    """動画アップロード"""

    if request.method == 'POST' and len(request.FILES.getlist('upfile')) > 0:  # noqa
        # 複数取得
        upfile = request.FILES.getlist('upfile')
        for v in upfile:
            fs = FileSystemStorage(location=settings.MY_VIDEO_PATH)
            # ファイル名作成
            time.sleep(0.2)
            dt_now = datetime.datetime.now()
            out = dt_now.strftime('%Y%m%d%H%M%S%f')
            _ = fs.save(out + ".mp4", v)

        ctx = {
            "title": "アップロード 完了"
        }
        subprocess.Popen("python sync_mtdb.py", shell=True)

    else:
        ctx = {
            "title": "アップロード"
        }

    return render(request, "upload.html", context=ctx)
