from __future__ import unicode_literals
from django.db import models


# Create your models here.
class NormalUser(models.Model):
    username=models.CharField('用户名',max_length=30)
    headImg=models.FileField('文件名',upload_to='./uploadFiles')
    def __str__(self):
        return self.username
    class Meta:
        ordering=['username']
