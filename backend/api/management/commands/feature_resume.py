from django.core.management.base import BaseCommand, CommandError

from api.models import Resume


class Command(BaseCommand):
    help = "Mark an existing resume as featured by slug."

    def add_arguments(self, parser):
        parser.add_argument("slug", help="Slug of the existing resume.")
        parser.add_argument(
            "--unset",
            action="store_true",
            help="Remove featured status instead of setting it.",
        )
        parser.add_argument(
            "--only",
            action="store_true",
            help="Unset featured status for all other resumes first.",
        )

    def handle(self, *args, **options):
        try:
            resume = Resume.objects.get(slug=options["slug"])
        except Resume.DoesNotExist as exc:
            raise CommandError(f"Resume with slug '{options['slug']}' does not exist.") from exc

        if options["only"] and not options["unset"]:
            Resume.objects.exclude(pk=resume.pk).update(is_featured=False)

        resume.is_featured = not options["unset"]
        resume.save(update_fields=["is_featured", "updated_at"])

        state = "featured" if resume.is_featured else "not featured"
        self.stdout.write(self.style.SUCCESS(f"{resume.slug} is now {state}."))
