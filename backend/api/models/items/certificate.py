from django.db import models

from ..base import OrderedSectionItem
from ..section import ResumeSection


class CertificateItem(OrderedSectionItem):
    expected_section_type = ResumeSection.SectionType.CERTIFICATES

    section = models.ForeignKey(
        ResumeSection,
        on_delete=models.CASCADE,
        related_name="certificate_items",
    )
    title = models.CharField(max_length=160)
    issuer = models.CharField(max_length=120, blank=True)
    issue_date = models.DateField(blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)
    credential_id = models.CharField(max_length=120, blank=True)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.title
