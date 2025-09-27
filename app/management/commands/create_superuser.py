import os
from typing import Any

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help: str = "Create a superuser"

    def handle(self, *args: Any, **options: Any) -> None:
        username: str = os.getenv("DJANGO_SUPERUSER_USERNAME", "ethan")
        password: str = os.getenv("DJANGO_SUPERUSER_PASSWORD", "@100/Chem")
        email: str = os.getenv("DJANGO_SUPERUSER_EMAIL", "ethan@gmail.com")
        first_name: str = os.getenv("DJANGO_SUPERUSER_FIRST_NAME", "Ethan")
        last_name: str = os.getenv("DJANGO_SUPERUSER_LAST_NAME", "Wanyoike")

        if not username or not email or not password:
            raise ValueError(
                "Please provide a username, password, " +
                "and email. Required for account creation."
                )

        # Create the superuser if it doesn't already exist
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username, email=email, password=password,
                first_name=first_name, last_name=last_name
            )
            self.stdout.write(
                msg=f"Superuser `{username}` created successfully.",
                style_func=self.style.SUCCESS
            )
        else:
            self.stdout.write(
                msg=f"Superuser `{username}` already exists. " +
                "Updating details...",
                style_func=self.style.SUCCESS
            )
            User.objects.filter(username=username).update(
                email=email, first_name=first_name, last_name=last_name
            )
            self.stdout.write(
                msg=f"Superuser `{username}` details: updated successfully.",
                style_func=self.style.SUCCESS
            )
