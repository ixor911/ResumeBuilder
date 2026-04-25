from django.conf import settings
from django.db import models
from django.utils.text import slugify

from .base import TimestampedModel
from .section import ResumeSection


class Resume(TimestampedModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="resumes",
    )
    title = models.CharField(max_length=120, default="Untitled resume")
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    language = models.CharField(max_length=10, default="en")
    is_public = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["-is_featured", "-updated_at", "title"]
        indexes = [
            models.Index(fields=["is_public", "is_featured"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._build_unique_slug()
        super().save(*args, **kwargs)

    def _build_unique_slug(self):
        base_slug = slugify(self.title) or "resume"
        slug = base_slug[:120]
        counter = 2

        while Resume.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            suffix = f"-{counter}"
            slug = f"{base_slug[: 140 - len(suffix)]}{suffix}"
            counter += 1

        return slug

    def ensure_default_sections(self):
        defaults = [
            (ResumeSection.SectionType.SUMMARY, "Summary", ResumeSection.Placement.MAIN, 1),
            (
                ResumeSection.SectionType.EXPERIENCE,
                "Experience",
                ResumeSection.Placement.MAIN,
                2,
            ),
            (ResumeSection.SectionType.PROJECTS, "Projects", ResumeSection.Placement.MAIN, 3),
            (
                ResumeSection.SectionType.EDUCATION,
                "Education",
                ResumeSection.Placement.MAIN,
                4,
            ),
            (
                ResumeSection.SectionType.CERTIFICATES,
                "Certificates",
                ResumeSection.Placement.MAIN,
                5,
            ),
            (ResumeSection.SectionType.LINKS, "Links", ResumeSection.Placement.SIDEBAR, 1),
            (ResumeSection.SectionType.SKILLS, "Skills", ResumeSection.Placement.SIDEBAR, 2),
            (
                ResumeSection.SectionType.LANGUAGES,
                "Languages",
                ResumeSection.Placement.SIDEBAR,
                3,
            ),
        ]

        for section_type, title, placement, order in defaults:
            ResumeSection.objects.get_or_create(
                resume=self,
                type=section_type,
                defaults={"title": title, "placement": placement, "order": order},
            )

