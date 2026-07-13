import { useState } from "react";
import { predictText } from "../api/client.js";

const MAX_LENGTH = 10000;

export default function AnalyzerCard({ onResult }) {
  const [text, setText] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const isDisabled = isLoading || text.trim().length === 0;

  async function handleAnalyze() {
    setError(null);
    setIsLoading(true);
    try {
      const result = await predictText(text);
      onResult(result);
    } catch (err) {
      setError(err.message || "Something went wrong. Please try again.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <section className="rounded-2xl border border-line bg-white p-2">
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value.slice(0, MAX_LENGTH))}
        placeholder="Paste your text here to analyze..."
        rows={8}
        className="w-full resize-none rounded-xl border-0 p-4 text-sm text-ink placeholder:text-muted focus:outline-none"
      />
      <div className="flex items-center justify-between px-4 pb-2 text-xs text-muted">
        <span>{error ? <span className="text-flagged">{error}</span> : "\u00A0"}</span>
        <span className="font-mono tabular-nums">
          {text.length.toLocaleString()} / {MAX_LENGTH.toLocaleString()}
        </span>
      </div>
      <button
        type="button"
        onClick={handleAnalyze}
        disabled={isDisabled}
        className="w-full rounded-xl bg-ink py-3 text-sm font-medium text-white transition-opacity disabled:opacity-40 enabled:hover:opacity-90"
      >
        {isLoading ? "Analyzing…" : "Analyze text"}
      </button>
    </section>
  );
}
