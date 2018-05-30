from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.contrib.postgres.fields import JSONField

# Store the results of our varioius API calls. This is largely kept for
# flexibility allowing us to change the processed data without re-running
# the api calls.
class ReportData(models.Model):
    CHANNEL_STATS = 'CS'
    VIDEO_STATS = 'VS'
    VIEWS_TIME_STATS = 'VTS'
    COMMENT_LIST = 'CL'

    REPORT_CHOICES = (
        (CHANNEL_STATS, 'CS'),
        (VIDEO_STATS, 'VS'),
        (VIEWS_TIME_STATS, 'VTS'),
        (COMMENT_LIST, 'CL'),
    )

    channel_id = models.CharField(max_length=100)
    report_name = models.CharField(max_length=50, choices=REPORT_CHOICES)
    data = models.TextField()

    class Meta:

        # For now we'll only store one of each report for a channel (i.e. we
        # don't keep old logs).
        unique_together = ('channel_id', 'report_name',)

# Store the processed result of ReportData.data. This just serves as a way of
# caching any formatting.
class ProcessedData(models.Model):
    channel_id = models.CharField(primary_key=True, max_length=100)
    data = models.TextField()
