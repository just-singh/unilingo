import os
import json

import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow, Flow

from youtubeApp.models import ReportData
from youtubeApp.settings import CLIENT_SECRETS_FILE, REDIRECT_URI


SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
_DEFAULT_AUTH_CODE_MESSAGE = ('Enter the authorization code: ')

def get_authenticated_service():
    flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES,
        redirect_uri=REDIRECT_URI)
    authorization_url, state = flow.authorization_url(access_type='offline',
        approval_prompt='force')
    print authorization_url
    code = input(_DEFAULT_AUTH_CODE_MESSAGE)
    flow.fetch_token(code=code)
    credentials = flow.credentials
    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def print_response(response):
    print(response)

# Remove keyword arguments that are not set
def remove_empty_kwargs(**kwargs):
    good_kwargs = {}
    if kwargs is not None:
        for key, value in kwargs.iteritems():
            if value:
                good_kwargs[key] = value
    return good_kwargs

def channels_list_by_id(client, **kwargs):
    kwargs = remove_empty_kwargs(**kwargs)
    response = client.channels().list(**kwargs).execute()
    return response

def fetch_channel_statistics(client, channel_id):
    json_response = channels_list_by_id(client,
        part='snippet,contentDetails,statistics',
        id=channel_id)
    report, created = ReportData.objects.get_or_create(
        channel_id=channel_id,
        report_name=ReportData.CHANNEL_STATS
    )
    report.data = json.dumps(json_response)
    report.save()
    return json_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

def playlist_item_call(client, **kwargs):
    kwargs = remove_empty_kwargs(**kwargs)

    response = client.playlistItems().list(
        **kwargs
    ).execute()
    return response

def video_data_call(client, **kwargs):
    kwargs = remove_empty_kwargs(**kwargs)

    response = client.videos().list(
        **kwargs
    ).execute()
    return response

def fetch_video_statistics(client, channel_id, upload_list_id):
    playlist_response = playlist_item_call(client,
        playlistId=upload_list_id,
        part='contentDetails'
    )

    videoList = []
    for video_data in playlist_response['items']:
        videoList.append(video_data['contentDetails']['videoId'])

    video_response = video_data_call(client,
        id=",".join(videoList),
        part='statistics'
    )

    report, created = ReportData.objects.get_or_create(
        channel_id=channel_id,
        report_name=ReportData.VIDEO_STATS
    )
    report.data = json.dumps(video_response)
    report.save()

def comments_list(client, **kwargs):
    kwargs = remove_empty_kwargs(**kwargs)

    response = client.commentThreads().list(
        **kwargs
        ).execute()
    return response

def fetch_comments(client, channel_id, video_id):
    comment_response = comments_list(client,
        part='snippet',
        videoId=video_id)
    report, created = ReportData.objects.get_or_create(
        channel_id=channel_id,
        report_name=ReportData.COMMENT_LIST
    )
    report.data = json.dumps(comment_response)
    report.save()


def update_v3_reports(channel_id, comment_video_id):
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    client = get_authenticated_service()
    upload_list_id = fetch_channel_statistics(client, channel_id)
    fetch_video_statistics(client, channel_id, upload_list_id)
    fetch_comments(client, channel_id, comment_video_id)
