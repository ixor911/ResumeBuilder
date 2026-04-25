from django.db import models

from ..base import OrderedSectionItem
from ..section import ResumeSection


class ExperienceItem(OrderedSectionItem):
    class EmploymentType(models.TextChoices):
        FULL_TIME = "full_time", "Full-time"
        PART_TIME = "part_time", "Part-time"
        CONTRACT = "contract", "Contract"
        FREELANCE = "freelance", "Freelance"
        INTERNSHIP = "internship", "Internship"
        VOLUNTEER = "volunteer", "Volunteer"

    expected_section_type = ResumeSection.SectionType.EXPERIENCE

    section = models.ForeignKey(
        ResumeSection,
        on_delete=models.CASCADE,
        related_name="experience_items",
    )
    position = models.CharField(max_length=120)
    company = models.CharField(max_length=120)
    location = models.CharField(max_length=120, blank=True)
    employment_type = models.CharField(
        max_length=30,
        choices=EmploymentType.choices,
        blank=True,
    )
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.position} at {self.company}"
