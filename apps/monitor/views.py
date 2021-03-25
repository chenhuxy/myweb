from django.shortcuts import render,render_to_response
from .models import  *
from django.http import Http404
# Create your views here
def get_host(request):
    hosts=Host.objects.all().order_by('hostid')
    return  render_to_response('host_list.html',{'hosts':hosts})
def get_host_detail(request,hostid):
    try:
        host=Host.objects.all().get(hostid=hostid)
    except host.DoesNotExist:
        raise Http404
    return render_to_response('host_detail.html')

