import os

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Create the Django superuser if it does not already exist"

    def handle(self, *args, **kwargs):

        username = os.environ.get(
            "DJANGO_SUPERUSER_USERNAME",
            "admin"
        )

        email = os.environ.get(
            "DJANGO_SUPERUSER_EMAIL",
            ""
        )

        password = os.environ.get(
            "DJANGO_SUPERUSER_PASSWORD",
            "admin123"
        )

        if User.objects.filter(username=username).exists():

            self.stdout.write(
                self.style.WARNING(
                    f"Superuser '{username}' already exists."
                )
            )

            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Superuser '{username}' created successfully."
            )
        )