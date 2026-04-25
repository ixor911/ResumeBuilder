from rest_framework import serializers

from api.models import (
    CertificateItem,
    EducationItem,
    ExperienceItem,
    LanguageItem,
    LinkItem,
    ProjectItem,
    ResumeSection,
    SkillItem,
    SummaryItem,
)


class SectionItemSerializer(serializers.ModelSerializer):
    expected_section_type = None

    def validate_section(self, section):
        if self.expected_section_type and section.type != self.expected_section_type:
            raise serializers.ValidationError(
                f"Expected a {self.expected_section_type!r} section."
            )
        return section


class SummaryItemSerializer(SectionItemSerializer):
    expected_section_type = ResumeSection.SectionType.SUMMARY

    class Meta:
        model = SummaryItem
        fields = [
            "id",
            "section",
            "text",
            "order",
            "is_visible",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class ExperienceItemSerializer(SectionItemSerializer):
    expected_section_type = ResumeSection.SectionType.EXPERIENCE

    class Meta:
        model = ExperienceItem
        fields = [
            "id",
            "section",
            "position",
            "company",
            "location",
            "employment_type",
            "start_date",
            "end_date",
            "is_current",
            "description",
            "order",
            "is_visible",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class EducationItemSerializer(SectionItemSerializer):
    expected_section_type = ResumeSection.SectionType.EDUCATION

    class Meta:
        model = EducationItem
        fields = [
            "id",
            "section",
            "institution",
            "degree",
            "field_of_study",
            "location",
            "start_date",
            "end_date",
            "is_current",
            "description",
            "order",
            "is_visible",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class ProjectItemSerializer(SectionItemSerializer):
    expected_section_type = ResumeSection.SectionType.PROJECTS

    class Meta:
        model = ProjectItem
        fields = [
            "id",
            "section",
            "title",
            "role",
            "description",
            "url",
            "start_date",
            "end_date",
            "is_featured",
            "tech_stack",
            "order",
            "is_visible",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class SkillItemSerializer(SectionItemSerializer):
    expected_section_type = ResumeSection.SectionType.SKILLS

    class Meta:
        model = SkillItem
        fields = [
            "id",
            "section",
            "name",
            "category",
            "level",
            "description",
            "order",
            "is_visible",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_level(self, value):
        if value is not None and not 1 <= value <= 5:
            raise serializers.ValidationError("Skill level must be between 1 and 5.")
        return value


class LanguageItemSerializer(SectionItemSerializer):
    expected_section_type = ResumeSection.SectionType.LANGUAGES

    class Meta:
        model = LanguageItem
        fields = [
            "id",
            "section",
            "name",
            "proficiency",
            "order",
            "is_visible",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class LinkItemSerializer(SectionItemSerializer):
    expected_section_type = ResumeSection.SectionType.LINKS

    class Meta:
        model = LinkItem
        fields = [
            "id",
            "section",
            "label",
            "url",
            "icon",
            "order",
            "is_visible",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class CertificateItemSerializer(SectionItemSerializer):
    expected_section_type = ResumeSection.SectionType.CERTIFICATES

    class Meta:
        model = CertificateItem
        fields = [
            "id",
            "section",
            "title",
            "issuer",
            "issue_date",
            "expiration_date",
            "credential_id",
            "url",
            "order",
            "is_visible",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


SECTION_ITEM_SERIALIZERS = {
    ResumeSection.SectionType.SUMMARY: (SummaryItem, SummaryItemSerializer),
    ResumeSection.SectionType.EXPERIENCE: (ExperienceItem, ExperienceItemSerializer),
    ResumeSection.SectionType.EDUCATION: (EducationItem, EducationItemSerializer),
    ResumeSection.SectionType.PROJECTS: (ProjectItem, ProjectItemSerializer),
    ResumeSection.SectionType.SKILLS: (SkillItem, SkillItemSerializer),
    ResumeSection.SectionType.LANGUAGES: (LanguageItem, LanguageItemSerializer),
    ResumeSection.SectionType.LINKS: (LinkItem, LinkItemSerializer),
    ResumeSection.SectionType.CERTIFICATES: (CertificateItem, CertificateItemSerializer),
}
