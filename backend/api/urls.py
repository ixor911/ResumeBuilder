from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CertificateItemViewSet,
    EducationItemViewSet,
    ExperienceItemViewSet,
    LanguageItemViewSet,
    LinkItemViewSet,
    ProjectItemViewSet,
    ResumeSectionViewSet,
    ResumeViewSet,
    SkillItemViewSet,
    SummaryItemViewSet,
)

router = DefaultRouter()
router.register("resumes", ResumeViewSet, basename="resume")
router.register("sections", ResumeSectionViewSet, basename="section")
router.register("summary-items", SummaryItemViewSet, basename="summary-item")
router.register("experience-items", ExperienceItemViewSet, basename="experience-item")
router.register("education-items", EducationItemViewSet, basename="education-item")
router.register("project-items", ProjectItemViewSet, basename="project-item")
router.register("skill-items", SkillItemViewSet, basename="skill-item")
router.register("language-items", LanguageItemViewSet, basename="language-item")
router.register("link-items", LinkItemViewSet, basename="link-item")
router.register("certificate-items", CertificateItemViewSet, basename="certificate-item")

urlpatterns = [
    path("", include(router.urls)),
]
