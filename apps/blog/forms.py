#!/usr/bin/env python
# _*_ coding:utf-8 _*_



from django import forms

class CommentForm(forms.Form):
    name=forms.CharField(label='称呼',max_length=16,error_messages={
        'required':'请填写称呼',
        'max_length':'称呼太长'
    })
    email=forms.EmailField(label='邮箱',error_messages={
        'required':'请填写邮箱',
        'invalid':'邮箱格式错误'
    })
    content=forms.CharField(label='评论',error_messages={
        'required':'请填写评论',
        'max_length':'评论太长'
    })
