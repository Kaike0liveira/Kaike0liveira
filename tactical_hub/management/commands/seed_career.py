"""Seed a default Tactical Hub career for local testing."""

from django.core.management.base import BaseCommand
from django.db import transaction

from tactical_hub.models import Career, Player, Season, TacticalFormation


INITIAL_PLAYERS = [
    ("Bento", "GOL", 82, 86, 25),
    ("Yan Couto", "LD", 79, 84, 24),
    ("Murilo", "ZAG", 81, 84, 28),
    ("Beraldo", "ZAG", 78, 86, 22),
    ("Caio Henrique", "LE", 80, 83, 28),
    ("André", "VOL", 82, 86, 24),
    ("João Gomes", "MC", 80, 84, 25),
    ("Claudinho", "MEI", 81, 82, 29),
    ("Savinho", "PD", 79, 87, 22),
    ("Martinelli", "PE", 84, 88, 25),
    ("Rwan Seco", "ATA", 72, 80, 25),
    ("Marcos Leonardo", "ATA", 78, 84, 23),
    ("Vanderson", "LD", 78, 83, 25),
    ("Pablo Maia", "VOL", 77, 83, 24),
    ("Wesley", "PE", 75, 82, 24),
]

DEFAULT_POSITIONS = {
    "GOL": {"x": 50, "y": 92},
    "LD": {"x": 78, "y": 72},
    "ZAG_1": {"x": 40, "y": 75},
    "ZAG_2": {"x": 60, "y": 75},
    "LE": {"x": 22, "y": 72},
    "VOL": {"x": 50, "y": 58},
    "MC_1": {"x": 38, "y": 45},
    "MC_2": {"x": 62, "y": 45},
    "PD": {"x": 78, "y": 25},
    "PE": {"x": 22, "y": 25},
    "ATA": {"x": 50, "y": 18},
}


class Command(BaseCommand):
    """Create a default career, season, squad, and tactical formation."""

    help = "Seed Tactical Hub with one career, one season, and an initial squad."

    @transaction.atomic
    def handle(self, *args, **options):
        career, _ = Career.objects.get_or_create(
            name="Carreira Tactical Hub",
            defaults={
                "club_name": "Tactical FC",
                "manager_name": "Professor",
                "game": "EA Sports FC",
                "cash_balance": 25_000_000,
            },
        )
        season, _ = Season.objects.get_or_create(
            career=career,
            name="2026/27",
            defaults={"year": 2026, "is_current": True},
        )

        created_players = 0
        for name, position, overall, potential, age in INITIAL_PLAYERS:
            _, created = Player.objects.get_or_create(
                career=career,
                name=name,
                defaults={
                    "position": position,
                    "overall": overall,
                    "potential": potential,
                    "age": age,
                    "nationality": "Brasil",
                },
            )
            created_players += int(created)

        TacticalFormation.objects.get_or_create(
            career=career,
            name="4-3-3 Base",
            defaults={
                "formation": "4-3-3",
                "positions_json": DEFAULT_POSITIONS,
                "is_default": True,
            },
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Seed concluído: carreira={career.id}, temporada={season.id}, "
                f"novos_jogadores={created_players}."
            )
        )
