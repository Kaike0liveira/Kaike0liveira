"""Service layer for AI-assisted Tactical Hub match processing."""

import json
import os


TACTICAL_HUB_SYSTEM_PROMPT = """Você é o Diretor Esportivo e Analista Tático do Tactical Hub, um assistente inteligente para o Modo Carreira do EA Sports FC. Seu objetivo é extrair os dados de uma crônica ou mensagem rápida enviada pelo treinador após uma partida e transformá-la em um JSON estrito para atualizar o banco de dados.
Regras de Negócio:
- Mapeie as posições estritamente usando as siglas PT-BR: [GOL, ZAG, LD, LE, ADD, ADE, VOL, MC, MEI, MD, ME, PD, PE, SA, ATA].
- Se o usuário não mencionar a nota de um jogador que fez gol/assistência, assuma 8.0 para gol e 7.5 para assistência. Se não mencionar os minutos, assuma 90.
- Defina o resultado como 'W' (Vitória), 'D' (Empate) ou 'L' (Derrota).
- Escreva uma crônica curta e impactante no campo 'ai_summary' no estilo Globo Esporte."""

MATCH_ANALYSIS_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["match_info", "player_performances"],
    "properties": {
        "match_info": {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "opponent",
                "competition",
                "goals_for",
                "goals_against",
                "is_home",
                "match_day",
                "ai_summary",
            ],
            "properties": {
                "opponent": {"type": "string"},
                "competition": {"type": "string"},
                "goals_for": {"type": "number"},
                "goals_against": {"type": "number"},
                "is_home": {"type": "boolean"},
                "match_day": {"type": "number"},
                "ai_summary": {"type": "string"},
            },
        },
        "player_performances": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "player_name",
                    "position",
                    "is_starter",
                    "minutes_played",
                    "goals",
                    "assists",
                    "rating",
                    "clean_sheet",
                ],
                "properties": {
                    "player_name": {"type": "string"},
                    "position": {
                        "type": "string",
                        "enum": [
                            "GOL",
                            "ZAG",
                            "LD",
                            "LE",
                            "ADD",
                            "ADE",
                            "VOL",
                            "MC",
                            "MEI",
                            "MD",
                            "ME",
                            "PD",
                            "PE",
                            "SA",
                            "ATA",
                        ],
                    },
                    "is_starter": {"type": "boolean"},
                    "minutes_played": {"type": "number"},
                    "goals": {"type": "number"},
                    "assists": {"type": "number"},
                    "rating": {"type": "number"},
                    "clean_sheet": {"type": "boolean"},
                },
            },
        },
    },
}


class AIProcessor:
    """Coordinate OpenAI Structured Outputs for career match updates."""

    def __init__(self, model=None):
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    def process_message(self, *, career_id, message):
        """Convert a coach message into strict structured match JSON."""
        from openai import OpenAI

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.responses.create(
            model=self.model,
            input=[
                {"role": "system", "content": TACTICAL_HUB_SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"career_id={career_id}\nMensagem do treinador: {message}",
                },
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "tactical_hub_match_analysis",
                    "strict": True,
                    "schema": MATCH_ANALYSIS_SCHEMA,
                }
            },
        )
        return json.loads(response.output_text)
