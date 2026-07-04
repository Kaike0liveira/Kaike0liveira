interface TacticalBoardProps {
  careerId: number;
}

export function TacticalBoard({ careerId }: TacticalBoardProps) {
  return (
    <section className="min-h-screen bg-[#030305] p-8 text-zinc-100">
      <div className="mx-auto max-w-6xl rounded-[2rem] border border-white/10 bg-zinc-950/80 p-8 shadow-2xl shadow-black/40">
        <p className="text-xs font-semibold uppercase tracking-[0.35em] text-emerald-300">Central Tática</p>
        <h1 className="mt-4 text-4xl font-black tracking-tight">Prancheta do Tactical Hub</h1>
        <p className="mt-3 max-w-2xl text-sm leading-6 text-zinc-400">
          Carreira #{careerId}. Conecte aqui o campo tático definitivo para editar posições X/Y,
          arrastar jogadores e salvar a formação via API.
        </p>

        <div className="mt-8 aspect-[16/10] rounded-[2rem] border border-emerald-400/20 bg-gradient-to-b from-emerald-950/40 to-zinc-950 p-6">
          <div className="flex h-full items-center justify-center rounded-[1.5rem] border border-emerald-300/20 bg-emerald-500/5 text-sm uppercase tracking-[0.3em] text-emerald-100/70">
            Campo tático
          </div>
        </div>
      </div>
    </section>
  );
}

export default TacticalBoard;
