const SIZE = 200;
const CENTER = SIZE / 2;
const RING_RADIUS = 78;
const CIRCUMFERENCE = 2 * Math.PI * RING_RADIUS;
const TICK_COUNT = 40;

const TONE_STYLES = {
  verified: { stroke: "#2F5D50", track: "#E7EEEC" },
  flagged: { stroke: "#B5502F", track: "#F6E9E4" },
};

function Ticks({ activeColor, percentage }) {
  const activeTicks = Math.round((percentage / 100) * TICK_COUNT);

  return Array.from({ length: TICK_COUNT }).map((_, i) => {
    const angle = (i / TICK_COUNT) * 2 * Math.PI - Math.PI / 2;
    const isMajor = i % 5 === 0;
    const outer = RING_RADIUS + 12;
    const inner = outer - (isMajor ? 7 : 4);
    const x1 = CENTER + inner * Math.cos(angle);
    const y1 = CENTER + inner * Math.sin(angle);
    const x2 = CENTER + outer * Math.cos(angle);
    const y2 = CENTER + outer * Math.sin(angle);
    const isActive = i < activeTicks;

    return (
      <line
        key={i}
        x1={x1}
        y1={y1}
        x2={x2}
        y2={y2}
        stroke={isActive ? activeColor : "#E6E7E3"}
        strokeWidth={isMajor ? 2 : 1}
        strokeLinecap="round"
      />
    );
  });
}

export default function ConfidenceGauge({ percentage, primaryLabel, secondaryLabel, tone }) {
  const style = TONE_STYLES[tone] ?? TONE_STYLES.verified;
  const offset = CIRCUMFERENCE * (1 - percentage / 100);

  return (
    <div className="relative mx-auto" style={{ width: SIZE, height: SIZE }}>
      <svg
        width={SIZE}
        height={SIZE}
        viewBox={`0 0 ${SIZE} ${SIZE}`}
        role="img"
        aria-label={`${percentage.toFixed(0)}% confidence, predicted ${primaryLabel}`}
      >
        <Ticks activeColor={style.stroke} percentage={percentage} />
        <circle
          cx={CENTER}
          cy={CENTER}
          r={RING_RADIUS}
          fill="none"
          stroke={style.track}
          strokeWidth={10}
        />
        <circle
          cx={CENTER}
          cy={CENTER}
          r={RING_RADIUS}
          fill="none"
          stroke={style.stroke}
          strokeWidth={10}
          strokeLinecap="round"
          strokeDasharray={CIRCUMFERENCE}
          strokeDashoffset={offset}
          transform={`rotate(-90 ${CENTER} ${CENTER})`}
          style={{ transition: "stroke-dashoffset 0.6s ease" }}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="font-mono text-3xl font-medium tabular-nums text-ink">
          {percentage.toFixed(0)}%
        </span>
        <span className="mt-1 text-xs font-medium uppercase tracking-wide text-muted">
          {primaryLabel}
        </span>
        <span className="text-[11px] text-muted">{secondaryLabel}</span>
      </div>
    </div>
  );
}
