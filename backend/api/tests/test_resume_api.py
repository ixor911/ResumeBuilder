from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from rest_framework.test import APIClient

from api.models import Resume, ResumeProfile, ResumeSection, SkillItem, SummaryItem


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

    def test_guest_cannot_read_private_resume(self):
        resume = Resume.objects.create(
            owner=self.user,
            title="Private Resume",
            is_public=False,
        )

        response = self.client.get(f"/api/resumes/{resume.slug}/")

        self.assertEqual(response.status_code, 404)

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

    def test_non_owner_cannot_edit_public_resume(self):
        other_user = get_user_model().objects.create_user(
            username="bob",
            password="password123",
        )
        resume = Resume.objects.create(owner=self.user, title="Public Resume")

        self.client.force_authenticate(other_user)
        response = self.client.patch(
            f"/api/resumes/{resume.slug}/",
            {"title": "Hijacked"},
            format="json",
        )

        self.assertEqual(response.status_code, 403)
        resume.refresh_from_db()
        self.assertEqual(resume.title, "Public Resume")

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

    def test_hidden_item_is_hidden_from_guest_but_visible_to_owner(self):
        resume = Resume.objects.create(owner=self.user, title="Public Resume")
        resume.ensure_default_sections()
        summary_section = resume.sections.get(type=ResumeSection.SectionType.SUMMARY)
        SummaryItem.objects.create(
            section=summary_section,
            text="Visible summary",
            order=1,
            is_visible=True,
        )
        SummaryItem.objects.create(
            section=summary_section,
            text="Hidden summary",
            order=2,
            is_visible=False,
        )

        guest_response = self.client.get(f"/api/resumes/{resume.slug}/")
        summary_data = next(
            section
            for section in guest_response.data["sections"]
            if section["type"] == ResumeSection.SectionType.SUMMARY
        )
        self.assertEqual(len(summary_data["items"]), 1)
        self.assertEqual(summary_data["items"][0]["text"], "Visible summary")

        self.client.force_authenticate(self.user)
        owner_response = self.client.get(f"/api/resumes/{resume.slug}/")
        owner_summary_data = next(
            section
            for section in owner_response.data["sections"]
            if section["type"] == ResumeSection.SectionType.SUMMARY
        )
        self.assertEqual(len(owner_summary_data["items"]), 2)

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

    def test_owner_can_crud_skill_item_endpoint(self):
        self.client.force_authenticate(self.user)
        resume = Resume.objects.create(owner=self.user, title="Draft Resume")
        resume.ensure_default_sections()
        skills_section = resume.sections.get(type=ResumeSection.SectionType.SKILLS)

        create_response = self.client.post(
            "/api/skill-items/",
            {
                "section": skills_section.id,
                "name": "Python",
                "category": "Backend",
                "level": 5,
                "order": 1,
            },
            format="json",
        )

        self.assertEqual(create_response.status_code, 201)
        item_id = create_response.data["id"]
        self.assertTrue(
            SkillItem.objects.filter(
                id=item_id,
                section=skills_section,
                name="Python",
            ).exists()
        )

        update_response = self.client.patch(
            f"/api/skill-items/{item_id}/",
            {
                "name": "Django",
                "order": 2,
            },
            format="json",
        )

        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.data["name"], "Django")
        self.assertEqual(update_response.data["order"], 2)

        delete_response = self.client.delete(f"/api/skill-items/{item_id}/")

        self.assertEqual(delete_response.status_code, 204)
        self.assertFalse(SkillItem.objects.filter(id=item_id).exists())

    def test_non_owner_cannot_create_item_in_foreign_section(self):
        other_user = get_user_model().objects.create_user(
            username="bob",
            password="password123",
        )
        resume = Resume.objects.create(owner=self.user, title="Draft Resume")
        resume.ensure_default_sections()
        skills_section = resume.sections.get(type=ResumeSection.SectionType.SKILLS)

        self.client.force_authenticate(other_user)
        response = self.client.post(
            "/api/skill-items/",
            {
                "section": skills_section.id,
                "name": "Python",
                "level": 5,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 403)
        self.assertFalse(SkillItem.objects.filter(section=skills_section).exists())

    def test_resume_list_supports_search_and_mine_filter(self):
        other_user = get_user_model().objects.create_user(
            username="bob",
            password="password123",
        )
        Resume.objects.create(owner=self.user, title="Backend Resume", is_public=True)
        Resume.objects.create(owner=other_user, title="Frontend Resume", is_public=True)
        Resume.objects.create(owner=self.user, title="Private Backend Draft", is_public=False)

        search_response = self.client.get("/api/resumes/?search=Frontend")
        self.assertEqual(search_response.status_code, 200)
        self.assertEqual(len(search_response.data), 1)
        self.assertEqual(search_response.data[0]["title"], "Frontend Resume")

        self.client.force_authenticate(self.user)
        mine_response = self.client.get("/api/resumes/?mine=true")
        titles = {item["title"] for item in mine_response.data}
        self.assertEqual(titles, {"Backend Resume", "Private Backend Draft"})

    def test_feature_resume_command_marks_existing_resume_featured(self):
        resume = Resume.objects.create(owner=self.user, title="Public Resume")

        call_command("feature_resume", resume.slug)

        resume.refresh_from_db()
        self.assertTrue(resume.is_featured)
