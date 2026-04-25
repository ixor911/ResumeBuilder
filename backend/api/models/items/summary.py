from django.db import models

from ..base import OrderedSectionItem
from ..section import ResumeSection


class SummaryItem(OrderedSectionItem):
    expected_section_type = ResumeSection.SectionType.SUMMARY

    section = models.ForeignKey(
        ResumeSection,
        on_delete=models.CASCADE,
        related_name="summary_items",
    )
    text = models.TextField(blank=True)

    def __str__(self):
        return self.text[:60] or "Summary item"
