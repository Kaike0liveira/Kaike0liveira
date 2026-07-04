"""Serializers for the Tactical Hub API v1."""

from rest_framework import serializers

from .models import (
    Career,
    Match,
    MatchPlayerPerformance,
    Player,
    PlayerSeasonStats,
    Season,
    TacticalFormation,
)


class CareerSerializer(serializers.ModelSerializer):
    """Serialize career/save metadata."""

    class Meta:
        model = Career
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")


class SeasonSerializer(serializers.ModelSerializer):
    """Serialize seasons belonging to a career."""

    career_name = serializers.CharField(source="career.name", read_only=True)

    class Meta:
        model = Season
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")


class PlayerSerializer(serializers.ModelSerializer):
    """Serialize players scoped to a career."""

    career_name = serializers.CharField(source="career.name", read_only=True)
    position_display = serializers.CharField(source="get_position_display", read_only=True)

    class Meta:
        model = Player
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")


class PlayerSeasonStatsSerializer(serializers.ModelSerializer):
    """Serialize clean aggregated player statistics for a season."""

    player_name = serializers.CharField(source="player.name", read_only=True)
    player_position = serializers.CharField(source="player.position", read_only=True)
    player_position_display = serializers.CharField(
        source="player.get_position_display",
        read_only=True,
    )
    season_name = serializers.CharField(source="season.name", read_only=True)
    career_id = serializers.IntegerField(source="season.career_id", read_only=True)
    goals_per_match = serializers.SerializerMethodField()
    assists_per_match = serializers.SerializerMethodField()
    goal_contributions = serializers.SerializerMethodField()

    class Meta:
        model = PlayerSeasonStats
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")

    def get_goals_per_match(self, obj):
        """Return goals per match rounded to two decimal places."""
        return self._safe_rate(obj.goals, obj.matches)

    def get_assists_per_match(self, obj):
        """Return assists per match rounded to two decimal places."""
        return self._safe_rate(obj.assists, obj.matches)

    def get_goal_contributions(self, obj):
        """Return goals plus assists."""
        return obj.goals + obj.assists

    @staticmethod
    def _safe_rate(value, total):
        """Calculate a per-match rate without division-by-zero errors."""
        if not total:
            return 0
        return round(value / total, 2)


class MatchPlayerPerformanceSerializer(serializers.ModelSerializer):
    """Serialize individual player performance within a match."""

    player_name = serializers.CharField(source="player.name", read_only=True)
    position_display = serializers.CharField(source="get_position_display", read_only=True)
    match_opponent = serializers.CharField(source="match.opponent", read_only=True)
    career_id = serializers.IntegerField(source="match.season.career_id", read_only=True)

    class Meta:
        model = MatchPlayerPerformance
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")


class MatchSerializer(serializers.ModelSerializer):
    """Serialize matches and optional nested player performances."""

    season_name = serializers.CharField(source="season.name", read_only=True)
    career_id = serializers.IntegerField(source="season.career_id", read_only=True)
    player_performances = MatchPlayerPerformanceSerializer(many=True, read_only=True)

    class Meta:
        model = Match
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")


class TacticalFormationSerializer(serializers.ModelSerializer):
    """Serialize tactical formations with validated JSON position data."""

    career_name = serializers.CharField(source="career.name", read_only=True)
    positions_json = serializers.JSONField(required=False)

    class Meta:
        model = TacticalFormation
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")

    def validate_positions_json(self, value):
        """Ensure the tactical positions payload is a JSON object."""
        if value in (None, ""):
            return {}
        if not isinstance(value, dict):
            raise serializers.ValidationError(
                "positions_json deve ser um objeto JSON com as posições táticas."
            )
        return value


class AIChatRequestSerializer(serializers.Serializer):
    """Validate AI chat requests for career-scoped processing."""

    career_id = serializers.IntegerField(min_value=1)
    message = serializers.CharField(allow_blank=False, trim_whitespace=True)

class DashboardSerializer(serializers.Serializer):
    """Serialize the Tactical Hub dashboard payload."""

    career = serializers.DictField()
    next_match = serializers.DictField(allow_null=True)
    last_result = serializers.DictField(allow_null=True)
    month_highlight = serializers.DictField(allow_null=True)
    feed = serializers.ListField(child=serializers.DictField())
