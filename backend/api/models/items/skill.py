from django.db import models

from ..base import OrderedSectionItem
from ..section import ResumeSection


class SkillItem(OrderedSectionItem):
    expected_section_type = ResumeSection.SectionType.SKILLS

    section = models.ForeignKey(
        ResumeSection,
        on_delete=models.CASCADE,
        related_name="skill_items",
    )
    name = models.CharField(max_length=80)
    category = models.CharField(max_length=80, blank=True)
    level = models.PositiveSmallIntegerField(blank=True, null=True)
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name
