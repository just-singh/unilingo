import json

from django.core.management.base import BaseCommand, CommandError

from youtubeApp.models import ReportData, ProcessedData

# This command takes the raw data we've stored from the API calls and Formats
# it into a single JSON block we store. This saves us from having to reprocess
# everytime the data is requested.
class Command(BaseCommand):
    help = 'Formats the raw data and store it.'

    def add_arguments(self, parser):
        parser.add_argument('channel_id', type=str)

    def handle(self, *args, **options):
        channel_id = options['channel_id']

        # Channel Stats Report Data
        channel_stats_report = ReportData.objects.get(channel_id = channel_id,
            report_name = ReportData.CHANNEL_STATS)

        json_data = json.loads(channel_stats_report.data)
        title = json_data['items'][0]['snippet']['title']
        description = json_data['items'][0]['snippet']['description']
        thumbnail = \
            json_data['items'][0]['snippet']['thumbnails']['medium']['url']
        stats_json = json_data['items'][0]['statistics']

        # Video Report Data
        video_stats_report = ReportData.objects.get(channel_id = channel_id,
            report_name = ReportData.VIDEO_STATS)
        video_report_json = json.loads(video_stats_report.data)

        total_likes = 0
        total_dislikes = 0
        for video_data in video_report_json['items']:
            total_likes = total_likes \
                + int(video_data['statistics']['likeCount'])
            total_dislikes = total_dislikes + \
                int(video_data['statistics']['dislikeCount'])

        # If we have no likes and no dislikes we can't generate a graph, return
        # None instead.
        if total_likes == 0 and total_dislikes == 0:
            likes_dislikes_data = None
        else:
            likes_dislikes_data = [{'name': 'Likes', 'value': total_likes},
                {'name': 'Disikes', 'value': total_dislikes}]

        # View TIme Report Data
        view_time_report = ReportData.objects.get(channel_id = channel_id,
            report_name = ReportData.VIEWS_TIME_STATS)
        view_time_json = json.loads(view_time_report.data)
        view_time_data = []
        total_views = 0

        for row in view_time_json['rows']:
            total_views = total_views + int(row[1])
            view_time_data.append({'date': str(row[0]), 'views': total_views})

        # Comment Report Data
        comment_report = ReportData.objects.get(channel_id = channel_id,
            report_name = ReportData.COMMENT_LIST)
        comment_json = json.loads(comment_report.data)
        comment_list = []
        for comment in comment_json['items']:
            comment_text = comment['snippet']['topLevelComment']['snippet']\
                ['textDisplay']
            comment_img = comment['snippet']['topLevelComment']['snippet']\
                ['authorProfileImageUrl']
            comment_name = comment['snippet']['topLevelComment']['snippet']\
                ['authorDisplayName']
            comment_list.append({'name': comment_name, 'thumb': comment_img,
                'text': comment_text})

        # If we have no comments and no views we can't generate a graph, return
        # None instead.
        if int(stats_json['commentCount']) == 0 and \
            int(stats_json['viewCount']) == 0:
            comment_view_data = None
        else:
            comment_view_data = [
                {'name': 'Comments', 'value': int(stats_json['commentCount'])},
                {'name': 'Views', 'value': int(stats_json['viewCount'])}]

        channel_json = {
            'commentCount': stats_json['commentCount'],
            'viewCount': stats_json['viewCount'],
            'subscriberCount': stats_json['subscriberCount'],
            'videoCount': stats_json['videoCount'],
            'title': title,
            'description': description,
            'thumb': thumbnail,
            'likeCount': total_likes,
            'dislikeCount': total_dislikes,
            'likeDislikeData': likes_dislikes_data,
            'commentViewData': comment_view_data,
            'viewTimeData': view_time_data,
            'commentList': comment_list
        }

        processed_data, created = ProcessedData.objects.get_or_create(
          channel_id=channel_id,
          data=json.dumps(channel_json))
        processed_data.save()

        self.stdout.write(self.style.SUCCESS('Data formatting complete.'))
