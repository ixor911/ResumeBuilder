from django.db import models
from rest_framework import serializers


class Resume(models.Model):
    name = models.CharField(max_length=100)


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = '__all__'