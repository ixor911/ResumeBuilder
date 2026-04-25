from django.db.models import Q
from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied

from api.models import (
    CertificateItem,
    EducationItem,
    ExperienceItem,
    LanguageItem,
    LinkItem,
    ProjectItem,
    Resume,
    ResumeSection,
    SkillItem,
    SummaryItem,
)
from api.permissions import IsOwnerOrPublicReadOnly
from api.serializers import (
    CertificateItemSerializer,
    EducationItemSerializer,
    ExperienceItemSerializer,
    LanguageItemSerializer,
    LinkItemSerializer,
    ProjectItemSerializer,
    ResumeDetailSerializer,
    ResumeListSerializer,
    ResumeSectionSerializer,
    ResumeWriteSerializer,
    SkillItemSerializer,
    SummaryItemSerializer,
)


class PublicOrOwnedQuerysetMixin:
    def public_or_owned_filter(self):
        user = self.request.user
        if user.is_staff:
            return Q()
        if user.is_authenticated:
            return Q(section__resume__owner=user) | Q(
                section__resume__is_public=True,
                section__is_visible=True,
                is_visible=True,
            )
        return Q(
            section__resume__is_public=True,
            section__is_visible=True,
            is_visible=True,
        )

    def check_section_owner(self, section):
        user = self.request.user
        if not user.is_authenticated:
            raise PermissionDenied("Authentication is required.")
        if section.resume.owner != user and not user.is_staff:
            raise PermissionDenied("You can edit only your own resume.")


class ResumeViewSet(viewsets.ModelViewSet):
    lookup_field = "slug"
    permission_classes = [IsOwnerOrPublicReadOnly]

    def get_queryset(self):
        queryset = (
            Resume.objects.select_related("owner", "profile")
            .prefetch_related("sections")
            .order_by("-is_featured", "-updated_at", "title")
        )
        user = self.request.user

        if user.is_staff:
            return queryset
        if user.is_authenticated:
            return queryset.filter(Q(is_public=True) | Q(owner=user))

        return queryset.filter(is_public=True)

    def get_permissions(self):
        if self.action == "create":
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ResumeWriteSerializer
        if self.action == "list":
            return ResumeListSerializer
        return ResumeDetailSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ResumeSectionViewSet(viewsets.ModelViewSet):
    serializer_class = ResumeSectionSerializer
    permission_classes = [IsOwnerOrPublicReadOnly]

    def get_queryset(self):
        queryset = ResumeSection.objects.select_related("resume", "resume__owner").order_by(
            "resume_id",
            "placement",
            "order",
            "id",
        )
        user = self.request.user

        if user.is_staff:
            return queryset
        if user.is_authenticated:
            return queryset.filter(
                Q(resume__owner=user) | Q(resume__is_public=True, is_visible=True)
            )

        return queryset.filter(resume__is_public=True, is_visible=True)

    def perform_create(self, serializer):
        resume = serializer.validated_data["resume"]
        user = self.request.user
        if not user.is_authenticated:
            raise PermissionDenied("Authentication is required.")
        if resume.owner != user and not user.is_staff:
            raise PermissionDenied("You can edit only your own resume.")
        serializer.save()


class SectionItemViewSet(PublicOrOwnedQuerysetMixin, viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrPublicReadOnly]
    model = None

    def get_queryset(self):
        return (
            self.model.objects.select_related(
                "section",
                "section__resume",
                "section__resume__owner",
            )
            .filter(self.public_or_owned_filter())
            .order_by("section_id", "order", "id")
        )

    def perform_create(self, serializer):
        self.check_section_owner(serializer.validated_data["section"])
        serializer.save()


class SummaryItemViewSet(SectionItemViewSet):
    model = SummaryItem
    serializer_class = SummaryItemSerializer


class ExperienceItemViewSet(SectionItemViewSet):
    model = ExperienceItem
    serializer_class = ExperienceItemSerializer


class EducationItemViewSet(SectionItemViewSet):
    model = EducationItem
    serializer_class = EducationItemSerializer


class ProjectItemViewSet(SectionItemViewSet):
    model = ProjectItem
    serializer_class = ProjectItemSerializer


class SkillItemViewSet(SectionItemViewSet):
    model = SkillItem
    serializer_class = SkillItemSerializer


class LanguageItemViewSet(SectionItemViewSet):
    model = LanguageItem
    serializer_class = LanguageItemSerializer


class LinkItemViewSet(SectionItemViewSet):
    model = LinkItem
    serializer_class = LinkItemSerializer


class CertificateItemViewSet(SectionItemViewSet):
    model = CertificateItem
    serializer_class = CertificateItemSerializer
