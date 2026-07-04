"""URL routing for the Tactical Hub API v1."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AIChatView,
    DashboardView,
    CareerViewSet,
    MatchPlayerPerformanceViewSet,
    MatchViewSet,
    PlayerSeasonStatsViewSet,
    PlayerViewSet,
    SeasonViewSet,
    TacticalFormationViewSet,
)

app_name = "tactical_hub"

router = DefaultRouter()
router.register(r"careers", CareerViewSet, basename="career")
router.register(r"seasons", SeasonViewSet, basename="season")
router.register(r"players", PlayerViewSet, basename="player")
router.register(r"player-season-stats", PlayerSeasonStatsViewSet, basename="player-season-stats")
router.register(r"matches", MatchViewSet, basename="match")
router.register(
    r"match-player-performances",
    MatchPlayerPerformanceViewSet,
    basename="match-player-performance",
)
router.register(r"tactical-formations", TacticalFormationViewSet, basename="tactical-formation")

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("ai/chat/", AIChatView.as_view(), name="ai-chat"),
    path("", include(router.urls)),
]
