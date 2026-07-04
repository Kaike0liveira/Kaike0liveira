"""Core domain models for Tactical Hub career mode data."""

from django.db import models
from django.utils.translation import gettext_lazy as _


class TimestampedModel(models.Model):
    """Abstract base model with creation and update timestamps."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Career(TimestampedModel):
    """Represents a single isolated career/save."""

    name = models.CharField(_("nome"), max_length=120)
    club_name = models.CharField(_("clube"), max_length=120)
    manager_name = models.CharField(_("treinador"), max_length=120, blank=True)
    game = models.CharField(_("jogo"), max_length=80, blank=True)
    cash_balance = models.DecimalField(_("saldo em caixa"), max_digits=14, decimal_places=2, default=0)
    is_active = models.BooleanField(_("ativa"), default=True)

    class Meta:
        ordering = ["name"]
        verbose_name = _("carreira")
        verbose_name_plural = _("carreiras")

    def __str__(self):
        return self.name


class Season(TimestampedModel):
    """Represents one season inside a career."""

    career = models.ForeignKey(Career, related_name="seasons", on_delete=models.CASCADE)
    name = models.CharField(_("temporada"), max_length=40)
    year = models.PositiveSmallIntegerField(_("ano"), null=True, blank=True)
    is_current = models.BooleanField(_("temporada atual"), default=False)

    class Meta:
        ordering = ["career_id", "-year", "-id"]
        unique_together = [("career", "name")]
        verbose_name = _("temporada")
        verbose_name_plural = _("temporadas")

    def __str__(self):
        return f"{self.career} - {self.name}"


class Player(TimestampedModel):
    """Represents a football player scoped to a career."""

    class Position(models.TextChoices):
        GOL = "GOL", _("Goleiro")
        LD = "LD", _("Lateral direito")
        ZAG = "ZAG", _("Zagueiro")
        LE = "LE", _("Lateral esquerdo")
        ADD = "ADD", _("Ala direito")
        ADE = "ADE", _("Ala esquerdo")
        VOL = "VOL", _("Volante")
        MC = "MC", _("Meio-campista")
        MEI = "MEI", _("Meia")
        MD = "MD", _("Meia direita")
        ME = "ME", _("Meia esquerda")
        PE = "PE", _("Ponta esquerda")
        PD = "PD", _("Ponta direita")
        SA = "SA", _("Segundo atacante")
        ATA = "ATA", _("Atacante")

    career = models.ForeignKey(Career, related_name="players", on_delete=models.CASCADE)
    name = models.CharField(_("nome"), max_length=120)
    position = models.CharField(_("posição"), max_length=4, choices=Position.choices)
    overall = models.PositiveSmallIntegerField(_("overall"), null=True, blank=True)
    potential = models.PositiveSmallIntegerField(_("potencial"), null=True, blank=True)
    age = models.PositiveSmallIntegerField(_("idade"), null=True, blank=True)
    nationality = models.CharField(_("nacionalidade"), max_length=80, blank=True)
    is_active = models.BooleanField(_("ativo"), default=True)

    class Meta:
        ordering = ["name"]
        verbose_name = _("jogador")
        verbose_name_plural = _("jogadores")

    def __str__(self):
        return self.name


class PlayerSeasonStats(TimestampedModel):
    """Aggregated player statistics for one season."""

    player = models.ForeignKey(Player, related_name="season_stats", on_delete=models.CASCADE)
    season = models.ForeignKey(Season, related_name="player_stats", on_delete=models.CASCADE)
    matches = models.PositiveSmallIntegerField(_("jogos"), default=0)
    goals = models.PositiveSmallIntegerField(_("gols"), default=0)
    assists = models.PositiveSmallIntegerField(_("assistências"), default=0)
    clean_sheets = models.PositiveSmallIntegerField(_("jogos sem sofrer gols"), default=0)
    yellow_cards = models.PositiveSmallIntegerField(_("cartões amarelos"), default=0)
    red_cards = models.PositiveSmallIntegerField(_("cartões vermelhos"), default=0)
    average_rating = models.DecimalField(_("nota média"), max_digits=4, decimal_places=2, null=True, blank=True)
    minutes_played = models.PositiveIntegerField(_("minutos jogados"), default=0)

    class Meta:
        ordering = ["season_id", "player__name"]
        unique_together = [("player", "season")]
        verbose_name = _("estatística por temporada")
        verbose_name_plural = _("estatísticas por temporada")

    def __str__(self):
        return f"{self.player} - {self.season}"


class Match(TimestampedModel):
    """Represents a match in a season."""

    season = models.ForeignKey(Season, related_name="matches", on_delete=models.CASCADE)
    opponent = models.CharField(_("adversário"), max_length=120)
    played_at = models.DateField(_("data da partida"), null=True, blank=True)
    competition = models.CharField(_("competição"), max_length=120, blank=True)
    home_score = models.PositiveSmallIntegerField(_("gols do time"), default=0)
    away_score = models.PositiveSmallIntegerField(_("gols do adversário"), default=0)
    is_home = models.BooleanField(_("mandante"), default=True)
    match_day = models.PositiveSmallIntegerField(_("rodada"), null=True, blank=True)
    ai_summary = models.TextField(_("resumo da IA"), blank=True)

    class Meta:
        ordering = ["-played_at", "-id"]
        verbose_name = _("partida")
        verbose_name_plural = _("partidas")

    def __str__(self):
        return f"{self.season} x {self.opponent}"


class MatchPlayerPerformance(TimestampedModel):
    """Individual player performance in a match."""

    match = models.ForeignKey(Match, related_name="player_performances", on_delete=models.CASCADE)
    player = models.ForeignKey(Player, related_name="match_performances", on_delete=models.CASCADE)
    position = models.CharField(_("posição"), max_length=4, choices=Player.Position.choices)
    goals = models.PositiveSmallIntegerField(_("gols"), default=0)
    assists = models.PositiveSmallIntegerField(_("assistências"), default=0)
    rating = models.DecimalField(_("nota"), max_digits=4, decimal_places=2, null=True, blank=True)
    yellow_cards = models.PositiveSmallIntegerField(_("cartões amarelos"), default=0)
    red_cards = models.PositiveSmallIntegerField(_("cartões vermelhos"), default=0)
    minutes_played = models.PositiveSmallIntegerField(_("minutos jogados"), default=90)

    class Meta:
        ordering = ["match_id", "player__name"]
        unique_together = [("match", "player")]
        verbose_name = _("performance na partida")
        verbose_name_plural = _("performances na partida")

    def __str__(self):
        return f"{self.player} - {self.match}"


class TacticalFormation(TimestampedModel):
    """Tactical setup scoped to a career."""

    career = models.ForeignKey(Career, related_name="tactical_formations", on_delete=models.CASCADE)
    name = models.CharField(_("nome"), max_length=120)
    formation = models.CharField(_("formação"), max_length=20)
    positions_json = models.JSONField(_("posições"), default=dict, blank=True)
    is_default = models.BooleanField(_("padrão"), default=False)

    class Meta:
        ordering = ["career_id", "name"]
        verbose_name = _("formação tática")
        verbose_name_plural = _("formações táticas")

    def __str__(self):
        return f"{self.name} ({self.formation})"
