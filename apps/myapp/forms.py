#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from django import forms

class LoginForm(forms.Form):
    name = forms.CharField()