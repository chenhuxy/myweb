#!/usr/bin/env python
# _*_ coding:utf-8 _*_


from django.contrib import admin
from .models import *
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title','category','content','publish','last_modify',)
    list_filter = ('title','content',)
    search_fields = ('title','content',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('blog','name','content','publish',)
    list_filter = ('name','content')
    search_fields = ('name','content',)

admin.site.register(Category,CategoryAdmin)
admin.site.register(Tag,TagAdmin)
admin.site.register(Blog,BlogAdmin)
admin.site.register(Comment,CommentAdmin)
