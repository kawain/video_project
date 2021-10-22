import os
import sqlite3
import pathlib
import cv2
from tqdm import tqdm

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "video_project.settings")

import django  # noqa
django.setup()

from django.conf import settings  # noqa

# ↓ django.setup()の後にする
from app_main.models import VideoModel  # noqa


def first_import():
    """初回のインポート"""

    dbname = "video.db"
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute('SELECT * FROM data')
    res = cur.fetchall()
    cur.close()
    conn.close()

    for v in tqdm(res):
        obj = VideoModel()
        obj.name = v[1]
        obj.rank = v[2]
        obj.save()


def make_thumb(videoPath, outputPath):
    """動画からサムネイル作成(10枚)"""

    cap = cv2.VideoCapture(videoPath)
    if not cap.isOpened():
        return

    # フレーム数を取得
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    for i in range(10):
        # フレーム位置を設定
        cap.set(cv2.CAP_PROP_POS_FRAMES, i * frame_count / 10)

        _, img = cap.read()
        # imgは読み込んだフレームのNumpy配列でのピクセル情報(BGR)
        # imgのshapeは (高さ, 横幅, 3)

        # 画像サイズを取得
        # width = img.shape[1]
        # height = img.shape[0]

        # 縮小後のサイズを決定
        newWidth = 120
        newHeight = 80

        # リサイズ
        img = cv2.resize(img, (newWidth, newHeight))

        # 画像ファイルで書き出す
        # ファイル名には連番を付ける
        cv2.imwrite(outputPath % i, img)


def synchronize():
    """フォルダ内の動画ファイルと画像、DBを同期する"""

    dic = {}

    # 動画フォルダ一覧
    tmp = pathlib.Path(settings.MY_VIDEO_PATH)
    videos = tmp.glob("./*.mp4")
    for v in videos:
        # ファイル名 = [動画, 画像, DB]
        dic[v.stem] = [True, False, False]

    # 画像フォルダ一覧
    tmp = pathlib.Path(settings.MY_THUMBNAIL_PATH)
    thumbnails = tmp.glob("./*.jpg")
    for v in thumbnails:
        if str(v.stem) in dic:
            dic[v.stem][1] = True
        else:
            dic[v.stem] = [False, True, False]

    # DB一覧
    all = VideoModel.objects.all()
    for v in all:
        if v.name in dic:
            dic[v.name][2] = True
        else:
            dic[v.name] = [False, False, True]

    # 辞書ループ [動画, 画像, DB]
    for k, v in tqdm(dic.items()):
        # 全部揃っている場合
        if v[0] and v[1] and v[2]:
            continue

        # 動画があって
        if v[0]:
            # サムネがない
            if v[1] is False:
                make_thumb(f"{settings.MY_VIDEO_PATH}{k}.mp4", f"{settings.MY_PATH}/%d.jpg")  # noqa
                img0 = cv2.imread(f"{settings.MY_PATH}/0.jpg")
                img1 = cv2.imread(f"{settings.MY_PATH}/1.jpg")
                img2 = cv2.imread(f"{settings.MY_PATH}/2.jpg")
                img3 = cv2.imread(f"{settings.MY_PATH}/3.jpg")
                img4 = cv2.imread(f"{settings.MY_PATH}/4.jpg")
                img5 = cv2.imread(f"{settings.MY_PATH}/5.jpg")
                img6 = cv2.imread(f"{settings.MY_PATH}/6.jpg")
                img7 = cv2.imread(f"{settings.MY_PATH}/7.jpg")
                img8 = cv2.imread(f"{settings.MY_PATH}/8.jpg")
                img9 = cv2.imread(f"{settings.MY_PATH}/9.jpg")
                im_h = cv2.hconcat([img0, img1, img2, img3, img4, img5, img6, img7, img8, img9])  # noqa
                # 拡張子なしのファイル名
                cv2.imwrite(f"{settings.MY_THUMBNAIL_PATH}{k}.jpg", im_h)

            # DBにない
            if v[2] is False:
                # DBに追加
                obj = VideoModel()
                obj.name = k
                obj.save()

        # 動画がないのに
        if v[0] is False:
            # サムネがある
            if v[1]:
                # ファイル削除
                os.remove(f"{settings.MY_THUMBNAIL_PATH}{k}.jpg")

            # DBにある
            if v[2]:
                # DBから削除
                VideoModel.objects.filter(name=k).delete()


if __name__ == '__main__':
    # first_import()
    synchronize()
