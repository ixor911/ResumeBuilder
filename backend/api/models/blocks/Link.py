from django.db import models
from rest_framework import serializers

from .. import Block


class Link(Block):
    label = models.CharField(max_length=100, blank=True)
    url = models.URLField()


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = '__all__'
