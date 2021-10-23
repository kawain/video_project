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

## collectstatic

```
静的ファイルを一つの場所に集める
collectstaticする前に、集める場所をsettings.pyに設定する
STATIC_ROOT = '/home/user/Dropbox/app/django_videos/collect/static'

python manage.py collectstatic
```

## nginx

gunicorn で動かす設定

pip install gunicorn

```
*.conf を作成
sudo nano /etc/nginx/conf.d/django_video.conf
sudo micro /etc/nginx/conf.d/django_video.conf


server {
    listen  80;
    server_name 192.168.3.3;

    client_max_body_size 2G;

    location /static {
        alias /home/user/repo/django_videos/collect/static;
    }

    location /media {
        alias /home/user/videos/media;
    }

    location / {
        proxy_pass http://127.0.0.1:8889;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

設定ファイルの構文が正しいか確認
sudo nginx -t

nginxを再起動
sudo systemctl restart nginx

エラーログの場所
/var/log/nginx/error.log

sudo chown -R "$USER":root /webdirectory
sudo chmod -R 0755 /webdirectory

sudo chmod 755 /home/user/

```

```
gunicorn --workers 3 --bind 127.0.0.1:8889 video_project.wsgi:application
```

## サービス化

systemd のユーザーごとの設定

/home/user/.config/systemd/user

この中に *.service ファイルを作成

シェルスクリプトの実行権限

chmod +x start.sh


django_videos.service
```
[Unit]
Description = django videos

[Service]
ExecStart = /home/user/repo/django_videos/start.sh
Restart = no
Type = simple

[Install]
WantedBy = default.target
```

```
// 有効化
systemctl --user enable django_videos.service

// 自動起動の無効化
systemctl --user disable django_videos

// 自動起動が有効になっているか確認
systemctl --user is-enabled django_videos

// サービスが実行中かどうかの確認
systemctl --user is-active django_videos

// サービスの稼動状況確認
systemctl --user status django_videos

// サービスの開始
systemctl --user start django_videos

// サービスの停止
systemctl --user stop django_videos

// サービスの再起動
systemctl --user restart django_videos
```

