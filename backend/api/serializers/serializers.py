from rest_framework import serializers

from api.models import (
    Resume,
    ResumeProfile,
    ResumeSection,
)

from .item_serializers import SECTION_ITEM_SERIALIZERS


class ResumeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeProfile
        fields = [
            "id",
            "first_name",
            "last_name",
            "job_title",
            "email",
            "phone",
            "country",
            "city",
            "avatar",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class ResumeSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeSection
        fields = [
            "id",
            "resume",
            "type",
            "placement",
            "title",
            "order",
            "is_visible",
            "is_locked",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, attrs):
        section_type = attrs.get("type", getattr(self.instance, "type", None))
        placement = attrs.get(
            "placement",
            getattr(self.instance, "placement", ResumeSection.Placement.MAIN),
        )

        if placement not in ResumeSection.allowed_placements_for(section_type):
            raise serializers.ValidationError(
                {
                    "placement": (
                        f"{section_type!r} section cannot be placed in "
                        f"{placement!r}."
                    )
                }
            )

        return attrs


class ResumeListSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    profile = ResumeProfileSerializer(read_only=True)

    class Meta:
        model = Resume
        fields = [
            "id",
            "owner",
            "title",
            "slug",
            "language",
            "is_public",
            "is_featured",
            "profile",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "owner",
            "slug",
            "is_featured",
            "created_at",
            "updated_at",
        ]


class ResumeDetailSerializer(ResumeListSerializer):
    sections = serializers.SerializerMethodField()

    class Meta(ResumeListSerializer.Meta):
        fields = ResumeListSerializer.Meta.fields + ["sections"]

    def get_sections(self, resume):
        request = self.context.get("request")
        is_owner = (
            request
            and request.user.is_authenticated
            and (request.user == resume.owner or request.user.is_staff)
        )

        sections = resume.sections.all().order_by("placement", "order", "id")
        if not is_owner:
            sections = sections.filter(is_visible=True)

        payload = []
        for section in sections:
            section_data = ResumeSectionSerializer(section, context=self.context).data
            item_model, item_serializer = SECTION_ITEM_SERIALIZERS.get(
                section.type,
                (None, None),
            )
            if item_model:
                items = item_model.objects.filter(section=section).order_by("order", "id")
                if not is_owner:
                    items = items.filter(is_visible=True)
                section_data["items"] = item_serializer(
                    items,
                    many=True,
                    context=self.context,
                ).data
            else:
                section_data["items"] = []
            payload.append(section_data)

        return payload


class ResumeWriteSerializer(serializers.ModelSerializer):
    profile = ResumeProfileSerializer(required=False)

    class Meta:
        model = Resume
        fields = [
            "id",
            "title",
            "slug",
            "language",
            "is_public",
            "is_featured",
            "profile",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "slug", "is_featured", "created_at", "updated_at"]

    def create(self, validated_data):
        profile_data = validated_data.pop("profile", {})
        resume = Resume.objects.create(**validated_data)
        ResumeProfile.objects.create(resume=resume, **profile_data)
        resume.ensure_default_sections()
        return resume

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", None)
        resume = super().update(instance, validated_data)

        if profile_data is not None:
            profile, _ = ResumeProfile.objects.get_or_create(resume=resume)
            for field, value in profile_data.items():
                setattr(profile, field, value)
            profile.save()

        return resume
