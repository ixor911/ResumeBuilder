from django.db import models

from ..base import OrderedSectionItem
from ..section import ResumeSection


class ProjectItem(OrderedSectionItem):
    expected_section_type = ResumeSection.SectionType.PROJECTS

    section = models.ForeignKey(
        ResumeSection,
        on_delete=models.CASCADE,
        related_name="project_items",
    )
    title = models.CharField(max_length=160)
    role = models.CharField(max_length=120, blank=True)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    tech_stack = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.title
