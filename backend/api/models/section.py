from django.core.exceptions import ValidationError
from django.db import models

from .base import TimestampedModel


class ResumeSection(TimestampedModel):
    class SectionType(models.TextChoices):
        SUMMARY = "summary", "Summary"
        EXPERIENCE = "experience", "Experience"
        EDUCATION = "education", "Education"
        PROJECTS = "projects", "Projects"
        SKILLS = "skills", "Skills"
        LANGUAGES = "languages", "Languages"
        LINKS = "links", "Links"
        CERTIFICATES = "certificates", "Certificates"
        CUSTOM = "custom", "Custom"

    class Placement(models.TextChoices):
        MAIN = "main", "Main"
        SIDEBAR = "sidebar", "Sidebar"

    ALLOWED_PLACEMENTS = {
        SectionType.SUMMARY: {Placement.MAIN},
        SectionType.EXPERIENCE: {Placement.MAIN},
        SectionType.EDUCATION: {Placement.MAIN},
        SectionType.PROJECTS: {Placement.MAIN},
        SectionType.SKILLS: {Placement.MAIN, Placement.SIDEBAR},
        SectionType.LANGUAGES: {Placement.MAIN, Placement.SIDEBAR},
        SectionType.LINKS: {Placement.MAIN, Placement.SIDEBAR},
        SectionType.CERTIFICATES: {Placement.MAIN, Placement.SIDEBAR},
        SectionType.CUSTOM: {Placement.MAIN, Placement.SIDEBAR},
    }

    resume = models.ForeignKey(
        "api.Resume",
        on_delete=models.CASCADE,
        related_name="sections",
    )
    type = models.CharField(max_length=30, choices=SectionType.choices)
    placement = models.CharField(
        max_length=20,
        choices=Placement.choices,
        default=Placement.MAIN,
    )
    title = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)
    is_visible = models.BooleanField(default=True)
    is_locked = models.BooleanField(default=False)

    class Meta:
        ordering = ["placement", "order", "id"]
        indexes = [
            models.Index(fields=["resume", "order"]),
            models.Index(fields=["resume", "placement", "order"]),
            models.Index(fields=["type"]),
        ]

    def __str__(self):
        return f"{self.resume}: {self.title}"

    @classmethod
    def allowed_placements_for(cls, section_type):
        return cls.ALLOWED_PLACEMENTS.get(section_type, {cls.Placement.MAIN})

    def clean(self):
        super().clean()
        allowed_placements = self.allowed_placements_for(self.type)
        if self.placement not in allowed_placements:
            raise ValidationError(
                {
                    "placement": (
                        f"{self.type!r} section cannot be placed in "
                        f"{self.placement!r}."
                    )
                }
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
