import { ReactNode, useState } from 'react';
import Dashboard from './Dashboard';
import TacticalBoard from './TacticalBoard';

type AppView = 'dashboard' | 'tactical';

interface MainLayoutProps {
  careerId?: number;
}

interface NavigationItem {
  id: AppView;
  label: string;
  icon: ReactNode;
}

function DashboardIcon() {
  return (
    <svg aria-hidden="true" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M4 13h6V4H4v9Zm0 7h6v-4H4v4Zm10 0h6v-9h-6v9Zm0-13h6V4h-6v3Z" />
    </svg>
  );
}

function TacticalIcon() {
  return (
    <svg aria-hidden="true" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
      <rect x="4" y="3" width="16" height="18" rx="2.5" />
      <path strokeLinecap="round" d="M8 7h8M8 11h8M8 15h5" />
      <circle cx="17" cy="16" r="1.5" />
    </svg>
  );
}

const navigationItems: NavigationItem[] = [
  { id: 'dashboard', label: 'Dashboard', icon: <DashboardIcon /> },
  { id: 'tactical', label: 'Central Tática', icon: <TacticalIcon /> },
];

export function MainLayout({ careerId = 1 }: MainLayoutProps) {
  const [currentView, setCurrentView] = useState<AppView>('dashboard');

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100 lg:grid lg:grid-cols-[18rem_1fr]">
      <aside className="sticky top-0 z-40 flex h-screen flex-col border-r border-zinc-900 bg-zinc-950 px-4 py-5">
        <div className="px-3 py-2">
          <div className="flex items-center gap-3">
            <span className="h-3 w-3 rounded-full bg-emerald-400 shadow-[0_0_24px_rgba(52,211,153,0.75)]" />
            <div>
              <p className="text-lg font-black tracking-tight text-white">Tactical Hub</p>
              <p className="text-[0.65rem] font-semibold uppercase tracking-[0.28em] text-emerald-300">Career AI</p>
            </div>
          </div>
        </div>

        <nav className="mt-8 space-y-2" aria-label="Navegação principal">
          {navigationItems.map((item) => {
            const isActive = currentView === item.id;
            return (
              <button
                key={item.id}
                type="button"
                onClick={() => setCurrentView(item.id)}
                className={`group relative flex w-full items-center gap-3 rounded-2xl px-4 py-3 text-left text-sm font-semibold transition duration-200 ${
                  isActive
                    ? 'bg-zinc-900 text-white shadow-lg shadow-black/20'
                    : 'text-zinc-500 hover:bg-zinc-900/60 hover:text-zinc-200'
                }`}
              >
                <span
                  className={`absolute left-0 top-1/2 h-7 w-1 -translate-y-1/2 rounded-r-full transition ${
                    isActive ? 'bg-emerald-400 opacity-100' : 'bg-transparent opacity-0'
                  }`}
                />
                <span className={isActive ? 'text-emerald-300' : 'text-zinc-500 group-hover:text-emerald-300'}>{item.icon}</span>
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>

        <div className="mt-auto rounded-3xl border border-zinc-900 bg-zinc-900/40 p-4">
          <p className="text-xs font-semibold uppercase tracking-[0.25em] text-zinc-500">Manager</p>
          <div className="mt-3 flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-emerald-400/10 text-sm font-black text-emerald-300">
              GX
            </div>
            <div>
              <p className="text-sm font-bold text-white">Gabriel Xavier</p>
              <p className="text-xs text-zinc-500">Treinador</p>
            </div>
          </div>
        </div>
      </aside>

      <main className="h-screen overflow-y-auto bg-zinc-950">
        {currentView === 'dashboard' ? <Dashboard careerId={careerId} /> : <TacticalBoard careerId={careerId} />}
      </main>
    </div>
  );
}

export default MainLayout;
