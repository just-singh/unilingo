import argparse
import os
from io import FileIO
import json

import google.oauth2.credentials
import google_auth_oauthlib.flow
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow

from youtubeApp.models import ReportData
from settings import CLIENT_SECRETS_FILE


# This OAuth 2.0 access scope allows for read access to YouTube Analytics
# monetary reports for the authenticated user's account. Any request that
# retrieves earnings or ad performance metrics must use this scope.
SCOPES = ['https://www.googleapis.com/auth/youtube',
  'https://www.googleapis.com/auth/youtube.readonly',
  'https://www.googleapis.com/auth/youtubepartner',
  'https://www.googleapis.com/auth/yt-analytics-monetary.readonly',
  'https://www.googleapis.com/auth/yt-analytics.readonly']

API_SERVICE_NAME = 'youtubeAnalytics'
API_VERSION = 'v2'

_DEFAULT_AUTH_CODE_MESSAGE = (
    'Enter the authorization code: ')

def get_service():
  flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE,
    scopes=SCOPES, redirect_uri="http://127.0.0.1:8000/oauth2callback")

  authorization_url, state = flow.authorization_url(access_type='offline', approval_prompt='force')
  print authorization_url

  code = input(_DEFAULT_AUTH_CODE_MESSAGE)
  flow.fetch_token(code=code)
  credentials = flow.credentials

  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def execute_api_request(client_library_function, **kwargs):
  response = client_library_function(
    **kwargs
  ).execute()

  return response

def update_v2_reports(channel_id):
  # *DO NOT* leave this option enabled when running in production.
  os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

  youtubeAnalytics = get_service()
  views_time_response = execute_api_request(
      youtubeAnalytics.reports().query,
      ids='channel==' + channel_id,
      startDate='2000-01-01',
      endDate='2018-05-29',
      metrics='views',
      dimensions='day',
      sort='day'
  )
  report, created = ReportData.objects.get_or_create(
      channel_id=channel_id,
      report_name=ReportData.VIEWS_TIME_STATS
  )
  report.data = json.dumps(views_time_response)
  report.save()
