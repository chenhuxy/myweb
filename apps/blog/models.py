#!/usr/bin/env python
# _*_ coding:utf-8 _*_


from __future__ import unicode_literals
from django.db import models
from DjangoUeditor.models import UEditorField

# Create your models here.
class Category(models.Model):
    name=models.CharField('名称',max_length=30)
    class Meta:
        verbose_name='类别'
        verbose_name_plural=verbose_name
    def __unicode__(self):
        return self.name

class Tag(models.Model):
    name=models.CharField('名称',max_length=30)
    class Meta:
        verbose_name='标签'
        verbose_name_plural=verbose_name
    def __unicode__(self):
        return self.name

class Blog(models.Model):
    title=models.CharField('标题',max_length=30)
    author=models.CharField('作者',max_length=30)
    content=models.TextField('内容')
    #content=UEditorField('内容',width=600,height=300,toolbars='full',imagePath='/media/uploads/blog/images/',filePath='/media/uploads/blog/files/',blank=True)
    publish=models.DateTimeField('发布时间',auto_now_add=True)
    last_modify=models.DateTimeField('最后修改',auto_now=True)
    category=models.ForeignKey(Category,verbose_name='分类',on_delete=models.CASCADE)
    tag=models.ManyToManyField(Tag,verbose_name='标签')
    class Meta:
        verbose_name='博客'
        verbose_name_plural=verbose_name
    def __unicode__(self):
        return self.title

class Comment(models.Model):
    blog=models.ForeignKey(Blog,verbose_name='博客',on_delete=models.CASCADE)
    name=models.CharField('昵称',max_length=30)
    email=models.EmailField('邮箱')
    content=models.CharField('内容',max_length=240)
    publish=models.DateTimeField('发布时间',auto_now_add=True)
    class Meta:
        verbose_name='评论'
        verbose_name_plural=verbose_name
    def __unicode__(self):
        return self.content
