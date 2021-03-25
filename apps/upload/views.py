from django.shortcuts import render
from django import forms
from django.http import HttpResponse
from apps.upload.models import *

# Create your views here.
class NormalUserForm(forms.Form):
    username=forms.CharField()
    headImg=forms.FileField()
def registerNormalUser(request):
    if request.method=='POST':
        uf=NormalUserForm(request.POST,request.FILES)
        if uf.is_valid():
            username=uf.cleaned_data['username']
            headImg=uf.cleaned_data['headImg']
            normalUser=NormalUser()
            normalUser.username=username
            normalUser.headImg=headImg
            normalUser.save()
            return HttpResponse('Upload Success!')
    else:
        uf=NormalUserForm()
    return render(request,'register.html',{'uf':uf})