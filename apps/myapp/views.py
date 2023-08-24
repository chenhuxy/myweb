#!/usr/bin/env python
# _*_ coding:utf-8 _*_


from django.shortcuts import render_to_response
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect,get_object_or_404
import time
import json
from django.utils.safestring import mark_safe
from apps.myapp.models import *
from  apps.myapp import common
from apps.myapp import page_helper
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.template import context
from apps.myapp import zabbix
from apps.myapp import prometheus
from apps.myapp import encrypt_helper
from django.core.mail import send_mail
from django.utils.safestring import mark_safe
#from myapp import ansible_api
from django.template import loader,RequestContext
from apps.myapp import token_helper
from apps.myapp import tasks
from django.core.cache import cache
from django.utils import timezone
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.clickjacking import xframe_options_deny
from django.views.decorators.clickjacking import xframe_options_sameorigin
#from apps.myapp import workflow,wf
from SpiffWorkflow.specs import WorkflowSpec
from SpiffWorkflow.serializer.prettyxml import XmlSerializer
from SpiffWorkflow import Workflow
#  form upload
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from apps.myapp.auth_helper import custom_login_required,custom_permission_required
from django.contrib.auth.models import Permission,Group
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password,check_password
from django.utils.crypto import get_random_string, salted_hmac
from django.contrib.auth.decorators import permission_required

#####################################################################################################################################
from django.shortcuts import render,render_to_response,HttpResponse
#from rest_framework.decorators import api_view
#from rest_framework.response import Response
import urllib
import urllib.parse


# Create your views here.

# 添加index函数，用于返回index.html页面



