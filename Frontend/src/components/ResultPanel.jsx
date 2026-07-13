import ConfidenceGauge from "./ConfidenceGauge.jsx";

const BAR_TONE = {
  Human: { bar: "bg-verified", text: "text-verified" },
  AI: { bar: "bg-flagged", text: "text-flagged" },
};

export default function ResultPanel({ result }) {
  const { prediction, confidence, probabilities, processing_time_ms } = result;
  const tone = prediction === "Human" ? "verified" : "flagged";

  return (
    <section className="mt-6 rounded-2xl border border-line bg-surface p-6">
      <p className="text-center text-xs font-medium uppercase tracking-wide text-muted">
        Analysis result
      </p>

      <div className="mt-4">
        <ConfidenceGauge
          percentage={confidence * 100}
          primaryLabel={prediction}
          secondaryLabel="confidence"
          tone={tone}
        />
      </div>

      <div className="mt-6 space-y-3">
        {Object.entries(probabilities).map(([label, prob]) => (
          <div key={label}>
            <div className="mb-1 flex items-center justify-between text-xs">
              <span className={`font-medium ${BAR_TONE[label]?.text ?? "text-ink"}`}>
                {label}
              </span>
              <span className="font-mono tabular-nums text-muted">
                {(prob * 100).toFixed(1)}%
              </span>
            </div>
            <div className="h-1.5 w-full overflow-hidden rounded-full bg-line">
              <div
                className={`h-full rounded-full ${BAR_TONE[label]?.bar ?? "bg-ink"}`}
                style={{ width: `${prob * 100}%`, transition: "width 0.6s ease" }}
              />
            </div>
          </div>
        ))}
      </div>

      <p className="mt-5 text-center text-[11px] text-muted">
        Analyzed with RoBERTa in {processing_time_ms.toFixed(0)} ms
      </p>
    </section>
  );
}
