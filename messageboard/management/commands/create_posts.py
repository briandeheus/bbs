import random

from django.core.management.base import BaseCommand
from faker import Faker

from messageboard.models import User
from posts.models import Post  # Update import based on your project


class Command(BaseCommand):
    help = "Creates N number of posts"

    def add_arguments(self, parser):
        parser.add_argument(
            "total", type=int, help="Indicates the number of posts to be created"
        )

    def handle(self, *args, **kwargs):
        fake = Faker()
        total = kwargs["total"]
        users = User.objects.all()

        if not users:
            self.stdout.write(
                self.style.ERROR("No users found. Please create some users first.")
            )
            return

        for i in range(total):
            post = Post(
                title=fake.sentence(),
                body=fake.text(),
                actor=random.choice(users),
                pinned=random.choice([True, False]),
            )
            post.save()
            self.stdout.write(self.style.SUCCESS(f"Post {i + 1} created"))

        self.stdout.write(self.style.SUCCESS(f"{total} posts created successfully"))
