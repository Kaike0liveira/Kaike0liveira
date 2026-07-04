"""Signals that keep Tactical Hub aggregate statistics consistent."""

from django.db.models import Avg, Count, Sum
from django.db.models.signals import post_delete, post_save
from django.db.models.functions import Coalesce
from django.dispatch import receiver

from .models import MatchPlayerPerformance, PlayerSeasonStats


def recalculate_player_season_stats(player, season):
    """Recalculate a player's exact aggregated metrics for one season."""
    aggregates = MatchPlayerPerformance.objects.filter(
        player=player,
        match__season=season,
    ).aggregate(
        matches=Count("match", distinct=True),
        goals=Coalesce(Sum("goals"), 0),
        assists=Coalesce(Sum("assists"), 0),
        yellow_cards=Coalesce(Sum("yellow_cards"), 0),
        red_cards=Coalesce(Sum("red_cards"), 0),
        minutes_played=Coalesce(Sum("minutes_played"), 0),
        average_rating=Avg("rating"),
    )

    PlayerSeasonStats.objects.update_or_create(
        player=player,
        season=season,
        defaults={
            "matches": aggregates["matches"],
            "goals": aggregates["goals"],
            "assists": aggregates["assists"],
            "yellow_cards": aggregates["yellow_cards"],
            "red_cards": aggregates["red_cards"],
            "minutes_played": aggregates["minutes_played"],
            "average_rating": aggregates["average_rating"],
        },
    )


@receiver(post_save, sender=MatchPlayerPerformance)
def update_player_season_stats_on_save(sender, instance, **kwargs):
    """Refresh aggregates after a player performance is created or updated."""
    recalculate_player_season_stats(instance.player, instance.match.season)


@receiver(post_delete, sender=MatchPlayerPerformance)
def update_player_season_stats_on_delete(sender, instance, **kwargs):
    """Refresh aggregates after a player performance is deleted."""
    recalculate_player_season_stats(instance.player, instance.match.season)
