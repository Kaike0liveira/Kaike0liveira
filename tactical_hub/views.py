"""ViewSets for the Tactical Hub API v1."""

from rest_framework import status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .ai_processor import AIProcessor
from .models import (
    Career,
    Match,
    MatchPlayerPerformance,
    Player,
    PlayerSeasonStats,
    Season,
    TacticalFormation,
)
from .serializers import (
    AIChatRequestSerializer,
    CareerSerializer,
    DashboardSerializer,
    MatchPlayerPerformanceSerializer,
    MatchSerializer,
    PlayerSeasonStatsSerializer,
    PlayerSerializer,
    SeasonSerializer,
    TacticalFormationSerializer,
)


class StandardResultsSetPagination(PageNumberPagination):
    """Default lightweight pagination for list endpoints."""

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class CareerViewSet(viewsets.ModelViewSet):
    """CRUD endpoint for careers/saves."""

    queryset = Career.objects.all()
    serializer_class = CareerSerializer
    permission_classes = (IsAuthenticated,)


class SeasonViewSet(viewsets.ModelViewSet):
    """CRUD endpoint for career seasons."""

    serializer_class = SeasonSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Season.objects.select_related("career")
        career_id = self.request.query_params.get("career_id")
        if career_id:
            queryset = queryset.filter(career_id=career_id)
        return queryset


class PlayerViewSet(viewsets.ModelViewSet):
    """CRUD endpoint for players isolated by career."""

    serializer_class = PlayerSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = Player.objects.select_related("career")
        career_id = self.request.query_params.get("career_id")
        if career_id is None:
            return queryset.none()
        return queryset.filter(career_id=career_id)


class PlayerSeasonStatsViewSet(viewsets.ModelViewSet):
    """CRUD endpoint for aggregated player season stats."""

    serializer_class = PlayerSeasonStatsSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = PlayerSeasonStats.objects.select_related(
            "player",
            "season",
            "season__career",
        )
        career_id = self.request.query_params.get("career_id")
        season_id = self.request.query_params.get("season_id")
        player_id = self.request.query_params.get("player_id")

        if career_id is None:
            return queryset.none()

        queryset = queryset.filter(season__career_id=career_id)
        if season_id:
            queryset = queryset.filter(season_id=season_id)
        if player_id:
            queryset = queryset.filter(player_id=player_id)
        return queryset


class MatchViewSet(viewsets.ModelViewSet):
    """CRUD endpoint for matches isolated through season career."""

    serializer_class = MatchSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = Match.objects.select_related("season", "season__career").prefetch_related(
            "player_performances",
            "player_performances__player",
        )
        career_id = self.request.query_params.get("career_id")
        season_id = self.request.query_params.get("season_id")

        if career_id is None:
            return queryset.none()

        queryset = queryset.filter(season__career_id=career_id)
        if season_id:
            queryset = queryset.filter(season_id=season_id)
        return queryset


class MatchPlayerPerformanceViewSet(viewsets.ModelViewSet):
    """CRUD endpoint for match performances isolated through match season career."""

    serializer_class = MatchPlayerPerformanceSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = MatchPlayerPerformance.objects.select_related(
            "match",
            "match__season",
            "match__season__career",
            "player",
        )
        career_id = self.request.query_params.get("career_id")
        match_id = self.request.query_params.get("match_id")
        player_id = self.request.query_params.get("player_id")

        if career_id is None:
            return queryset.none()

        queryset = queryset.filter(match__season__career_id=career_id)
        if match_id:
            queryset = queryset.filter(match_id=match_id)
        if player_id:
            queryset = queryset.filter(player_id=player_id)
        return queryset


class TacticalFormationViewSet(viewsets.ModelViewSet):
    """CRUD endpoint for tactical formations isolated by career."""

    serializer_class = TacticalFormationSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = TacticalFormation.objects.select_related("career")
        career_id = self.request.query_params.get("career_id")
        if career_id is None:
            return queryset.none()
        return queryset.filter(career_id=career_id)


class AIChatView(APIView):
    """Receive user chat messages for career-scoped AI processing."""

    permission_classes = (IsAuthenticated,)
    processor_class = AIProcessor

    def post(self, request, *args, **kwargs):
        """Validate the request and delegate text processing to the service layer."""
        serializer = AIChatRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        career_id = serializer.validated_data["career_id"]
        message = serializer.validated_data["message"]

        if not Career.objects.filter(id=career_id).exists():
            return Response(
                {"detail": "Carreira não encontrada."},
                status=status.HTTP_404_NOT_FOUND,
            )

        result = self.processor_class().process_message(
            career_id=career_id,
            message=message,
        )
        return Response(result, status=status.HTTP_202_ACCEPTED)

class DashboardView(APIView):
    """Return aggregated data for the Tactical Hub dashboard."""

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """Build a career-scoped dashboard payload."""
        career_id = request.query_params.get("career_id")
        if career_id is None:
            return Response(
                {"detail": "career_id é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            career = Career.objects.get(id=career_id)
        except Career.DoesNotExist:
            return Response(
                {"detail": "Carreira não encontrada."},
                status=status.HTTP_404_NOT_FOUND,
            )

        matches = Match.objects.filter(season__career=career).select_related("season")
        last_match = matches.exclude(played_at__isnull=True).order_by("-played_at", "-id").first()
        next_match = matches.filter(played_at__isnull=True).order_by("id").first()
        highlight = (
            PlayerSeasonStats.objects.filter(season__career=career, average_rating__isnull=False)
            .select_related("player")
            .order_by("-average_rating", "-goals", "-assists")
            .first()
        )

        feed = []
        if last_match and last_match.ai_summary:
            feed.append({"type": "ai_summary", "title": "Relatório da IA", "body": last_match.ai_summary})
        if highlight:
            feed.append({
                "type": "highlight",
                "title": "Destaque do mês",
                "body": f"{highlight.player.name} lidera o elenco com média {highlight.average_rating}.",
            })

        payload = {
            "career": {
                "id": career.id,
                "name": career.name,
                "club_name": career.club_name,
                "cash_balance": str(career.cash_balance),
            },
            "next_match": self._serialize_match(next_match),
            "last_result": self._serialize_match(last_match, include_result=True),
            "month_highlight": self._serialize_highlight(highlight),
            "feed": feed,
        }
        serializer = DashboardSerializer(payload)
        return Response(serializer.data)

    @staticmethod
    def _serialize_match(match, include_result=False):
        if match is None:
            return None
        data = {
            "id": match.id,
            "opponent": match.opponent,
            "competition": match.competition,
            "played_at": match.played_at,
            "home_score": match.home_score,
            "away_score": match.away_score,
            "is_home": match.is_home,
            "match_day": match.match_day,
            "ai_summary": match.ai_summary,
        }
        if include_result:
            if match.home_score > match.away_score:
                data["result"] = "W"
            elif match.home_score == match.away_score:
                data["result"] = "D"
            else:
                data["result"] = "L"
        return data

    @staticmethod
    def _serialize_highlight(highlight):
        if highlight is None:
            return None
        return {
            "player_id": highlight.player_id,
            "player_name": highlight.player.name,
            "position": highlight.player.position,
            "average_rating": str(highlight.average_rating),
            "goals": highlight.goals,
            "assists": highlight.assists,
        }
