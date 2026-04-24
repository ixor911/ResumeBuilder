from django.db import models
from . import Resume


class Block(models.Model):
    class Meta:
        abstract = True

    status = models.BooleanField(default=False)
    locked = models.BooleanField(default=False)
    position = models.PositiveSmallIntegerField(default=1)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
