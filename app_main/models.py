from django.db import models


class VideoModel(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="名称")
    rank = models.IntegerField(default=0, verbose_name="ランク")
    comment = models.CharField(max_length=255, default="", verbose_name="コメント")

    def __str__(self):
        return f"<{self.id}> {self.name}"
