# intranet_app/management/commands/setup_admin.py
import os
from django.core.management.base import BaseCommand
from intranet_app.models import Mitarbeiter

class Command(BaseCommand):
    help = 'Erstellt den ersten Administrator aus Umgebungsvariablen.'

    def handle(self, *args, **options):
        # 1. Daten sicher aus Render Umgebungsvariablen laden
        admin_username = os.environ.get('ADMIN_USERNAME')
        admin_email = os.environ.get('ADMIN_EMAIL')
        admin_password = os.environ.get('ADMIN_PASSWORD')

        if not admin_username or not admin_password:
            self.stdout.write(self.style.ERROR('ADMIN_USERNAME und ADMIN_PASSWORD Umgebungsvariablen fehlen.'))
            return

        # 2. Prüfen, ob der User bereits existiert
        if not Mitarbeiter.objects.filter(username=admin_username).exists():
            # 3. User erstellen und Kategorie C (HR/GF) zuweisen
            Mitarbeiter.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_password,
                kategorie='C', # Wichtig: Als HR/GF definieren
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write(self.style.SUCCESS(f'Administrator {admin_username} erfolgreich erstellt.'))
        else:
            self.stdout.write(self.style.WARNING(f'Administrator {admin_username} existiert bereits.'))
