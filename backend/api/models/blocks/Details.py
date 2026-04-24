from django.db import models
from rest_framework import serializers

from .. import Block, Resume


class Details(Block):
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE, primary_key=True)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True)
    job_title = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=50, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    image = models.ImageField(max_length=50, blank=True, null=True)




class DetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Details
        fields = '__all__'

