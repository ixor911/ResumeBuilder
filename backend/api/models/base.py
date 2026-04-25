from django.core.exceptions import ValidationError
from django.db import models


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class OrderedSectionItem(TimestampedModel):
    expected_section_type = None

    order = models.PositiveIntegerField(default=0)
    is_visible = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ["order", "id"]

    def clean(self):
        super().clean()
        if self.expected_section_type and self.section.type != self.expected_section_type:
            raise ValidationError(
                {
                    "section": (
                        f"This item belongs to the "
                        f"{self.expected_section_type!r} section type."
                    )
                }
            )
