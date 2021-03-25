#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from django.shortcuts import render,render_to_response
from blog import models
from blog import forms
from django.http import Http404
# Create your views here.


def get_blogs(request):
    blogs=models.Blog.objects.all().order_by('-publish')
    return render_to_response('blog_list.html',{'blogs':blogs})

def get_details(request,blog_id):
    try:
        blog = models.Blog.objects.get(id=blog_id)
    except Exception as e:
        print(e)
        raise Http404
    if request.method == 'GET':
        form = forms.CommentForm()
    else:
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            cleaned_data['blog'] = blog
            models.Comment.objects.create(**cleaned_data)
    ctx = {
        'blog': blog,
        #'comments': blog.comment_set.all().order_by('-publish'),
        'comments':models.Comment.objects.filter(blog=blog).order_by('-publish'),
        'form': form
    }
    print(ctx)
    return render(request, 'blog_details.html', ctx)

