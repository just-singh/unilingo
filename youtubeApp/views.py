import os
import logging
import httplib2
import json

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from googleapiclient.discovery import build

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponseRedirect,\
    JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext as _
from oauth2client.client import flow_from_clientsecrets

from youtubeApp.models import ReportData, ProcessedData
from youtubeApp.upload_video import upload_video

from settings import CLIENT_SECRETS_FILE, REDIRECT_URI


# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE,
        scopes=SCOPES, redirect_uri = REDIRECT_URI)
    credentials = flow.run_local_server()
    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

# An ajax function that returns our processed and formatted channel statistics.
def channel_stats_ajax(request):
    channel_id = request.GET.get('channel_id')
    processed_data = ProcessedData.objects.get(channel_id=channel_id).data
    channel_json = json.loads(processed_data)
    return JsonResponse(channel_json, safe=False)

def upload_ajax(request):
    if 'credentials' not in request.session:
        return redirect(request.build_absolute_uri(reverse('authorize')))
    credentials = Credentials(**request.session['credentials'])

    client = build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)
    upload_video(client)
    return HttpResponse(status=200)


def home_view(request):
    return render(request, 'home.html', {})

def authorize(request):
    flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = request.build_absolute_uri(reverse('ouath_callback'))

    authorization_url, state = flow.authorization_url(access_type='offline',\
      include_granted_scopes='true', approval_prompt='force')
    request.session['state'] = state
    authorization_url = authorization_url + '/'
    return redirect(authorization_url)


def oauth_callback_request(request):
    state = request.session['state']
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = request.build_absolute_uri(reverse('ouath_callback'))

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    code = request.GET.get('code')
    flow.fetch_token(code=code)

    credentials = flow.credentials
    request.session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    return redirect(reverse('upload_ajax'))
