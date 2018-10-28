from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.filter(username="erickadmin").exists():
            User.objects.create_superuser("erickadmin", "erick@admin.com", "admin")

        if not User.objects.filter(username="nilooadmin").exists():
            User.objects.create_superuser("nilooadmin", "niloo@admin.com", "admin")

        if not User.objects.filter(username="nancyadmin").exists():
            User.objects.create_superuser("nancyadmin", "nancy@admin.com", "admin")

        if not User.objects.filter(username="graceadmin").exists():
            User.objects.create_superuser("graceadmin", "grace@admin.com", "admin")
