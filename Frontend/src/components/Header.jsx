const STATUS_COPY = {
  checking: { label: "Connecting…", dot: "bg-muted" },
  ready: { label: "Model ready", dot: "bg-verified" },
  loading: { label: "Model loading…", dot: "bg-flagged animate-pulse" },
  unreachable: { label: "Backend unreachable", dot: "bg-flagged" },
};

export default function Header({ status }) {
  const copy = STATUS_COPY[status] ?? STATUS_COPY.checking;

  return (
    <header className="flex items-center justify-between py-5">
      <div className="flex items-center gap-2">
        <span className="flex h-6 w-6 items-center justify-center rounded-full bg-ink text-white text-xs font-display">
          ✓
        </span>
        <span className="font-display text-sm font-semibold tracking-tight">
          VerifyAI
        </span>
      </div>
      <div className="flex items-center gap-1.5 text-xs text-muted">
        <span className={`h-1.5 w-1.5 rounded-full ${copy.dot}`} />
        {copy.label}
      </div>
    </header>
  );
}
