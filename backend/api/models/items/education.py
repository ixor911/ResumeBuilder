from django.db import models

from ..base import OrderedSectionItem
from ..section import ResumeSection


class EducationItem(OrderedSectionItem):
    expected_section_type = ResumeSection.SectionType.EDUCATION

    section = models.ForeignKey(
        ResumeSection,
        on_delete=models.CASCADE,
        related_name="education_items",
    )
    institution = models.CharField(max_length=160)
    degree = models.CharField(max_length=160, blank=True)
    field_of_study = models.CharField(max_length=160, blank=True)
    location = models.CharField(max_length=120, blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.institution
