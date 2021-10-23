#!/bin/sh

cd /home/user/repo/django_videos
/home/user/.pyenv/shims/gunicorn --workers 3 --bind 127.0.0.1:8889 video_project.wsgi:application

