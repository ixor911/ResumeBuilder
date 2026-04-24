from django.db import models
from rest_framework import serializers

from .. import Block


class Summary(Block):
    label = models.CharField(max_length=50, blank=False, default='Summary')
    text = models.TextField(blank=True)


class SummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Summary
        fields = '__all__'