# Djangoで動画一覧

## 最初

バージョン確認
```
python -m django --version
```
プロジェクト作成
```
該当フォルダ内で(※最後のドットが重要)
django-admin startproject video_project .
```
settings.py の日本語日本時間設定
```
LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
```
.gitignore を作成
```
*__pycache__
*.sqlite3
など
```
データベース作成(Djangoで用意している10個以上のテーブルができる)
```
python manage.py migrate
```
スーパーユーザー作成
```
python manage.py createsuperuser
```
開発用サーバー起動
```
python manage.py runserver

http://127.0.0.1:8000/
スーパーユーザーでログイン
http://127.0.0.1:8000/admin/
```

## アプリケーション作成

```
python manage.py startapp <appname>
```

## マイグレーション

settings.py の INSTALLED_APPS に該当 models.py のアプリを登録しておく

```
マイグレーションファイルを作成
python manage.py makemigrations

マイグレーションファイルをデータベースに適用
python manage.py migrate
```

admin.py に登録すると管理画面で見れる

```
from django.contrib import admin
from .models import VideoModel

admin.site.register(VideoModel)
```

