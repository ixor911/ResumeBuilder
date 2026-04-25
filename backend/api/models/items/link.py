from django.db import models

from ..base import OrderedSectionItem
from ..section import ResumeSection


class LinkItem(OrderedSectionItem):
    expected_section_type = ResumeSection.SectionType.LINKS

    section = models.ForeignKey(
        ResumeSection,
        on_delete=models.CASCADE,
        related_name="link_items",
    )
    label = models.CharField(max_length=80)
    url = models.URLField()
    icon = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.label
