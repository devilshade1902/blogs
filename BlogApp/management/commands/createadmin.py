from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Creates a superuser without needing the shell'

    def handle(self, *args, **kwargs):
        username = 'admin'  # set your admin username here
        password = 'admin1234'  # set your admin password here
        email = 'dhruvsawant1811@gmail.com'  # set your admin email here

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, password=password, email=email)
            self.stdout.write(self.style.SUCCESS('Superuser created successfully!'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser already exists.'))
