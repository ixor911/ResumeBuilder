from django.db import models

from .base import TimestampedModel


class ResumeProfile(TimestampedModel):
    resume = models.OneToOneField(
        "api.Resume",
        on_delete=models.CASCADE,
        related_name="profile",
    )
    first_name = models.CharField(max_length=80, blank=True)
    last_name = models.CharField(max_length=80, blank=True)
    job_title = models.CharField(max_length=120, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=80, blank=True)
    city = models.CharField(max_length=80, blank=True)
    avatar = models.FileField(upload_to="resume_avatars/", blank=True, null=True)

    class Meta:
        ordering = ["resume_id"]

    def __str__(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or f"Profile for {self.resume}"
