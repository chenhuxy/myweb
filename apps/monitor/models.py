from __future__ import unicode_literals
from django.db import models

# Create your models here
class Host(models.Model):
    ip=models.CharField(max_length=50)
    hostid=models.IntegerField()
    createdate=models.DateTimeField(auto_now_add=True)
    lastmodified=models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return self.ip,self.hostid,self.createdate,self.lastmodified


