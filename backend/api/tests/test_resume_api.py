from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from api.models import Resume, ResumeProfile, ResumeSection


class ResumeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="alice",
            password="password123",
        )

    def test_authenticated_user_can_create_resume_with_default_sections(self):
        self.client.force_authenticate(self.user)

        response = self.client.post(
            "/api/resumes/",
            {
                "title": "Alice Developer",
                "profile": {
                    "first_name": "Alice",
                    "job_title": "Backend Developer",
                },
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        resume = Resume.objects.get(title="Alice Developer")
        self.assertEqual(resume.owner, self.user)
        self.assertTrue(ResumeProfile.objects.filter(resume=resume).exists())
        self.assertEqual(ResumeSection.objects.filter(resume=resume).count(), 8)
        placements = dict(
            ResumeSection.objects.filter(resume=resume).values_list("type", "placement")
        )
        self.assertEqual(
            placements[ResumeSection.SectionType.SUMMARY],
            ResumeSection.Placement.MAIN,
        )
        self.assertEqual(
            placements[ResumeSection.SectionType.SKILLS],
            ResumeSection.Placement.SIDEBAR,
        )
        self.assertEqual(
            placements[ResumeSection.SectionType.LINKS],
            ResumeSection.Placement.SIDEBAR,
        )

    def test_guest_can_read_public_resume(self):
        resume = Resume.objects.create(owner=self.user, title="Public Resume")
        ResumeProfile.objects.create(resume=resume, first_name="Alice")
        resume.ensure_default_sections()

        response = self.client.get(f"/api/resumes/{resume.slug}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Public Resume")
        self.assertIn("sections", response.data)

    def test_guest_cannot_create_resume(self):
        response = self.client.post(
            "/api/resumes/",
            {"title": "Unauthorized"},
            format="json",
        )

        self.assertEqual(response.status_code, 401)

    def test_user_can_register_and_use_jwt_to_create_resume(self):
        register_response = self.client.post(
            "/api/auth/register/",
            {
                "username": "charlie",
                "email": "charlie@example.com",
                "password": "strong-password-123",
            },
            format="json",
        )

        self.assertEqual(register_response.status_code, 201)
        self.assertIn("access", register_response.data)
        self.assertIn("refresh", register_response.data)
        self.assertNotIn("first_name", register_response.data["user"])
        self.assertNotIn("last_name", register_response.data["user"])

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {register_response.data['access']}"
        )
        create_response = self.client.post(
            "/api/resumes/",
            {"title": "Charlie's Resume"},
            format="json",
        )

        self.assertEqual(create_response.status_code, 201)
        self.assertTrue(Resume.objects.filter(title="Charlie's Resume").exists())

    def test_non_owner_cannot_read_hidden_public_section(self):
        other_user = get_user_model().objects.create_user(
            username="bob",
            password="password123",
        )
        resume = Resume.objects.create(owner=self.user, title="Public Resume")
        hidden_section = ResumeSection.objects.create(
            resume=resume,
            type=ResumeSection.SectionType.SUMMARY,
            title="Hidden Summary",
            is_visible=False,
        )

        self.client.force_authenticate(other_user)
        response = self.client.get(f"/api/sections/{hidden_section.id}/")

        self.assertEqual(response.status_code, 404)

    def test_summary_section_cannot_be_placed_in_sidebar(self):
        self.client.force_authenticate(self.user)
        resume = Resume.objects.create(owner=self.user, title="Public Resume")

        response = self.client.post(
            "/api/sections/",
            {
                "resume": resume.id,
                "type": ResumeSection.SectionType.SUMMARY,
                "placement": ResumeSection.Placement.SIDEBAR,
                "title": "Summary",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("placement", response.data)

    def test_skill_section_can_be_placed_in_main(self):
        self.client.force_authenticate(self.user)
        resume = Resume.objects.create(owner=self.user, title="Public Resume")

        response = self.client.post(
            "/api/sections/",
            {
                "resume": resume.id,
                "type": ResumeSection.SectionType.SKILLS,
                "placement": ResumeSection.Placement.MAIN,
                "title": "Technical Skills",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["placement"], ResumeSection.Placement.MAIN)
