from django.contrib import admin

from .models import (
    CertificateItem,
    EducationItem,
    ExperienceItem,
    LanguageItem,
    LinkItem,
    ProjectItem,
    Resume,
    ResumeProfile,
    ResumeSection,
    SkillItem,
    SummaryItem,
)


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "slug", "is_public", "is_featured", "updated_at")
    list_filter = ("is_public", "is_featured", "language")
    search_fields = ("title", "slug", "owner__username", "owner__email")
    readonly_fields = ("created_at", "updated_at")


@admin.register(ResumeProfile)
class ResumeProfileAdmin(admin.ModelAdmin):
    list_display = ("resume", "first_name", "last_name", "job_title", "email")
    search_fields = ("first_name", "last_name", "job_title", "email", "resume__title")


@admin.register(ResumeSection)
class ResumeSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "resume", "type", "order", "is_visible", "is_locked")
    list_filter = ("type", "is_visible", "is_locked")
    search_fields = ("title", "resume__title")


class SectionItemAdmin(admin.ModelAdmin):
    list_display = ("__str__", "section", "order", "is_visible", "updated_at")
    list_filter = ("is_visible",)
    readonly_fields = ("created_at", "updated_at")


admin.site.register(SummaryItem, SectionItemAdmin)
admin.site.register(ExperienceItem, SectionItemAdmin)
admin.site.register(EducationItem, SectionItemAdmin)
admin.site.register(ProjectItem, SectionItemAdmin)
admin.site.register(SkillItem, SectionItemAdmin)
admin.site.register(LanguageItem, SectionItemAdmin)
admin.site.register(LinkItem, SectionItemAdmin)
admin.site.register(CertificateItem, SectionItemAdmin)
