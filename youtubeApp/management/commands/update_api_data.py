from django.core.management.base import BaseCommand, CommandError

from youtubeApp.youtube_api_v3 import update_v3_reports
from youtubeApp.youtube_api_v2 import update_v2_reports

# Accesses the youtube api to retrieve and store the required reports. We call
# both a v3 and v2 file for version 3 and version 2 of the api respectively.
class Command(BaseCommand):
    help = 'Gathers data from the specified channel, and video using' + \
        ' the youtube api.'

    def add_arguments(self, parser):
        parser.add_argument('channel_id', type=str)
        parser.add_argument('comment_video_id', type=str)

    def handle(self, *args, **options):
        channel_id = options['channel_id']
        comment_video_id = options['comment_video_id']

        update_v3_reports(channel_id, comment_video_id)
        update_v2_reports(channel_id)

        self.stdout.write(self.style.SUCCESS('Update process complete'))
