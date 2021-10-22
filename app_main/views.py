import time
import datetime
import subprocess
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
        pass

    return JsonResponse({})


@ensure_csrf_cookie
def del_update(request):
    if request.method == 'POST':
        pass

    return JsonResponse({})


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
            # _ = fs.save(v.name, v)
            _ = fs.save(out + ".mp4", v)

        ctx = {
            "title": "アップロード 完了"
        }
    else:
        ctx = {
            "title": "アップロード"
        }

    subprocess.Popen("python sync_mtdb.py", shell=True)

    return render(request, "upload.html", context=ctx)
