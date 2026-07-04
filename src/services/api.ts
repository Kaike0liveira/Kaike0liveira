const API_BASE_URL =
  import.meta.env.VITE_DJANGO_API_BASE_URL ??
  import.meta.env.VITE_API_BASE_URL ??
  'http://localhost:8000/api/v1';

export type MatchResult = 'W' | 'D' | 'L';

export interface DashboardData {
  career: {
    id: number;
    name: string;
    club_name: string;
    cash_balance: string;
  };
  next_match: DashboardMatch | null;
  last_result: (DashboardMatch & { result?: MatchResult }) | null;
  month_highlight: {
    player_id: number;
    player_name: string;
    position: string;
    average_rating: string;
    goals: number;
    assists: number;
  } | null;
  feed: Array<{
    type: string;
    title: string;
    body: string;
  }>;
}

export interface DashboardMatch {
  id: number;
  opponent: string;
  competition: string;
  played_at: string | null;
  home_score: number;
  away_score: number;
  is_home: boolean;
  match_day: number | null;
  ai_summary: string;
}

export interface TacticalFormation {
  id: number;
  career: number;
  career_name: string;
  name: string;
  formation: string;
  positions_json: Record<string, { x: number; y: number }>;
  is_default: boolean;
}

export interface AIChatResponse {
  match_info: {
    opponent: string;
    competition: string;
    goals_for: number;
    goals_against: number;
    is_home: boolean;
    match_day: number;
    ai_summary: string;
    result?: MatchResult;
  };
  player_performances: Array<{
    player_name: string;
    position: string;
    is_starter: boolean;
    minutes_played: number;
    goals: number;
    assists: number;
    rating: number;
    clean_sheet: boolean;
  }>;
}

interface PaginatedResponse<T> {
  results: T[];
}

async function apiRequest<T>(path: string, init: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
      'Accept-Language': navigator.language || 'pt-BR',
      ...init.headers,
    },
  });

  if (!response.ok) {
    const errorBody = await response.json().catch(() => null);
    throw new Error(errorBody?.detail ?? `API request failed with ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export function getDashboardData(careerId: number): Promise<DashboardData> {
  return apiRequest<DashboardData>(`/dashboard/?career_id=${careerId}`);
}

export async function getTacticalFormation(careerId: number): Promise<TacticalFormation | null> {
  const data = await apiRequest<PaginatedResponse<TacticalFormation> | TacticalFormation[]>(
    `/tactical-formations/?career_id=${careerId}`,
  );
  const formations = Array.isArray(data) ? data : data.results;
  return formations.find((formation) => formation.is_default) ?? formations[0] ?? null;
}

export async function updateTacticalFormation(
  careerId: number,
  positionsJson: TacticalFormation['positions_json'],
): Promise<TacticalFormation> {
  const currentFormation = await getTacticalFormation(careerId);
  if (!currentFormation) {
    return apiRequest<TacticalFormation>('/tactical-formations/', {
      method: 'POST',
      body: JSON.stringify({
        career: careerId,
        name: 'Formação principal',
        formation: '4-3-3',
        positions_json: positionsJson,
        is_default: true,
      }),
    });
  }

  return apiRequest<TacticalFormation>(`/tactical-formations/${currentFormation.id}/`, {
    method: 'PATCH',
    body: JSON.stringify({ positions_json: positionsJson }),
  });
}

export function sendAIChatMessage(careerId: number, message: string): Promise<AIChatResponse> {
  return apiRequest<AIChatResponse>('/ai/chat/', {
    method: 'POST',
    body: JSON.stringify({ career_id: careerId, message }),
  });
}
