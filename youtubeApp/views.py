import os
import logging
import httplib2
import json

import google.oauth2.credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext as _
from oauth2client.client import flow_from_clientsecrets
from googleapiclient.discovery import build

from youtubeApp.models import ReportData, ProcessedData

CLIENT_SECRETS_FILE = '/Users/justinsingh/Desktop/Web/django/youtubeApp/secrets/client_id.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
CLIENT_SECRETS_FILE = '/Users/justinsingh/Desktop/Web/django/youtubeApp/secrets/client_id.json'


# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES, redirect_uri ="http://127.0.0.1:8000/oauth2callback")
    print flow.redirect_uri
    print "PLEASE"
    credentials = flow.run_local_server()
    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def channel_stats_ajax(request):
    channel_id = request.GET.get('channel_id')
    processed_data = ProcessedData.objects.get(channel_id=channel_id).data
    channel_json = json.loads(processed_data)
    return JsonResponse(channel_json, safe=False)

def home_view(request):
    #service = get_authenticated_service()
    return render(request, 'home.html', {})

def oauth_callback_request(request):
  '''
  if not xsrfutil.validate_token(settings.SECRET_KEY, request.REQUEST['state'],
                                 request.user):
    return  HttpResponseBadRequest()
  credential = FLOW.step2_exchange(request.REQUEST)
  storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
  storage.put(credential)
  '''
  print "callback"
  code = request.GET['code']
  print code
  state = request.GET['state']

  #flow.redirect_uri = "http://127.0.0.1:8000/oauth2callback"
  return HttpResponseRedirect("/")
