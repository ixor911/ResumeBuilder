from django.db import models

from ..base import OrderedSectionItem
from ..section import ResumeSection


class LanguageItem(OrderedSectionItem):
    class Proficiency(models.TextChoices):
        A1 = "a1", "A1"
        A2 = "a2", "A2"
        B1 = "b1", "B1"
        B2 = "b2", "B2"
        C1 = "c1", "C1"
        C2 = "c2", "C2"
        NATIVE = "native", "Native"

    expected_section_type = ResumeSection.SectionType.LANGUAGES

    section = models.ForeignKey(
        ResumeSection,
        on_delete=models.CASCADE,
        related_name="language_items",
    )
    name = models.CharField(max_length=80)
    proficiency = models.CharField(
        max_length=20,
        choices=Proficiency.choices,
        blank=True,
    )

    def __str__(self):
        return self.name
