from django.core.management.base import BaseCommand
from core.models import Department, Rayon


class Command(BaseCommand):
    help = "Initialise les données de base : les 9 rayons et les 7 départements."

    def handle(self, *args, **options):
        rayons = [
            "Beni", "Auberge", "Vungi", "MGL", "Centre ville",
            "Vusenga", "Kitulu", "Mahamba", "Musimba",
        ]
        for nom in rayons:
            obj, created = Rayon.objects.get_or_create(nom=nom)
            self.stdout.write(
                self.style.SUCCESS(f"Rayon '{nom}' {'créé' if created else 'déjà existant'}")
            )

        for nom_code, _ in Department.Nom.choices:
            obj, created = Department.objects.get_or_create(nom=nom_code)
            self.stdout.write(
                self.style.SUCCESS(f"Département '{obj}' {'créé' if created else 'déjà existant'}")
            )

        self.stdout.write(self.style.SUCCESS("Seed terminé."))
