import { useEffect, useMemo, useState } from 'react';
import { DashboardData, getDashboardData, MatchResult } from '../services/api';

interface DashboardProps {
  careerId: number;
}

const resultStyles: Record<MatchResult, string> = {
  W: 'border-emerald-400/40 bg-emerald-400/10 text-emerald-300',
  D: 'border-zinc-400/40 bg-zinc-400/10 text-zinc-200',
  L: 'border-rose-400/40 bg-rose-400/10 text-rose-300',
};

const resultLabels: Record<MatchResult, string> = {
  W: 'Vitória',
  D: 'Empate',
  L: 'Derrota',
};

function formatCurrency(value?: string): string {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'EUR',
    maximumFractionDigits: 0,
  }).format(Number(value ?? 0));
}

export function Dashboard({ careerId }: DashboardProps) {
  const [dashboard, setDashboard] = useState<DashboardData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;

    getDashboardData(careerId)
      .then((data) => {
        if (isMounted) {
          setDashboard(data);
          setError(null);
        }
      })
      .catch((apiError: Error) => {
        if (isMounted) {
          setError(apiError.message);
        }
      })
      .finally(() => {
        if (isMounted) {
          setIsLoading(false);
        }
      });

    return () => {
      isMounted = false;
    };
  }, [careerId]);

  const automaticNews = useMemo(() => {
    if (!dashboard?.month_highlight) {
      return 'Elenco em avaliação: dispute partidas para liberar relatórios inteligentes.';
    }

    return `${dashboard.month_highlight.player_name} virou termômetro do time com média ${dashboard.month_highlight.average_rating}.`;
  }, [dashboard]);

  if (isLoading) {
    return <div className="min-h-screen bg-black p-8 text-zinc-300">Carregando Tactical Hub...</div>;
  }

  if (error || !dashboard) {
    return <div className="min-h-screen bg-black p-8 text-rose-300">Erro ao carregar dashboard: {error}</div>;
  }

  const result = dashboard.last_result?.result;

  return (
    <main className="min-h-screen bg-[#030305] text-zinc-100">
      <section className="mx-auto grid max-w-7xl grid-cols-1 gap-6 px-6 py-8 lg:grid-cols-[1fr_360px]">
        <div className="space-y-6">
          <header className="rounded-[2rem] border border-white/10 bg-white/[0.03] p-8 shadow-2xl shadow-black/40">
            <p className="text-xs font-semibold uppercase tracking-[0.4em] text-emerald-300">Tactical Hub</p>
            <div className="mt-4 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
              <div>
                <h1 className="text-4xl font-black tracking-tight md:text-6xl">{dashboard.career.club_name}</h1>
                <p className="mt-2 text-sm text-zinc-400">{dashboard.career.name}</p>
              </div>
              <div className="rounded-2xl border border-emerald-400/20 bg-emerald-400/10 px-5 py-4 text-right">
                <p className="text-xs uppercase tracking-[0.25em] text-emerald-200/70">Saldo em caixa</p>
                <strong className="text-2xl text-emerald-200">{formatCurrency(dashboard.career.cash_balance)}</strong>
              </div>
            </div>
          </header>

          <div className="grid gap-4 md:grid-cols-3">
            <article className="rounded-3xl border border-white/10 bg-zinc-950/80 p-6">
              <p className="text-xs uppercase tracking-[0.25em] text-zinc-500">Próximo compromisso</p>
              <h2 className="mt-4 text-2xl font-bold">{dashboard.next_match?.opponent ?? 'A definir'}</h2>
              <p className="mt-2 text-sm text-zinc-400">{dashboard.next_match?.competition ?? 'Calendário pendente'}</p>
            </article>

            <article className="rounded-3xl border border-white/10 bg-zinc-950/80 p-6">
              <p className="text-xs uppercase tracking-[0.25em] text-zinc-500">Último resultado</p>
              <h2 className="mt-4 text-2xl font-bold">{dashboard.last_result?.opponent ?? 'Sem jogos'}</h2>
              {dashboard.last_result && (
                <div className="mt-3 flex items-center justify-between">
                  <span className="text-xl font-black">
                    {dashboard.last_result.home_score} x {dashboard.last_result.away_score}
                  </span>
                  {result && (
                    <span className={`rounded-full border px-3 py-1 text-xs font-bold ${resultStyles[result]}`}>
                      {resultLabels[result]}
                    </span>
                  )}
                </div>
              )}
            </article>

            <article className="rounded-3xl border border-amber-300/20 bg-amber-300/10 p-6">
              <p className="text-xs uppercase tracking-[0.25em] text-amber-200/70">Destaque do mês</p>
              <h2 className="mt-4 text-2xl font-bold">{dashboard.month_highlight?.player_name ?? 'Em aberto'}</h2>
              <p className="mt-2 text-sm text-amber-100/70">
                {dashboard.month_highlight
                  ? `${dashboard.month_highlight.position} · Média ${dashboard.month_highlight.average_rating}`
                  : 'Aguardando estatísticas'}
              </p>
            </article>
          </div>
        </div>

        <aside className="rounded-[2rem] border border-white/10 bg-zinc-950/90 p-6">
          <p className="text-xs font-semibold uppercase tracking-[0.35em] text-zinc-500">Feed do clube</p>
          <div className="mt-6 space-y-4">
            {dashboard.feed.map((item) => (
              <article key={`${item.type}-${item.title}`} className="rounded-2xl border border-white/10 bg-white/[0.03] p-4">
                <h3 className="font-bold text-zinc-100">{item.title}</h3>
                <p className="mt-2 text-sm leading-6 text-zinc-400">{item.body}</p>
              </article>
            ))}
            <article className="rounded-2xl border border-sky-300/20 bg-sky-300/10 p-4">
              <h3 className="font-bold text-sky-100">Radar Tactical</h3>
              <p className="mt-2 text-sm leading-6 text-sky-100/70">{automaticNews}</p>
            </article>
          </div>
        </aside>
      </section>
    </main>
  );
}

export default Dashboard;
